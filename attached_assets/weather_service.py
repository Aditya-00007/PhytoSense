"""
Weather service for PhytoSense application
Provides weather data and alerts for farmers
"""

import os
import json
import time
import requests
import streamlit as st
from datetime import datetime, timedelta
from dotenv import load_dotenv
from profile_utils import get_profile_field

# Load environment variables
load_dotenv()

# Get API key from environment variables
WEATHER_API_KEY ="f4923cb2515212f8108721ed67014dc5"

WEATHER_CACHE_TTL = 3600  # Cache weather data for 1 hour (in seconds)
CACHE_DIR = "weather_data"
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15

def get_weather_icon_url(icon_code):
    """Get URL for weather icon"""
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def load_weather_cache():
    """Load cached weather data"""
    cache_file = os.path.join(CACHE_DIR, "weather_cache.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_weather_cache(cache):
    """Save weather data to cache"""
    cache_file = os.path.join(CACHE_DIR, "weather_cache.json")
    with open(cache_file, "w") as f:
        json.dump(cache, f)

def get_cache_key(location, endpoint="weather"):
    """Generate a cache key for a location and endpoint"""
    return f"{location.lower().strip()}_{endpoint}"

def is_cache_valid(cache_entry):
    """Check if cache entry is valid (not expired)"""
    if not cache_entry or "timestamp" not in cache_entry:
        return False
    
    # Check if cache has expired
    cache_time = cache_entry["timestamp"]
    current_time = time.time()
    return (current_time - cache_time) < WEATHER_CACHE_TTL

def fetch_weather_data(location, use_cache=True):
    """
    Fetch current weather data for a location
    
    Args:
        location (str): City name or location
        use_cache (bool): Whether to use cached data if available
        
    Returns:
        dict: Weather data or None if error
    """
    if not location:
        return None
    
    if not WEATHER_API_KEY:
        st.warning("Weather API key not set. Weather data cannot be retrieved.")
        return None
    
    # Check cache first if enabled
    cache = load_weather_cache()
    cache_key = get_cache_key(location)
    
    if use_cache and cache_key in cache and is_cache_valid(cache[cache_key]):
        return cache[cache_key]["data"]
    
    # Fetch fresh data
    try:
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        response = requests.get(f"{WEATHER_BASE_URL}/weather", params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Cache the data
            cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }
            save_weather_cache(cache)
            
            return data
        else:
            st.error(f"Error fetching weather data: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

def fetch_forecast_data(location, use_cache=True):
    """
    Fetch 5-day forecast data for a location
    
    Args:
        location (str): City name or location
        use_cache (bool): Whether to use cached data if available
        
    Returns:
        dict: Forecast data or None if error
    """
    if not location:
        return None
    
    if not WEATHER_API_KEY:
        st.warning("Weather API key not set. Forecast data cannot be retrieved.")
        return None
    
    # Check cache first if enabled
    cache = load_weather_cache()
    cache_key = get_cache_key(location, "forecast")
    
    if use_cache and cache_key in cache and is_cache_valid(cache[cache_key]):
        return cache[cache_key]["data"]
    
    # Fetch fresh data
    try:
        params = {
            "q": location,
            "appid": WEATHER_API_KEY,
            "units": "metric"  # Use metric units (Celsius)
        }
        
        response = requests.get(f"{WEATHER_BASE_URL}/forecast", params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Cache the data
            cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }
            save_weather_cache(cache)
            
            return data
        else:
            st.error(f"Error fetching forecast data: {response.status_code} - {response.text}")
            return None
    
    except Exception as e:
        st.error(f"Error fetching forecast data: {str(e)}")
        return None

def get_weather_alerts(weather_data):
    """
    Generate weather alerts based on current conditions
    
    Args:
        weather_data (dict): Weather data from API
        
    Returns:
        list: List of alert messages
    """
    alerts = []
    
    if not weather_data:
        return alerts
    
    # Check temperature alerts
    temp = weather_data.get("main", {}).get("temp")
    if temp is not None:
        if temp > 35:
            alerts.append({
                "type": "danger",
                "message": "Extreme heat alert! Ensure proper irrigation and consider shade for sensitive crops."
            })
        elif temp > 30:
            alerts.append({
                "type": "warning",
                "message": "High temperature alert. Monitor water levels and irrigation needs."
            })
        elif temp < 5:
            alerts.append({
                "type": "danger",
                "message": "Frost risk alert! Protect sensitive crops from cold damage."
            })
        elif temp < 10:
            alerts.append({
                "type": "warning",
                "message": "Low temperature alert. Be prepared for potential frost conditions."
            })
    
    # Check humidity alerts
    humidity = weather_data.get("main", {}).get("humidity")
    if humidity is not None:
        if humidity > 85:
            alerts.append({
                "type": "warning",
                "message": "High humidity alert. Monitor for fungal diseases and reduce leaf wetness."
            })
        elif humidity < 30:
            alerts.append({
                "type": "warning",
                "message": "Low humidity alert. Increase irrigation to prevent crop stress."
            })
    
    # Check rain alerts
    if "rain" in weather_data:
        rain_1h = weather_data.get("rain", {}).get("1h", 0)
        rain_3h = weather_data.get("rain", {}).get("3h", 0)
        
        if rain_1h > 10 or rain_3h > 20:
            alerts.append({
                "type": "danger",
                "message": "Heavy rain alert! Be cautious of flooding and soil erosion."
            })
        elif rain_1h > 5 or rain_3h > 10:
            alerts.append({
                "type": "warning",
                "message": "Moderate rain alert. Check drainage systems and field conditions."
            })
    
    # Check wind alerts
    wind_speed = weather_data.get("wind", {}).get("speed")
    if wind_speed is not None:
        if wind_speed > 10:  # m/s = ~36 km/h
            alerts.append({
                "type": "danger",
                "message": "Strong wind alert! Secure structures and protect young plants."
            })
        elif wind_speed > 7:  # m/s = ~25 km/h
            alerts.append({
                "type": "warning",
                "message": "Moderate wind alert. Monitor for crop damage and increased water loss."
            })
    
    # Check weather conditions
    weather_id = weather_data.get("weather", [{}])[0].get("id") if weather_data.get("weather") else None
    if weather_id:
        # Thunderstorm
        if 200 <= weather_id < 300:
            alerts.append({
                "type": "danger",
                "message": "Thunderstorm alert! Seek shelter and be cautious of lightning strikes."
            })
        # Drizzle/Rain
        elif 300 <= weather_id < 400 or 500 <= weather_id < 600:
            if 502 <= weather_id <= 504:
                alerts.append({
                    "type": "warning",
                    "message": "Heavy rain alert. Check field drainage and avoid waterlogging."
                })
        # Snow
        elif 600 <= weather_id < 700:
            alerts.append({
                "type": "warning",
                "message": "Snow alert. Protect sensitive crops from cold damage."
            })
        # Atmosphere (fog, haze, etc.)
        elif 700 <= weather_id < 800:
            if weather_id == 731 or weather_id == 751 or weather_id == 761:
                alerts.append({
                    "type": "warning",
                    "message": "Dust/Sand alert. Protect sensitive equipment and crops from dust damage."
                })
            elif weather_id == 762:
                alerts.append({
                    "type": "danger",
                    "message": "Volcanic ash alert! Take immediate precautions to protect yourself and livestock."
                })
    
    return alerts

def format_forecast_data(forecast_data):
    """
    Format forecast data for display
    
    Args:
        forecast_data (dict): Raw forecast data
        
    Returns:
        list: Formatted forecast entries
    """
    if not forecast_data or "list" not in forecast_data:
        return []
    
    formatted_entries = []
    forecast_list = forecast_data["list"]
    
    # Group by day
    days = {}
    for entry in forecast_list:
        dt = datetime.fromtimestamp(entry["dt"])
        day = dt.strftime("%Y-%m-%d")
        
        if day not in days:
            days[day] = []
        
        days[day].append(entry)
    
    # Process each day
    for day, entries in days.items():
        dt = datetime.strptime(day, "%Y-%m-%d")
        day_name = dt.strftime("%A")  # Get day name (Monday, Tuesday, etc.)
        
        # Calculate average values for the day
        temp_sum = sum(entry["main"]["temp"] for entry in entries)
        temp_min = min(entry["main"]["temp_min"] for entry in entries)
        temp_max = max(entry["main"]["temp_max"] for entry in entries)
        humidity_sum = sum(entry["main"]["humidity"] for entry in entries)
        
        # Get the most common weather condition
        weather_descriptions = [entry["weather"][0]["description"] for entry in entries]
        weather_icons = [entry["weather"][0]["icon"] for entry in entries]
        
        # Use the most common description and corresponding icon
        # This is a simple approach - you could use a more sophisticated method
        from collections import Counter
        common_desc = Counter(weather_descriptions).most_common(1)[0][0]
        
        # Find an icon that matches the common description
        common_icon = next((icon for desc, icon in zip(weather_descriptions, weather_icons) 
                           if desc == common_desc), weather_icons[0])
        
        # Calculate rain if available
        total_rain = 0
        for entry in entries:
            if "rain" in entry:
                total_rain += entry["rain"].get("3h", 0)
        
        # Format the entry
        formatted_entry = {
            "day": day,
            "day_name": day_name,
            "avg_temp": temp_sum / len(entries),
            "min_temp": temp_min,
            "max_temp": temp_max,
            "avg_humidity": humidity_sum / len(entries),
            "weather_description": common_desc.capitalize(),
            "weather_icon": common_icon,
            "total_rain": total_rain
        }
        
        formatted_entries.append(formatted_entry)
    
    return formatted_entries

def display_weather_widget(location=None):
    """
    Display weather widget in the sidebar
    
    Args:
        location (str): Location to display weather for, defaults to user's location
    """
    with st.sidebar:
        st.markdown("### Weather Information")
        
        # Get user location if not provided
        if not location and st.session_state.user_profile:
            location = get_profile_field(st.session_state.user_profile, 'farm_location')
        
        if not location:
            st.info("Farm location not set. Update your profile to see weather alerts.")
            return
        
        # Fetch weather data
        weather_data = fetch_weather_data(location)
        
        if not weather_data:
            st.warning("Unable to retrieve weather data. Please check your location or API key.")
            
            # Show API key setup prompt if needed
            if not WEATHER_API_KEY:
                st.info("To enable weather features, please add your OpenWeatherMap API key to the .env file.")
            return
        
        # Display current weather
        try:
            weather_icon = weather_data.get("weather", [{}])[0].get("icon")
            weather_desc = weather_data.get("weather", [{}])[0].get("description", "").capitalize()
            temp = weather_data.get("main", {}).get("temp")
            feels_like = weather_data.get("main", {}).get("feels_like")
            humidity = weather_data.get("main", {}).get("humidity")
            wind_speed = weather_data.get("wind", {}).get("speed")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if weather_icon:
                    st.image(get_weather_icon_url(weather_icon), width=60)
            
            with col2:
                st.markdown(f"**{location}**")
                st.markdown(f"{weather_desc}")
                
            # Temperature and conditions
            st.markdown(f"**Temperature:** {temp:.1f}°C (Feels like: {feels_like:.1f}°C)")
            st.markdown(f"**Humidity:** {humidity}%")
            st.markdown(f"**Wind:** {wind_speed} m/s")
            
            # Check for critical alerts
            alerts = get_weather_alerts(weather_data)
            if alerts:
                st.markdown("#### Weather Alerts")
                for alert in alerts:
                    if alert["type"] == "danger":
                        st.error(alert["message"])
                    else:
                        st.warning(alert["message"])
            
            # View full forecast link
            if st.button("View Full Forecast", key="sidebar_forecast"):
                st.session_state.page = "weather"
                st.rerun()
        
        except Exception as e:
            st.error(f"Error displaying weather data: {str(e)}")

def show_weather_page():
    """Display the full weather page"""
    st.header("Weather Forecasting & Agricultural Advisories")
    
    # Get user location
    location = None
    if st.session_state.user_profile:
        location = get_profile_field(st.session_state.user_profile, 'location')
    
    # Location selector with default to user's location
    location_input = st.text_input("Location", value=location if location else "")
    
    if st.button("Get Weather"):
        if location_input:
            location = location_input
        else:
            st.warning("Please enter a location.")
    
    if not location:
        st.info("Enter a location to view weather data and agricultural advisories.")
        return
    
    # Fetch current weather
    weather_data = fetch_weather_data(location, use_cache=False)
    
    if not weather_data:
        st.warning("Unable to retrieve weather data. Please check your location or API key.")
        
        # Prompt for API key if needed
        if not WEATHER_API_KEY:
            st.info("""
            To enable weather features, you need an OpenWeatherMap API key:
            1. Sign up at https://openweathermap.org/api
            2. Get your API key
            3. Add it to the .env file as WEATHER_API_KEY
            """)
        return
    
    # Display current weather
    try:
        st.subheader(f"Current Weather in {location}")
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            weather_icon = weather_data.get("weather", [{}])[0].get("icon")
            if weather_icon:
                st.image(get_weather_icon_url(weather_icon), width=100)
        
        with col2:
            weather_desc = weather_data.get("weather", [{}])[0].get("description", "").capitalize()
            st.markdown(f"### {weather_desc}")
            
            temp = weather_data.get("main", {}).get("temp")
            feels_like = weather_data.get("main", {}).get("feels_like")
            
            st.markdown(f"**Temperature:** {temp:.1f}°C (Feels like: {feels_like:.1f}°C)")
            
            humidity = weather_data.get("main", {}).get("humidity")
            st.markdown(f"**Humidity:** {humidity}%")
            
            wind_speed = weather_data.get("wind", {}).get("speed")
            wind_direction = weather_data.get("wind", {}).get("deg")
            wind_dir_text = ""
            if wind_direction is not None:
                directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
                index = round(wind_direction / 45) % 8
                wind_dir_text = f" from {directions[index]}"
            
            st.markdown(f"**Wind:** {wind_speed} m/s{wind_dir_text}")
            
            pressure = weather_data.get("main", {}).get("pressure")
            st.markdown(f"**Pressure:** {pressure} hPa")
            
            visibility = weather_data.get("visibility")
            if visibility:
                st.markdown(f"**Visibility:** {visibility / 1000:.1f} km")
            
            sunrise = weather_data.get("sys", {}).get("sunrise")
            sunset = weather_data.get("sys", {}).get("sunset")
            
            if sunrise and sunset:
                sunrise_time = datetime.fromtimestamp(sunrise).strftime("%H:%M")
                sunset_time = datetime.fromtimestamp(sunset).strftime("%H:%M")
                st.markdown(f"**Sunrise:** {sunrise_time} | **Sunset:** {sunset_time}")
        
        # Weather alerts
        alerts = get_weather_alerts(weather_data)
        if alerts:
            st.subheader("Weather Alerts & Farming Advisories")
            for alert in alerts:
                if alert["type"] == "danger":
                    st.error(alert["message"])
                else:
                    st.warning(alert["message"])
        
        # Fetch 5-day forecast
        forecast_data = fetch_forecast_data(location, use_cache=False)
        
        if forecast_data and "list" in forecast_data:
            st.subheader("5-Day Weather Forecast")
            
            # Format and display forecast
            formatted_forecast = format_forecast_data(forecast_data)
            
            if formatted_forecast:
                # Create a row of columns for each day's forecast
                cols = st.columns(min(5, len(formatted_forecast)))
                
                for i, day_forecast in enumerate(formatted_forecast[:5]):  # Show up to 5 days
                    with cols[i]:
                        st.markdown(f"**{day_forecast['day_name']}**")
                        st.image(get_weather_icon_url(day_forecast['weather_icon']), width=50)
                        st.markdown(day_forecast['weather_description'])
                        st.markdown(f"{day_forecast['min_temp']:.1f}°C - {day_forecast['max_temp']:.1f}°C")
                        
                        if day_forecast['total_rain'] > 0:
                            st.markdown(f"Rain: {day_forecast['total_rain']:.1f} mm")
                
                # Agricultural implications
                st.subheader("Agricultural Implications")
                
                # Generate farming recommendations based on forecast
                recommendations = []
                
                # Check if rain is expected in next 48 hours
                next_48h_entries = forecast_data["list"][:16]  # 8 entries per day, 3-hour intervals
                rain_expected = any("rain" in entry for entry in next_48h_entries)
                
                high_temp_expected = any(entry["main"]["temp_max"] > 30 for entry in next_48h_entries)
                low_temp_expected = any(entry["main"]["temp_min"] < 10 for entry in next_48h_entries)
                
                # Add recommendations based on conditions
                if rain_expected:
                    recommendations.append("• Consider delaying pesticide or fertilizer application as rain may wash them away.")
                    recommendations.append("• Ensure proper drainage in fields to prevent waterlogging.")
                else:
                    recommendations.append("• Good conditions for pesticide or fertilizer application (no rain expected).")
                    recommendations.append("• Monitor irrigation needs as dry conditions are expected.")
                
                if high_temp_expected:
                    recommendations.append("• Increase irrigation frequency during high temperature periods.")
                    recommendations.append("• Consider creating shade for sensitive crops.")
                
                if low_temp_expected:
                    recommendations.append("• Be prepared to protect sensitive crops from low temperatures.")
                    recommendations.append("• Delay sowing of temperature-sensitive crops.")
                
                # Display recommendations
                for rec in recommendations:
                    st.markdown(rec)
                
                # Add seasonal advice based on current date
                current_month = datetime.now().month
                if 3 <= current_month <= 5:  # Spring (March-May)
                    st.markdown("### Seasonal Advisory (Spring)")
                    st.markdown("• Prepare fields for kharif season crops.")
                    st.markdown("• Monitor for early pest activity as temperatures rise.")
                    st.markdown("• Begin sowing of summer vegetables and early maturing crops.")
                
                elif 6 <= current_month <= 9:  # Summer/Monsoon (June-September)
                    st.markdown("### Seasonal Advisory (Monsoon)")
                    st.markdown("• Monitor rainfall patterns for timely sowing of kharif crops.")
                    st.markdown("• Ensure proper drainage to avoid waterlogging during heavy rains.")
                    st.markdown("• Watch for increased pest and disease pressure in humid conditions.")
                
                elif 10 <= current_month <= 11:  # Fall (October-November)
                    st.markdown("### Seasonal Advisory (Fall)")
                    st.markdown("• Prepare for rabi crop sowing as monsoon withdraws.")
                    st.markdown("• Monitor soil moisture levels for optimal planting conditions.")
                    st.markdown("• Begin harvesting of mature kharif crops.")
                
                else:  # Winter (December-February)
                    st.markdown("### Seasonal Advisory (Winter)")
                    st.markdown("• Protect sensitive crops from frost and low temperatures.")
                    st.markdown("• Monitor irrigation needs as winter tends to be dry.")
                    st.markdown("• Apply recommended doses of fertilizers to rabi crops.")
        
        # Additional Weather Information
        with st.expander("Weather Impact on Crops"):
            st.markdown("""
            ### How Weather Affects Your Crops
            
            **Temperature Impact:**
            - High temperatures (>35°C) can cause heat stress, affecting pollination and fruit development.
            - Low temperatures (<10°C) may slow growth and cause cold injury to sensitive crops.
            
            **Rainfall Impact:**
            - Adequate rainfall or irrigation is essential for crop growth and development.
            - Excessive rain can lead to waterlogging, increased disease pressure, and nutrient leaching.
            - Insufficient rain can cause drought stress and reduced yields.
            
            **Humidity Impact:**
            - High humidity can increase disease pressure, especially fungal pathogens.
            - Low humidity combined with high temperatures increases water requirements.
            
            **Wind Impact:**
            - Strong winds can cause mechanical damage to crops, especially tall or fragile ones.
            - Persistent winds increase evapotranspiration, leading to higher water demands.
            """)
        
        with st.expander("Weather Data Sources & Reliability"):
            st.markdown("""
            ### Weather Data Information
            
            **Data Source:**
            - Weather data provided by OpenWeatherMap API
            - Forecasts typically updated every 3 hours
            
            **Accuracy Considerations:**
            - Short-term forecasts (1-3 days) are generally more reliable
            - Long-term predictions (4-5 days) have increased uncertainty
            - Local variations in weather may occur due to topography and microclimate
            
            **Using Weather Data for Farming Decisions:**
            - Combine weather forecasts with local observations
            - Consider multiple forecasts for important decisions
            - Monitor changes in predictions as forecast dates approach
            """)
    
    except Exception as e:
        st.error(f"Error displaying weather page: {str(e)}")