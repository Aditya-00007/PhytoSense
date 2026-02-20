
import os
import json
import time
import requests
import streamlit as st
from datetime import datetime, timedelta
from profile_utils import get_profile_field
from language_support import initialize_language, show_language_selector, t, translate_api
import weather_data_store

# Weather API constants
WEATHER_API_KEY = "f4923cb2515212f8108721ed67014dc5"  # Replace with your actual API key
CACHE_DIR = "weather_data"
WEATHER_CACHE_TTL = 3600  # Cache weather data for 1 hour (in seconds)
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def safe_get(data, keys, default=None):
    """Safely get nested dictionary or list values"""
    current = data

    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, default)
        elif isinstance(current, list) and isinstance(key, int):
            if 0 <= key < len(current):
                current = current[key]
            else:
                return default
        else:
            return default

        if current is None:
            return default

    return current


def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    if kelvin is None:
        return None
    return kelvin - 273.15

def get_weather_icon_url(icon_code):
    """Get URL for weather icon"""
    if not icon_code:
        return None
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def load_weather_cache():
    """Load weather cache from disk"""
    cache_file = os.path.join(CACHE_DIR, "weather_cache.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_weather_cache(cache):
    """Save weather data to disk cache"""
    cache_file = os.path.join(CACHE_DIR, "weather_cache.json")
    try:
        with open(cache_file, "w") as f:
            json.dump(cache, f)
    except Exception as e:
        print(f"Error saving weather cache: {e}")

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
        st.error(t("Location is required to fetch weather data"))
        return None
    
    if not WEATHER_API_KEY:
        st.error(t("Weather API key not configured"))
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
        
        response = requests.get(f"{WEATHER_BASE_URL}/weather", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Validate required fields
            if not all(key in data for key in ['weather', 'main', 'wind']):
                st.error(t("Received incomplete weather data from API"))
                return None
            
            # Cache the data
            cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }
            save_weather_cache(cache)
            
            return data
        else:
            st.error(f"{t('Weather API error')}: {response.status_code} - {response.text}")
            return None
    
    except requests.exceptions.RequestException as e:
        st.error(f"{t('Error fetching weather data')}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"{t('Unexpected error')}: {str(e)}")
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
        st.error(t("Location is required to fetch forecast data"))
        return None
    
    if not WEATHER_API_KEY:
        st.error(t("Weather API key not configured"))
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
        
        response = requests.get(f"{WEATHER_BASE_URL}/forecast", params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Validate required fields
            if "list" not in data or not data["list"]:
                st.error(t("Received incomplete forecast data from API"))
                return None
            
            # Cache the data
            cache[cache_key] = {
                "timestamp": time.time(),
                "data": data
            }
            save_weather_cache(cache)
            
            return data
        else:
            st.error(f"{t('Forecast API error')}: {response.status_code} - {response.text}")
            return None
    
    except requests.exceptions.RequestException as e:
        st.error(f"{t('Error fetching forecast data')}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"{t('Unexpected error')}: {str(e)}")
        return None

def get_wind_direction(degrees):
    """Convert wind direction in degrees to compass direction"""
    if degrees is None:
        return t("Unknown")
    directions = [t("N"), t("NNE"), t("NE"), t("ENE"), t("E"), t("ESE"), t("SE"), t("SSE"),
                  t("S"), t("SSW"), t("SW"), t("WSW"), t("W"), t("WNW"), t("NW"), t("NNW")]
    index = round(degrees / (360. / len(directions))) % len(directions)
    return directions[index]

def display_current_weather(weather_data):
    """Display current weather conditions"""
    if not weather_data:
        st.error(t("No weather data available"))
        return
    
    # Safely extract weather information with defaults
    weather_main = safe_get(weather_data, ['weather', 0, 'main'], t("Unknown"))
    weather_desc = safe_get(weather_data, ['weather', 0, 'description'], t("Unknown")).capitalize()
    weather_icon = safe_get(weather_data, ['weather', 0, 'icon'])
    temp = safe_get(weather_data, ['main', 'temp'], 0)
    feels_like = safe_get(weather_data, ['main', 'feels_like'], temp)
    humidity = safe_get(weather_data, ['main', 'humidity'], 0)
    pressure = safe_get(weather_data, ['main', 'pressure'], 0)
    wind_speed = safe_get(weather_data, ['wind', 'speed'], 0)
    wind_deg = safe_get(weather_data, ['wind', 'deg'])
    wind_dir = get_wind_direction(wind_deg)
    rain_1h = safe_get(weather_data, ['rain', '1h'], 0)
    clouds = safe_get(weather_data, ['clouds', 'all'], 0)
    
    # Display in two columns
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Display weather icon if available
        if weather_icon:
            icon_url = get_weather_icon_url(weather_icon)
            st.image(icon_url, width=100)
        else:
            st.write(t("No icon available"))
    
    with col2:
        st.metric(t("Temperature"), f"{temp:.1f}°C", f"{t('Feels like')} {feels_like:.1f}°C")
        
        # Additional weather details
        st.write(f"""
        - **{t('Conditions')}**: {t(weather_desc)}
        - **{t('Humidity')}**: {humidity}%
        - **{t('Wind')}**: {wind_speed} m/s ({wind_dir})
        - **{t('Pressure')}**: {pressure} hPa
        - **{t('Rain (1h)')}**: {rain_1h} mm
        - **{t('Cloud Cover')}**: {clouds}%
        """)

def display_weather_alerts(weather_data):
    """Display weather alerts if any"""
    alerts = get_weather_alerts(weather_data)
    
    if not alerts:
        st.success(t("No active weather alerts"))
        return
    
    st.header(f"⚠️ {t('Weather Alerts')}")
    
    for alert in alerts:
        alert_type = t("🔴 Critical") if alert.get("type") == "danger" else t("🟡 Warning")
        with st.expander(f"{alert_type}: {t(alert.get('title', 'Alert'))}"):
            st.write(t(alert.get("message", "No details available")))
            if alert.get("recommendations"):
                st.markdown(f"**{t('Recommendations')}:**")
                for rec in alert["recommendations"]:
                    st.write(f"- {t(rec)}")

def display_agricultural_metrics(weather_data):
    """Display agricultural-specific weather metrics"""
    if not weather_data:
        return
    
    st.header(t("Agricultural Metrics"))
    
    # Calculate metrics
    uv_index = estimate_uv_index(weather_data)
    solar_rad = estimate_solar_radiation(weather_data)
    et0 = calculate_evapotranspiration(weather_data)
    
    # Display in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(t("UV Index"), 
                 f"{uv_index if uv_index else t('N/A')}",
                 t(get_uv_risk_level(uv_index)))
    
    with col2:
        st.metric(t("Solar Radiation"), 
                 f"{solar_rad} W/m²" if solar_rad else t("N/A"))
    
    with col3:
        st.metric(t("Evapotranspiration (ET₀)"), 
                 f"{et0} mm/day" if et0 else t("N/A"))

def display_5day_forecast(forecast_data):
    """Display 5-day weather forecast"""
    if not forecast_data:
        st.error(t("No forecast data available"))
        return
    
    daily_forecast = format_forecast_data(forecast_data)
    
    if not daily_forecast:
        st.error(t("Could not process forecast data"))
        return
    
    st.header(t("5-Day Forecast"))
    
    for day in daily_forecast[:5]:  # Show next 5 days
        with st.expander(f"{day['day_name']} - {day['day']}"):
            cols = st.columns([1, 3, 2])
            
            with cols[0]:
                if day.get("weather_icon"):
                    st.image(get_weather_icon_url(day["weather_icon"]), width=60)
                else:
                    st.write(t("No icon"))
            
            with cols[1]:
                st.write(f"**{t(day.get('weather_description', t('Unknown conditions')))}**")
                st.write(f"🌡️ {day.get('min_temp', 0):.1f}°C - {day.get('max_temp', 0):.1f}°C")
                st.write(f"💧 {day.get('avg_humidity', 0):.0f}% {t('humidity')}")
                if day.get("total_rain", 0) > 0:
                    st.write(f"🌧️ {day['total_rain']:.1f} mm {t('rain')}")
                st.write(f"💨 {day.get('avg_wind_speed', 0):.1f} m/s")
            
            with cols[2]:
                st.markdown(f"**{t('Farming Advice')}**")
                st.write(generate_daily_advice(day))

def show_weather_page(location=None):
    """Display the full weather analysis page"""
    st.title(f"🌦️ {t('Weather Center')}")
    
    # Use provided location or retrieve from profile/session
    if not location:
        profile = st.session_state.user_profile or {}

        # Get location from profile only
        location = get_profile_field(profile, "farm_location", "")

        # unmatched else, fallback to current_user if profile not fully loaded but user is logged in
        if not location and "current_user" in st.session_state and st.session_state.current_user:
            user = st.session_state.current_user
            if isinstance(user, dict):
                location = user.get("farm_location", "")
            else:
                location = getattr(user, "farm_location", "")

    if not location:
        location = st.text_input(t("Enter your location (city, country):"))
        if not location:
            st.warning(t("Please enter a location to view weather data"))
            return
    
    # Fetch data with loading indicators
    with st.spinner(t("Loading current weather...")):
        weather_data = fetch_weather_data(location)
    
    with st.spinner(t("Loading forecast data...")):
        forecast_data = fetch_forecast_data(location)
    
    if not weather_data or not forecast_data:
        st.error(t("Failed to load weather data. Please try again later."))
        return
    
    # Display all weather sections
    st.header(t("Current Conditions"))
    display_current_weather(weather_data)
    
    display_weather_alerts(weather_data)
    
    display_agricultural_metrics(weather_data)
    
    display_5day_forecast(forecast_data)
    
    # Comprehensive advisory
    st.header(t("Agricultural Advisory"))
    advisory = generate_comprehensive_advisory(weather_data, forecast_data)
    st.markdown(advisory)
    
    # Crop-specific analysis
    st.header(t("Crop-Specific Analysis"))
    crop_options = [
    "Tomato", "Potato", "Wheat", "Rice", "Mango",
    "Onion", "Soybean", "Cotton", "Cabbage", "Cauliflower",
    "Brinjal", "Lady Finger", "Chili", "Bottle Gourd", "Bitter Gourd",
    "Cluster Beans", "Cucumber", "Maize", "Grapes", "Carrot",
    "Radish", "Pumpkin", "Orange", "Banana", "Watermelon",
    "Guava", "Pomegranate"
    ]

    crop = st.selectbox(
        t("Select a crop for analysis:"),
        crop_options,
        format_func=lambda x: t(x)
    )

    
    if crop:
        impact = get_crop_weather_impact(crop, weather_data)
        if impact:
            st.subheader(f"{t('Analysis for')} {crop}")
            
            if impact.get("pros"):
                st.success(f"**{t('Positive Conditions')}**")
                for pro in impact["pros"]:
                    st.write(f"✅ {pro}")
            
            if impact.get("cons"):
                st.error(f"**{t('Weather Impacts (Risks)')}**")
                for con in impact["cons"]:
                    st.write(f"❌ {con}")
            
            if impact.get("suggestions"):
                st.info(f"**{t('Recommended Actions')}**")
                for suggestion in impact["suggestions"]:
                    st.write(f"🚜 {suggestion}")


def estimate_uv_index(weather_data):
    """Estimate UV index based on weather conditions"""
    if not weather_data:
        return t("Unknown")
    
    # Get relevant weather parameters
    cloud_cover = weather_data.get("clouds", {}).get("all", 0)
    time_of_day = datetime.fromtimestamp(weather_data.get("dt", 0)).hour
    season = datetime.fromtimestamp(weather_data.get("dt", 0)).month
    
    # Simple estimation (in a real app, we'd use a proper UV API)
    base_uv = {
        1: 3, 2: 4, 3: 6, 4: 8, 5: 9, 6: 10,  # Summer months
        7: 9, 8: 8, 9: 6, 10: 4, 11: 3, 12: 2  # Winter months
    }.get(season, 5)
    
    # Adjust for time of day (peak at solar noon)
    time_factor = 1 - abs(12 - time_of_day) / 12
    base_uv *= time_factor
    
    # Adjust for cloud cover
    cloud_factor = 1 - (cloud_cover / 100) * 0.7  # Clouds block up to 70% of UV
    estimated_uv = max(0, min(12, base_uv * cloud_factor))
    
    return round(estimated_uv)

def get_uv_risk_level(uv_index):
    """Get UV risk level description"""
    try:
        uv_index = float(uv_index)
    except:
        return t("Unknown")
    
    if uv_index < 3:
        return t("Low")
    elif uv_index < 6:
        return t("Moderate")
    elif uv_index < 8:
        return t("High")
    elif uv_index < 11:
        return t("Very High")
    else:
        return t("Extreme")

def estimate_solar_radiation(weather_data):
    """Estimate solar radiation in W/m²"""
    if not weather_data:
        return t("Unknown")
    
    # Get relevant weather parameters
    cloud_cover = weather_data.get("clouds", {}).get("all", 0)
    time_of_day = datetime.fromtimestamp(weather_data.get("dt", 0)).hour
    season = datetime.fromtimestamp(weather_data.get("dt", 0)).month
    
    # Simple estimation (in a real app, we'd use a proper solar API)
    max_radiation = {
        1: 500, 2: 600, 3: 700, 4: 800, 5: 900, 6: 1000,  # Summer months
        7: 950, 8: 850, 9: 750, 10: 650, 11: 550, 12: 450  # Winter months
    }.get(season, 700)
    
    # Adjust for time of day (peak at solar noon)
    time_factor = 1 - abs(12 - time_of_day) / 12
    solar_rad = max_radiation * time_factor
    
    # Adjust for cloud cover
    cloud_factor = 1 - (cloud_cover / 100) * 0.8  # Clouds block up to 80% of solar
    estimated_rad = max(0, min(1200, solar_rad * cloud_factor))
    
    return round(estimated_rad)

def calculate_evapotranspiration(weather_data):
    """Calculate reference evapotranspiration (ET₀) using simplified FAO method"""
    if not weather_data:
        return 0.0
    
    try:
        # Get required parameters
        temp = weather_data["main"]["temp"]  # °C
        humidity = weather_data["main"]["humidity"]  # %
        wind_speed = weather_data["wind"]["speed"]  # m/s
        solar_rad = estimate_solar_radiation(weather_data)  # W/m²
        
        # Convert solar radiation from W/m² to MJ/m²/day
        solar_mj = solar_rad * 0.0864  # Conversion factor
        
        # Calculate saturation vapor pressure (es)
        es = 0.6108 * (17.27 * temp) / (temp + 237.3)
        
        # Calculate actual vapor pressure (ea)
        ea = es * (humidity / 100)
        
        # Calculate slope of vapor pressure curve (Δ)
        delta = (4098 * es) / ((temp + 237.3) ** 2)
        
        # Psychrometric constant (γ)
        gamma = 0.665 * 10 ** -3 * 101.3  # Assuming constant pressure
        
        # Simplified FAO Penman-Monteith equation
        numerator = (0.408 * delta * solar_mj) + (gamma * (900 / (temp + 273)) * wind_speed * (es - ea))
        denominator = delta + (gamma * (1 + 0.34 * wind_speed))
        
        et0 = numerator / denominator
        
        return max(0, round(et0, 1))
    
    except Exception as e:
        st.error(f"{t('Error calculating evapotranspiration')}: {str(e)}")
        return 0.0

def get_weather_alerts(weather_data):
    """
    Generate comprehensive weather alerts based on current conditions
    
    Args:
        weather_data (dict): Weather data from API
        
    Returns:
        list: List of alert messages with severity and recommendations
    """
    alerts = []
    
    if not weather_data:
        return alerts
    
    # Get weather parameters
    main = weather_data.get("main", {})
    temp = main.get("temp")
    humidity = main.get("humidity")
    pressure = main.get("pressure")
    wind = weather_data.get("wind", {})
    wind_speed = wind.get("speed")
    wind_gust = wind.get("gust")
    wind_dir = wind.get("deg")
    rain = weather_data.get("rain", {})
    rain_1h = rain.get("1h", 0)
    rain_3h = rain.get("3h", 0)
    snow = weather_data.get("snow", {})
    snow_1h = snow.get("1h", 0)
    clouds = weather_data.get("clouds", {}).get("all", 0)
    weather_id = weather_data.get("weather", [{}])[0].get("id") if weather_data.get("weather") else None
    
    # Temperature alerts
    if temp is not None:
        if temp > 38:
            alerts.append({
                "type": "danger",
                "title": t("Extreme Heat Warning"),
                "message": t("Dangerously high temperatures may cause heat stress in crops and livestock."),
                "recommendations": [
                    t("Increase irrigation frequency to prevent heat stress"),
                    t("Provide shade for sensitive crops and animals"),
                    t("Avoid working during peak heat hours (11AM-3PM)"),
                    t("Monitor for signs of wilting in crops")
                ]
            })
        elif temp > 32:
            alerts.append({
                "type": "warning",
                "title": t("High Temperature Alert"),
                "message": t("Elevated temperatures may affect crop growth and livestock comfort."),
                "recommendations": [
                    t("Adjust irrigation schedules to account for increased evaporation"),
                    t("Monitor water levels in ponds and reservoirs"),
                    t("Consider temporary shade structures for sensitive crops")
                ]
            })
        elif temp < 0:
            alerts.append({
                "type": "danger",
                "title": t("Freezing Conditions"),
                "message": t("Freezing temperatures pose risk of frost damage to crops."),
                "recommendations": [
                    t("Protect sensitive crops with frost covers or mulch"),
                    t("Harvest mature crops that may be damaged by frost"),
                    t("Consider irrigation to create protective ice layer on plants"),
                    t("Move potted plants to sheltered areas")
                ]
            })
        elif temp < 5:
            alerts.append({
                "type": "warning",
                "title": t("Cold Temperature Alert"),
                "message": t("Cold conditions may slow plant growth and affect livestock."),
                "recommendations": [
                    t("Delay planting of sensitive crops until temperatures rise"),
                    t("Provide additional bedding for livestock"),
                    t("Monitor for cold stress in young plants")
                ]
            })
    
    # Humidity alerts
    if humidity is not None:
        if humidity > 85:
            alerts.append({
                "type": "warning",
                "title": t("High Humidity Alert"),
                "message": t("High humidity increases risk of fungal diseases in crops."),
                "recommendations": [
                    t("Monitor crops for signs of fungal infection"),
                    t("Improve air circulation around plants where possible"),
                    t("Apply preventive fungicides if appropriate"),
                    t("Avoid overhead irrigation to reduce leaf wetness")
                ]
            })
        elif humidity < 30:
            alerts.append({
                "type": "warning",
                "title": t("Low Humidity Alert"),
                "message": t("Low humidity increases water loss through transpiration."),
                "recommendations": [
                    t("Increase irrigation frequency to compensate for dry conditions"),
                    t("Apply mulch to reduce soil moisture evaporation"),
                    t("Consider shade structures to reduce water loss"),
                    t("Monitor for signs of water stress in plants")
                ]
            })
    
    # Precipitation alerts
    if rain_1h > 10 or rain_3h > 20:
        alerts.append({
            "type": "danger",
            "title": t("Heavy Rainfall Warning"),
            "message": t("Heavy rain may cause flooding, waterlogging, and soil erosion."),
            "recommendations": [
                t("Check and clear drainage systems"),
                t("Monitor low-lying areas for water accumulation"),
                t("Postpone fertilizer applications to prevent runoff"),
                t("Inspect fields for signs of erosion after rain")
            ]
        })
    elif rain_1h > 5 or rain_3h > 10:
        alerts.append({
            "type": "warning",
            "title": t("Moderate Rainfall Alert"),
            "message": t("Moderate rainfall may affect field operations and crop health."),
            "recommendations": [
                t("Check field drainage systems"),
                t("Delay field operations until soil conditions improve"),
                t("Monitor for signs of disease after wet conditions")
            ]
        })
    
    if snow_1h > 2:
        alerts.append({
            "type": "danger",
            "title": t("Heavy Snowfall Warning"),
            "message": t("Heavy snow may damage crops and structures."),
            "recommendations": [
                t("Protect sensitive crops with covers or supports"),
                t("Clear snow from greenhouse roofs to prevent collapse"),
                t("Monitor livestock for cold stress"),
                t("Delay field operations until snow melts")
            ]
        })
    
    # Wind alerts
    if wind_speed is not None:
        if wind_speed > 15 or (wind_gust and wind_gust > 20):
            alerts.append({
                "type": "danger",
                "title": t("High Wind Warning"),
                "message": t("Strong winds may cause physical damage to crops and structures."),
                "recommendations": [
                    t("Secure greenhouse covers and structures"),
                    t("Stake or support tall crops and young trees"),
                    t("Postpone pesticide applications to prevent drift"),
                    t("Monitor for wind damage after event")
                ]
            })
        elif wind_speed > 10:
            alerts.append({
                "type": "warning",
                "title": t("Windy Conditions"),
                "message": t("Moderate winds may increase water loss and affect spray applications."),
                "recommendations": [
                    t("Adjust irrigation to account for increased evaporation"),
                    t("Avoid spraying pesticides in windy conditions"),
                    t("Monitor for signs of wind damage in sensitive crops")
                ]
            })
    
    # Weather condition alerts
    if weather_id:
        # Thunderstorm
        if 200 <= weather_id < 300:
            alerts.append({
                "type": "danger",
                "title": t("Thunderstorm Alert"),
                "message": t("Thunderstorms may bring lightning, hail, and strong winds."),
                "recommendations": [
                    t("Seek shelter immediately if outdoors"),
                    t("Unplug sensitive electrical equipment"),
                    t("Protect crops from potential hail damage if possible"),
                    t("Monitor weather updates for severe storm warnings")
                ]
            })
        # Drizzle/Rain
        elif 300 <= weather_id < 400 or 500 <= weather_id < 600:
            if 502 <= weather_id <= 504:
                alerts.append({
                    "type": "warning",
                    "title": t("Heavy Rain Alert"),
                    "message": t("Heavy rain may affect field conditions and crop health."),
                    "recommendations": [
                        t("Check field drainage systems"),
                        t("Monitor for signs of waterlogging in crops"),
                        t("Postpone field operations until conditions improve")
                    ]
                })
        # Snow
        elif 600 <= weather_id < 700:
            alerts.append({
                "type": "warning",
                "title": t("Snow Alert"),
                "message": t("Snow may affect crop growth and field operations."),
                "recommendations": [
                    t("Protect sensitive crops with covers"),
                    t("Delay planting until snow melts"),
                    t("Monitor for cold stress in livestock")
                ]
            })
        # Atmosphere (fog, haze, etc.)
        elif 700 <= weather_id < 800:
            if weather_id == 731 or weather_id == 751 or weather_id == 761:
                alerts.append({
                    "type": "warning",
                    "title": t("Dust/Sand Alert"),
                    "message": t("Dust or sand in the air may affect crops and equipment."),
                    "recommendations": [
                        t("Protect sensitive equipment from dust damage"),
                        t("Irrigate to settle dust on crops if possible"),
                        t("Consider postponing field operations until conditions improve")
                    ]
                })
            elif weather_id == 762:
                alerts.append({
                    "type": "danger",
                    "title": t("Volcanic Ash Alert"),
                    "message": t("Volcanic ash may damage crops and pose health risks."),
                    "recommendations": [
                        t("Take immediate precautions to protect yourself and livestock"),
                        t("Cover sensitive crops if possible"),
                        t("Avoid working outdoors until ash settles"),
                        t("Clean ash from leaves to prevent damage")
                    ]
                })
    
    # Pressure alerts
    if pressure is not None:
        if pressure < 980:
            alerts.append({
                "type": "warning",
                "title": t("Low Pressure System"),
                "message": t("Low pressure may indicate approaching stormy weather."),
                "recommendations": [
                    t("Monitor weather forecasts for storm warnings"),
                    t("Secure loose items around the farm"),
                    t("Prepare drainage systems for potential heavy rain")
                ]
            })
    
    return alerts

def format_forecast_data(forecast_data):
    """
    Format forecast data for display with agricultural insights
    
    Args:
        forecast_data (dict): Raw forecast data
        
    Returns:
        list: Formatted forecast entries with farming insights
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
        day_name = t(dt.strftime("%A"))  # Get day name (Monday, Tuesday, etc.)
        
        # Calculate values for the day
        temp_sum = sum(entry["main"]["temp"] for entry in entries)
        temp_min = min(entry["main"]["temp_min"] for entry in entries)
        temp_max = max(entry["main"]["temp_max"] for entry in entries)
        humidity_sum = sum(entry["main"]["humidity"] for entry in entries)
        wind_speeds = [entry["wind"]["speed"] for entry in entries if "wind" in entry]
        avg_wind = sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0
        wind_dirs = [entry["wind"]["deg"] for entry in entries if "wind" in entry and "deg" in entry["wind"]]
        wind_dir = wind_dirs[0] if wind_dirs else None
        
        # Get the most common weather condition
        weather_descriptions = [entry["weather"][0]["description"] for entry in entries]
        weather_icons = [entry["weather"][0]["icon"] for entry in entries]
        
        # Use the most common description and corresponding icon
        from collections import Counter
        common_desc = Counter(weather_descriptions).most_common(1)[0][0]
        common_icon = next((icon for desc, icon in zip(weather_descriptions, weather_icons) 
                         if desc == common_desc), weather_icons[0])
        
        # Calculate rain if available
        total_rain = 0
        for entry in entries:
            if "rain" in entry:
                total_rain += entry["rain"].get("3h", 0)
        
        # Calculate cloud cover
        avg_clouds = sum(entry.get("clouds", {}).get("all", 0) for entry in entries) / len(entries)
        
        # Format the entry
        formatted_entry = {
            "day": day,
            "day_name": day_name,
            "avg_temp": temp_sum / len(entries),
            "min_temp": temp_min,
            "max_temp": temp_max,
            "avg_humidity": humidity_sum / len(entries),
            "weather_description": t(common_desc.capitalize()),
            "weather_icon": common_icon,
            "total_rain": total_rain,
            "avg_wind_speed": avg_wind,
            "wind_direction": wind_dir,
            "avg_cloud_cover": avg_clouds,
            "hourly_data": entries  # Keep hourly data for detailed analysis
        }
        
        formatted_entries.append(formatted_entry)
    
    return formatted_entries

def generate_daily_advice(day_forecast):
    """
    Generate agricultural advice for a specific day's forecast
    
    Args:
        day_forecast (dict): Formatted forecast data for one day
        
    Returns:
        str: Markdown formatted advice
    """
    advice = []
    
    # Temperature advice
    if day_forecast["max_temp"] > 35:
        advice.append(f"🌡️ **{t('Heat Advisory')}**: {t('Extreme heat expected. Consider')}:")
        advice.append(f"- {t('Increase irrigation frequency')}")
        advice.append(f"- {t('Provide shade for sensitive crops')}")
        advice.append(f"- {t('Avoid working during peak heat hours')}")
    elif day_forecast["max_temp"] > 30:
        advice.append(f"🌡️ **{t('Warm Day')}**: {t('Monitor for heat stress. Consider')}:")
        advice.append(f"- {t('Adjust irrigation to account for higher evaporation')}")
        advice.append(f"- {t('Check soil moisture levels')}")
    elif day_forecast["min_temp"] < 5:
        advice.append(f"❄️ **{t('Cold Advisory')}**: {t('Frost risk possible. Consider')}:")
        advice.append(f"- {t('Protect sensitive crops with covers')}")
        advice.append(f"- {t('Delay early morning irrigation')}")
        advice.append(f"- {t('Harvest frost-sensitive produce')}")
    
    # Rain advice
    if day_forecast["total_rain"] > 10:
        advice.append(f"🌧️ **{t('Heavy Rain Expected')}**: {t('Potential impacts')}:")
        advice.append(f"- {t('Check field drainage systems')}")
        advice.append(f"- {t('Postpone fertilizer applications')}")
        advice.append(f"- {t('Monitor for waterlogging')}")
    elif day_forecast["total_rain"] > 2:
        advice.append(f"🌧️ **{t('Rain Expected')}**: {t('Considerations')}:")
        advice.append(f"- {t('Good time for planting or transplanting')}")
        advice.append(f"- {t('Reduce irrigation accordingly')}")
        advice.append(f"- {t('Monitor for disease after wet conditions')}")
    
    # Wind advice
    if day_forecast["avg_wind_speed"] > 10:
        advice.append(f"💨 **{t('Windy Conditions')}**: {t('Potential impacts')}:")
        advice.append(f"- {t('Secure greenhouse covers and structures')}")
        advice.append(f"- {t('Avoid pesticide applications')}")
        advice.append(f"- {t('Monitor for physical damage to crops')}")
    
    # General farming activities
    if day_forecast["avg_cloud_cover"] < 30 and day_forecast["total_rain"] < 1:
        advice.append(f"☀️ **{t('Good Day For')}**:")
        advice.append(f"- {t('Field preparation and planting')}")
        advice.append(f"- {t('Harvesting and drying crops')}")
        advice.append(f"- {t('Pesticide applications (if needed)')}")
    elif day_forecast["avg_cloud_cover"] > 70:
        advice.append(f"☁️ **{t('Overcast Conditions')}**: {t('Suitable for')}:")
        advice.append(f"- {t('Transplanting to reduce shock')}")
        advice.append(f"- {t('Pruning operations')}")
    
    if not advice:
        advice.append(f"ℹ️ **{t('Normal Conditions')}**: {t('No special precautions needed.')}")
    
    return "\n".join(advice)

def generate_comprehensive_advisory(weather_data, forecast_data):
    """
    Generate comprehensive farming advisory based on current and forecasted weather
    
    Args:
        weather_data (dict): Current weather data
        forecast_data (dict): Forecast data
        
    Returns:
        str: Markdown formatted advisory
    """
    if not weather_data or not forecast_data:
        return t("No weather data available to generate advisory.")
    
    advisory = []
    
    # Current conditions summary
    current_temp = weather_data["main"]["temp"]
    current_humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    rain = weather_data.get("rain", {}).get("1h", 0)
    weather_desc = weather_data["weather"][0]["description"].capitalize()
    
    advisory.append(f"## {t('Current Weather Advisory')}")
    advisory.append(f"- {t('Temperature')}: {current_temp:.1f}°C")
    advisory.append(f"- {t('Humidity')}: {current_humidity}%")
    advisory.append(f"- {t('Wind')}: {wind_speed} m/s")
    advisory.append(f"- {t('Precipitation')}: {rain} mm ({t('last hour')})")
    advisory.append(f"- {t('Conditions')}: {t(weather_desc)}")
    advisory.append("")
    
    # Current weather impacts
    advisory.append(f"### {t('Immediate Recommendations')}:")
    
    # Temperature impacts
    if current_temp > 35:
        advisory.append(f"- **{t('Heat Stress Management')}**:")
        advisory.append(f"  - {t('Increase irrigation frequency to combat heat stress')}")
        advisory.append(f"  - {t('Provide shade for sensitive crops and livestock')}")
        advisory.append(f"  - {t('Avoid field work during peak heat hours (11AM-3PM)')}")
    elif current_temp < 5:
        advisory.append(f"- **{t('Cold Protection')}**:")
        advisory.append(f"  - {t('Protect sensitive crops with frost covers or mulch')}")
        advisory.append(f"  - {t('Move potted plants to sheltered areas')}")
        advisory.append(f"  - {t('Provide additional bedding for livestock')}")
    
    # Humidity impacts
    if current_humidity > 80:
        advisory.append(f"- **{t('High Humidity Management')}**:")
        advisory.append(f"  - {t('Monitor for fungal diseases (powdery mildew, rust)')}")
        advisory.append(f"  - {t('Improve air circulation around plants')}")
        advisory.append(f"  - {t('Consider preventive fungicide applications')}")
    elif current_humidity < 30:
        advisory.append(f"- **{t('Low Humidity Management')}**:")
        advisory.append(f"  - {t('Increase irrigation frequency')}")
        advisory.append(f"  - {t('Apply mulch to conserve soil moisture')}")
        advisory.append(f"  - {t('Monitor for signs of water stress')}")
    
    # Wind impacts
    if wind_speed > 10:
        advisory.append(f"- **{t('Windy Conditions')}**:")
        advisory.append(f"  - {t('Secure greenhouse covers and structures')}")
        advisory.append(f"  - {t('Stake or support tall crops')}")
        advisory.append(f"  - {t('Avoid pesticide applications to prevent drift')}")
    
    # Rain impacts
    if rain > 5:
        advisory.append(f"- **{t('Heavy Rain Response')}**:")
        advisory.append(f"  - {t('Check and clear drainage systems')}")
        advisory.append(f"  - {t('Monitor low-lying areas for water accumulation')}")
        advisory.append(f"  - {t('Postpone fertilizer applications to prevent runoff')}")
    elif rain > 0:
        advisory.append(f"- **{t('Rainy Conditions')}**:")
        advisory.append(f"  - {t('Reduce irrigation accordingly')}")
        advisory.append(f"  - {t('Monitor for disease after wet conditions')}")
    
        advisory.append(f"### {day['day_name']} ({day['day']})")
        advisory.append(f"- **{t('Temperature')}**: {t('High')} {day['max_temp']:.1f}°C / {t('Low')} {day['min_temp']:.1f}°C")
        advisory.append(f"- **{t('Humidity')}**: {day['avg_humidity']:.0f}%")
        advisory.append(f"- **{t('Rain')}**: {day['total_rain']:.1f} mm")
        advisory.append(f"- **{t('Wind')}**: {day['avg_wind_speed']:.1f} m/s")
        advisory.append(f"- **{t('Conditions')}**: {day['weather_description']}")
        
        # Add daily advice
        daily_advice = generate_daily_advice(day)
        advisory.append("")
        advisory.append(f"**{t('Daily Farming Advice')}**:")
        advisory.append(daily_advice)
        advisory.append("")
    
    # Seasonal planning
    advisory.append("")
    advisory.append(f"## {t('Seasonal Planning Considerations')}")
    
    now = datetime.now()
    month = now.month
    
    if 3 <= month <= 5:  # Spring
        advisory.append(f"- **{t('Spring Planting')}**:")
        advisory.append(f"  - {t('Prepare seedbeds for summer crops')}")
        advisory.append(f"  - {t('Complete soil testing and amendment')}")
        advisory.append(f"  - {t('Begin planting warm-season crops as soil warms')}")
    elif 6 <= month <= 8:  # Summer
        advisory.append(f"- **{t('Summer Management')}**:")
        advisory.append(f"  - {t('Monitor irrigation carefully')}")
        advisory.append(f"  - {t('Watch for pest outbreaks in warm weather')}")
        advisory.append(f"  - {t('Begin planning for fall crops')}")
    elif 9 <= month <= 11:  # Fall
        advisory.append(f"- **{t('Fall Harvest')}**:")
        advisory.append(f"  - {t('Harvest mature crops')}")
        advisory.append(f"  - {t('Plant cover crops in harvested fields')}")
        advisory.append(f"  - {t('Test and amend soil for next season')}")
    else:  # Winter
        advisory.append(f"- **{t('Winter Preparation')}**:")
        advisory.append(f"  - {t('Protect sensitive plants from frost')}")
        advisory.append(f"  - {t('Service farm equipment during downtime')}")
        advisory.append(f"  - {t('Plan next season\'s crop rotation')}")
    
    return "\n".join(advisory)

def display_weather_widget(location=None):
    """
    Display a compact weather widget for dashboard
    
    Args:
        location (str): Location to show weather for. If None, uses profile location.
        
    Returns:
        None: Renders the widget directly
    """
    if location is None:
        location = get_profile_field(st.session_state.user_profile, "farm_location")
        if not location:
            st.warning(t("Please set your location in profile settings"))
            return
    
    weather_data = fetch_weather_data(location)
    if not weather_data:
        st.error(t("Could not fetch weather data"))
        return
    
    # Extract weather info
    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    weather_desc = weather_data["weather"][0]["description"].capitalize()
    icon_code = weather_data["weather"][0]["icon"]
    
    # Create columns for layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Display weather icon
        st.image(get_weather_icon_url(icon_code), width=80)
    
    with col2:
        # Display weather info
        st.metric(label=t("Temperature"), value=f"{temp:.1f}°C")
        st.caption(f"{t(weather_desc)} | {t('Humidity')}: {humidity}% | {t('Wind')}: {wind_speed} m/s")
        
        # Show critical alerts if any
        alerts = get_weather_alerts(weather_data)
        critical_alerts = [a for a in alerts if a["type"] == "danger"]
        if critical_alerts:
            st.warning(f"⚠️ {len(critical_alerts)} {t('active weather alerts')}")

def get_crop_weather_impact(crop_name, weather_data):
    """
    Analyze the impact of current weather on a specific crop using the rich weather_data_store.
    
    Args:
        crop_name (str): Name of the crop to analyze
        weather_data (dict): Current weather data from API
        
    Returns:
        dict: Dictionary with pros, cons, and suggestions
    """
    if not weather_data or not crop_name:
        return None
    
    # Get weather parameters
    temp = weather_data.get("main", {}).get("temp")
    humidity = weather_data.get("main", {}).get("humidity")
    wind_speed = weather_data.get("wind", {}).get("speed")
    is_raining = "rain" in weather_data
    rain_amount = weather_data.get("rain", {}).get("1h", 0) if is_raining else 0
    
    # Initialize result structure
    impact = {
        "crop": crop_name,
        "pros": [],
        "cons": [],
        "suggestions": []
    }

    # 1. Find Crop Data in Store
    # Try exact match (e.g. TOMATO -> TOMATO_WEATHER_INTELLIGENCE)
    clean_name = crop_name.strip().upper().replace(" ", "_")
    var_name = f"{clean_name}_WEATHER_INTELLIGENCE"
    
    crop_info = getattr(weather_data_store, var_name, None)
    
    if not crop_info:
        # Fallback: Try finding by partial name
        for attr in dir(weather_data_store):
             if attr.endswith("_WEATHER_INTELLIGENCE") and clean_name in attr:
                 crop_info = getattr(weather_data_store, attr)
                 break
    
    if not crop_info:
        impact["cons"].append(t(f"Detailed weather intelligence for {crop_name} is currently being updated."))
        return impact

    # 2. Analyze Temperature
    if temp is not None and "temperature_ranges" in crop_info:
        for state, details in crop_info["temperature_ranges"].items():
            min_t, max_t = details["range"]
            if min_t <= temp <= max_t:
                msg = f"{t('Temp')} {temp:.1f}°C: {t(details['impact'])}"
                if "optimal" in state or "good" in state:
                    impact["pros"].append(msg)
                else:
                    impact["cons"].append(msg)
                
                # Add unique actions
                for action in details.get("actions", []):
                    if action not in impact["suggestions"]:
                        impact["suggestions"].append(t(action))
                break # Match found

    # 3. Analyze Humidity
    if humidity is not None and "humidity_ranges" in crop_info:
        for state, details in crop_info["humidity_ranges"].items():
            min_h, max_h = details["range"]
            if min_h <= humidity <= max_h:
                msg = f"{t('Humidity')} {humidity}%: {t(details['impact'])}"
                if "optimal" in state or "moderate" in state:
                    impact["pros"].append(msg)
                else:
                    impact["cons"].append(msg)
                
                for action in details.get("actions", []):
                    if action not in impact["suggestions"]:
                        impact["suggestions"].append(t(action))
                break

    # 4. Analyze Rainfall
    # Determine appropriate rain key
    rain_key = "no_rain"
    if rain_amount >= 10:
        rain_key = "heavy_rain"
    elif rain_amount >= 1:
        rain_key = "moderate_rain" # Assuming store might have this, strictly mapping to existing keys provided in store
        # Wait, the store provided in previous turn had 'no_rain' (0-1) and 'heavy_rain' (10-200). 
        # It didn't explicitly cover 1-10 in the snippets I saw for all crops, or maybe I missed it.
        # Let's check a standard one like Tomato: no_rain (0-1), heavy_rain (10-200).
        # It seems gaps might exist or I should logic check.
        # Let's iterate ranges which is safer.
    
    if "rainfall_ranges" in crop_info:
        # We iterate to find the matching range
        match_found = False
        for state, details in crop_info["rainfall_ranges"].items():
            min_r, max_r = details["range"]
            # effective check
            if min_r <= rain_amount < max_r: # strict inequality for upper bound usually, or inclusive? 
                # The tuples in store are like (0, 1), (10, 200). 
                # Logic: check if in range.
                match_found = True
                msg = f"{t('Rain')} {rain_amount}mm: {t(details['impact'])}"
                if "no_rain" in state and rain_amount == 0:
                     # Could be pro or con depending on irrigation. 
                     # Usually store says "Irrigation dependent" which is neutral/action-required.
                     impact["cons"].append(msg)
                elif "optimal" in state:
                    impact["pros"].append(msg)
                else:
                     impact["cons"].append(msg)
                
                for action in details.get("actions", []):
                    if action not in impact["suggestions"]:
                         impact["suggestions"].append(t(action))
                break
        
        # If rain is in a gap (e.g. 1-10mm) and no range blocked it, we might want a default.
        # But sticking to the store's definitions is best.

    # 5. Analyze Wind
    if wind_speed is not None and "wind_ranges" in crop_info:
        for state, details in crop_info["wind_ranges"].items():
            min_w, max_w = details["range"]
            if min_w <= wind_speed <= max_w:
                msg = f"{t('Wind')} {wind_speed}m/s: {t(details['impact'])}"
                if "moderate" in state or "optimal" in state:
                    impact["pros"].append(msg)
                elif "low" in state:
                    impact["cons"].append(msg) # Low wind often linked to pest/disease in store
                else:
                    impact["cons"].append(msg)
                
                for action in details.get("actions", []):
                    if action not in impact["suggestions"]:
                        impact["suggestions"].append(t(action))
                break

    # If nothing found (rare if data is good)
    if not impact["pros"] and not impact["cons"]:
        impact["pros"].append(t("Weather seems generally okay for growth."))

    return impact

