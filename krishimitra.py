import streamlit as st
import json
import os
import datetime
from language_support import t
from profile_utils import get_profile_field
from weather_service import fetch_weather_data, fetch_forecast_data
import weather_data_store

# Groq Wrapper
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

class KrishiMitra:
    def __init__(self):
        self.history_file = "farmer_history.json"
        
        # Try to get API key from secrets or environment
        self.api_key = os.getenv("GROQ_API_KEY")

        # If not found, safely try Streamlit secrets (local dev)
        if not self.api_key:
            try:
                self.api_key = st.secrets["GROQ_API_KEY"]
            except Exception:
                self.api_key = None
        
        self.client = None
        if HAS_GROQ and self.api_key:
            self.client = Groq(api_key=self.api_key)

    def load_farmer_data(self, user_id):
        """Load farmer profile from database"""
        try:
            from db_adapter import get_user_profile
            profile = get_user_profile(user_id)
            return profile or {} 
        except Exception as e:
            return {}

    def load_chat_history(self, user_id):
        """Load chat history from JSON file"""
        if not os.path.exists(self.history_file):
            return []
            
        try:
            with open(self.history_file, "r") as f:
                data = json.load(f)
                return data.get(user_id, [])
        except Exception:
            return []

    def save_interaction(self, user_id, query, response):
        """Save chat interaction to JSON file"""
        data = {}
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        
        if user_id not in data:
            data[user_id] = []
            
        interaction = {
            "timestamp": datetime.datetime.now().isoformat(),
            "query": query,
            "response": response
        }
        data[user_id].append(interaction)
        
        with open(self.history_file, "w") as f:
            json.dump(data, f, indent=4)

    def get_detailed_weather_context(self, location):
        """Get detailed weather context including current and forecast"""
        if not location:
            return "Weather data not available (Location missing)."
        
        context_parts = []
        
        # 1. Current Weather
        try:
            current = fetch_weather_data(location)
            if current:
                main = current.get('main', {})
                wind = current.get('wind', {})
                weather_desc = current.get('weather', [{}])[0].get('description', 'Unknown')
                rain_1h = current.get('rain', {}).get('1h', 0)
                
                context_parts.append(f"CURRENT WEATHER in {location}:")
                context_parts.append(f"- Condition: {weather_desc}")
                context_parts.append(f"- Temp: {main.get('temp')}°C (Humidity: {main.get('humidity')}%)")
                context_parts.append(f"- Wind: {wind.get('speed')} m/s")
                if rain_1h > 0:
                    context_parts.append(f"- Rain (1h): {rain_1h}mm")
        except Exception as e:
            context_parts.append(f"Current weather unavailable: {e}")

        # 2. Forecast (Next few days)
        try:
            forecast = fetch_forecast_data(location)
            if forecast and 'list' in forecast:
                context_parts.append("\nFORECAST (Next 48 hrs):")
                # Grab a few representative points
                seen_dates = set()
                count = 0
                for item in forecast['list']:
                    dt = datetime.datetime.fromtimestamp(item['dt'])
                    date_str = dt.strftime('%Y-%m-%d')
                    if date_str not in seen_dates:
                        seen_dates.add(date_str)
                        temp_max = item['main']['temp_max']
                        temp_min = item['main']['temp_min']
                        desc = item['weather'][0]['description']
                        rain = item.get('rain', {}).get('3h', 0)
                        wind_speed = item.get('wind', {}).get('speed', 0)
                        
                        context_parts.append(f"- {date_str}: {desc}, Temp: {temp_min}-{temp_max}°C, Rain: {rain}mm, Wind: {wind_speed} m/s")
                        count += 1
                        if count >= 3: break
        except Exception as e:
            context_parts.append(f"Forecast unavailable: {e}")
            
        return "\n".join(context_parts)

    def get_crop_intelligence_context(self, crops_list):
        """Retrieve specifically relevant crop variables"""
        context_str = ""
        found_data = False
        
        for crop in crops_list:
            clean_crop = crop.strip().upper().replace(" ", "_")
            # 1. Try exact match
            var_name = f"{clean_crop}_WEATHER_INTELLIGENCE"
            pass
            
            # Simple fuzzy lookup in the module
            data_found = None
            if hasattr(weather_data_store, var_name):
                data_found = getattr(weather_data_store, var_name)
            else:
                # Try to find partial match in module attributes
                for attr in dir(weather_data_store):
                    if attr.endswith("_WEATHER_INTELLIGENCE"):
                        base_name = attr.replace("_WEATHER_INTELLIGENCE", "")
                        if base_name in clean_crop or clean_crop in base_name:
                            data_found = getattr(weather_data_store, attr)
                            break
            
            if data_found:
                found_data = True
                context_str += f"\n--- INTELLIGENCE FOR {crop.upper()} ---\n"
                context_str += json.dumps(data_found, indent=2) + "\n"
        
        if not found_data:
            return "No specific crop datasets found. Use general agricultural principles."
            
        return context_str

    def determine_intent(self, query):
        """Simple keyword matching for intent"""
        query_lower = query.lower()
        if any(w in query_lower for w in ["weather", "hawa", "paus", "rain"]):
            return "weather"
        if any(w in query_lower for w in ["market", "bajar", "bhav", "price", "rate"]):
            return "market"
        if any(w in query_lower for w in ["crop", "pik", "disease", "rog", "khat", "fertilizer"]):
            return "crop_advisory"
        return "general"

    def generate_response(self, user_profile, query):
        """Generate response using Groq with Enhanced Context"""
        if not self.client:
            return t("Error: Groq API Key not found or library not installed. Please add GROQ_API_KEY to secrets or environment variables.")

        # 1. Build Context
        name = user_profile.get("name", "Farmer")
        location = user_profile.get("farm_location", "")
        crops_str = user_profile.get("primary_crops", "")
        crops_list = [c.strip() for c in crops_str.split(",") if c.strip()]
        water = user_profile.get("Water_Availability", "Unknown")
        income = user_profile.get("Income", "Unknown")
        lang = user_profile.get("preferred_language", "English")

        # Fetch detailed weather and crop intelligence
        weather_info = self.get_detailed_weather_context(location)
        crop_intelligence = self.get_crop_intelligence_context(crops_list)

        # Add context from previous interactions (Hidden from UI but visible to Bot)
        history_context = ""
        if "context_history" in st.session_state and st.session_state.context_history:
            history_context = "\n--- RECENT CONVERSATION HISTORY (Last 10 Days) ---\n"
            # Limit to last 5 exchanges to avoid token overflow
            for item in st.session_state.context_history[-5:]:
                history_context += f"Farmer: {item['query']}\nKrishiMitra: {item['response']}\n"

        # 2. System Prompt (Strict Language Control & Structured Output)
        system_context = f"""
You are 'KrishiMitra', an expert agricultural AI assistant for farmers in Maharashtra, India.
Your goal is to provide **Actionable, Risk-Prioritized, and Integrated Weather Advisories**.

--- FARMER PROFILE ---
- Name: {name}
- Location: {location}
- Crops: {crops_str}
- Water Availability: {water}
- Estimated Income Level: {income}
- Preferred Language: {lang}

--- REAL-TIME WEATHER & FORECAST ---
{weather_info}

--- CROP INTELLIGENCE DATASETS ---
{crop_intelligence}
{history_context}

--- STRICT LANGUAGE RULES (CRITICAL) ---
1. **ENGLISH ONLY**: 
   - ALWAYS respond in **English**, regardless of whether the user asks in Marathi, Hindi, or English.
   - Do NOT use Marathi script or words.
   - Use **SIMPLE, EASY-TO-UNDERSTAND ENGLISH**. Avoid complex words.
   - **NEVER** mix languages. No "Hinglish".

2. **NO REPETITION**:
   - Check your output. If you see repeated phrases like "aapche kheti aani...", DELETE THEM immediately.
   - Do not repeat the greetings or the situation multiple times.

--- RESPONSE LOGIC ---
Before answering, classify the user's question type:
- **Weather/Crop Advisory**: Use the Weather & Crop Intelligence data.
- **Equipment/Tractor**: Suggest HP/Budget based on farm size ({user_profile.get('farm_size', 'Unknown')}).
- **Market/Price**: Give general market trends if specific data is missing.
- **General**: Provide simple, practical advice.
- **Contextual**: Refer to previous conversation history if relevant to the current question.

--- REQUIRED RESPONSE FORMAT ---

Greeting: "Ram Ram {name} ji,"
**Situation:** [1 sentence summary of weather/crop status]
**Recommendation:** [Direct answer to the query]
**Why:** [Simple reasoning]
**Action Plan:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
**Conclusion:** [Encouraging closing]

--- QUALITY CHECKS ---
- Keep sentences **short** and **simple**.
- Avoid technical jargon. Use farmer-friendly terms.
- **NO FILLER TEXT**. Get straight to the point.
- Ensure the response is logically structured.

Respond directly to the user's query: "{query}"
"""

        # 3. Call Groq
        try:
            chat = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=800,
            )
            return chat.choices[0].message.content
        except Exception as e:
            return f"Error contacting AI: {str(e)}"

