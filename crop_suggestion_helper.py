import streamlit as st
import os
import numpy as np
import time
from PIL import Image
import matplotlib.pyplot as plt
import io
import base64
import json
from datetime import datetime
import random
import requests
import pandas as pd

# Import custom modules
from image_processing import preprocess_image, extract_features
from model_handler import identify_plant, detect_water_content, detect_diseases, detect_pests
from recommendations import get_preventive_measures, get_fertilizer_recommendations
from utils import load_svg, get_example_images, generate_report_markdown, format_probability, save_uploaded_image, get_secret
from db_adapter import create_user, verify_user, update_user_profile, save_analysis, get_user_analyses, get_user_by_id, get_user_profile
from maharashtra import get_local_recommendations
from profile_utils import get_profile_field, get_select_index
from soil_analyzer import analyze_soil, get_soil_details
from model import load_model
from plant_analysis import enhanced_analysis
from weather_service import display_weather_widget, show_weather_page, fetch_weather_data, fetch_forecast_data, get_weather_alerts
from language_support import initialize_language, show_language_selector, t,translate_api


# Add these helper functions at the top of your file

def get_weather_data(location, api_key=None):
    """
    Fetch weather data from OpenWeatherMap API
    If no API key or location, return simulated data for demonstration
    """
    # For demo purposes - you can replace with actual API call
    # Sign up for free API key at https://openweathermap.org/api
    
    api_key = get_secret("WEATHER_API_KEY")

    if api_key and location and location != t("Field name or coordinates"):
        try:
            # Try to get coordinates if location is a place name
            geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
            geo_response = requests.get(geocoding_url)
            
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                if geo_data:
                    lat = geo_data[0]['lat']
                    lon = geo_data[0]['lon']
                    
                    # Get weather forecast
                    weather_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                    weather_response = requests.get(weather_url)
                    
                    if weather_response.status_code == 200:
                        weather_data = weather_response.json()
                        return process_weather_data(weather_data)
        except Exception as e:
            st.warning(f"{t('Could not fetch live weather data')}: {str(e)}. {t('Using simulated data.')}")
    
    # Return simulated data for demo
    return get_simulated_weather_data()


def process_weather_data(weather_data):
    """Process raw weather API data into useful format"""
    processed = {
        "current_temp": None,
        "forecast_3month": [],
        "rainfall_prediction": {},
        "season_suitability": {},
        "extreme_events": [],
        "summary": ""
    }
    
    try:
        # Get current conditions
        if 'list' in weather_data and len(weather_data['list']) > 0:
            current = weather_data['list'][0]
            processed['current_temp'] = current['main']['temp']
            
            # Process 3-month forecast (approximate from 5-day forecast)
            daily_data = {}
            for item in weather_data['list']:
                date = item['dt_txt'].split()[0]
                if date not in daily_data:
                    daily_data[date] = {
                        'temp': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'rain': item.get('rain', {}).get('3h', 0),
                        'description': item['weather'][0]['description']
                    }
            
            # Aggregate to monthly
            months = {}
            for date, data in daily_data.items():
                month = date[:7]  # YYYY-MM
                if month not in months:
                    months[month] = {'temps': [], 'rain': 0, 'days': 0}
                months[month]['temps'].append(data['temp'])
                months[month]['rain'] += data.get('rain', 0)
                months[month]['days'] += 1
            
            # Calculate averages
            for month, data in months.items():
                avg_temp = sum(data['temps']) / len(data['temps'])
                total_rain = data['rain']
                processed['forecast_3month'].append({
                    'month': month,
                    'avg_temp': round(avg_temp, 1),
                    'total_rain': round(total_rain, 1),
                    'rain_days': data['days']
                })
            
            # Determine season suitability
            for month_data in processed['forecast_3month'][:3]:  # Next 3 months
                temp = month_data['avg_temp']
                rain = month_data['total_rain']
                
                # Simple classification
                if temp > 25:
                    temp_category = "hot"
                elif temp > 15:
                    temp_category = "warm"
                else:
                    temp_category = "cool"
                
                if rain > 100:
                    rain_category = "heavy"
                elif rain > 50:
                    rain_category = "moderate"
                elif rain > 10:
                    rain_category = "light"
                else:
                    rain_category = "dry"
                
                processed['season_suitability'][month_data['month']] = {
                    'temp': temp_category,
                    'rain': rain_category,
                    'description': f"{temp_category} and {rain_category}"
                }

        # Generate Descriptive Summary for Next 3 Months
        summary_parts = []
        if processed['forecast_3month']:
            months = processed['forecast_3month'][:3]
            
            # Temperature Trend
            temps = [m['avg_temp'] for m in months]
            avg_t = sum(temps) / len(temps)
            trend = "stable"
            if temps[-1] > temps[0] + 2:
                trend = "rising"
            elif temps[-1] < temps[0] - 2:
                trend = "falling"
            
            summary_parts.append(f"{t('Expect')} **{t(trend)} {t('temperatures')}** {t('averaging around')} {avg_t:.1f}°C.")
            
            # Rainfall Probability
            total_rain = sum(m['total_rain'] for m in months)
            if total_rain > 200:
                summary_parts.append(f"{t('High probability of')} **{t('heavy rainfall')}** ({total_rain:.0f}mm {t('total')}).")
            elif total_rain > 50:
                summary_parts.append(f"{t('Possibility of')} **{t('moderate rain')}** ({total_rain:.0f}mm).")
            else:
                summary_parts.append(t("Conditions will likely be **mostly dry**."))
                
            processed['summary'] = " ".join(summary_parts)
    
    except Exception as e:
        st.error(f"{t('Error processing weather data')}: {str(e)}")
    
    return processed


def get_simulated_weather_data():
    """Generate simulated weather data for demonstration"""
    import random
    from datetime import datetime, timedelta
    
    weather = {
        "current_temp": random.randint(20, 35),
        "forecast_3month": [],
        "rainfall_prediction": {},
        "season_suitability": {},
        "extreme_events": [],
        "summary": ""
    }
    
    current_date = datetime.now()
    
    for i in range(3):
        month_date = current_date + timedelta(days=30*i)
        month_name = month_date.strftime("%Y-%m")
        
        # Simulate seasonal patterns
        if month_date.month in [6, 7, 8, 9]:  # Monsoon months
            avg_temp = random.randint(28, 35)
            total_rain = random.randint(150, 300)
            rain_category = "heavy"
            temp_category = "hot"
        elif month_date.month in [10, 11]:  # Post-monsoon
            avg_temp = random.randint(25, 32)
            total_rain = random.randint(50, 150)
            rain_category = "moderate"
            temp_category = "warm"
        elif month_date.month in [12, 1, 2]:  # Winter
            avg_temp = random.randint(15, 25)
            total_rain = random.randint(10, 50)
            rain_category = "light"
            temp_category = "cool"
        else:  # Summer
            avg_temp = random.randint(30, 40)
            total_rain = random.randint(0, 30)
            rain_category = "dry"
            temp_category = "hot"
        
        weather['forecast_3month'].append({
            'month': month_name,
            'avg_temp': avg_temp,
            'total_rain': total_rain,
            'rain_days': random.randint(rain_category == "heavy" and 15 or 5, rain_category == "heavy" and 25 or 15)
        })
        
        weather['season_suitability'][month_name] = {
            'temp': temp_category,
            'rain': rain_category,
            'description': f"{temp_category} and {rain_category}"
        }
    
    # Random extreme events
    if random.random() > 0.7:
        weather['extreme_events'].append(random.choice([
            "Heat wave possible", "Heavy rainfall warning", "Dry spell expected"
        ]))
    
    # Generate summary
    avg_temp = sum(m['avg_temp'] for m in weather['forecast_3month']) / 3
    total_rain = sum(m['total_rain'] for m in weather['forecast_3month'])
    
    if total_rain > 400:
        rain_summary = "heavy rainfall"
    elif total_rain > 200:
        rain_summary = "moderate rainfall"
    else:
        rain_summary = "low rainfall"
    
    weather['summary'] = f"{t('Next 3 months')}: {t('Average temperature')} {avg_temp:.1f}°C {t('with')} {t(rain_summary)} ({t('approx')} {total_rain:.0f}mm {t('total')})."
    
    return weather


