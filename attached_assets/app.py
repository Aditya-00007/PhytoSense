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

from image_processing import preprocess_image, extract_features
from model_handler import identify_plant, detect_water_content, detect_diseases, detect_pests
from recommendations import get_preventive_measures, get_fertilizer_recommendations
from utils import load_svg, get_example_images, generate_report_markdown, format_probability, save_uploaded_image
from db_adapter import create_user, verify_user, update_user_profile, save_analysis, get_user_analyses, get_user_by_id, get_user_profile
from maharashtra import get_local_recommendations
from resources import show_resources_page
from language_support import initialize_language, show_language_selector, t
from weather_service import display_weather_widget, show_weather_page

# Add these helper functions near the top of the file (around line 50)
def get_profile_field(profile_data, field_name, default=""):
    """Safely get a field from profile data, handling missing keys."""
    if not profile_data:
        return default
    return profile_data.get(field_name, default)

def get_select_index(current_value, options):
    """Get the index of the current value in the options list."""
    try:
        return options.index(current_value) if current_value in options else 0
    except ValueError:
        return 0
    
# Page configuration
st.set_page_config(
    page_title="PhytoSense - AI Plant Health Monitoring",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# Apply custom CSS
with open(".streamlit/custom.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add some interactivity with CSS animations
st.markdown("""
<style>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideInFromLeft {
  from { transform: translateX(-50px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.fadeIn {
  animation: fadeIn 1.5s ease-in-out;
}

.slideIn {
  animation: slideInFromLeft 0.8s ease-out;
}

.stAlert {
  animation: fadeIn 1s ease-in;
}

/* Add a cool gradient button */
.gradient-button {
  background-image: linear-gradient(to right, #6EDB3E, #4CAF50);
  color: white;
  padding: 10px 20px;
  border-radius: 25px;
  font-weight: bold;
  text-align: center;
  cursor: pointer;
  display: inline-block;
  transition: all 0.3s ease;
  margin: 10px 0px;
  box-shadow: 0 4px 15px rgba(110, 219, 62, 0.3);
}

.gradient-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 7px 20px rgba(110, 219, 62, 0.5);
}
</style>
""", unsafe_allow_html=True)

# Create data directories if they don't exist
if not os.path.exists("data"):
    os.makedirs("data")
if not os.path.exists("uploads"):
    os.makedirs("uploads")
if not os.path.exists("assets"):
    os.makedirs("assets")
if not os.path.exists("assets/examples"):
    os.makedirs("assets/examples")
if not os.path.exists("weather_data"):
    os.makedirs("weather_data")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "soil_results" not in st.session_state:
    st.session_state.soil_results = None
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
if "soil_analysis_complete" not in st.session_state:
    st.session_state.soil_analysis_complete = False
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []
if "uploaded_soil_image" not in st.session_state:
    st.session_state.uploaded_soil_image = None
if "processed_image" not in st.session_state:
    st.session_state.processed_image = None
if "processed_images" not in st.session_state:
    st.session_state.processed_images = []
if "plant_info" not in st.session_state:
    st.session_state.plant_info = None
if "water_content" not in st.session_state:
    st.session_state.water_content = None
if "diseases" not in st.session_state:
    st.session_state.diseases = None
if "pests" not in st.session_state:
    st.session_state.pests = None
if "preventive_measures" not in st.session_state:
    st.session_state.preventive_measures = []
if "fertilizer_recommendations" not in st.session_state:
    st.session_state.fertilizer_recommendations = []
if "soil_fertility" not in st.session_state:
    st.session_state.soil_fertility = None
if "crop_suggestions" not in st.session_state:
    st.session_state.crop_suggestions = []
if "history" not in st.session_state:
    st.session_state.history = []
if "show_account_created" not in st.session_state:
    st.session_state.show_account_created = False
if "current_tab" not in st.session_state:
    st.session_state.current_tab = "dashboard"
if "plant_details" not in st.session_state:
    st.session_state.plant_details = {
        "crop_type": None,
        "plant_age": None,
        "symptoms": None,
        "planting_date": None,
        "irrigation_method": None,
        "previous_treatments": None
    }

# Weather-related session state variables
if "weather_location" not in st.session_state:
    st.session_state.weather_location = None
if "weather_data" not in st.session_state:
    st.session_state.weather_data = None
if "forecast_data" not in st.session_state:
    st.session_state.forecast_data = None
if "weather_alerts" not in st.session_state:
    st.session_state.weather_alerts = []

# Navigation functions
def go_to_login():
    st.session_state.page = "login"
    st.session_state.show_account_created = False

def go_to_signup():
    st.session_state.page = "signup"

def go_to_profile_setup():
    st.session_state.page = "profile_setup"

def go_to_dashboard():
    st.session_state.page = "dashboard"

def go_to_crop_test():
    st.session_state.page = "crop_test"
    st.session_state.analysis_complete = False
    st.session_state.uploaded_image = None
    st.session_state.processed_image = None

def go_to_soil_analysis():
    st.session_state.page = "soil_analysis"
    st.session_state.soil_analysis_complete = False
    st.session_state.uploaded_soil_image = None

def go_to_history():
    st.session_state.page = "history"

def go_to_resources():
    st.session_state.page = "resources"

def go_to_weather():
    st.session_state.page = "weather"

def logout():
    st.session_state.current_user = None
    st.session_state.user_profile = {}
    st.session_state.page = "login"
    st.session_state.analysis_complete = False
    st.session_state.soil_analysis_complete = False
    st.session_state.uploaded_image = None
    st.session_state.uploaded_soil_image = None
    st.session_state.processed_image = None
    st.session_state.plant_info = None
    st.session_state.water_content = None
    st.session_state.diseases = None
    st.session_state.pests = None
    st.session_state.preventive_measures = []
    st.session_state.fertilizer_recommendations = []
    st.session_state.soil_fertility = None
    st.session_state.crop_suggestions = []
    st.session_state.history = []
    # Clear weather-related state
    st.session_state.weather_location = None
    st.session_state.weather_data = None
    st.session_state.forecast_data = None
    st.session_state.weather_alerts = []

# Soil analysis function
def analyze_soil(image):
    # In a real app, this would use computer vision to analyze soil properties
    # For demo purposes, we'll generate simulated soil analysis results
    
    soil_types = ["Sandy", "Clay", "Loamy", "Silty", "Peaty", "Chalky"]
    soil_fertility = {
        "type": random.choice(soil_types),
        "pH": round(random.uniform(5.5, 8.0), 1),
        "organic_matter": f"{random.randint(1, 8)}%",
        "nitrogen": f"{random.randint(10, 80)} ppm",
        "phosphorus": f"{random.randint(5, 100)} ppm",
        "potassium": f"{random.randint(50, 300)} ppm",
        "moisture": f"{random.randint(5, 25)}%"
    }
    
    # Suggest crops based on soil type
    crop_suggestions = {
        "Sandy": ["Carrots", "Potatoes", "Radishes", "Corn", "Lettuce"],
        "Clay": ["Cabbage", "Broccoli", "Brussels Sprouts", "Beans", "Peas"],
        "Loamy": ["Wheat", "Rice", "Tomatoes", "Eggplant", "Zucchini", "Peppers"],
        "Silty": ["Roses", "Tomatoes", "Lettuce", "Cabbage", "Strawberries"],
        "Peaty": ["Blueberries", "Potatoes", "Carrots", "Lettuce", "Onions"],
        "Chalky": ["Spinach", "Beets", "Sweet Corn", "Cabbage", "Lavender"]
    }
    
    # Consider weather and water availability (in real app, these would be actual parameters)
    rainfall = random.choice(["Low", "Moderate", "High"])
    season = random.choice(["Spring", "Summer", "Fall", "Winter"])
    
    # Adjust recommendations based on rainfall and season
    recommendations = crop_suggestions[soil_fertility["type"]][:3]  # Select base crops
    
    # Add seasonal recommendations
    seasonal_crops = {
        "Spring": ["Lettuce", "Peas", "Spinach", "Radishes"],
        "Summer": ["Tomatoes", "Corn", "Cucumber", "Peppers"],
        "Fall": ["Kale", "Carrots", "Broccoli", "Cabbage"],
        "Winter": ["Garlic", "Onions", "Winter Squash"]
    }
    
    # Add 1-2 seasonal recommendations if not already included
    for crop in seasonal_crops[season]:
        if crop not in recommendations and len(recommendations) < 5:
            recommendations.append(crop)
    
    return soil_fertility, recommendations, rainfall, season

# Save analysis to history
def save_to_history(analysis_type, data):
    # Save to database if user is authenticated
    if st.session_state.current_user:
        # Convert PIL image to path for storage
        image_path = None
        if analysis_type == "plant" and st.session_state.uploaded_image:
            image_path = save_uploaded_image(st.session_state.uploaded_image)
        elif analysis_type == "soil" and st.session_state.uploaded_soil_image:
            image_path = save_uploaded_image(st.session_state.uploaded_soil_image)
        
        # Get user_id safely, supporting both object and dict access
        user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
        
        # Save analysis to database
        success, analysis_id = save_analysis(
            user_id=user_id,
            analysis_type=analysis_type,
            image_path=image_path,
            results=data
        )
        
        if success:
            # Update the session state history
            user_analyses = get_user_analyses(user_id)
            st.session_state.history = user_analyses

# Header with navigation
def show_header():
    # Logo and title
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        # Placeholder logo (in a real app, we'd use a proper logo file)
        svg_content = load_svg("assets/logo.svg")
        st.image(svg_content, width=80)
    
    with col2:
        st.title("PhytoSense")
        st.subheader("AI-Powered Plant Health Monitoring System")
    
    # Navigation menu for logged-in users
    if st.session_state.current_user:
        with col3:
            username = st.session_state.current_user['username'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.username
            st.write(f"Welcome, {username}")
            if st.button("Logout"):
                logout()
        
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Dashboard", "Test Your Crop", "Soil Analysis", "History", "Resources", "Weather"])
        
        with tab1:
            if st.button("Go to Dashboard", key="nav_dashboard"):
                go_to_dashboard()
        
        with tab2:
            if st.button("Analyze Plant Health", key="nav_crop_test"):
                go_to_crop_test()
        
        with tab3:
            if st.button("Analyze Soil", key="nav_soil_analysis"):
                go_to_soil_analysis()
        
        with tab4:
            if st.button("View History", key="nav_history"):
                go_to_history()
                
        with tab5:
            if st.button("Farming Resources", key="nav_resources"):
                go_to_resources()
                
        with tab6:
            if st.button("Weather Alerts", key="nav_weather"):
                go_to_weather()
    
    st.markdown("---")

# Login page
def show_login_page():
    st.header("Login")
    
    if st.session_state.show_account_created:
        st.success("Account created successfully! Please login.")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Login"):
            if not username or not password:
                st.error("Please enter both username and password.")
            else:
                user = verify_user(username, password)
                if user:
                    st.session_state.current_user = user
                    user_profile = get_user_profile(user['id'])
                    if user_profile:
                        st.session_state.user_profile = user_profile
                        go_to_dashboard()
                    else:
                        go_to_profile_setup()
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    
    with col2:
        if st.button("Sign Up"):
            go_to_signup()
            st.rerun()

# Sign up page
def show_signup_page():
    st.header("Create a New Account")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    email = st.text_input("Email (Optional)")
    farm_location = st.text_input("Farm Location (Format: 'City,CountryCode', e.g., 'Nashik,IN') *")
    
    if st.button("Create Account"):
        if not username or not password or not confirm_password:
            st.error("Please fill in all required fields.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            success, message = create_user(username, password, email)
            if success:
                st.session_state.show_account_created = True
                go_to_login()
                st.rerun()
            else:
                st.error(message)

# Profile setup page
def show_profile_setup_page():
    # Check if we're updating an existing profile
    is_update = "user_profile" in st.session_state and st.session_state.user_profile
    
    st.header("Update Your Profile" if is_update else "Complete Your Profile")
    
    # Pre-fill form with existing data if updating
    profile_data = st.session_state.user_profile if is_update else {}
    
    with st.form("profile_form"):
        st.subheader("Personal Information")
        full_name = st.text_input(
            "Full Name *", 
            value=profile_data.get('full_name', '')
        )
        
        st.subheader("Farm Information")
        farm_name = st.text_input(
            "Farm Name",
            value=profile_data.get('farm_name', '')
        )
        location = st.text_input(
            "Farm Location (Format: 'City,CountryCode', e.g., 'Nashik,IN') *",
            value=profile_data.get('location', '')
        )
        farm_size = st.text_input(
            "Farm Size (e.g., '5 acres')",
            value=profile_data.get('farm_size', '')
        )
        
        st.subheader("Crop Information")
        main_crops = st.text_input(
            "Current Crops (separated by commas)",
            value=profile_data.get('main_crops', '')
        )
        soil_type = st.selectbox(
            "Primary Soil Type", 
            ["Select Soil Type", "Sandy", "Clay", "Loamy", "Silty", "Peaty", "Chalky", "Not Sure"],
            index=0 if not profile_data.get('soil_type') else 
                 ["Sandy", "Clay", "Loamy", "Silty", "Peaty", "Chalky", "Not Sure"].index(profile_data['soil_type']) + 1
        )
        irrigation_method = st.selectbox(
            "Primary Irrigation Method", 
            ["Select Method", "Drip Irrigation", "Sprinkler", "Flood Irrigation", 
             "Furrow Irrigation", "Rainfed", "Other"],
            index=0 if not profile_data.get('irrigation_method') else 
                 ["Drip Irrigation", "Sprinkler", "Flood Irrigation", 
                  "Furrow Irrigation", "Rainfed", "Other"].index(profile_data['irrigation_method']) + 1
        )
        
        st.subheader("Current Status")
        crop_status = st.text_area(
            "Current Crop Health Status (Any issues you're facing?)",
            value=profile_data.get('crop_status', '')
        )
        
        st.markdown("**Required fields*")
        submit_button = st.form_submit_button("Update Profile" if is_update else "Save Profile")
        
        if submit_button:
            if not full_name or not location:
                st.error("Please fill in all required fields (Full Name and Location).")
            else:
                # Clean up the selections
                selected_soil = soil_type if soil_type != "Select Soil Type" else ""
                selected_irrigation = irrigation_method if irrigation_method != "Select Method" else ""
                
                new_profile_data = {
                    "full_name": full_name,
                    "farm_name": farm_name,
                    "location": location,
                    "farm_size": farm_size,
                    "main_crops": main_crops,
                    "soil_type": selected_soil,
                    "irrigation_method": selected_irrigation,
                    "crop_status": crop_status
                }
                
                # Get user_id safely, supporting both object and dict access
                user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
                
                success, message = update_user_profile(user_id, new_profile_data)
                
                if success:
                    st.session_state.user_profile = get_user_profile(user_id)
                    st.success("Profile updated successfully!")
                    time.sleep(1)
                    go_to_dashboard()
                    st.rerun()
                else:
                    st.error(f"Error updating profile: {message}")

# Dashboard page
def show_dashboard_page():
    st.header("Dashboard")
    
    user_profile = st.session_state.user_profile
    
    # User info card
    with st.container():
        st.subheader("Welcome to PhytoSense")
        
        # Create two columns for user profile information
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="fadeIn" style="animation-delay: 0.2s;">
                <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin-bottom: 20px; height: 100%;">
                    <h3 style="color: #2E7D32;">Your Profile</h3>
                    <p><strong>Name:</strong> {user_profile.get('full_name', '')}</p>
                    <p><strong>Farm:</strong> {user_profile.get('farm_name', '')}</p>
                    <p><strong>Location:</strong> {user_profile.get('location', '')}</p>
                    <p><strong>District:</strong> {user_profile.get('district', '')}</p>
                    <p><strong>Farm Size:</strong> {user_profile.get('farm_size', '')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="fadeIn" style="animation-delay: 0.4s;">
                <div style="background-color: #E8F5E9; padding: 20px; border-radius: 10px; margin-bottom: 20px; height: 100%;">
                    <h3 style="color: #2E7D32;">Crop Information</h3>
                    <p><strong>Main Crops:</strong> {user_profile.get('main_crops', '')}</p>
                    <p><strong>Soil Type:</strong> {user_profile.get('soil_type', '')}</p>
                    <p><strong>Irrigation Method:</strong> {user_profile.get('irrigation_method', '')}</p>
                    <p><strong>Current Status:</strong> {user_profile.get('crop_status', 'No issues reported')}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        # Add an "Update Profile" button
        with st.container():
            st.markdown("---")
            if st.button("Update Profile", key="update_profile_button"):
                st.session_state.page = "profile_setup"
                st.rerun()
    
    # Quick actions
    with st.container():
        st.subheader("Quick Actions")
        
        row1_col1, row1_col2 = st.columns(2)
        
        with row1_col1:
            st.markdown("""
            <div class="slideIn" style="animation-delay: 0.4s;">
                <div style="background-color: #C8E6C9; padding: 15px; border-radius: 10px; text-align: center; min-height: 180px;">
                    <img src="https://img.icons8.com/color/96/000000/plant-under-sun.png" style="width: 64px; height: 64px;">
                    <h4 style="color: #2E7D32;">Analyze Plant Health</h4>
                    <p style="font-size: 14px;">Upload a photo of your plant to detect diseases</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Analyze Plant", key="dash_analyze_plant"):
                go_to_crop_test()
                st.rerun()
        
        with row1_col2:
            st.markdown("""
            <div class="slideIn" style="animation-delay: 0.6s;">
                <div style="background-color: #C8E6C9; padding: 15px; border-radius: 10px; text-align: center; min-height: 180px;">
                    <img src="https://img.icons8.com/color/96/000000/soil.png" style="width: 64px; height: 64px;">
                    <h4 style="color: #2E7D32;">Analyze Soil</h4>
                    <p style="font-size: 14px;">Upload a photo of your soil to get composition analysis</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Analyze Soil", key="dash_analyze_soil"):
                go_to_soil_analysis()
                st.rerun()
        
        row2_col1, row2_col2, row2_col3 = st.columns(3)
        
        with row2_col1:
            st.markdown("""
            <div class="slideIn" style="animation-delay: 0.8s;">
                <div style="background-color: #C8E6C9; padding: 15px; border-radius: 10px; text-align: center; min-height: 180px;">
                    <img src="https://img.icons8.com/color/96/000000/activity-history.png" style="width: 64px; height: 64px;">
                    <h4 style="color: #2E7D32;">View History</h4>
                    <p style="font-size: 14px;">Check your previous analyses and track plant health</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("View History", key="dash_view_history"):
                go_to_history()
                st.rerun()
                
        with row2_col2:
            st.markdown("""
            <div class="slideIn" style="animation-delay: 1.0s;">
                <div style="background-color: #C8E6C9; padding: 15px; border-radius: 10px; text-align: center; min-height: 180px;">
                    <img src="https://img.icons8.com/color/96/000000/book-shelf.png" style="width: 64px; height: 64px;">
                    <h4 style="color: #2E7D32;">Farming Resources</h4>
                    <p style="font-size: 14px;">Access guides on crops, soil types, and farming advice</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Resources", key="dash_resources"):
                go_to_resources()
                st.rerun()
                
        with row2_col3:
            st.markdown("""
            <div class="slideIn" style="animation-delay: 1.2s;">
                <div style="background-color: #C8E6C9; padding: 15px; border-radius: 10px; text-align: center; min-height: 180px;">
                    <img src="https://img.icons8.com/color/96/000000/partly-cloudy-day.png" style="width: 64px; height: 64px;">
                    <h4 style="color: #2E7D32;">Weather Alerts</h4>
                    <p style="font-size: 14px;">Check real-time weather updates and agricultural advisories</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Weather", key="dash_weather"):
                go_to_weather()
                st.rerun()
    
    # Recent analyses
    with st.container():
        st.subheader("Recent Analyses")
        
        # Get user's analyses from the database
        if st.session_state.current_user:
            user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
            analyses = get_user_analyses(user_id, limit=3)
            
            if not analyses:
                st.info("You haven't performed any analyses yet. Try analyzing a plant or soil sample!")
            else:
                for analysis in analyses:
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        if isinstance(analysis, dict) and analysis.get('image_path') and os.path.exists(analysis['image_path']):
                            st.image(analysis['image_path'], width=150)
                        else:
                            st.markdown("🖼️ No image")
                    
                    with col2:
                        # Handle timestamp (could be string or datetime)
                        timestamp = analysis.get('timestamp')
                        if timestamp is None:
                            time_str = "Unknown time"
                        elif isinstance(timestamp, str):
                            try:
                                time_str = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M")
                            except ValueError:
                                time_str = timestamp
                        else:
                            time_str = timestamp.strftime("%Y-%m-%d %H:%M")
                        
                        st.markdown(f"**{analysis.get('analysis_type', 'unknown').capitalize()} Analysis** - {time_str}")
                        
                        results = analysis.get('results', {})
                        
                        if analysis.get('analysis_type') == "plant" and results:
                            if "diseases" in results and results["diseases"]:
                                primary_disease = results["diseases"][0]
                                disease_name = primary_disease.get("name", "Unknown")
                                probability = primary_disease.get("probability", 0)
                                st.markdown(f"Condition: {disease_name} ({probability:.1f}%)")
                        
                        elif analysis.get('analysis_type') == "soil" and results:
                            soil_type = results.get("type", "Unknown")
                            st.markdown(f"Soil Type: {soil_type}")
                            if "recommendations" in results:
                                st.markdown(f"Crop Suggestions: {', '.join(results['recommendations'][:3])}")
                
                if st.button("View All History"):
                    go_to_history()
                    st.rerun()

# Crop test page
def show_crop_test_page():
    st.header("Plant Health Analysis")
    
    if not st.session_state.analysis_complete:
        st.markdown("""
        Upload a photo of your plant and provide additional details to get a comprehensive analysis:
        - Disease detection
        - Water content analysis
        - Pest identification
        - Treatment recommendations
        - Maharashtra-specific crop advice
        """)
        
        # First collect details about the plant
        with st.expander("Plant Details (helps improve analysis accuracy)", expanded=True):
            st.subheader("Tell us about your crop")
            
            # Crop selection
            crop_type = st.selectbox(
                "Crop Type", 
                ["Select Crop Type", "Tomato", "Onion", "Potato", "Wheat", "Rice", "Cotton", 
                 "Sugarcane", "Soybean", "Corn/Maize", "Groundnut", "Other"]
            )
            
            # Only proceed if a crop type is selected
            if crop_type != "Select Crop Type":
                col1, col2 = st.columns(2)
                
                with col1:
                    # Plant age
                    plant_age = st.selectbox(
                        "Plant Age/Growth Stage",
                        ["Select Stage", "Seedling", "Vegetative", "Flowering", "Fruiting", "Mature"]
                    )
                    
                    # Planting date
                    planting_date = st.date_input("Planting Date (approximate)")
                
                with col2:
                    # Irrigation method
                    irrigation_method = st.selectbox(
                        "Irrigation Method",
                        ["Select Method", "Drip Irrigation", "Sprinkler", "Flood Irrigation", 
                         "Furrow Irrigation", "Rainfed", "Other"]
                    )
                    
                    # Previous treatments
                    previous_treatments = st.text_area("Any treatments already applied?", 
                                                     placeholder="e.g., fungicides, pesticides, fertilizers...")
                
                # Observed symptoms
                symptoms = st.text_area("Describe any symptoms or issues you've observed", 
                                      placeholder="e.g., yellowing leaves, spots, wilting, stunted growth...")
                
                # Save plant details to session state
                if crop_type != "Select Crop Type":
                    st.session_state.plant_details = {
                        "crop_type": crop_type if crop_type != "Select Crop Type" else None,
                        "plant_age": plant_age if plant_age != "Select Stage" else None,
                        "symptoms": symptoms if symptoms else None,
                        "planting_date": planting_date.strftime("%Y-%m-%d") if planting_date else None,
                        "irrigation_method": irrigation_method if irrigation_method != "Select Method" else None,
                        "previous_treatments": previous_treatments if previous_treatments else None
                    }
                    
                    st.success("Plant details recorded. These will be used to improve analysis accuracy!")
            else:
                st.warning("Please select a crop type to continue.")
        
        # Create a 2-column layout for upload options
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Upload an Image")
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            
            if uploaded_file is not None:
                # Store the uploaded image
                image = Image.open(uploaded_file)
                st.session_state.uploaded_image = uploaded_file
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                # Preprocess the image
                try:
                    processed_image = preprocess_image(image)
                    st.session_state.processed_image = processed_image
                    
                    # Show a success message
                    st.success("Image successfully uploaded and processed!")
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")
        
        with col2:
            st.subheader("Or Choose an Example")
            example_images = get_example_images()
            
            if not example_images:
                st.info("No example images available. Please upload your own image.")
            else:
                # Create a grid of example images (if available)
                example_grid = st.container()
                with example_grid:
                    for i in range(0, len(example_images), 2):
                        cols = st.columns(2)
                        for j in range(2):
                            if i + j < len(example_images):
                                img_path = example_images[i + j]
                                with cols[j]:
                                    st.image(img_path, caption=os.path.basename(img_path), width=150)
                                    if st.button("Use This", key=f"example_{i}_{j}"):
                                        # Load and use example image
                                        with open(img_path, "rb") as f:
                                            file_content = f.read()
                                        file_name = os.path.basename(img_path)
                                        
                                        # Create a file-like object
                                        file_object = io.BytesIO(file_content)
                                        # Add a name attribute to make it compatible with st.file_uploader
                                        file_object.name = file_name
                                        
                                        # Update session state
                                        st.session_state.uploaded_image = file_object
                                        image = Image.open(file_object)
                                        st.session_state.processed_image = preprocess_image(image)
                                        st.rerun()
        
        # Analyze button (only show if an image is uploaded and crop type is selected)
        if st.session_state.processed_image is not None and st.session_state.plant_details["crop_type"] is not None:
            analyze_col1, analyze_col2 = st.columns([3, 1])
            with analyze_col1:
                if st.button("Analyze Plant Health", key="analyze_button", use_container_width=True):
                    with st.spinner("Analyzing plant health..."):
                        # Identify the plant (consider the user-selected crop type)
                        st.session_state.plant_info = identify_plant(st.session_state.processed_image)
                        
                        # Override plant_info with user-provided crop type if available
                        if st.session_state.plant_details["crop_type"]:
                            st.session_state.plant_info["name"] = st.session_state.plant_details["crop_type"]
                        
                        # Analyze water content
                        st.session_state.water_content = detect_water_content(st.session_state.processed_image)
                        
                        # Detect diseases (use the user-confirmed plant name)
                        plant_name = st.session_state.plant_info["name"]
                        st.session_state.diseases = detect_diseases(st.session_state.processed_image, plant_name)
                        
                        # Detect pests
                        st.session_state.pests = detect_pests(st.session_state.processed_image)
                        
                        # Get preventive measures and recommendations
                        primary_condition = st.session_state.diseases[0] if st.session_state.diseases else None
                        st.session_state.preventive_measures = get_preventive_measures(plant_name, primary_condition)
                        
                        # Get fertilizer recommendations
                        st.session_state.fertilizer_recommendations = get_fertilizer_recommendations(plant_name)
                        
                        # Get Maharashtra specific recommendations
                        maharashtra_recommendations = get_local_recommendations(plant_name)
                        
                        # Compile results for saving to history
                        results = {
                            "plant_info": st.session_state.plant_info,
                            "plant_details": st.session_state.plant_details,
                            "water_content": st.session_state.water_content,
                            "diseases": st.session_state.diseases,
                            "pests": st.session_state.pests,
                            "preventive_measures": st.session_state.preventive_measures,
                            "fertilizer_recommendations": st.session_state.fertilizer_recommendations,
                            "maharashtra_recommendations": maharashtra_recommendations
                        }
                        
                        # Save analysis to history
                        save_to_history("plant", results)
                        
                        # Mark analysis as complete
                        st.session_state.analysis_complete = True
                        st.rerun()
        elif st.session_state.processed_image is not None:
            st.warning("Please select a crop type in the Plant Details section before analysis.")
    
    else:
        # Display analysis results
        plant_info = st.session_state.plant_info
        water_content = st.session_state.water_content
        diseases = st.session_state.diseases
        pests = st.session_state.pests
        preventive_measures = st.session_state.preventive_measures
        fertilizer_recommendations = st.session_state.fertilizer_recommendations
        
        # Display the original image
        if st.session_state.uploaded_image:
            image = Image.open(st.session_state.uploaded_image)
            st.image(image, caption="Analyzed Image", width=400)
        
        # Plant identification results
        st.subheader("Plant Identification")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="fadeIn">
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px;">
                    <h3 style="color: #2E7D32;">{plant_info['name']}</h3>
                    <p><em>{plant_info['scientific_name']}</em></p>
                    <p><strong>Confidence:</strong> {format_probability(plant_info['probability'])}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if "details" in plant_info:
                details = plant_info["details"]
                st.markdown(f"""
                <div class="fadeIn" style="animation-delay: 0.2s;">
                    <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px;">
                        <h4 style="color: #2E7D32;">Plant Details</h4>
                        <p><strong>Family:</strong> {details.get('family', 'Unknown')}</p>
                        <p><strong>Growing Season:</strong> {details.get('growing_season', 'Unknown')}</p>
                        <p><strong>Days to Maturity:</strong> {details.get('days_to_maturity', 'Unknown')}</p>
                        <p><strong>Sunlight Needs:</strong> {details.get('sunlight', 'Unknown')}</p>
                        <p><strong>Watering Needs:</strong> {details.get('watering', 'Unknown')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Disease detection results
        st.subheader("Disease Analysis")
        
        primary_disease = diseases[0] if diseases else None
        
        if primary_disease:
            disease_name = primary_disease.get("name", "Unknown")
            probability = primary_disease.get("probability", 0)
            description = primary_disease.get("description", "")
            treatments = primary_disease.get("treatments", [])
            
            # Determine the status color based on the disease name
            if "Healthy" in disease_name:
                status_color = "#4CAF50"  # Green
            else:
                status_color = "#F44336"  # Red
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="fadeIn" style="animation-delay: 0.4s;">
                    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px;">
                        <h3 style="color: {status_color};">{disease_name}</h3>
                        <p><strong>Confidence:</strong> {format_probability(probability)}</p>
                        <p>{description}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if treatments and "Healthy" not in disease_name:
                    st.markdown(f"""
                    <div class="fadeIn" style="animation-delay: 0.5s;">
                        <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px;">
                            <h4 style="color: #2E7D32;">Treatment Recommendations</h4>
                            <ul>
                            {"".join([f"<li>{treatment}</li>" for treatment in treatments])}
                            </ul>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Show secondary diseases if any
            if len(diseases) > 1 and "Healthy" not in disease_name:
                st.subheader("Other Potential Conditions")
                secondary_diseases = diseases[1:]
                
                for disease in secondary_diseases:
                    sec_name = disease.get("name", "Unknown")
                    sec_probability = disease.get("probability", 0)
                    sec_description = disease.get("description", "")
                    
                    st.markdown(f"""
                    <div class="fadeIn" style="animation-delay: 0.6s;">
                        <div style="background-color: #F9FBE7; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
                            <h4 style="color: #33691E;">{sec_name} ({format_probability(sec_probability)})</h4>
                            <p>{sec_description}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Water content analysis
        if water_content:
            st.subheader("Water Content Analysis")
            
            percentage = water_content.get("percentage", 0)
            status = water_content.get("status", "")
            recommendation = water_content.get("recommendation", "")
            color = water_content.get("color", "#4CAF50")
            
            st.markdown(f"""
            <div class="fadeIn" style="animation-delay: 0.7s;">
                <div style="background-color: #E1F5FE; padding: 15px; border-radius: 10px;">
                    <h3 style="color: {color};">{status}</h3>
                    <div style="background-color: #E0E0E0; height: 20px; border-radius: 10px; margin: 10px 0;">
                        <div style="background-color: {color}; width: {percentage}%; height: 20px; border-radius: 10px; text-align: center; color: white; line-height: 20px; font-weight: bold;">
                            {percentage}%
                        </div>
                    </div>
                    <p>{recommendation}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Pest detection
        if pests:
            st.subheader("Pest Analysis")
            
            pest_name = pests.get("name", "Unknown")
            infestation_level = pests.get("infestation_level", "None")
            description = pests.get("description", "")
            damage = pests.get("damage", "")
            control_methods = pests.get("control_methods", [])
            
            # Determine color based on infestation level
            if infestation_level == "None":
                level_color = "#4CAF50"  # Green
            elif infestation_level == "Low":
                level_color = "#FFC107"  # Amber
            elif infestation_level == "Moderate":
                level_color = "#FF9800"  # Orange
            else:
                level_color = "#F44336"  # Red
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="fadeIn" style="animation-delay: 0.8s;">
                    <div style="background-color: #FAFAFA; padding: 15px; border-radius: 10px;">
                        <h3 style="color: {level_color};">{pest_name}</h3>
                        <p><strong>Infestation Level:</strong> <span style="color: {level_color};">{infestation_level}</span></p>
                        <p>{description}</p>
                        {f"<p><strong>Damage:</strong> {damage}</p>" if damage and infestation_level != "None" else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if control_methods:
                    st.markdown(f"""
                    <div class="fadeIn" style="animation-delay: 0.9s;">
                        <div style="background-color: #F5F5F5; padding: 15px; border-radius: 10px;">
                            <h4 style="color: #212121;">Control Methods</h4>
                            <ul>
                            {"".join([f"<li>{method}</li>" for method in control_methods])}
                            </ul>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Preventive measures section
        if preventive_measures:
            st.subheader("Preventive Measures")
            
            # Display preventive measures in an expandable section
            with st.expander("View Preventive Measures", expanded=False):
                for measure in preventive_measures:
                    st.markdown(f"• {measure}")
        
        # Fertilizer recommendations
        if fertilizer_recommendations:
            st.subheader("Fertilizer Recommendations")
            
            # Display fertilizer recommendations in an expandable section
            with st.expander("View Fertilizer Recommendations", expanded=False):
                for fertilizer in fertilizer_recommendations:
                    name = fertilizer.get("name", "Unknown")
                    npk = fertilizer.get("npk", "N/A")
                    description = fertilizer.get("description", "No description available.")
                    application = fertilizer.get("application", "No application instructions available.")
                    
                    st.markdown(f"""
                    <div style="background-color: #F1F8E9; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                        <h4 style="color: #33691E;">{name}</h4>
                        <p><strong>NPK Ratio:</strong> {npk}</p>
                        <p>{description}</p>
                        <p><strong>Application:</strong> {application}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Generate a report
        st.subheader("Analysis Report")
        
        if st.button("Generate PDF Report"):
            # In a real app, this would generate a PDF
            st.info("PDF report generation would be implemented in a production app. For now, here's the report in Markdown format.")
            
            # Compile results
            analysis_results = {
                "plant_info": plant_info,
                "water_content": water_content,
                "diseases": diseases,
                "pests": pests,
                "preventive_measures": preventive_measures,
                "fertilizer_recommendations": fertilizer_recommendations
            }
            
            # Get user data if available
            user_data = None
            if st.session_state.user_profile:
                user_data = {
                    "full_name": st.session_state.user_profile.get('full_name', ''),
                    "farm_name": st.session_state.user_profile.get('farm_name', ''),
                    "location": st.session_state.user_profile.get('location', ''),
                    "district": st.session_state.user_profile.get('district', '')
                }
            
            # Generate markdown report
            report_md = generate_report_markdown(analysis_results, user_data)
            
            # Display the markdown
            st.markdown(report_md)
        
        # Button to start a new analysis
        if st.button("Start New Analysis"):
            st.session_state.analysis_complete = False
            st.session_state.uploaded_image = None
            st.session_state.processed_image = None
            st.session_state.plant_info = None
            st.session_state.water_content = None
            st.session_state.diseases = None
            st.session_state.pests = None
            st.session_state.preventive_measures = []
            st.session_state.fertilizer_recommendations = []
            st.rerun()

# Soil analysis page
def show_soil_analysis_page():
    st.header("Soil Analysis")
    
    if not st.session_state.soil_analysis_complete:
        st.markdown("""
        Upload a photo of your soil to analyze:
        - Soil type identification
        - Nutrient content estimation
        - Crop recommendations
        - Soil improvement suggestions
        - Maharashtra-specific advice
        """)
        
        # First collect context about the soil
        with st.expander("Soil Context (helps improve analysis accuracy)", expanded=True):
            st.subheader("Tell us about your soil")
            
            # Location information
            st.markdown("#### Location Information")
            col1, col2 = st.columns(2)
            
            with col1:
                district = st.selectbox("District in Maharashtra", 
                                     ["Select District", "Ahmednagar", "Akola", "Amravati", "Aurangabad", 
                                      "Beed", "Bhandara", "Buldhana", "Chandrapur", "Dhule", 
                                      "Gadchiroli", "Gondia", "Hingoli", "Jalgaon", "Jalna", 
                                      "Kolhapur", "Latur", "Mumbai City", "Mumbai Suburban", 
                                      "Nagpur", "Nanded", "Nandurbar", "Nashik", "Osmanabad", 
                                      "Palghar", "Parbhani", "Pune", "Raigad", "Ratnagiri", 
                                      "Sangli", "Satara", "Sindhudurg", "Solapur", "Thane", 
                                      "Wardha", "Washim", "Yavatmal", "Other"])
            
            with col2:
                terrain = st.selectbox("Terrain Type", 
                                     ["Select Terrain", "Flat Land", "Sloped Land", "Hill Top", 
                                      "River Basin", "Valley", "Coastal", "Other"])
            
            # Soil characteristics
            st.markdown("#### Current Soil Conditions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                soil_color = st.selectbox("Soil Color", 
                                        ["Select Color", "Dark Brown/Black", "Brown", "Reddish Brown", 
                                         "Yellow/Tan", "Grey", "White/Chalky"])
            
            with col2:
                soil_texture = st.selectbox("Soil Texture", 
                                          ["Select Texture", "Sandy (Gritty)", "Silty (Smooth)", 
                                           "Clay (Sticky)", "Loamy (Mixed)", "Rocky", "Other"])
            
            with col3:
                soil_moisture = st.selectbox("Current Moisture Level", 
                                           ["Select Moisture", "Dry", "Slightly Moist", 
                                            "Moist", "Wet", "Waterlogged"])
            
            # Farming history
            st.markdown("#### Farming History")
            col1, col2 = st.columns(2)
            
            with col1:
                previous_crop = st.text_input("Previous Crop Grown in This Soil")
                irrigation_source = st.selectbox("Primary Irrigation Source",
                                              ["Select Source", "Rain-fed", "Canal", "Well/Borewell", 
                                               "Pond/Lake", "River", "Other"])
            
            with col2:
                fertilizers_used = st.text_area("Fertilizers/Amendments Used Previously", 
                                              placeholder="e.g., NPK, compost, lime...")
                observed_issues = st.text_area("Any Issues Observed with This Soil?", 
                                             placeholder="e.g., poor drainage, slow growth, discoloration...")
            
            # Save soil context to session state
            if district != "Select District" or soil_texture != "Select Texture":
                soil_context = {
                    "district": district if district != "Select District" else None,
                    "terrain": terrain if terrain != "Select Terrain" else None,
                    "soil_color": soil_color if soil_color != "Select Color" else None,
                    "soil_texture": soil_texture if soil_texture != "Select Texture" else None,
                    "soil_moisture": soil_moisture if soil_moisture != "Select Moisture" else None,
                    "previous_crop": previous_crop,
                    "irrigation_source": irrigation_source if irrigation_source != "Select Source" else None,
                    "fertilizers_used": fertilizers_used,
                    "observed_issues": observed_issues
                }
                st.session_state.soil_context = soil_context
                st.success("Soil context recorded. This will help improve analysis accuracy!")
        
        # Upload soil image
        uploaded_file = st.file_uploader("Choose a soil image...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Store the uploaded image
            image = Image.open(uploaded_file)
            st.session_state.uploaded_soil_image = uploaded_file
            st.image(image, caption="Uploaded Soil Image", use_column_width=True)
            
            # Show an "Analyze" button
            if st.button("Analyze Soil", key="analyze_soil_button"):
                with st.spinner("Analyzing soil..."):
                    # Analyze soil (simulated function)
                    soil_fertility, crop_suggestions, rainfall, season = analyze_soil(image)
                    
                    # Store results in session state
                    st.session_state.soil_fertility = soil_fertility
                    st.session_state.crop_suggestions = crop_suggestions
                    
                    # Additional context data
                    st.session_state.soil_context = {
                        "rainfall": rainfall,
                        "season": season
                    }
                    
                    # Compile results for saving to history
                    results = {
                        "type": soil_fertility["type"],
                        "properties": soil_fertility,
                        "recommendations": crop_suggestions,
                        "context": {
                            "rainfall": rainfall,
                            "season": season
                        }
                    }
                    
                    # Save analysis to history
                    save_to_history("soil", results)
                    
                    # Mark analysis as complete
                    st.session_state.soil_analysis_complete = True
                    st.rerun()
    
    else:
        # Display soil analysis results
        soil_fertility = st.session_state.soil_fertility
        crop_suggestions = st.session_state.crop_suggestions
        soil_context = st.session_state.soil_context
        
        # Display the soil image
        if st.session_state.uploaded_soil_image:
            image = Image.open(st.session_state.uploaded_soil_image)
            st.image(image, caption="Analyzed Soil Image", width=400)
        
        # Soil type and properties
        st.subheader("Soil Analysis Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Main soil properties
            soil_type = soil_fertility["type"]
            ph_value = soil_fertility["pH"]
            
            # Determine pH status
            if 6.0 <= ph_value <= 7.5:
                ph_status = "Optimal"
                ph_color = "#4CAF50"  # Green
            elif 5.5 <= ph_value < 6.0 or 7.5 < ph_value <= 8.0:
                ph_status = "Acceptable"
                ph_color = "#FFC107"  # Amber
            else:
                ph_status = "Suboptimal"
                ph_color = "#F44336"  # Red
            
            st.markdown(f"""
            <div class="fadeIn">
                <div style="background-color: #EFEBE9; padding: 15px; border-radius: 10px;">
                    <h3 style="color: #795548;">{soil_type} Soil</h3>
                    <p><strong>pH Level:</strong> {ph_value} <span style="color: {ph_color};">({ph_status})</span></p>
                    <p><strong>Organic Matter:</strong> {soil_fertility["organic_matter"]}</p>
                    <p><strong>Moisture Content:</strong> {soil_fertility["moisture"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Nutrient levels
            st.markdown(f"""
            <div class="fadeIn" style="animation-delay: 0.2s;">
                <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px;">
                    <h4 style="color: #2E7D32;">Nutrient Levels</h4>
                    <p><strong>Nitrogen (N):</strong> {soil_fertility["nitrogen"]}</p>
                    <p><strong>Phosphorus (P):</strong> {soil_fertility["phosphorus"]}</p>
                    <p><strong>Potassium (K):</strong> {soil_fertility["potassium"]}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Environmental context
        st.subheader("Environmental Context")
        
        col1, col2 = st.columns(2)
        
        with col1:
            rainfall = soil_context["rainfall"]
            # Determine icon based on rainfall
            if rainfall == "Low":
                rainfall_icon = "☀️"
            elif rainfall == "Moderate":
                rainfall_icon = "🌤️"
            else:
                rainfall_icon = "🌧️"
                
            st.markdown(f"""
            <div class="fadeIn" style="animation-delay: 0.3s;">
                <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #1976D2;">{rainfall_icon} {rainfall} Rainfall</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            season = soil_context["season"]
            # Determine icon based on season
            if season == "Spring":
                season_icon = "🌱"
            elif season == "Summer":
                season_icon = "☀️"
            elif season == "Fall":
                season_icon = "🍂"
            else:
                season_icon = "❄️"
                
            st.markdown(f"""
            <div class="fadeIn" style="animation-delay: 0.4s;">
                <div style="background-color: #FFF3E0; padding: 15px; border-radius: 10px; text-align: center;">
                    <h3 style="color: #E65100;">{season_icon} {season} Season</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Crop recommendations
        st.subheader("Recommended Crops")
        
        # Display crop suggestions in a grid
        cols = st.columns(len(crop_suggestions))
        for i, crop in enumerate(crop_suggestions):
            with cols[i]:
                st.markdown(f"""
                <div class="fadeIn" style="animation-delay: {0.5 + i*0.1}s;">
                    <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px; text-align: center;">
                        <h4 style="color: #2E7D32;">{crop}</h4>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Soil improvement suggestions based on soil type
        st.subheader("Soil Improvement Suggestions")
        
        improvement_tips = {
            "Sandy": [
                "Add organic matter like compost or well-rotted manure to improve water retention",
                "Consider adding clay to improve nutrient retention",
                "Use mulch to reduce evaporation",
                "Water more frequently but in smaller amounts"
            ],
            "Clay": [
                "Add organic matter to improve drainage and aeration",
                "Consider adding gypsum to break up heavy clay",
                "Avoid working clay soil when it's too wet or too dry",
                "Raised beds can help improve drainage"
            ],
            "Loamy": [
                "Maintain organic matter levels with regular compost additions",
                "Rotate crops to maintain soil health",
                "Consider cover crops during off-seasons",
                "Minimal tillage to preserve soil structure"
            ],
            "Silty": [
                "Add organic matter to improve structure",
                "Avoid compaction by not walking on garden beds",
                "Consider raised beds for better drainage",
                "Use mulch to protect soil structure"
            ],
            "Peaty": [
                "Monitor pH levels regularly as peaty soils tend to be acidic",
                "Add lime if pH is too low",
                "Improve drainage if waterlogging occurs",
                "Consider adding balanced fertilizers as peaty soils may lack nutrients"
            ],
            "Chalky": [
                "Add organic matter to improve water retention",
                "Choose plants that tolerate alkaline conditions",
                "Use acidic fertilizers for plants that prefer lower pH",
                "Apply mulch to reduce moisture loss"
            ]
        }
        
        # Get tips for the specific soil type
        soil_type = soil_fertility["type"]
        tips = improvement_tips.get(soil_type, ["No specific recommendations available for this soil type."])
        
        with st.expander("View Soil Improvement Tips", expanded=True):
            for tip in tips:
                st.markdown(f"• {tip}")
        
        # Button to start a new analysis
        if st.button("Start New Soil Analysis"):
            st.session_state.soil_analysis_complete = False
            st.session_state.uploaded_soil_image = None
            st.session_state.soil_fertility = None
            st.session_state.crop_suggestions = []
            st.rerun()

# History page
def show_history_page():
    st.header("Analysis History")
    
    # Get user's analyses from the database
    if st.session_state.current_user:
        try:
            # Get user_id safely, supporting both object and dict access
            user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
            analyses = get_user_analyses(user_id)
            
            if not analyses:
                st.info("You haven't performed any analyses yet.")
                return
                
            # Group analyses by date
            analyses_by_date = {}
            for analysis in analyses:
                if not isinstance(analysis, dict):
                    st.warning("Unexpected analysis format. Expected dictionary.")
                    continue
                    
                try:
                    # Handle timestamp (could be string or datetime object)
                    timestamp = analysis.get('timestamp')
                    if timestamp is None:
                        date_str = "Unknown Date"
                    elif isinstance(timestamp, str):
                        try:
                            date_str = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d")
                        except ValueError:
                            date_str = timestamp.split('T')[0]  # Fallback for different formats
                    else:
                        date_str = timestamp.strftime("%Y-%m-%d")
                    
                    if date_str not in analyses_by_date:
                        analyses_by_date[date_str] = []
                    analyses_by_date[date_str].append(analysis)
                except Exception as e:
                    st.error(f"Error processing analysis timestamp: {str(e)}")
                    continue
            
            # Display analyses grouped by date
            for date_str, date_analyses in sorted(analyses_by_date.items(), reverse=True):
                with st.expander(f"Analyses from {date_str} ({len(date_analyses)})", expanded=False):
                    for analysis in date_analyses:
                        try:
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                image_path = analysis.get('image_path')
                                if image_path and os.path.exists(image_path):
                                    st.image(image_path, width=150)
                                else:
                                    st.markdown("🖼️ No image available")
                            
                            with col2:
                                # Handle timestamp display
                                timestamp = analysis.get('timestamp')
                                if timestamp is None:
                                    time_str = "Unknown time"
                                elif isinstance(timestamp, str):
                                    try:
                                        time_str = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f").strftime("%H:%M:%S")
                                    except ValueError:
                                        time_str = timestamp.split('T')[1].split('.')[0] if 'T' in timestamp else timestamp
                                else:
                                    time_str = timestamp.strftime("%H:%M:%S")
                                
                                analysis_type = analysis.get('analysis_type', 'unknown').capitalize()
                                st.markdown(f"**{analysis_type} Analysis** - {time_str}")
                                
                                results = analysis.get('results', {})
                                
                                if analysis.get('analysis_type') == "plant":
                                    plant_info = results.get('plant_info', {})
                                    st.markdown(f"Plant: {plant_info.get('name', 'Unknown')}")
                                    
                                    diseases = results.get('diseases', [])
                                    if diseases:
                                        primary_disease = diseases[0]
                                        disease_name = primary_disease.get('name', 'Unknown')
                                        probability = primary_disease.get('probability', 0)
                                        st.markdown(f"Condition: {disease_name} ({probability:.1f}%)")
                                    
                                    water_content = results.get('water_content', {})
                                    if water_content:
                                        status = water_content.get('status', 'Unknown')
                                        percentage = water_content.get('percentage', 0)
                                        st.markdown(f"Water Status: {status} ({percentage}%)")
                                
                                elif analysis.get('analysis_type') == "soil":
                                    soil_type = results.get('type', 'Unknown')
                                    st.markdown(f"Soil Type: {soil_type}")
                                    
                                    recommendations = results.get('recommendations', [])
                                    if recommendations:
                                        st.markdown(f"Crop Suggestions: {', '.join(recommendations[:3])}")
                                        if len(recommendations) > 3:
                                            st.markdown(f"*And {len(recommendations)-3} more...*")
                                
                                # Add a button to view full details
                                if st.button("View Details", key=f"details_{analysis.get('id', '')}"):
                                    st.session_state.current_analysis = analysis
                                    st.session_state.page = "analysis_details"
                                    st.rerun()
                        
                        except Exception as e:
                            st.error(f"Error displaying analysis: {str(e)}")
                            continue
            
            # Add a button to clear history (would need proper implementation)
            if st.button("Clear All History", type="secondary"):
                st.warning("This would clear your analysis history in a production app")
        
        except Exception as e:
            st.error(f"Error loading analysis history: {str(e)}")
    else:
        st.warning("Please log in to view your analysis history.")

# Main app logic
def main():
    # Initialize language support
    initialize_language()
    
    # Only show language selector and weather widget after login
    if st.session_state.current_user:
        with st.sidebar:
            # Add language selector in the sidebar
            st.markdown("### " + t("language_settings"))
            show_language_selector()
            
            # Display weather widget in sidebar
            display_weather_widget()
    
    show_header()
    
    if st.session_state.page == "login":
        show_login_page()
    elif st.session_state.page == "signup":
        show_signup_page()
    elif st.session_state.page == "profile_setup":
        show_profile_setup_page()
    elif st.session_state.page == "dashboard":
        show_dashboard_page()
    elif st.session_state.page == "crop_test":
        show_crop_test_page()
    elif st.session_state.page == "soil_analysis":
        show_soil_analysis_page()
    elif st.session_state.page == "history":
        show_history_page()
    elif st.session_state.page == "resources":
        show_resources_page()
    elif st.session_state.page == "weather":
        show_weather_page()

if __name__ == "__main__":
    main()