def show_chatbot_page():
    st.header(t("Krishi Mitra - Your Farming Assistant "))

    # Check Key
    # Priority: Session State > Secrets > Environment
    api_key =os.getenv("GROQ_API_KEY") or st.session_state.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        api_key_input = st.text_input(t("Enter Groq API Key to activate Krishi Mitra"), type="password")
        if api_key_input:
            st.session_state["GROQ_API_KEY"] = api_key_input
            os.environ["GROQ_API_KEY"] = api_key_input
            st.rerun()
        else:
            st.warning(t("Please provide a Groq API Key to use this feature."))
            st.markdown(t("[Get a free Groq API key here](https://console.groq.com/keys)"))
            return

    # Initialize Chatbot
    # We pass the key explicitly or rely on env/secrets inside the class, 
    # but here we ensure it's available in env if captured from input
    if "GROQ_API_KEY" not in os.environ and api_key:
        os.environ["GROQ_API_KEY"] = api_key

    bot = KrishiMitra()
    
    # Get Current User Profile
    user = st.session_state.get("current_user")
    if not user:
        st.error(t("Please login to use Krishi Mitra."))
        return
        
    # Get username/id
    # From profiles.json structure, keys are usernames
    username = user['username'] if isinstance(user, dict) else user.username
    user_profile = bot.load_farmer_data(username)
    
    # Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
        # Load historical messages from browser storage
        history = bot.load_chat_history(username)
        
        # Filter history for last 10 days
        ten_days_ago = datetime.datetime.now() - datetime.timedelta(days=10)
        recent_history = []
        
        for item in history:
            try:
                msg_time = datetime.datetime.fromisoformat(item["timestamp"])
                if msg_time > ten_days_ago:
                    recent_history.append(item)
            except ValueError:
                continue
        
        # Do NOT append detailed history to visible messages to keep UI clean
        # But we can store it in a separate state for context if needed
        st.session_state.context_history = recent_history

        # Add welcome message
        welcome_msg = t(f"Ram Ram {user_profile.get('name', 'Farmer')}! How can I help you with your farm today?")
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(t(message["content"]))

    # Chat input
    if prompt := st.chat_input("Ask Krishi Mitra..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(t(prompt))

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = bot.generate_response(user_profile, prompt)
                st.markdown(t(response))
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save to history
        bot.save_interaction(username, prompt, response)