def get_market_prices(crop_names=None, api_key=None):
    """
    Fetch market prices from API
    For demo, using simulated data - can be replaced with actual API like:
    - https://data.gov.in/ (India's open data platform)
    - Commodity market APIs
    """
    
    # Simulated market data for demonstration
    market_data = {
        "Wheat": {
            "current_price": random.randint(1800, 2200),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1900, 2400),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Rice": {
            "current_price": random.randint(2500, 3000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(2600, 3200),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Corn": {
            "current_price": random.randint(1500, 2000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1600, 2200),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Soybean": {
            "current_price": random.randint(3500, 4000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(3600, 4200),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Cotton": {
            "current_price": random.randint(5000, 6000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(5200, 6500),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Tomato": {
            "current_price": random.randint(1500, 3000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1600, 3500),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Potato": {
            "current_price": random.randint(1000, 1800),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1100, 2000),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Onion": {
            "current_price": random.randint(1500, 2500),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1600, 2800),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Cabbage": {
            "current_price": random.randint(1000, 2000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1200, 2200),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Watermelon": {
            "current_price": random.randint(500, 1500),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(600, 1600),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Pomegranate": {
            "current_price": random.randint(4000, 8000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(4200, 8500),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Cluster Beans": {
            "current_price": random.randint(2000, 4000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(2200, 4200),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Grapes": {
            "current_price": random.randint(3000, 6000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(3200, 6500),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Cucumber": {
            "current_price": random.randint(1000, 2500),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1200, 2800),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Bitter Gourd": {
            "current_price": random.randint(1500, 3000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1600, 3200),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Pumpkin": {
            "current_price": random.randint(500, 1200),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(600, 1400),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Bottle Gourd": {
            "current_price": random.randint(1000, 2000),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1100, 2200),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Cauliflower": {
            "current_price": random.randint(1000, 2500),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(1200, 2800),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        },
        "Lady Finger": {
            "current_price": random.randint(2000, 3500),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "demand": random.choice(["High", "Medium", "Low"]),
            "forecast_3months": random.randint(2200, 3800),
            "market_confidence": random.choice(["High", "Medium", "Low"]),
            "seasonal_factor": random.uniform(0.8, 1.2)
        }
    }
    
    # API Configuration
    # Resource ID for "Current Daily Price of Various Commodities from Mandis"
    RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070" 
    BASE_URL = f"https://api.data.gov.in/resource/{RESOURCE_ID}"
    DEFAULT_API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
    
    # Use provided key, secrets key, or default
    api_key = api_key or get_secret("AGMARKNET_API_KEY") or DEFAULT_API_KEY
    
    try:
        # We'll try to fetch data for Maharashtra (since it's the focus) to get some real data
        # The sample key has a limit of 10 records, so we'll just get what we can
        params = {
            "api-key": api_key,
            "format": "json",
            "limit": 100,  # Try to get more, though sample key might limit to 10
            "filters[State]": "Maharashtra"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)

        
        if response.status_code == 200:
            data = response.json()
            records = data.get("records", [])
            
            if records:
                # Update market_data with real values found in records
                for record in records:
                    commodity = record.get("Commodity", "")
                    modal_price = record.get("Modal_Price", "")
                    market = record.get("Market", "")
                    
                    # Normalize commodity name to match our keys
                    matched_key = None
                    for key in market_data.keys():
                        if key.lower() in commodity.lower() or commodity.lower() in key.lower():
                            matched_key = key
                            break
                    
                    if matched_key and modal_price:
                        try:
                            price = float(modal_price)
                            # Update with real data
                            market_data[matched_key]["current_price"] = price
                            market_data[matched_key]["market"] = market
                            market_data[matched_key]["is_real_data"] = True
                            
                            # Adjust forecast slightly based on real vs simulated difference
                            # (Simple heuristic logic)
                            simulated_price = market_data[matched_key]["current_price"]  # formerly simulated
                            # We just overwrote it, but if we hadn't, we could compare.
                            # Recalculate forecast based on real price
                            trend_factor = 1.1 if market_data[matched_key]["price_trend"] == "Increasing" else 0.9
                            market_data[matched_key]["forecast_3months"] = int(price * trend_factor)
                            
                        except ValueError:
                            pass
                            
                st.sidebar.success(f"Fetched {len(records)} live market records!")
            
    except Exception as e:
        # Fallback to simulated data silently or log warning
        # st.warning(f"Using simulated market data (API call failed: {str(e)})")
        pass

    # Filter if specific crops requested
    if crop_names:
        return {crop: data for crop, data in market_data.items() if crop in crop_names}
    
    return market_data


def get_price_prediction(crop_name, market_data, weather_data, time_horizon_months=3):
    """
    Generate price prediction based on market trends and weather impact
    """
    if crop_name not in market_data:
        return None
    
    crop_data = market_data[crop_name]
    
    # Base prediction on current price
    base_price = crop_data['current_price']
    trend_factor = {
        "Increasing": 1.1,
        "Stable": 1.0,
        "Decreasing": 0.9
    }.get(crop_data['price_trend'], 1.0)
    
    # Weather impact on price
    weather_impact = 1.0
    if weather_data and 'forecast_3month' in weather_data:
        # If weather is extreme, prices might increase due to supply shortage
        if len(weather_data.get('extreme_events', [])) > 0:
            weather_impact = 1.15  # 15% price increase due to extreme weather
    
    # Demand impact
    demand_factor = {
        "High": 1.2,
        "Medium": 1.0,
        "Low": 0.8
    }.get(crop_data['demand'], 1.0)
    
    # Calculate predicted price
    predicted_price = base_price * trend_factor * weather_impact * demand_factor
    
    # Apply seasonal factor
    predicted_price *= crop_data.get('seasonal_factor', 1.0)
    
    # Confidence score
    confidence = {
        "High": 0.85,
        "Medium": 0.65,
        "Low": 0.45
    }.get(crop_data['market_confidence'], 0.5)
    
    return {
        "current_price": base_price,
        "predicted_price": round(predicted_price, 2),
        "confidence": confidence,
        "trend": crop_data['price_trend'],
        "demand": crop_data['demand'],
        "roi_potential": round(((predicted_price - base_price) / base_price) * 100, 1),
        "factors": {
            "trend_impact": trend_factor,
            "weather_impact": weather_impact,
            "demand_impact": demand_factor,
            "seasonal_factor": crop_data.get('seasonal_factor', 1.0)
        }
    }


# Update the generate_crop_recommendations function to include weather and market data

def generate_crop_recommendations(soil_results, farmer_inputs):
    """Generate personalized crop recommendations based on soil, farmer inputs, weather, and market data"""
    
    st.markdown(f"### {t('🌱 Top Recommended Crops for Your Farm')}")
    
    # Calculate user duration in months for filtering
    user_duration_months = 3
    if farmer_inputs['time_duration']['unit'] == t("Months"):
        user_duration_months = int(farmer_inputs['time_duration']['value'])
    elif farmer_inputs['time_duration']['unit'] == t("Weeks"):
        user_duration_months = int(farmer_inputs['time_duration']['value'] / 4)
    else:  # Seasons
        user_duration_months = int(farmer_inputs['time_duration']['value'] * 4)
    
    # Ensure minimum 1 month
    user_duration_months = max(1, user_duration_months)

    # Fetch weather data
    location = farmer_inputs.get('sampling_location', '')
    weather_api_key = get_secret("WEATHER_API_KEY", None)
    weather_data = get_weather_data(location, weather_api_key)
    
    # Display weather summary (Personalized)
    with st.expander(t("📊 Current Weather Forecast"), expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{t('Current Temperature')}:** {weather_data.get('current_temp', 'N/A')}°C")
            st.markdown(f"**{t('Forecast for Your Duration')} ({user_duration_months} {t('months')}):**")
            
            # Show forecast matching user duration
            forecasts = weather_data.get('forecast_3month', [])
            # Extend forecast if needed by repeating pattern (simplistic) or just show what we have
            display_forecast = forecasts[:user_duration_months] if len(forecasts) >= user_duration_months else forecasts
            
            if not display_forecast:
                st.write(t("No forecast data available."))
            
            for month in display_forecast:
                st.markdown(f"- {month['month']}: {month['avg_temp']}°C, {month['total_rain']}mm rain")
        
        with col2:
            st.markdown(f"**{t('Weather Summary')}**")
            st.info(weather_data.get('summary', t('Weather data not available')))
            
            if weather_data.get('extreme_events'):
                st.warning(f"⚠️ {t('Extreme Weather Alerts')}: {', '.join(weather_data['extreme_events'])}")
    
    # Fetch market data
    interested = farmer_inputs.get('interested_crops', [])
    market_data = get_market_prices(crop_names=interested if interested else None)
    
    # Display market summary
    with st.expander(t("📈 Current Market Prices"), expanded=False):
        if not market_data:
            st.info(t("No market data available for selected crops."))
        else:
            # Create a table of current prices
            market_df = pd.DataFrame([
                {
                    t('Crop'): t(crop),
                    t('Current Price (₹/quintal)'): data['current_price'],
                    t('Trend'): t(data['price_trend']),
                    t('Demand'): t(data['demand']),
                    t('3-Month Forecast'): data['forecast_3months']
                }
                for crop, data in market_data.items()
            ])
            st.dataframe(market_df, use_container_width=True)
    
    # Sample crop database (consistent with other modules)
    crop_database = [
        {
            "name": "Wheat",
            "soil_types": ["Loamy", "Clay Loam", "Silty", "Black Soil", "Alluvial Soil"],
            "ph_range": (6.0, 7.5),
            "duration_months": 4,
            "investment_per_acre": 15000,
            "attention_level": "Medium",
            "risk_factor": "Low",
            "water_requirement": "Moderate",
            "season": "Rabi",
            "suitable_for_organic": True,
            "temperature_range": (15, 25),
            "rainfall_range": (50, 150),
            "weather_sensitivity": "Medium",
            "market_volatility": "Low",
            "profit_margin": "Medium"
        },
        {
            "name": "Rice",
            "soil_types": ["Clay", "Clay Loam", "Alluvial Soil", "Laterite Soil"],
            "ph_range": (5.5, 6.5),
            "duration_months": 5,
            "investment_per_acre": 20000,
            "attention_level": "High",
            "risk_factor": "Medium",
            "water_requirement": "High",
            "season": "Kharif",
            "suitable_for_organic": True,
            "temperature_range": (20, 35),
            "rainfall_range": (150, 300),
            "weather_sensitivity": "High",
            "market_volatility": "Low",
            "profit_margin": "Low"
        },
        {
            "name": "Corn",
            "soil_types": ["Loamy", "Sandy Loam", "Alluvial Soil", "Red Soil"],
            "ph_range": (5.8, 7.0),
            "duration_months": 3,
            "investment_per_acre": 18000,
            "attention_level": "Medium",
            "risk_factor": "Medium",
            "water_requirement": "Moderate",
            "season": "Kharif",
            "suitable_for_organic": True,
            "temperature_range": (18, 32),
            "rainfall_range": (50, 200),
            "weather_sensitivity": "Medium",
            "market_volatility": "Medium",
            "profit_margin": "Medium"
        },
        {
            "name": "Soybean",
            "soil_types": ["Loamy", "Silty", "Black Soil"],
            "ph_range": (6.0, 7.0),
            "duration_months": 3,
            "investment_per_acre": 12000,
            "attention_level": "Medium",
            "risk_factor": "Medium",
            "water_requirement": "Moderate",
            "season": "Kharif",
            "suitable_for_organic": True,
            "temperature_range": (20, 30),
            "rainfall_range": (40, 120),
            "weather_sensitivity": "Medium",
            "market_volatility": "Medium",
            "profit_margin": "High"
        },
        {
            "name": "Cotton",
            "soil_types": ["Black Soil", "Alluvial Soil"],
            "ph_range": (6.0, 8.0),
            "duration_months": 6,
            "investment_per_acre": 25000,
            "attention_level": "High",
            "risk_factor": "High",
            "water_requirement": "Moderate",
            "season": "Kharif",
            "suitable_for_organic": False,
            "temperature_range": (21, 37),
            "rainfall_range": (50, 150),
            "weather_sensitivity": "High",
            "market_volatility": "High",
            "profit_margin": "High"
        },
        {
            "name": "Tomato",
            "soil_types": ["Loamy", "Sandy Loam", "Red Soil", "Black Soil"],
            "ph_range": (6.0, 6.8),
            "duration_months": 3,
            "investment_per_acre": 30000,
            "attention_level": "Very High",
            "risk_factor": "High",
            "water_requirement": "High",
            "season": "All seasons",
            "suitable_for_organic": True,
            "temperature_range": (20, 30),
            "rainfall_range": (40, 100),
            "weather_sensitivity": "Very High",
            "market_volatility": "High",
            "profit_margin": "Very High"
        },
        {
            "name": "Potato",
            "soil_types": ["Loamy", "Sandy Loam", "Alluvial Soil"],
            "ph_range": (5.0, 6.5),
            "duration_months": 3,
            "investment_per_acre": 22000,
            "attention_level": "High",
            "risk_factor": "Medium",
            "water_requirement": "Moderate",
            "season": "Rabi",
            "suitable_for_organic": True,
            "temperature_range": (15, 25),
            "rainfall_range": (40, 80),
            "weather_sensitivity": "High",
            "market_volatility": "Medium",
            "profit_margin": "Medium"
        },
        {
            "name": "Onion",
            "soil_types": ["Loamy", "Silty", "Black Soil", "Red Soil"],
            "ph_range": (6.0, 7.0),
            "duration_months": 4,
            "investment_per_acre": 20000,
            "attention_level": "High",
            "risk_factor": "Medium",
            "water_requirement": "Moderate",
            "season": "Rabi",
            "suitable_for_organic": True,
            "temperature_range": (13, 35),
            "rainfall_range": (60, 100),
            "weather_sensitivity": "Medium",
            "market_volatility": "High",
            "profit_margin": "High"
        },
        {
            "name": "Cabbage",
            "soil_types": ["Sandy Loam", "Loamy", "Clay Loam"],
            "ph_range": (6.0, 6.8),
            "duration_months": 3,
            "investment_per_acre": 25000,
            "attention_level": "High",
            "risk_factor": "Medium",
            "water_requirement": "High",
            "season": "Winter",
            "suitable_for_organic": True,
            "temperature_range": (15, 25),
            "rainfall_range": (60, 100),
            "weather_sensitivity": "High",
            "market_volatility": "Medium",
            "profit_margin": "Medium"
        },
        {
            "name": "Watermelon",
            "soil_types": ["Sandy", "Sandy Loam", "Loamy"],
            "ph_range": (6.0, 7.0),
            "duration_months": 3,
            "investment_per_acre": 15000,
            "attention_level": "Medium",
            "risk_factor": "Medium",
            "water_requirement": "Moderate",
            "season": "Summer",
            "suitable_for_organic": True,
            "temperature_range": (25, 35),
            "rainfall_range": (40, 60),
            "weather_sensitivity": "High",
            "market_volatility": "High",
            "profit_margin": "High"
        },
        {
            "name": "Pomegranate",
            "soil_types": ["Loamy", "Sandy Loam", "Alluvial Soil", "Lateritic Soil"],
            "ph_range": (6.5, 7.5),
            "duration_months": 12,
            "investment_per_acre": 50000,
            "attention_level": "High",
            "risk_factor": "Medium",
            "water_requirement": "Moderate",
            "season": "All seasons",
            "suitable_for_organic": True,
            "temperature_range": (25, 35),
            "rainfall_range": (50, 70),
            "weather_sensitivity": "Medium",
            "market_volatility": "Low",
            "profit_margin": "Very High"
        },
        {
            "name": "Cluster Beans",
            "soil_types": ["Sandy", "Sandy Loam", "Loamy"],
            "ph_range": (7.0, 8.0),
            "duration_months": 3,
            "investment_per_acre": 10000,
            "attention_level": "Low",
            "risk_factor": "Low",
            "water_requirement": "Low",
            "season": "Kharif",
            "suitable_for_organic": True,
            "temperature_range": (25, 35),
            "rainfall_range": (30, 60),
            "weather_sensitivity": "Low",
            "market_volatility": "Low",
            "profit_margin": "Medium"
        },
        {
            "name": "Grapes",
            "soil_types": ["Sandy Loam", "Loamy", "Clay Loam"],
            "ph_range": (6.5, 7.5),
            "duration_months": 12,
            "investment_per_acre": 100000,
            "attention_level": "Very High",
            "risk_factor": "High",
            "water_requirement": "High",
            "season": "Rabi",
            "suitable_for_organic": True,
            "temperature_range": (15, 35),
            "rainfall_range": (40, 90),
            "weather_sensitivity": "Very High",
            "market_volatility": "High",
            "profit_margin": "Very High"
        },
        {
            "name": "Cucumber",
            "soil_types": ["Sandy Loam", "Loamy", "Silty Loam"],
            "ph_range": (6.0, 7.0),
            "duration_months": 2,
            "investment_per_acre": 20000,
            "attention_level": "High",
            "risk_factor": "Medium",
            "water_requirement": "High",
            "season": "Summer",
            "suitable_for_organic": True,
            "temperature_range": (20, 30),
            "rainfall_range": (50, 80),
            "weather_sensitivity": "High",
            "market_volatility": "Medium",
            "profit_margin": "Medium"
        },
        {
            "name": "Bitter Gourd",
            "soil_types": ["Sandy Loam", "Loamy", "Silty Loam"],
            "ph_range": (6.0, 7.0),
            "duration_months": 3,
            "investment_per_acre": 18000,
            "attention_level": "Medium",
            "risk_factor": "Low",
            "water_requirement": "Moderate",
            "season": "Zaid",
            "suitable_for_organic": True,
            "temperature_range": (25, 35),
            "rainfall_range": (60, 100),
            "weather_sensitivity": "Medium",
            "market_volatility": "Low",
            "profit_margin": "High"
        },
        {
            "name": "Pumpkin",
            "soil_types": ["Sandy Loam", "Loamy", "Silty Loam"],
            "ph_range": (6.0, 7.5),
            "duration_months": 3,
            "investment_per_acre": 15000,
            "attention_level": "Low",
            "risk_factor": "Low",
            "water_requirement": "Moderate",
            "season": "Kharif",
            "suitable_for_organic": True,
            "temperature_range": (20, 30),
            "rainfall_range": (50, 100),
            "weather_sensitivity": "Low",
            "market_volatility": "Low",
            "profit_margin": "Medium"
        },
        {
            "name": "Bottle Gourd",
            "soil_types": ["Sandy Loam", "Loamy", "Silty Loam"],
            "ph_range": (6.0, 7.5),
            "duration_months": 3,
            "investment_per_acre": 15000,
            "attention_level": "Low",
            "risk_factor": "Low",
            "water_requirement": "Moderate",
            "season": "Zaid",
            "suitable_for_organic": True,
            "temperature_range": (20, 35),
            "rainfall_range": (60, 100),
            "weather_sensitivity": "Low",
            "market_volatility": "Low",
            "profit_margin": "Medium"
        },
        {
            "name": "Cauliflower",
            "soil_types": ["Sandy Loam", "Loamy", "Clay Loam"],
            "ph_range": (6.0, 7.0),
            "duration_months": 3,
            "investment_per_acre": 25000,
            "attention_level": "High",
            "risk_factor": "Medium",
            "water_requirement": "High",
            "season": "Winter",
            "suitable_for_organic": True,
            "temperature_range": (15, 25),
            "rainfall_range": (60, 100),
            "weather_sensitivity": "High",
            "market_volatility": "Medium",
            "profit_margin": "Medium"
        },
        {
            "name": "Lady Finger",
            "soil_types": ["Sandy Loam", "Loamy", "Clay Loam"],
            "ph_range": (6.0, 6.8),
            "duration_months": 3,
            "investment_per_acre": 15000,
            "attention_level": "Medium",
            "risk_factor": "Low",
            "water_requirement": "Moderate",
            "season": "Summer",
            "suitable_for_organic": True,
            "temperature_range": (25, 35),
            "rainfall_range": (50, 100),
            "weather_sensitivity": "Medium",
            "market_volatility": "Low",
            "profit_margin": "High"
        }
    ]
    
    # Parse soil properties
    soil_type = str(soil_results.get("soil_type", "")).lower()
    soil_texture = str(soil_results.get("soil_texture", "")).lower()
    soil_properties = soil_results.get("properties", {})
    
    # Get pH value
    try:
        ph_str = str(soil_properties.get('ph', '7.0'))
        import re
        ph_match = re.search(r'(\d+\.?\d*)', ph_str)
        ph_value = float(ph_match.group(1)) if ph_match else 7.0
    except (ValueError, AttributeError):
        ph_value = 7.0
    
    budget_amount = farmer_inputs['budget']['amount']
    # Convert budget if per hectare (approx 2.47 acres per hectare)
    if farmer_inputs['budget']['unit'] == t("Per Hectare"):
        budget_amount = budget_amount / 2.47
        
    attention_level = farmer_inputs['attention_level']
    risk_tolerance = farmer_inputs['risk_tolerance']
    labor_availability = farmer_inputs.get('labor_availability', t('Adequate'))
    previous_crop = str(farmer_inputs.get('previous_crop', 'None')).lower()
    irrigation_available = farmer_inputs.get('irrigation_available', t('Limited'))
    
    # Calculate duration in months based on unit
    if farmer_inputs['time_duration']['unit'] == t("Months"):
        time_duration_months = farmer_inputs['time_duration']['value']
    elif farmer_inputs['time_duration']['unit'] == t("Weeks"):
        time_duration_months = farmer_inputs['time_duration']['value'] / 4
    else:  # Seasons
        time_duration_months = farmer_inputs['time_duration']['value'] * 4  # Assuming 4 months per season approx
    
    interested_crops = farmer_inputs.get('interested_crops', [])
    organic_preference = farmer_inputs.get('organic_preference', False)
    
    # Texture affinity matrix (Score out of 15 for texture match)
    texture_affinity = {
        "Wheat": {"loamy": 15, "clay loam": 15, "silty": 14, "clayey": 11, "sandy loam": 11, "sandy": 4},
        "Rice": {"clayey": 15, "clay loam": 15, "silty": 13, "loamy": 10, "sandy loam": 6, "sandy": 2},
        "Corn": {"loamy": 15, "sandy loam": 14, "clay loam": 12, "silty": 11, "clayey": 8, "sandy": 7},
        "Soybean": {"loamy": 15, "clay loam": 15, "clayey": 13, "silty": 13, "sandy loam": 10, "sandy": 5},
        "Cotton": {"clayey": 15, "clay loam": 15, "loamy": 12, "silty": 10, "sandy loam": 8, "sandy": 4},
        "Tomato": {"loamy": 15, "sandy loam": 15, "clay loam": 11, "silty": 11, "sandy": 8, "clayey": 5},
        "Potato": {"sandy loam": 15, "loamy": 14, "silty": 12, "sandy": 10, "clay loam": 8, "clayey": 3},
        "Onion": {"loamy": 15, "sandy loam": 15, "silty": 13, "clay loam": 11, "clayey": 7, "sandy": 7},
        "Cabbage": {"loamy": 15, "sandy loam": 14, "clay loam": 14, "silty": 12, "sandy": 6, "clayey": 7},
        "Watermelon": {"sandy": 15, "sandy loam": 15, "loamy": 12, "silty": 8, "clay loam": 6, "clayey": 3},
        "Pomegranate": {"loamy": 15, "sandy loam": 14, "clay loam": 12, "sandy": 10, "clayey": 7, "silty": 8},
        "Cluster Beans": {"sandy": 15, "sandy loam": 15, "loamy": 13, "clay loam": 8, "silty": 8, "clayey": 5},
        "Grapes": {"sandy loam": 15, "loamy": 15, "clay loam": 12, "silty": 10, "sandy": 8, "clayey": 4},
        "Cucumber": {"sandy loam": 15, "loamy": 15, "silty": 12, "sandy": 10, "clay loam": 8, "clayey": 4},
        "Bitter Gourd": {"sandy loam": 15, "loamy": 15, "silty": 12, "sandy": 10, "clay loam": 9, "clayey": 4},
        "Pumpkin": {"sandy loam": 15, "loamy": 15, "silty": 12, "sandy": 10, "clay loam": 9, "clayey": 4},
        "Bottle Gourd": {"sandy loam": 15, "loamy": 15, "silty": 12, "sandy": 10, "clay loam": 9, "clayey": 4},
        "Cauliflower": {"loamy": 15, "sandy loam": 14, "clay loam": 14, "silty": 12, "sandy": 6, "clayey": 7},
        "Lady Finger": {"sandy loam": 15, "loamy": 15, "clay loam": 12, "silty": 10, "sandy": 9, "clayey": 6}
    }
    
    # Check cache to ensure stability
    current_state_key = str(farmer_inputs) + str(soil_results.get('soil_type', '')) + str(soil_results.get('soil_texture', ''))
    
    crops_to_score = crop_database
    if 'cached_recommendations' in st.session_state and \
       st.session_state.get('recommendation_cache_key') == current_state_key:
       scored_crops = st.session_state.cached_recommendations
       crops_to_score = []
    else:
        # Score each crop
        scored_crops = []
    
    for crop in crops_to_score:
        score = 0
        reasons = []
        warnings = []
        
        # 1. SOIL & TEXTURE FACTORS (30% of total score)
        # Check texture affinity
        crop_tex_map = texture_affinity.get(crop['name'], {})
        base_tex_pts = crop_tex_map.get(soil_texture, 10)
        
        # Check regional soil type match
        has_regional_match = any(s.lower() in soil_type for s in crop['soil_types'])
        
        if has_regional_match and base_tex_pts >= 12:
            soil_type_score = 15
            reasons.append(t(f"✓ Soil type ({soil_type.title()}) and texture ({soil_texture.title()}) are optimal"))
        elif has_regional_match or base_tex_pts >= 12:
            soil_type_score = 12
            reasons.append(t(f"✓ Soil compatibility is high for {soil_texture.title()} / {soil_type.title()}"))
        elif base_tex_pts >= 8:
            soil_type_score = 8
            reasons.append(t(f"✓ Soil texture ({soil_texture.title()}) is moderately suitable"))
        else:
            soil_type_score = 3
            warnings.append(t(f"⚠ Soil texture ({soil_texture.title()}) or type may require conditioning for {crop['name']}"))

        # pH match (10%)
        if crop['ph_range'][0] <= ph_value <= crop['ph_range'][1]:
            ph_score = 10
            reasons.append(t(f"✓ Soil pH ({ph_value:.1f}) is within optimal range ({crop['ph_range'][0]}-{crop['ph_range'][1]})"))
        elif crop['ph_range'][0] - 0.5 <= ph_value <= crop['ph_range'][1] + 0.5:
            ph_score = 6
            reasons.append(t(f"✓ Soil pH ({ph_value:.1f}) is marginally suitable"))
        else:
            ph_score = 2
            warnings.append(t(f"⚠ pH ({ph_value:.1f}) outside ideal band ({crop['ph_range'][0]}-{crop['ph_range'][1]}); soil amendment recommended"))

        # NPK levels (5%)
        npk_score = 0
        for nutrient in ['nitrogen', 'phosphorus', 'potassium']:
            level = str(soil_properties.get(nutrient, 'Medium')).lower()
            if 'high' in level:
                npk_score += 1.7
            elif 'medium' in level:
                npk_score += 1.2
            else:
                npk_score += 0.5
        npk_score = min(5, round(npk_score))
        
        soil_sub_score = min(30, soil_type_score + ph_score + npk_score)

        # 2. WEATHER & CLIMATE FACTORS (25% of total score)
        # Temperature match (10%)
        forecast_months = weather_data.get('forecast_3month', [])
        cycle_temps = [m['avg_temp'] for m in forecast_months[:crop['duration_months']]]
        avg_temp = sum(cycle_temps) / len(cycle_temps) if cycle_temps else weather_data.get('current_temp', 25)
        
        t_min, t_max = crop['temperature_range']
        if t_min <= avg_temp <= t_max:
            temp_score = 10
            reasons.append(t(f"✓ Forecast temperature ({avg_temp:.1f}°C) within ideal growth range ({t_min}-{t_max}°C)"))
        elif abs(avg_temp - t_min) <= 3 or abs(avg_temp - t_max) <= 3:
            temp_score = 7
            reasons.append(t(f"✓ Forecast temperature ({avg_temp:.1f}°C) is tolerable for crop cycle"))
        elif abs(avg_temp - t_min) <= 6 or abs(avg_temp - t_max) <= 6:
            temp_score = 4
            warnings.append(t(f"⚠ Temperature ({avg_temp:.1f}°C) marginally suboptimal for vegetative growth"))
        else:
            temp_score = 1
            warnings.append(t(f"⚠ Temperature forecast ({avg_temp:.1f}°C) outside comfort zone ({t_min}-{t_max}°C)"))

        # Rainfall & Irrigation Synergy (10%)
        total_rain = sum(m['total_rain'] for m in forecast_months[:crop['duration_months']])
        r_min, r_max = crop['rainfall_range']
        drainage_val = str(soil_properties.get('drainage', 'Good')).lower()
        
        if r_min <= total_rain <= r_max:
            if crop.get('water_requirement') == 'High' and any(term in str(irrigation_available).lower() for term in ['rainfed', 'none']):
                rain_score = 5
                warnings.append(t(f"⚠ Rainfed risk: High water requirement crop ({total_rain:.0f}mm rain) lacks irrigation backup"))
            else:
                rain_score = 10
                reasons.append(t(f"✓ Forecast rainfall ({total_rain:.0f}mm) matches crop moisture demand ({r_min}-{r_max}mm)"))
        elif total_rain < r_min:
            # Deficit: Check irrigation compensation
            if any(term in str(irrigation_available).lower() for term in ['good', 'excellent']):
                rain_score = 9
                reasons.append(t(f"✓ Lower rainfall ({total_rain:.0f}mm) effectively compensated by {irrigation_available.lower()} irrigation"))
            elif 'limited' in str(irrigation_available).lower():
                rain_score = 4
                warnings.append(t(f"⚠ Rainfall deficit ({total_rain:.0f}mm vs need {r_min}mm); limited irrigation may restrict yield"))
            else:  # Rainfed only
                rain_score = 1
                warnings.append(t(f"⚠ High drought risk: rainfed conditions with low forecast rainfall ({total_rain:.0f}mm vs need {r_min}mm)"))
        else:  # Excess rainfall
            if any(d in drainage_val for d in ['good', 'excessive']):
                rain_score = 7
                reasons.append(t(f"✓ Higher rainfall ({total_rain:.0f}mm) manageable due to good soil drainage"))
            else:
                rain_score = 2
                warnings.append(t(f"⚠ Heavy rainfall ({total_rain:.0f}mm) carries waterlogging risk in slow-draining soil"))

        # Extreme Weather Resilience (5%)
        extreme_events = weather_data.get('extreme_events', [])
        if extreme_events:
            if crop.get('weather_sensitivity') == 'Low':
                extreme_score = 5
                reasons.append(t(f"✓ High climate resilience against active weather alerts ({', '.join(extreme_events)})"))
            elif crop.get('weather_sensitivity') == 'Medium':
                extreme_score = 3
                warnings.append(t(f"⚠ Moderate sensitivity to weather alerts ({', '.join(extreme_events)})"))
            else:
                extreme_score = 1
                warnings.append(t(f"⚠ High sensitivity to active weather alerts ({', '.join(extreme_events)})"))
        else:
            extreme_score = 5
            reasons.append(t("✓ Stable weather forecast without extreme risk alerts"))

        weather_sub_score = min(25, temp_score + rain_score + extreme_score)

        # 3. CROP ROTATION & AGRONOMIC SYNERGY (10% of total score)
        legume_terms = ['soybean', 'pulse', 'gram', 'bean', 'groundnut', 'peas', 'cluster beans']
        cereal_terms = ['wheat', 'rice', 'corn', 'cotton', 'sugarcane']
        solanaceae_terms = ['tomato', 'potato', 'brinjal', 'eggplant', 'chilli']
        
        crop_name_lower = crop['name'].lower()
        
        if any(leg in previous_crop for leg in legume_terms) and not any(leg in crop_name_lower for leg in legume_terms):
            rot_score = 10
            reasons.append(t("✓ Synergistic rotation: benefits from nitrogen fixed by previous legume crop"))
        elif any(cer in previous_crop for cer in cereal_terms) and any(leg in crop_name_lower for leg in legume_terms):
            rot_score = 10
            reasons.append(t("✓ Restorative rotation: replenishes soil nitrogen after heavy-feeding cereal"))
        elif any(sol in previous_crop for sol in solanaceae_terms) and any(sol in crop_name_lower for sol in solanaceae_terms):
            rot_score = 2
            warnings.append(t("⚠ Pest & disease carryover risk: consecutive Solanaceous crop cultivation"))
        elif previous_crop in [t("None"), "none", "unknown", ""]:
            rot_score = 7
        else:
            rot_score = 8
            reasons.append(t(f"✓ Good rotation compatibility following {previous_crop.title()}"))
            
        rotation_sub_score = min(10, rot_score)

        # 4. MARKET & ECONOMIC FACTORS (20% of total score)
        # Budget match (7%)
        if budget_amount >= crop['investment_per_acre']:
            budget_score = 7
            reasons.append(t("✓ Cultivation cost fits comfortably within budget"))
        elif budget_amount >= crop['investment_per_acre'] * 0.75:
            budget_score = 4
            reasons.append(t("✓ Budget is slightly tight but manageable"))
        else:
            budget_score = 1
            warnings.append(t(f"⚠ Estimated investment (₹{crop['investment_per_acre']}/acre) exceeds your allocated budget"))

        # Price prediction lookup
        price_pred = get_price_prediction(crop['name'], market_data, weather_data)
        trend_score = 0
        demand_score = 0
        roi_score = 0
        
        if price_pred:
            # Trend (4%)
            if price_pred['trend'] == "Increasing":
                trend_score = 4
                reasons.append(t("✓ Favorable upward market price trend"))
            elif price_pred['trend'] == "Stable":
                trend_score = 2
                reasons.append(t("✓ Stable market pricing"))
            
            # Demand (4%)
            if price_pred['demand'] == "High":
                demand_score = 4
                reasons.append(t("✓ High wholesale market demand"))
            elif price_pred['demand'] == "Medium":
                demand_score = 2
                reasons.append(t("✓ Steady market demand"))
            
            # ROI (5%)
            if price_pred['roi_potential'] > 15:
                roi_score = 5
                reasons.append(t(f"✓ Excellent ROI outlook ({price_pred['roi_potential']}%)"))
            elif price_pred['roi_potential'] > 5:
                roi_score = 3
                reasons.append(t(f"✓ Moderate ROI outlook ({price_pred['roi_potential']}%)"))
            else:
                roi_score = 1
        else:
            trend_score = 2
            demand_score = 2
            roi_score = 2
            
        market_sub_score = min(20, budget_score + trend_score + demand_score + roi_score)

        # 5. FARMER MANAGEMENT & RISK FIT (15% of total score)
        # Duration match (5%)
        if crop['duration_months'] <= time_duration_months:
            duration_score = 5
            reasons.append(t("✓ Crop duration fits within your available timeline"))
        elif crop['duration_months'] <= time_duration_months + 1:
            duration_score = 3
            reasons.append(t("✓ Slightly exceeds duration by ~1 month"))
        else:
            duration_score = 0
            warnings.append(t(f"⚠ Requires {crop['duration_months']} months, exceeding planned time"))

        # Attention level match (5%)
        attention_map = {t("Very Low"): 0.2, t("Low"): 0.4, t("Medium"): 0.6, t("High"): 0.8, t("Very High"): 1.0}
        crop_att_map = {"Very Low": 0.2, "Low": 0.4, "Medium": 0.6, "High": 0.8, "Very High": 1.0}
        user_att = attention_map.get(attention_level, 0.6)
        crop_att = crop_att_map.get(crop.get('attention_level', 'Medium'), 0.6)
        
        att_diff = abs(user_att - crop_att)
        if att_diff <= 0.2:
            attention_score = 5
            reasons.append(t("✓ Labor & attention commitment matches your preference"))
        elif att_diff <= 0.4:
            attention_score = 3
        else:
            attention_score = 1
            warnings.append(t(f"⚠ Crop requires {crop.get('attention_level')} management intensity"))

        # Risk tolerance match (5%)
        risk_map = {t("Very Low"): 0.2, t("Low"): 0.4, t("Medium"): 0.6, t("High"): 0.8, t("Very High"): 1.0}
        crop_risk_map = {"Very Low": 0.2, "Low": 0.4, "Medium": 0.6, "High": 0.8, "Very High": 1.0}
        user_risk = risk_map.get(risk_tolerance, 0.6)
        crop_risk = crop_risk_map.get(crop.get('risk_factor', 'Medium'), 0.6)
        
        if crop_risk <= user_risk + 0.2:
            risk_score = 5
            reasons.append(t("✓ Risk profile aligns with your tolerance"))
        else:
            risk_score = 1
            warnings.append(t("⚠ Higher financial/market risk than preferred"))

        management_sub_score = min(15, duration_score + attention_score + risk_score)

        # Calculate Total Score (Out of 100)
        total_score = soil_sub_score + weather_sub_score + rotation_sub_score + market_sub_score + management_sub_score
        
        # Check if user specifically showed interest in this crop
        is_user_interested = False
        if interested_crops:
            for ic in interested_crops:
                if crop['name'].lower() in str(ic).lower() or str(ic).lower() in crop['name'].lower():
                    is_user_interested = True
                    break
                    
        if is_user_interested:
            # Priority boost for farmer-indicated interest
            total_score = min(100, total_score + 5)
            reasons.insert(0, t("🎯 Matches your indicated crop preference"))

        # Clamp total score between 15% and 99%
        final_score = max(15, min(99, int(round(total_score))))

        # Add to scored list
        scored_crops.append({
            "name": crop['name'],
            "score": final_score,
            "reasons": reasons,
            "warnings": warnings,
            "details": crop,
            "price_prediction": price_pred,
            "is_user_interested": is_user_interested,
            "sub_scores": {
                "soil": int((soil_sub_score / 30.0) * 100),
                "weather": int((weather_sub_score / 25.0) * 100),
                "market": int((market_sub_score / 20.0) * 100),
                "rotation": int((rotation_sub_score / 10.0) * 100),
                "management": int((management_sub_score / 15.0) * 100)
            }
        })
    
    # Sort by score descending (with user-interested crops having slight tiebreaker advantage)
    scored_crops.sort(key=lambda x: (x.get('is_user_interested', False), x['score']), reverse=True)
    
    # Cache the results
    st.session_state.cached_recommendations = scored_crops
    st.session_state.recommendation_cache_key = current_state_key
    
    # Display top recommendations
    if scored_crops:
        for i, crop in enumerate(scored_crops[:5]):  # Show top 5
            with st.container():
                # Create a card-like appearance
                st.markdown(f"""
                <div style='background-color: {'#f0fff0' if i==0 else '#ffffff'}; 
                            padding: 20px; 
                            border-radius: 10px; 
                            border: 2px solid {'#4CAF50' if i==0 else '#e0e0e0'};
                            margin-bottom: 15px;'>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 4])
                
                with col1:
                    # Clean rank indicator
                    if i == 0:
                        st.markdown(f"<div style='background-color: #2E7D32; color: white; padding: 8px 4px; border-radius: 6px; text-align: center; font-weight: bold; font-size: 14px;'>#1 Pick</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='background-color: #f0f2f6; color: #424242; padding: 8px 4px; border-radius: 6px; text-align: center; font-weight: bold; font-size: 14px;'>#{i+1}</div>", unsafe_allow_html=True)
                
                with col2:
                    # Title and optional user interest tag
                    title_cols = st.columns([3, 1])
                    with title_cols[0]:
                        st.markdown(f"### {crop['name']}")
                    with title_cols[1]:
                        if crop.get('is_user_interested'):
                            st.markdown(f"<span style='background-color: #E8F5E9; color: #2E7D32; padding: 3px 8px; border-radius: 4px; font-weight: 600; font-size: 12px; border: 1px solid #C8E6C9;'>{t('Your Preference')}</span>", unsafe_allow_html=True)
                    
                    # Match score with clean badge and sub-score metrics
                    score_color = "#2E7D32" if crop['score'] >= 75 else "#F57C00" if crop['score'] >= 50 else "#D32F2F"
                    subs = crop.get('sub_scores', {})
                    st.markdown(f"""
                    <div style='display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 12px;'>
                        <div style='background-color: {score_color}; padding: 5px 10px; border-radius: 4px; color: white; font-weight: 600; font-size: 13px;'>
                            {t('Match Score')}: {crop['score']}%
                        </div>
                        <span style='background-color: #f5f5f5; color: #555; padding: 3px 8px; border-radius: 4px; font-size: 12px;'>{t('Soil')}: {subs.get('soil', 85)}%</span>
                        <span style='background-color: #f5f5f5; color: #555; padding: 3px 8px; border-radius: 4px; font-size: 12px;'>{t('Weather')}: {subs.get('weather', 85)}%</span>
                        <span style='background-color: #f5f5f5; color: #555; padding: 3px 8px; border-radius: 4px; font-size: 12px;'>{t('Market')}: {subs.get('market', 80)}%</span>
                        <span style='background-color: #f5f5f5; color: #555; padding: 3px 8px; border-radius: 4px; font-size: 12px;'>{t('Rotation')}: {subs.get('rotation', 80)}%</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create columns for crop details
                    det_col1, det_col2, det_col3, det_col4 = st.columns(4)
                    
                    with det_col1:
                        st.markdown(f"**{t('Duration')}**  \n{crop['details']['duration_months']} {t('months')}")
                    
                    with det_col2:
                        st.markdown(f"**{t('Investment')}**  \n₹{crop['details']['investment_per_acre']}/acre")
                    
                    with det_col3:
                        st.markdown(f"**{t('Risk')}**  \n{t(crop['details']['risk_factor'])}")
                    
                    with det_col4:
                        st.markdown(f"**{t('Water Need')}**  \n{t(crop['details']['water_requirement'])}")
                    
                    # Price prediction if available
                    if crop['price_prediction']:
                        pred = crop['price_prediction']
                        st.markdown(f"""
                        <div style='background-color: #F1F8E9; border-left: 3px solid #689F38; padding: 8px 12px; border-radius: 4px; margin: 8px 0; font-size: 13px;'>
                            <strong>{t('Price Outlook')}:</strong> ₹{pred['current_price']} → ₹{pred['predicted_price']} 
                            ({'+' if pred['roi_potential'] > 0 else ''}{pred['roi_potential']}%) 
                            | {t('Confidence')}: {pred['confidence']*100:.0f}%
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Reasons
                    if crop['reasons']:
                        st.markdown(f"**{t('Key Advantages')}:**")
                        for reason in crop['reasons'][:3]:  # Show top 3 reasons
                            st.markdown(f"- {reason}")
                    
                    # Warnings
                    if crop['warnings']:
                        st.markdown(f"**{t('Considerations')}:**")
                        for warning in crop['warnings'][:2]:  # Show top 2 warnings
                            st.markdown(f"- {warning}")
                    
                    # Quick action buttons
                    st.markdown("---")

                    # Key for visibility state
                    details_key = f"show_details_{crop['name']}_{i}"
                    profit_key = f"show_profit_{crop['name']}_{i}"

                    start_col1, start_col2 = st.columns(2)
                    
                    with start_col1:
                        # Toggle button for details
                        if st.button(t("Detailed Analysis"), key=f"btn_details_{crop['name']}_{i}", use_container_width=True):
                            st.session_state[details_key] = not st.session_state.get(details_key, False)
                            # Close profit if opening details
                            if st.session_state[details_key]:
                                st.session_state[profit_key] = False

                    with start_col2:
                        # Toggle button for profit
                        if st.button(t("Profit Calculator"), key=f"btn_profit_{crop['name']}_{i}", use_container_width=True):
                            st.session_state[profit_key] = not st.session_state.get(profit_key, False)
                            # Close details if opening profit
                            if st.session_state[profit_key]:
                                st.session_state[details_key] = False
                            
                    if st.session_state.get(details_key, False):
                        show_crop_details(crop, weather_data, market_data)
                        
                    if st.session_state.get(profit_key, False):
                        show_profit_calculator(crop, farmer_inputs, key_suffix=f"{crop['name']}_{i}")


                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info(t("No crops match your criteria. Try adjusting your preferences."))
        
    return scored_crops, weather_data, market_data


def show_crop_details(crop, weather_data, market_data):
    """Show detailed analysis for a specific crop"""
    with st.expander(f"{t('Detailed Analysis for')} {crop['name']}", expanded=True):
        st.markdown(f"### {t('Crop Requirements')}")
        
        # Use simple markdown columns to avoid nesting depth error
        st.markdown(f"""
        | {t('Property')} | {t('Value')} |
        |---|---|
        | **{t('Soil Type')}** | {', '.join([t(s) for s in crop['details']['soil_types']])} |
        | **{t('pH Range')}** | {crop['details']['ph_range'][0]} - {crop['details']['ph_range'][1]} |
        | **{t('Temperature Range')}** | {crop['details']['temperature_range'][0]}°C - {crop['details']['temperature_range'][1]}°C |
        | **{t('Rainfall Range')}** | {crop['details']['rainfall_range'][0]}mm - {crop['details']['rainfall_range'][1]}mm |
        | **{t('Season')}** | {t(crop['details']['season'])} |
        """)
        
        st.markdown(f"### {t('Market Analysis')}")
        if crop['price_prediction']:
            pred = crop['price_prediction']
            st.info(f"{t('Current Price')}: ₹{pred['current_price']} ({pred['roi_potential']}% forecast)")
            st.markdown(f"**{t('Demand')}:** {pred['demand']} | **{t('Confidence')}:** {pred['confidence']*100:.0f}%")
        
        st.markdown(f"### {t('Weather Forecast for Growing Period')}")
        months_needed = crop['details']['duration_months']
        forecast_df = pd.DataFrame(weather_data['forecast_3month'][:months_needed])
        st.dataframe(forecast_df, use_container_width=True)
        
        # Weather disadvantages/discrepancies
        disadvantages = []
        forecast_temps = [m['avg_temp'] for m in weather_data['forecast_3month'][:months_needed]]
        forecast_rain = sum(m['total_rain'] for m in weather_data['forecast_3month'][:months_needed])
        
        # Check temperature
        min_temp, max_temp = crop['details']['temperature_range']
        if forecast_temps:
            avg_forecast = sum(forecast_temps) / len(forecast_temps)
            if avg_forecast < min_temp - 2:
                disadvantages.append(f"{t('Temperature too low')} (Avg: {avg_forecast:.1f}°C vs Min: {min_temp}°C)")
            elif avg_forecast > max_temp + 2:
                disadvantages.append(f"{t('Temperature too high')} (Avg: {avg_forecast:.1f}°C vs Max: {max_temp}°C)")
                
        # Check rainfall
        min_rain, max_rain = crop['details']['rainfall_range']
        if forecast_rain < min_rain * 0.8:
            disadvantages.append(f"{t('Potential water shortage')} ({forecast_rain:.0f}mm vs Min: {min_rain}mm)")
        elif forecast_rain > max_rain * 1.2:
            disadvantages.append(f"{t('Risk of excess rainfall')} ({forecast_rain:.0f}mm vs Max: {max_rain}mm)")
            
        # Extreme weather
        if weather_data.get('extreme_events'):
             disadvantages.append(f"{t('Extreme weather risks')}: {', '.join(weather_data['extreme_events'])}")

        if disadvantages:
             st.markdown(f"### {t('Weather Risks')}")
             for risk in disadvantages:
                 st.markdown(f"- {risk}")


def show_profit_calculator(crop, farmer_inputs, key_suffix=""):
    """Show profit calculation tool"""
    with st.expander(f"{t('Profit Calculator for')} {crop['name']}", expanded=True):
        st.markdown(f"### {t('Input Costs')}")
        
        # Use unique keys for inputs
        land_area = st.number_input(t("Land Area (acres)"), min_value=0.1, value=1.0, step=0.1, key=f"land_{key_suffix}")
        
        # Base investment
        base_investment = crop['details']['investment_per_acre'] * land_area
        st.info(f"{t('Base Crop Investment')}: ₹{base_investment:,.2f}")
        
        # Additional costs
        st.markdown(f"**{t('Optional Expenses')}**")
        
        # Use columns for compact layout, but ensure no nesting issues (Level 2 is max allowed inside card)
        # Since we are inside a card (Level 1), we can use columns (Level 2)
        pc1, pc2 = st.columns(2)
        with pc1:
            fertilizer_cost = st.number_input(t("Fertilizer Cost"), value=0.0, key=f"fert_{key_suffix}")
            labor_cost = st.number_input(t("Labor Cost"), value=0.0, key=f"lab_{key_suffix}")
        with pc2:
            irrigation_cost = st.number_input(t("Irrigation Cost"), value=0.0, key=f"irr_{key_suffix}")
            miscellaneous = st.number_input(t("Miscellaneous"), value=0.0, key=f"misc_{key_suffix}")
        
        # Correct Total Cost = Base + Optional
        total_cost = base_investment + fertilizer_cost + labor_cost + irrigation_cost + miscellaneous
        
        st.markdown("---")
        st.markdown(f"### {t('Expected Returns')}")
            
        if crop['price_prediction']:
            expected_price = crop['price_prediction']['predicted_price']
            
            # Average yield per acre (simplified)
            yields = {
                "Wheat": 20, "Rice": 25, "Corn": 30, "Soybean": 15,
                "Cotton": 10, "Tomato": 200, "Potato": 150, "Onion": 120
            }
            expected_yield = yields.get(crop['name'], 50) * land_area
            
            gross_return = expected_yield * expected_price
            net_profit = gross_return - total_cost
            roi = (net_profit / total_cost) * 100 if total_cost > 0 else 0
            
            st.metric(t("Expected Yield"), f"{expected_yield:.0f} quintals")
            st.metric(t("Gross Return"), f"₹{gross_return:,.0f}")
            st.metric(t("Net Profit"), f"₹{net_profit:,.0f}", delta=f"{roi:.1f}% ROI")
            
            # Break-even analysis
            break_even_price = total_cost / expected_yield if expected_yield > 0 else 0
            st.markdown(f"**{t('Break-even Price')}:** ₹{break_even_price:.0f}/quintal")
            st.markdown(f"**{t('Current Market Price')}:** ₹{crop['price_prediction']['current_price']}/quintal")
            
            # Risk assessment
            if roi > 50:
                st.success(t("High profit potential"))
            elif roi > 20:
                st.info(t("Moderate profit potential"))
            else:
                st.warning(t("Low profit margin"))




        