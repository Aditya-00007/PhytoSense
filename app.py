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


# Import custom modules
from image_processing import preprocess_image, extract_features
from model_handler import identify_plant, detect_water_content, detect_diseases, detect_pests
from recommendations import get_preventive_measures, get_fertilizer_recommendations
from utils import load_svg, get_example_images, generate_report_markdown, format_probability, save_uploaded_image
from db_adapter import create_user, verify_user, update_user_profile, save_analysis, get_user_analyses, get_user_by_id, get_user_profile, save_session, get_active_session, clear_session, verify_forgot_password, reset_password
from maharashtra import get_local_recommendations
from profile_utils import get_profile_field, get_select_index
from soil_analyzer import analyze_soil, get_soil_details
from model import load_model
from plant_analysis import enhanced_analysis
from weather_service import display_weather_widget, show_weather_page, fetch_weather_data, fetch_forecast_data, get_weather_alerts
from language_support import initialize_language, show_language_selector, t,translate_api
from crop_suggestion_helper import *
from krishimitra import show_chatbot_page

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
    /* Main container styling */
    .auth-container {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    
    /* Camera Input Styling */
    .stCamera {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stCamera button {
        background-color: #4CAF50 !important;
    }
    [data-testid="stCameraInputButton"] {
        border-radius: 20px !important;
    }
            
    /* Form styling */
    .auth-form {
        background-color: white;
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input, 
    .stTextInput>div>div>input:focus {
        border: 1px solid #4CAF50;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* Button styling */
    .auth-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 10px 0;
        cursor: pointer;
        border-radius: 25px;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .auth-button:hover {
        background-color: #3e8e41;
        transform: translateY(-2px);
    }
    
    /* Secondary button styling */
    .secondary-button {
        background-color: white;
        color: #4CAF50;
        border: 1px solid #4CAF50;
    }
    
    .secondary-button:hover {
        background-color: #f1f8e9;
    }
    
    /* Background styling */
    .stApp {
        background-image: linear-gradient(to bottom, #e8f5e9, #f1f8e9);
    }
    
    /* Logo styling */
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .logo-img {
        width: 120px;
        height: auto;
    }
    
    /* Welcome text styling */
    .welcome-text {
        color: #2e7d32;
        margin-bottom: 20px;
    }
    
    /* Feature list styling */
    .feature-list {
        padding-left: 20px;
    }
    
    .feature-list li {
        margin-bottom: 10px;
        color: #555;
    }
    
    /* Animation for the form */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated-form {
        animation: fadeInUp 0.6s ease-out;
    }

    /* Additional Animations */
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

    /* Gradient button */
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

    /* Hide Streamlit Toolbar only */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* Custom Header Styling */
    .unified-header {
        max-width: 40% ;
        background-color: white;
        padding: 1rem 2rem;
        border-bottom: 3px solid #4CAF50;
        margin-bottom: 0rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        overflow: hidden;
    }
    
    .header-title {
        color: #2e7d32; 
        font-size: 2.6rem;
        font-weight: bold; 
        margin: 0;
        line-height: 1.2;
    }
    
    .header-subtitle {
        color: #666; 
        font-size: 1.3rem; 
        margin: 0;
    }

    /* Navbar Buttons - Global Styles */
    div[data-testid="column"] button {
        width: 100%;
        margin: 0px;
        padding: 0.5rem;
    }

    /* Active Button (Primary) */
    div[data-testid="column"] button[kind="primary"] {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 5px !important;
        box-shadow: 0 2px 5px rgba(76, 175, 80, 0.3) !important;
    }

    /* Inactive Button (Secondary) */
    div[data-testid="column"] button[kind="secondary"] {
        background-color: transparent !important;
        color: #555 !important;
        border: 1px solid transparent !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="column"] button[kind="secondary"]:hover {
        background-color: #f0f0f0 !important;
        color: #2e7d32 !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 5px !important;
    }

    /* Remove default focus outline */
    button:focus {
        outline: none !important;
    }

        
        /* Header Optimization */
        .unified-header {
            max-width: 40% ;
            padding: 0.5rem 1rem !important;
            margin-bottom: 0rem !important;
            background-color:#f8f9fa !important;
            position: sticky;
            top: 0;
            z-index: 999;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header-title {
            font-size: 2.6rem !important;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .header-subtitle {
            /* Display restored */
            display: block !important;
            margin-top: 2px !important;
        }

        /* Content Alignment & Spacing */
        .block-container {
            padding-top: 0rem !important;
            padding-left: 6% !important;
            padding-right: 6% !important;
            max-width: 100% !important;
        }
        
        /* Column stacking */
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 10px !important;
        }
        
        /* Container adjustments */
        .auth-container {
            padding: 15px !important;
            margin: 10px 0 !important;
            border-radius: 10px !important;
        }
        
        /* Inputs & Buttons */
        .stTextInput input, .stSelectbox, .stNumberInput input {
            min-height: 45px !important;
            font-size: 16px !important;
        }
        
        button {
            min-height: 45px !important;
        }
        
        /* Header 2-column layout */
        div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"] {
            min-width: 0 !important;
        }
        
        /* Brand Column (First) */
        div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-of-type(1) {
            width: 60% !important;
            flex: 0 0 60% !important;
            max-width: 40% !important;
        }
        
        /* Spacer Column (Second) - Hide it */
        div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-of-type(2) {
            display: none !important;
        }
        
        /* User Column (Third) */
        div[data-testid="stHorizontalBlock"]:nth-of-type(1) div[data-testid="column"]:nth-of-type(3) {
            width: 40% !important;
            flex: 0 0 40% !important;
            max-width: 40% !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
/* =========================
   STICKY NAVBAR
========================= */
.sticky-navbar {
    position: sticky;
    top: 120px; /* Adjusted for larger header */
    z-index: 998;
    padding: 10px 0;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
}

/* Force horizontal layout even on mobile for sticky navbar columns */
.sticky-navbar [data-testid="stHorizontalBlock"] {
    display: flex !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    gap: 10px !important;
    padding-bottom: 5px !important;
    -webkit-overflow-scrolling: touch;
}

.sticky-navbar [data-testid="column"] {
    min-width: 120px !important; /* Ensure buttons don't shrink too much */
    flex: 0 0 auto !important;
    width: auto !important;
    margin-bottom: 0 !important;
}

/* Hide scrollbar for clean look */
.sticky-navbar [data-testid="stHorizontalBlock"]::-webkit-scrollbar {
    height: 4px;
}
.sticky-navbar [data-testid="stHorizontalBlock"]::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 2px;
}

    
/* =========================
   NAVBAR VISIBILITY
========================= */

/* Navbar Visibility - Restored to common handling */

@media (max-width: 400px) {

    /* Navbar */
    /* Navbar visibility reset */

    /* Header Optimization */
    .unified-header {
        max-width: 40% !important;
        padding: 0.5rem 0.5rem !important;
        margin-bottom: 0rem !important;
        background-color: #ffffff !important;
        position: sticky;
        top: 0;
        z-index: 999;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        overflow: hidden;
    }

    /* Hide scrollbar visually */
section[data-testid="stSidebar"]::-webkit-scrollbar {
    display: none;
}

section[data-testid="stSidebar"] > div {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    overflow: hidden !important; 
    z-index: 99999;
}

section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
    overflow: hidden !important;
    max-height: 100vh !important;
}

    .header-title {
        font-size: 1.5rem !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .header-subtitle {
        font-size: 1.1rem !important;
        display: block !important;
    }

    /* Layout */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 6% !important;
        padding-right: 6% !important;
        max-width: 100% !important;
    }

    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
        min-width: 100% !important;
        margin-bottom: 10px !important;
    }

    .auth-container {
        padding: 15px !important;
        margin: 10px 0 !important;
        border-radius: 10px !important;
    }

    .stTextInput input,
    .stSelectbox,
    .stNumberInput input {
        min-height: 45px !important;
        font-size: 16px !important;
    }

    button {
        min-height: 45px !important;
    }

    /* Header column layout */
    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
    div[data-testid="column"]:nth-of-type(1) {
        width: 60% !important;
        flex: 0 0 60% !important;
        max-width: 40% !important;
    }

    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
    div[data-testid="column"]:nth-of-type(2) {
        display: none !important;
    }

    div[data-testid="stHorizontalBlock"]:nth-of-type(1)
    div[data-testid="column"]:nth-of-type(3) {
        width: 40% !important;
        flex: 0 0 40% !important;
        max-width: 40% !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-top: 10px;
    }

    .sticky-navbar {
        display: none !important;
    }
}


</style>
""", unsafe_allow_html=True)

# Create data directories if they don't exist
for directory in ["data", "uploads", "assets", "assets/examples", "weather_data"]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
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
    if "soil_analysis_saved" not in st.session_state:
        st.session_state.soil_analysis_saved = False
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
    # Language support
    if "language" not in st.session_state:
        st.session_state.language = "en"
    if "image_source" not in st.session_state:
        st.session_state.image_source = None 
    if "image_capture_method" not in st.session_state:
        st.session_state.image_capture_method = None # Will store 'upload', 'example', or 'live'

    # Check for persistent session if user is not logged in
    if st.session_state.current_user is None:
        active_username = get_active_session()
        if active_username:
            # Load user data
            user_data = verify_user(active_username, "dummy") # We don't have password, need another way or trust the file
            # Actually, better to use get_user_by_id if we trust the session file
            # But get_user_by_id requires ID. For JSON DB, ID is username.
            # Let's try to get user data directly.
            # verify_user is for login form.
            # We need a way to load user by username without password.
            # In local_db, get_user_by_id takes ID (which is username).
            try:
                user = get_user_by_id(active_username)
                if user:
                    st.session_state.current_user = user
                    st.session_state.page = "dashboard"
                    
                    # Load profile
                    user_id = user['id'] if isinstance(user, dict) else user.id
                    profile = get_user_profile(user_id)
                    if profile:
                        st.session_state.user_profile = profile
            except Exception:
                pass

# Initialize session state
init_session_state()

# Initialize language support
initialize_language()

# Navigation functions
def go_to_login():
    st.session_state.page = "login"
    st.session_state.show_account_created = False

def go_to_forgot_password():
    st.session_state.page = "forgot_password"

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

def go_to_chatbot():
    st.session_state.page = "chatbot"

def go_to_weather():
    st.session_state.page = "weather"

def logout():
    """Log out the current user and reset session state variables"""
    # Reset all session state variables
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
    
    # Clear persistent session
    clear_session()

# Save analysis to history
def save_to_history(analysis_type, data):
    """Save analysis results to user history"""
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

# translate list
def t_list(text_list):
    return [t(text) for text in text_list]

# Helper function to render navigation items
def _render_nav_items(container, key_prefix, is_mobile=False):
    """Render navigation buttons inside a container"""
    real_nav = [
        ("Dashboard", "dashboard"),
        ("Krishi Mitra", "chatbot"),
        ("Test Crop", "crop_test"),
        ("Soil Analysis", "soil_analysis"),
        ("Resources", "resources"),
        ("Weather", "weather"),
        ("History", "history")
    ]
    
    current_page = st.session_state.page
    
    if is_mobile:
        # Stacked buttons for mobile - each in its own row
        for label, page_key in real_nav:
            btn_type = "primary" if current_page == page_key else "secondary"
            # Create a new row for each button
            if container.button(t(label), key=f"{key_prefix}_{page_key}", type=btn_type, use_container_width=True):
                if current_page != page_key:
                    st.session_state.page = page_key
                    st.rerun()
    else:
        # Horizontal columns for desktop
        nav_cols = container.columns(len(real_nav))
        for i, (label, page_key) in enumerate(real_nav):
            with nav_cols[i]:
                btn_type = "primary" if current_page == page_key else "secondary"
                if st.button(t(label), key=f"{key_prefix}_{page_key}", type=btn_type, use_container_width=True):
                    if current_page != page_key:
                        st.session_state.page = page_key
                        st.rerun()


# Header with unified layout
def show_header():
    """Display unified header consistent across all pages"""
    
    # 1. Main Header Container
    with st.container():
        # Use a custom class to identify header container for CSS
        st.markdown('<div class="main-header-container">', unsafe_allow_html=True)
        col_brand, col_spacer, col_user = st.columns([4, 2, 3])

        # --- Left: Brand ---
        with col_brand:
            st.markdown('<div class="brand-column">', unsafe_allow_html=True) # Marker
            brand_cols = st.columns([1, 4])
            with brand_cols[0]:
                svg_content = load_svg("assets/logo.svg")
                st.image(svg_content, width=85)
            with brand_cols[1]:
                st.markdown(f"""
                <div style='margin-top: 5px;'>
                    <div class='header-title'>{t("PhytoSense")}</div>
                    <div class='header-subtitle'>{t("AI-Powered Plant Health Monitoring System")}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # --- Right: User & Language ---
        with col_user:
            st.markdown('<div class="user-column">', unsafe_allow_html=True) # Marker
            if st.session_state.get("current_user"):
                r_cols = st.columns([1, 1.5])
                with r_cols[0]:
                    show_language_selector(sidebar=False, key="header_lang")
                with r_cols[1]:
                    username = (
                        st.session_state.current_user['username']
                        if isinstance(st.session_state.current_user, dict)
                        else st.session_state.current_user.username
                    )
                    st.write(f"👤 **{username}**")
                    if st.button(t("Logout"), key="header_logout", use_container_width=True):
                        logout()
                        st.rerun()
            else:
                r_cols = st.columns([2, 2]) 
                with r_cols[1]:
                    show_language_selector(sidebar=False, key="header_auth_lang")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Navigation (Logged in only)
    if st.session_state.get("current_user"):
        st.markdown('<div class="sticky-navbar">', unsafe_allow_html=True)
        # Use is_mobile=False to force generic horizontal columns, 
        # but CSS will handle the scrolling/stacking behavior
        _render_nav_items(st, "nav_main", is_mobile=False)
        st.markdown('</div>', unsafe_allow_html=True)



# Login page
def show_login_page():
    """Display the login page with enhanced design and functionality"""
    # Create a container for the entire login page
    with st.container():
        # Create user container - Note: Header is now global
            
        # Create two columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Login form container
            st.markdown(f"## {t('Login to PhytoSense')}")
            
            # Show success message if account was just created
            if st.session_state.show_account_created:
                st.success(t("Account created successfully! Please login."))
                st.session_state.show_account_created = False

            # Login form
            username = st.text_input(t("Username"), key="login_username", placeholder=t("Enter your username"))
            password = st.text_input(t("Password"), type="password", key="login_password", placeholder=t("Enter your password"))
            
            # Remember me checkbox
            remember_me = st.checkbox(t("Remember me"), value=True)
            
            # Login button with loading state
            if st.button(t("Login"), key="login_button", type="primary"):
                if not username or not password:
                    st.error(t("Please enter both username and password"))
                else:
                    with st.spinner(t("Authenticating...")):
                        try:
                            user = verify_user(username, password)
                            if user:
                                st.session_state.current_user = user
                                # Save persistent session if "Remember me" is checked
                                if remember_me:
                                    username_val = user['username'] if isinstance(user, dict) else user.username
                                    save_session(username_val)
                                
                                st.success(t("Login successful!"))
                                
                                # Load user profile if exists
                                user_id = user['id'] if isinstance(user, dict) else user.id
                                profile = get_user_profile(user_id)
                                if profile:
                                    st.session_state.user_profile = profile
                                
                                # Redirect based on profile completion
                                if not user.get("profile_complete", False):
                                    go_to_profile_setup()
                                else:
                                    go_to_dashboard()
                                st.rerun()
                            else:
                                st.error(t("Invalid username or password"))
                        except Exception as e:
                            st.error(f"{t('Login failed')}: {str(e)}")
            
            # Forgot password link
            if st.button(t("Forgot password?"), key="forgot_password_link"):
                go_to_forgot_password()
            
            # Signup prompt
            st.markdown(t("Don't have an account?"))
            if st.button(t("Create Account"), key="signup_prompt_button"):
                go_to_signup()

        with col2:
            # Features section
            st.markdown(f"## {t('Why Use PhytoSense?')}")
            
            # Point 1
            feature_cols = st.columns([1, 4])
            with feature_cols[0]:
                st.markdown("<h3>🔍</h3>", unsafe_allow_html=True)
            with feature_cols[1]:
                st.markdown(f"**{t('Instant Disease Diagnosis')}**")
                st.markdown(t("Detect crop diseases early with AI-powered image analysis."))
            
            # Point 2
            feature_cols = st.columns([1, 4])
            with feature_cols[0]:
                st.markdown("<h3>💧</h3>", unsafe_allow_html=True)
            with feature_cols[1]:
                st.markdown(f"**{t('Smart Resource Management')}**")
                st.markdown(t("Optimize water and fertilizer usage for maximum yield."))
            
            # Point 3
            feature_cols = st.columns([1, 4])
            with feature_cols[0]:
                st.markdown("<h3>📢</h3>", unsafe_allow_html=True)
            with feature_cols[1]:
                st.markdown(f"**{t('Real-Time Weather Alerts')}**")
                st.markdown(t("Stay ahead of climate risks with localized forecasts."))
            
            # Point 4
            feature_cols = st.columns([1, 4])
            with feature_cols[0]:
                st.markdown("<h3>👨‍🌾</h3>", unsafe_allow_html=True)
            with feature_cols[1]:
                st.markdown(f"**{t('Expert Crop Advisory')}**")
                st.markdown(t("Get personalized farming tips and government scheme info."))
            
            # Point 5
            feature_cols = st.columns([1, 4])
            with feature_cols[0]:
                st.markdown("<h3>📈</h3>", unsafe_allow_html=True)
            with feature_cols[1]:
                st.markdown(f"**{t('Yield Tracking & History')}**")
                st.markdown(t("Monitor crop health progress and maintain digital records."))
                
            # Testimonial
            st.markdown("---")
            st.markdown(f"> *\"{t('PhytoSense helped me reduce crop losses by 30%')}\"*")
            st.markdown(f"> **- {t('Rajesh K., Maharashtra Farmer')}**")


def show_forgot_password_page():
    """Display simple forgot password flow"""
    with st.container():
        # Center the form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown(f"## {t('Reset Password')}")
            
            # Step 1: Verification
            if "reset_verified" not in st.session_state:
                st.session_state.reset_verified = False
                st.session_state.reset_username = None
            
            if not st.session_state.reset_verified:
                st.info(t("Please enter your details to verify your identity."))
                
                with st.form("verify_form"):
                    username = st.text_input(t("Username"))
                    email = st.text_input(t("Email"))
                    full_name = st.text_input(t("Full Name (as in profile)"))
                    
                    submitted = st.form_submit_button(t("Verify Identity"))
                    
                    if submitted:
                        if verify_forgot_password(username, email, full_name):
                            st.session_state.reset_verified = True
                            st.session_state.reset_username = username
                            st.rerun()
                        else:
                            st.error(t("Email and name do not match our records."))
            
            else:
                # Step 2: Reset Password
                st.success(t("Identity verified! Please enter your new password."))
                
                with st.form("reset_form"):
                    new_password = st.text_input(t("New Password"), type="password")
                    confirm_password = st.text_input(t("Confirm Password"), type="password")
                    
                    submitted = st.form_submit_button(t("Reset Password"))
                    
                    if submitted:
                        if new_password != confirm_password:
                            st.error(t("Passwords do not match"))
                        elif len(new_password) < 8:
                            st.error(t("Password must be at least 8 characters"))
                        else:
                            if reset_password(st.session_state.reset_username, new_password):
                                st.success(t("Password reset successfully! Redirecting to login..."))
                                time.sleep(2)
                                # Clear reset state
                                del st.session_state.reset_verified
                                del st.session_state.reset_username
                                go_to_login()
                                st.rerun()
                            else:
                                st.error(t("Failed to reset password. Please try again."))
            
            # Back to login
            st.markdown("---")
            if st.button(t("Back to Login")):
                if "reset_verified" in st.session_state:
                    del st.session_state.reset_verified
                if "reset_username" in st.session_state:
                    del st.session_state.reset_username
                go_to_login()

def show_signup_page():
    """Display the signup page with enhanced design and validation"""
    # Create a container for the entire page
    with st.container():
        # Create two columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Form container
            st.markdown(f"## {t('Create Your Account')}")
            
            # Signup form with validation
            with st.form("signup_form"):
                # Required fields
                username = st.text_input(f"{t('Username')}*", help=t("Required. 4-20 characters, letters and numbers only"))
                email = st.text_input(f"{t('Email')}*", help=t("Required for account recovery"))
                password = st.text_input(f"{t('Password')}*", type="password", 
                                       help=t("Minimum 8 characters with at least one number and special character"))
                confirm_password = st.text_input(f"{t('Confirm Password')}*", type="password")
                
                # Optional fields
                farm_location = st.text_input(t("Farm Location"), help=t("Optional - helps provide localized recommendations"))
                phone = st.text_input(t("Phone Number"), help=t("Optional - for SMS alerts"))
                
                # Terms checkbox
                agree_terms = st.checkbox(t("I agree to the Terms of Service and Privacy Policy*"), value=False)
                
                # Marketing consent
                receive_updates = st.checkbox(t("I'd like to receive product updates and farming tips"), value=True)
                
                # Form submission
                submitted = st.form_submit_button(t("Create Account"), type="primary")

                # Testimonial image placeholder
                st.markdown("---")
                st.image("https://images.unsplash.com/photo-1500382017468-9049fed747ef?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80", 
                        caption=f"\"{t('PhytoSense helped me reduce crop losses by 30%')}\" - {t('Rajesh K., Maharashtra Farmer')}")

                 # (Logic stays)

        with col2:
            # Benefits section
            st.markdown(f"## {t('Why Join PhytoSense?')}")
            
            benefit_cols = st.columns([1, 3])
            with benefit_cols[0]:
                st.markdown("🌾")
            with benefit_cols[1]:
                st.markdown(f"**{t('Smart Farming')}**")
                st.markdown(t("Get AI-powered insights for your crops"))
            
            benefit_cols = st.columns([1, 3])
            with benefit_cols[0]:
                st.markdown("💧")
            with benefit_cols[1]:
                st.markdown(f"**{t('Water Optimization')}**")
                st.markdown(t("Prevent over/under watering with precise analysis"))
            
            benefit_cols = st.columns([1, 3])
            with benefit_cols[0]:
                st.markdown("🔬")
            with benefit_cols[1]:
                st.markdown(f"**{t('Disease Detection')}**")
                st.markdown(t("Identify plant issues before they become serious"))
            
            benefit_cols = st.columns([1, 3])
            with benefit_cols[0]:
                st.markdown("📊")
            with benefit_cols[1]:
                st.markdown(f"**{t('Track Progress')}**")
                st.markdown(t("Monitor your farm's health over time"))
            
             
            # Login Redirect
            st.markdown("---")
            st.markdown(f"**{t('Already have an account?')}**")
            if st.button(t("Login Here"), key="signup_login_redirect"):
                go_to_login()
                
                if submitted:
                    # Validate inputs
                    errors = []
                    
                    if not username:
                        errors.append(t("Username is required"))
                    elif len(username) < 4 or len(username) > 20:
                        errors.append(t("Username must be 4-20 characters"))
                    elif not username.isalnum():
                        errors.append(t("Username can only contain letters and numbers"))
                    
                    if not email:
                        errors.append(t("Email is required"))
                    elif "@" not in email or "." not in email:
                        errors.append(t("Please enter a valid email address"))
                    
                    if not password:
                        errors.append(t("Password is required"))
                    elif len(password) < 8:
                        errors.append(t("Password must be at least 8 characters"))
                    elif not any(char.isdigit() for char in password):
                        errors.append(t("Password must contain at least one number"))
                    elif not any(not char.isalnum() for char in password):
                        errors.append(t("Password must contain at least one special character"))
                    
                    if password != confirm_password:
                        errors.append(t("Passwords do not match"))
                    
                    if not agree_terms:
                        errors.append(t("You must agree to the terms of service"))
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        with st.spinner(t("Creating your account...")):
                            try:
                                # Create user
                                success, message = create_user(
                                username=username,
                                password=password,
                                email=email,
                                farm_location=farm_location
                                )
                                
                                if success:
                                    st.session_state.show_account_created = True
                                    st.success(t("Account created successfully!"))
                                    time.sleep(1)  # Show success message briefly
                                    go_to_login()
                                    st.rerun()
                                else:
                                    st.error(f"{t('Error')}: {message}")
                            except Exception as e:
                                st.error(f"{t('Account creation failed')}: {str(e)}")
            
            # Login prompt
            st.markdown(t("Already have an account?"))
            if st.button(t("Back to Login"), key="login_prompt_button"):
                go_to_login()
        
            


# Profile setup page
def show_profile_setup_page():
    """Display the profile setup page"""
    st.markdown(f"<h2 class='slideIn'>{t('Complete Your Farmer Profile')}</h2>", unsafe_allow_html=True)
    
    # Fetch existing profile data if available
    user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
    profile_data = get_user_profile(user_id) or {}
    
    # Create form for profile setup
    with st.form("profile_form"):
        # Personal information
        st.subheader(t("Personal Information"))
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(t("Full Name"), value=get_profile_field(profile_data, 'name'))
            
        with col2:
            farm_location = st.text_input(t("Farm Location"), 
                                         value=get_profile_field(profile_data, 'farm_location') or 
                                         (st.session_state.current_user.get('farm_location', '') if isinstance(st.session_state.current_user, dict) else getattr(st.session_state.current_user, 'farm_location', '')))
        
        # Farm details
        st.subheader(t("Farm Details"))
        col1, col2, col3 = st.columns(3)
        
        with col1:
            farm_size = st.text_input(t("Farm Size (acres)"), value=get_profile_field(profile_data, 'farm_size'))
            
        with col2:
            farming_type_options = ["Conventional", "Organic", "Mixed", "Transitioning to Organic"]
            farming_type = st.selectbox(
                t("Farming Type"), 
                options=farming_type_options,
                format_func=t,
                index=get_select_index(get_profile_field(profile_data, 'farming_type'), farming_type_options)
            )
            
        with col3:
            irrigation_options = ["Drip", "Sprinkler", "Flood", "Rainwater Only", "Multiple Methods"]
            irrigation = st.selectbox(
                t("Irrigation Method"), 
                options=irrigation_options,
                format_func=t,
                index=get_select_index(get_profile_field(profile_data, 'irrigation'), irrigation_options)
            )

        col1, col2 = st.columns(2)
        with col1:
             water_options = ["Low", "Medium", "High"]
             water_availability = st.selectbox(
                t("Water Availability"),
                options=water_options,
                format_func=t,
                index=get_select_index(get_profile_field(profile_data, 'Water_Availability', "Medium"), water_options)
             )
        with col2:
             income = st.text_input(t("Estimated Annual Income (₹)"), value=get_profile_field(profile_data, 'Income'))
        
        # Crop information
        st.subheader(t("Crops"))
        col1, col2 = st.columns(2)
        
        with col1:
            primary_crops = st.text_input(t("Primary Crops (comma-separated)"), value=get_profile_field(profile_data, 'primary_crops'))
            
        with col2:
            secondary_crops = st.text_input(t("Secondary Crops (comma-separated)"), value=get_profile_field(profile_data, 'secondary_crops'))
        
        # Additional preferences
        st.subheader(t("Preferences"))
        col1, col2 = st.columns(2)
        
        with col1:
            receive_weather_alerts = st.checkbox(t("Receive Weather Alerts"), value=get_profile_field(profile_data, 'receive_weather_alerts', True))
            
        with col2:
            language_options = ["English", "Hindi", "Marathi", "Gujarati", "Bengali"]
            preferred_language = st.selectbox(
                t("Preferred Language"), 
                options=language_options,
                format_func=t,
                index=get_select_index(get_profile_field(profile_data, 'preferred_language', "English"), language_options)
            )
        
        # Submit button
        submitted = st.form_submit_button(t("Save Profile"))
        
        if submitted:
            # Prepare profile data
            profile_data = {
                'name': name,
                'farm_location': farm_location,
                'farm_size': farm_size,
                'farming_type': farming_type,
                'irrigation': irrigation,
                'Water_Availability': water_availability,
                'Income': income,
                'primary_crops': primary_crops,
                'secondary_crops': secondary_crops,
                'receive_weather_alerts': receive_weather_alerts,
                'preferred_language': preferred_language,
                'last_updated': datetime.now().isoformat()
            }
            
            # Update profile
            success, message = update_user_profile(user_id, profile_data)
            
            if success:
                # Update session state with new profile data
                st.session_state.user_profile = profile_data
                
                # Update current_user profile_complete status
                if isinstance(st.session_state.current_user, dict):
                    st.session_state.current_user['profile_complete'] = True
                else:
                    st.session_state.current_user.profile_complete = True
                
                st.success(t("Profile updated successfully!"))
                
                # Redirect to dashboard
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error(f"{t('Error updating profile')}: {message}")
                
    # Back button
    if st.button(t("Skip for Now")):
        go_to_dashboard()

# Dashboard page
def show_dashboard_page():
    """Display the main dashboard page with overview, quick actions, and recent activities"""

    st.markdown(f"<h2 class='slideIn'>{t('Farmer Dashboard')}</h2>", unsafe_allow_html=True)

    # Get user data
    user_id = st.session_state.current_user['id'] if isinstance(
        st.session_state.current_user, dict
    ) else st.session_state.current_user.id

    profile = st.session_state.user_profile or {}

    # ================= OVERVIEW =================
    st.markdown(f"""
    <div style='background-color:#4CAF50; padding:10px; border-radius:5px;'>
        <h3 style='color:white; margin:0;'>{t("Farm Overview")}</h3>
    </div>
    <div class='tab-content'>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # ---------- FARM PROFILE ----------
    with col1:
        st.markdown(f"### 🏡 {t('Farm Profile')}")
        
        # Personal Info
        username = st.session_state.current_user['username'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.username
        st.markdown(f"**{t('Username')}:** {username}")
        st.markdown(f"**{t('Full Name')}:** {get_profile_field(profile,'name','Not set')}")
        
        # Farm Details
        st.markdown(f"**{t('Location')}:** {get_profile_field(profile,'farm_location','Not set')}")
        st.markdown(f"**{t('Size')}:** {get_profile_field(profile,'farm_size','Not set')} {t('acres')}")
        st.markdown(f"**{t('Farming Type')}:** {get_profile_field(profile,'farming_type','Not set')}")
        st.markdown(f"**{t('Irrigation')}:** {get_profile_field(profile,'irrigation','Not set')}")
        st.markdown(f"**{t('Water Availability')}:** {get_profile_field(profile,'Water_Availability','Not set')}")
        st.markdown(f"**{t('Annual Income')}:** ₹{get_profile_field(profile,'Income','Not set')}")
        
        # Crops & Preferences
        st.markdown(f"**{t('Primary Crops')}:** {get_profile_field(profile,'primary_crops','Not set')}")
        st.markdown(f"**{t('Secondary Crops')}:** {get_profile_field(profile,'secondary_crops','Not set')}")
        st.markdown(f"**{t('Language')}:** {get_profile_field(profile,'preferred_language','Not set')}")
        st.markdown(f"**{t('Weather Alerts')}:** {t('Yes') if get_profile_field(profile,'receive_weather_alerts',True) else t('No')}")

        if st.button(t("✏️ Edit Profile"), key="edit_profile_dash"):
            go_to_profile_setup()

    # ---------- SEASON SUMMARY ----------
    with col2:
        st.markdown(f"### 📅 {t('Seasonal Summary')}")

        now = datetime.now()
        month = now.month

        if 3 <= month <= 5:
            season = t("Spring")
            season_color = "#6EDB3E"
            season_icon = "🌱"
            season_tips = t_list([
                "Prepare soil for planting",
                "Start summer crop seedlings",
                "Apply pre-emergent herbicides",
                "Check irrigation systems"
            ])

        elif 6 <= month <= 8:
            season = t("Summer")
            season_color = "#FF9800"
            season_icon = "☀️"
            season_tips = t_list([
                "Monitor for heat stress",
                "Increase irrigation frequency",
                "Apply mulch to retain moisture",
                "Watch for pest outbreaks"
            ])

        elif 9 <= month <= 11:
            season = t("Fall")
            season_color = "#FF5722"
            season_icon = "🍂"
            season_tips = t_list([
                "Harvest mature crops",
                "Plant cover crops",
                "Test and amend soil",
                "Clean and store equipment"
            ])

        else:
            season = t("Winter")
            season_color = "#2196F3"
            season_icon = "❄️"
            season_tips = t_list([
                "Protect sensitive plants",
                "Service farm equipment",
                "Plan next season's crops",
                "Take training courses"
            ])

        st.markdown(f"""
        <div style='background-color:{season_color}; padding:10px; border-radius:5px; color:white; margin-bottom:15px;'>
            <span style='font-size:24px;'>{season_icon}</span>
            <strong>{season} {t("Season")}</strong>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**{t('Seasonal Tips')}:**")
        for tip in season_tips:
            st.markdown(f"- {tip}")

    st.markdown("</div>", unsafe_allow_html=True)

# Crop test page
def show_crop_test_page():
    """Display the crop testing page"""
    st.markdown(f"<h2 class='slideIn'>{t('Plant Health Analysis')}</h2>", unsafe_allow_html=True)
    
    # Create tabs for different ways to add images
    tab_upload, tab_live = st.tabs([t("📁 Upload"), t("📷 Live Capture")])
    
    with tab_upload:
        uploaded_file = st.file_uploader(t("Upload an image of your crop for analysis"), type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Save the uploaded image to session state
            image = Image.open(uploaded_file)
            st.session_state.uploaded_image = image
            st.session_state.image_source = "upload"
            
            # Display the uploaded image
            st.image(image, caption=t("Uploaded Image"), use_container_width=True
)
    


    with tab_live:
        st.markdown(f"### {t('Capture Plant Image Live')}")
        st.warning(t("Camera access is required. Your image will not be stored permanently."))
        
        # Add a toggle for camera visibility
        if 'show_camera' not in st.session_state:
            st.session_state.show_camera = False
        
        if not st.session_state.show_camera:
            if st.button(t("Open Camera"), key="open_camera"):
                st.session_state.show_camera = True
                st.rerun()
        else:
            # Camera widget
            captured_image = st.camera_input(
                t("Position your plant and click capture"),
                key="live_camera",
                help=t("Ensure good lighting and focus on affected areas")
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if captured_image:
                    st.session_state.uploaded_image = Image.open(captured_image)
                    st.session_state.image_capture_method = 'live'
                    st.success(t("Image captured! Scroll down for analysis."))
                    st.session_state.show_camera = False
                    st.rerun()
            
            with col2:
                if st.button(t("Close Camera"), key="close_camera"):
                    st.session_state.show_camera = False
                    st.rerun()
    
    # Form for additional plant details
    if st.session_state.uploaded_image:
        st.markdown(f"### {t('Additional Information (Optional)')}")
        st.markdown(t("Providing more details helps improve analysis accuracy."))
        
        # Create a three-column layout for form inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crop_type = st.selectbox(
                t("Crop Type"),
                options=[t("Unknown"), t("Tomato"), t("Potato"), t("Corn"), t("Wheat"), t("Rice"), t("Onion"), t("Soybean"), t("Cotton"), 
                         t("Cabbage"), t("Watermelon"), t("Pomegranate"), t("Cluster Beans"), t("Grapes"), t("Cucumber"), t("Bitter Gourd"), t("Pumpkin"), t("Bottle Gourd"), t("Cauliflower"), t("Lady Finger")],
                index=0
            )
            
            st.session_state.plant_details["crop_type"] = None if crop_type == t("Unknown") else crop_type
        
        with col2:
            plant_age = st.selectbox(
                t("Plant Age"),
                options=[t("Unknown"), t("Seedling"), t("Vegetative"), t("Flowering"), t("Fruiting"), t("Mature")],
                index=0
            )
            
            st.session_state.plant_details["plant_age"] = None if plant_age == t("Unknown") else plant_age
        
        with col3:
            planting_date = st.date_input(
                t("Planting Date"),
                value=None
            )
            
            st.session_state.plant_details["planting_date"] = planting_date.isoformat() if planting_date else None
        
        col1, col2 = st.columns(2)
        
        with col1:
            symptoms = st.text_area(
                t("Visible Symptoms"),
                placeholder=t("Describe any visible symptoms (e.g., yellow leaves, spots, wilting)")
            )
            
            st.session_state.plant_details["symptoms"] = symptoms if symptoms else None
        
        with col2:
            irrigation_method = st.selectbox(
                t("Irrigation Method"),
                options=[t("Unknown"), t("Drip"), t("Sprinkler"), t("Flood"), t("Rainwater Only"), t("None")],
                index=0
            )
            
            st.session_state.plant_details["irrigation_method"] = None if irrigation_method == t("Unknown") else irrigation_method
            
            previous_treatments = st.text_area(
                t("Previous Treatments"),
                placeholder=t("List any treatments already applied")
            )
            
            st.session_state.plant_details["previous_treatments"] = previous_treatments if previous_treatments else None
        
        # Analyze button
        if st.button(t("Analyze Plant Health"), key="analyze_plant_btn"):
            if st.session_state.uploaded_image:
                with st.spinner(t("Analyzing image... Please wait")):
                    # Preprocess the image
                    image = st.session_state.uploaded_image
                    processed_image = preprocess_image(image)
                    st.session_state.processed_image = processed_image
                    
                    # Perform analysis
                    # Perform analysis using enhanced logic for all cases
                    results = enhanced_analysis(
                        image, 
                        crop_type=st.session_state.plant_details.get("crop_type"),
                        plant_details=st.session_state.plant_details
                    )
                    
                    # Get preventive measures and fertilizer recommendations
                    preventive_measures = get_preventive_measures(
                        results["plant_info"]["name"], 
                        results["diseases"], 
                        results["pests"]
                    )
                    
                    fertilizer_recommendations = get_fertilizer_recommendations(
                        results["plant_info"]["name"]
                    )
                    
                    # Update session state with results
                    st.session_state.analysis_results = results
                    st.session_state.plant_info = results["plant_info"]
                    st.session_state.water_content = results["water_content"]
                    st.session_state.diseases = results["diseases"]
                    st.session_state.pests = results["pests"]
                    st.session_state.crop_details = results.get("crop_details", {})
                    st.session_state.deficiencies = results.get("deficiencies", {})
                    st.session_state.preventive_measures = preventive_measures
                    st.session_state.fertilizer_recommendations = fertilizer_recommendations
                    st.session_state.analysis_complete = True
                    
                    # Save results to history
                    save_to_history("plant", {
                        "plant_info": results["plant_info"],
                        "water_content": results["water_content"],
                        "diseases": results["diseases"],
                        "pests": results["pests"],
                        "preventive_measures": preventive_measures,
                        "fertilizer_recommendations": fertilizer_recommendations,
                        "plant_details": st.session_state.plant_details
                    })
                    

                
                # Force a rerun to show results
                st.rerun()
    
    # Display analysis results
    if st.session_state.analysis_complete and st.session_state.analysis_results:
        st.markdown("---")
        st.markdown(f"<h2 class='fadeIn'>{t('Plant Analysis Results')}</h2>", unsafe_allow_html=True)
        if hasattr(st.session_state, 'image_capture_method') and st.session_state.image_capture_method:
            if st.session_state.image_capture_method == 'live':
                st.markdown(f"*{t('Image source: Live capture')}*")
            elif st.session_state.image_capture_method == 'upload':
                st.markdown(f"*{t('Image source: File upload')}*")
            elif st.session_state.image_capture_method == 'example':
                st.markdown(f"*{t('Image source: Example image')}*")
        
        results = st.session_state.analysis_results
        
        # Side-by-side layout with image and structured report
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Display the processed image
            if st.session_state.processed_image is not None:
                st.image(st.session_state.processed_image, caption=t("Processed Image"), use_container_width=True
)
            else:
                st.image(st.session_state.uploaded_image, caption=t("Uploaded Image"), use_container_width=True
)
            
            # Plant identification result
            st.markdown(f"### {t('Plant Identification')}")
            plant_info = results["plant_info"]
            st.markdown(f"**{t('Detected Plant')}:** {plant_info['name']}")
            if "scientific_name" in plant_info and plant_info["scientific_name"]:
                st.markdown(f"**{t('Scientific Name')}:** {plant_info['scientific_name']}")
            st.markdown(f"**{t('Confidence')}:** {format_probability(plant_info['probability'])}%")
            
            # Water content
            st.markdown(f"### {t('Water Content')}")
            water_content = results["water_content"]
            
            # Use different status classes based on water content
            if water_content["status"] == "Optimal":
                status_class = "status-healthy"
            elif water_content["status"] == "Low":
                status_class = "status-warning"
            elif water_content["status"] == "Critical":
                status_class = "status-danger"
            else:
                status_class = ""
                
            st.markdown(f"**{t('Status')}:** <span class='{status_class}'>{t(water_content['status'])}</span>", unsafe_allow_html=True)
            st.markdown(f"**{t('Estimated Water Content')}:** {water_content['percentage']}%")
            
            # Local recommendations
            if "local_recommendations" in results:
                st.markdown(f"### {t('Maharashtra-Specific Advice')}")
                local_recommendations = results["local_recommendations"]
                
                if local_recommendations:
                    if "seasonal" in local_recommendations:
                        st.markdown(f"**{t('Seasonal Recommendation')}:** {t(local_recommendations['seasonal'])}")
                    
                    if "irrigation" in local_recommendations:
                        st.markdown(f"**{t('Irrigation Advice')}:** {t(local_recommendations['irrigation'])}")
                        
                    if "practices" in local_recommendations:
                        st.markdown(f"**{t('Recommended Practices')}:**")
                        for practice in local_recommendations["practices"]:
                            st.markdown(f"- {t(practice)}")
                else:
                    st.info(t("No region-specific recommendations available for this crop."))
        
        with col2:
            # Create a structured report following the requested format
            st.markdown("<div class='structured-report'>", unsafe_allow_html=True)
            
            # Section 1: General Information of Plant & Water Content
            st.markdown(f"<h3 class='section-general'>1. {t('General Information')}</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
            # Basic plant information
            st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>{t('Identified Plant')}:</strong> {plant_info['name']}</p>", unsafe_allow_html=True)
            if "scientific_name" in plant_info and plant_info["scientific_name"]:
                st.markdown(f"<p><strong>{t('Scientific Name')}:</strong> <em>{plant_info['scientific_name']}</em></p>", unsafe_allow_html=True)
            
            # Water content analysis
            water_content = results["water_content"]
            status = water_content["status"]
            
            # Determine water status class for styling
            if status == "Low":
                water_status_class = "status-warning"
            elif status == "Critical":
                water_status_class = "status-danger"
            elif status == "Optimal":
                water_status_class = "status-healthy"
            else:
                water_status_class = ""
            
            st.markdown(f"<p><strong>{t('Water Content Status')}:</strong> <span class='{water_status_class}'>{t(status)}</span></p>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>{t('Estimated Water Content')}:</strong> {water_content['percentage']}%</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)  # Close analysis-result
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close analysis-section
            
            # Section 2: Disease Detection with preventive measures
            st.markdown(f"<h3 class='section-disease'>2. {t('Disease Detection')}</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
            diseases = results["diseases"]
            
            if diseases["detected"]:
                for disease in diseases["diseases"]:
                    # Create a card-like container for each disease
                    st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                    
                    # Determine status class based on confidence
                    confidence = disease["confidence"]
                    if confidence > 80:
                        status_class = "status-danger"
                    elif confidence > 60:
                        status_class = "status-warning"
                    else:
                        status_class = ""
                    
                    st.markdown(f"<div class='result-header'><div class='result-icon'>🔬</div><h4 class='result-title'>{t(disease['name'])}</h4></div>", unsafe_allow_html=True)
                    st.markdown("<div class='result-content'>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>{t('Confidence')}:</strong> <span class='{status_class}'>{format_probability(confidence)}%</span></p>", unsafe_allow_html=True)
                    
                    if "description" in disease:
                        st.markdown(f"<p><strong>{t('Description')}:</strong> {t(disease['description'])}</p>", unsafe_allow_html=True)
                    
                    if "treatment" in disease:
                        st.markdown(f"<p><strong>{t('Treatment')}:</strong> {t(disease['treatment'])}</p>", unsafe_allow_html=True)
                    
                    # Display detailed database information if available
                    if "detailed_info" in disease:
                        st.markdown("<div class='detailed-info'>", unsafe_allow_html=True)
                        
                        if disease["detailed_info"]["symptoms"]:
                            st.markdown(f"<p><strong>{t('Symptoms')}:</strong> {t(disease['detailed_info']['symptoms'])}</p>", unsafe_allow_html=True)
                        
                        if disease["detailed_info"]["causes"]:
                            st.markdown(f"<p><strong>{t('Causes')}:</strong> {t(disease['detailed_info']['causes'])}</p>", unsafe_allow_html=True)
                        
                        if disease["detailed_info"]["treatment"]:
                            st.markdown(f"<p><strong>{t('Recommended Treatment')}:</strong> {t(disease['detailed_info']['treatment'])}</p>", unsafe_allow_html=True)
                            
                        if disease["detailed_info"]["prevention"]:
                            st.markdown(f"<p><strong>{t('Prevention')}:</strong> {t(disease['detailed_info']['prevention'])}</p>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                st.markdown(f"<p><span class='status-healthy'>{t('No diseases detected.')}</span> {t('The plant appears healthy.')}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)  # Close the disease analysis section
            
            # Section 3: Pest/Insect Detection with treatments
            st.markdown(f"<h3 class='section-pest'>3. {t('Pest/Insect Detection')}</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
            pests = results["pests"]
            
            if pests["detected"]:
                for pest in pests["pests"]:
                    # Create a card-like container for each pest
                    st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                    
                    # Determine status class based on infestation level
                    level = pest["infestation_level"]
                    if level == "High":
                        status_class = "status-danger"
                    elif level == "Medium":
                        status_class = "status-warning"
                    else:
                        status_class = ""
                    
                    st.markdown(f"<div class='result-header'><div class='result-icon'>🐞</div><h4 class='result-title'>{t(pest['name'])}</h4></div>", unsafe_allow_html=True)
                    st.markdown("<div class='result-content'>", unsafe_allow_html=True)
                    st.markdown(f"<p><strong>{t('Infestation Level')}:</strong> <span class='{status_class}'>{t(level)}</span></p>", unsafe_allow_html=True)
                    
                    if "description" in pest:
                        st.markdown(f"<p><strong>{t('Description')}:</strong> {t(pest['description'])}</p>", unsafe_allow_html=True)
                    
                    if "treatment" in pest:
                        st.markdown(f"<p><strong>{t('Treatment')}:</strong> {t(pest['treatment'])}</p>", unsafe_allow_html=True)
                        
                    # Display detailed database information if available
                    if "detailed_info" in pest:
                        st.markdown("<div class='detailed-info'>", unsafe_allow_html=True)
                        
                        if pest["detailed_info"]["symptoms"]:
                            st.markdown(f"<p><strong>{t('Symptoms')}:</strong> {t(pest['detailed_info']['symptoms'])}</p>", unsafe_allow_html=True)
                        
                        if pest["detailed_info"]["description"]:
                            st.markdown(f"<p><strong>{t('About')}:</strong> {t(pest['detailed_info']['description'])}</p>", unsafe_allow_html=True)
                        
                        if pest["detailed_info"]["treatment"]:
                            st.markdown(f"<p><strong>{t('Recommended Treatment')}:</strong> {t(pest['detailed_info']['treatment'])}</p>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                st.markdown(f"<p><span class='status-healthy'>{t('No pests detected.')}</span> {t('The plant appears pest-free.')}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close pest section
            
            # Section 4: Nutrient Deficiency with cures
            st.markdown(f"<h3 class='section-deficiency'>4. {t('Nutrient Deficiency')}</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
            if hasattr(st.session_state, 'deficiencies') and st.session_state.deficiencies:
                deficiencies = st.session_state.deficiencies
                for deficiency_name, deficiency_info in deficiencies.items():
                    st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='result-header'><div class='result-icon'>🧪</div><h4 class='result-title'>{t(deficiency_name)} {t('Deficiency')}</h4></div>", unsafe_allow_html=True)
                    st.markdown("<div class='result-content'>", unsafe_allow_html=True)
                    
                    if "symptoms" in deficiency_info:
                        st.markdown(f"<p><strong>{t('Symptoms')}:</strong> {t(deficiency_info['symptoms'])}</p>", unsafe_allow_html=True)
                    
                    if "treatment" in deficiency_info:
                        st.markdown(f"<p><strong>{t('Cure/Treatment')}:</strong> {t(deficiency_info['treatment'])}</p>", unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                st.markdown(f"<p>{t('No specific nutrient deficiencies identified based on the image analysis.')}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close nutrient deficiency section
            
            # Section 5: Overall Assessment
            st.markdown(f"<h3 class='section-assessment'>5. {t('Overall Assessment')}</h3>", unsafe_allow_html=True)
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            
            # Generate an overall assessment based on all findings
            has_disease = diseases["detected"]
            has_pests = pests["detected"]
            water_status = water_content["status"]
            
            overall_status = t("Healthy")
            overall_class = "status-healthy"
            overall_recommendations = []
            
            if has_disease or has_pests or water_status in ["Low", "Critical"]:
                if has_disease and has_pests:
                    overall_status = t("Critical Attention Needed")
                    overall_class = "status-danger"
                    overall_recommendations.append(t("The plant is showing signs of both disease and pest infestation which require immediate attention."))
                elif has_disease:
                    overall_status = t("Attention Required")
                    overall_class = "status-warning"
                    overall_recommendations.append(t("The plant is showing disease symptoms that need to be addressed promptly."))
                elif has_pests:
                    overall_status = t("Attention Required")
                    overall_class = "status-warning"
                    overall_recommendations.append(t("The plant has pest infestations that need to be controlled."))
                
                if water_status == "Low":
                    overall_recommendations.append(t("The plant needs more water. Increase watering frequency."))
                elif water_status == "Critical":
                    overall_status = t("Critical Attention Needed")
                    overall_class = "status-danger"
                    overall_recommendations.append(t("The plant is severely dehydrated and needs immediate watering."))
            else:
                overall_recommendations.append(t("The plant appears to be in good health with no major issues detected."))
            
            st.markdown("<div class='assessment-box'>", unsafe_allow_html=True)
            st.markdown(f"<p><strong>{t('Overall Plant Status')}:</strong> <span class='{overall_class}'>{overall_status}</span></p>", unsafe_allow_html=True)
            
            st.markdown(f"<p><strong>{t('Assessment Summary')}:</strong></p>", unsafe_allow_html=True)
            for recommendation in overall_recommendations:
                st.markdown(f"<p>• {recommendation}</p>", unsafe_allow_html=True)
            
            # Add crop-specific care advice if available
            if hasattr(st.session_state, 'crop_details') and st.session_state.crop_details:
                crop_details = st.session_state.crop_details
                if "best_season" in crop_details and crop_details["best_season"]:
                    st.markdown(f"<p><strong>{t('Optimal Growing Season')}:</strong> {t(crop_details['best_season'])}</p>", unsafe_allow_html=True)
                
                if "best_soil" in crop_details and crop_details["best_soil"]:
                    st.markdown(f"<p><strong>{t('Ideal Soil Conditions')}:</strong> {t(crop_details['best_soil'])}</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close assessment box
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close analysis section
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close structured report
        
        # Crop Information (if available)
        if hasattr(st.session_state, 'crop_details') and st.session_state.crop_details:
            st.markdown("---")
            st.markdown(f"<h2 class='fadeIn'>{t('Detailed Crop Information')}</h2>", unsafe_allow_html=True)
            
            crop_details = st.session_state.crop_details
            
            # Create expandable sections for detailed information
            with st.expander(t("Crop Details"), expanded=True):
                # Show varieties
                if "varieties" in crop_details and crop_details["varieties"]:
                    st.markdown(f"### {t('Common Varieties')}")
                    varieties_html = '<div class="variety-container">'
                    for variety in crop_details["varieties"]:
                        varieties_html += f'<span class="variety-pill">{t(variety)}</span>'
                    varieties_html += '</div>'
                    st.markdown(varieties_html, unsafe_allow_html=True)
                
                # Show growing information
                if "best_season" in crop_details and crop_details["best_season"]:
                    st.markdown(f"### {t('Best Growing Season')}")
                    st.markdown(f"{t(crop_details['best_season'])}")
                
                if "best_soil" in crop_details and crop_details["best_soil"]:
                    st.markdown(f"### {t('Ideal Soil Type')}")
                    st.markdown(f"{t(crop_details['best_soil'])}")
                
                if "time_period" in crop_details and crop_details["time_period"]:
                    st.markdown(f"### {t('Growth Period')}")
                    st.markdown(f"{t(crop_details['time_period'])}")
            
            # Show nutrient deficiencies if available
            if hasattr(st.session_state, 'deficiencies') and st.session_state.deficiencies:
                with st.expander(t("Common Nutrient Deficiencies"), expanded=True):
                    deficiencies = st.session_state.deficiencies
                    for deficiency_name, deficiency_info in deficiencies.items():
                        st.markdown("<div class='deficiency-card'>", unsafe_allow_html=True)
                        st.markdown(f"<h3>{t(deficiency_name)} {t('Deficiency')}</h3>", unsafe_allow_html=True)
                        
                        if "symptoms" in deficiency_info:
                            st.markdown(f"<p><strong>{t('Symptoms')}:</strong> {t(deficiency_info['symptoms'])}</p>", unsafe_allow_html=True)
                        
                        if "treatment" in deficiency_info:
                            st.markdown(f"<p><strong>{t('Treatment')}:</strong> {t(deficiency_info['treatment'])}</p>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recommendations section
        st.markdown("---")
        st.markdown(f"## {t('Recommendations')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Preventive measures
            st.markdown(f"### {t('Preventive Measures')}")
            if st.session_state.preventive_measures:
                for measure in st.session_state.preventive_measures:
                    st.markdown(f"- {t(measure) if isinstance(measure, str) else measure}")
            else:
                st.info(t("No specific preventive measures available."))
        
        with col2:
            # Fertilizer recommendations
            st.markdown(f"### {t('Fertilizer Recommendations')}")
            if st.session_state.fertilizer_recommendations:
                for recommendation in st.session_state.fertilizer_recommendations:
                    if isinstance(recommendation, dict):
                        # Format dictionary recommendations
                        st.markdown("<div class='fertilizer-rec'>", unsafe_allow_html=True)
                        st.markdown(f"<h4>{t(recommendation.get('name', 'Fertilizer'))}</h4>", unsafe_allow_html=True)
                        if 'npk' in recommendation:
                            st.markdown(f"<p><strong>{t('NPK Ratio')}:</strong> {recommendation['npk']}</p>", unsafe_allow_html=True)
                        if 'description' in recommendation:
                            st.markdown(f"<p>{t(recommendation['description'])}</p>", unsafe_allow_html=True)
                        if 'application' in recommendation:
                            st.markdown(f"<p><strong>{t('Application')}:</strong> {t(recommendation['application'])}</p>", unsafe_allow_html=True)
                        if 'conditions' in recommendation:
                            st.markdown(f"<p><strong>{t('Best For')}:</strong> {t(recommendation['conditions'])}</p>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                    else:
                        # Handle string recommendations
                        st.markdown(f"- {t(recommendation)}")
            else:
                st.info(t("No specific fertilizer recommendations available."))
        
        # Generate report button
        if st.button(t("Generate Detailed Report")):
            report_md = generate_report_markdown(
                plant_info=results["plant_info"],
                water_content=results["water_content"],
                diseases=results["diseases"],
                pests=results["pests"],
                preventive_measures=st.session_state.preventive_measures,
                fertilizer_recommendations=st.session_state.fertilizer_recommendations,
                local_recommendations=results.get("local_recommendations", {}),
                plant_details=st.session_state.plant_details
            )
            
            # Convert markdown to PDF (in a real app) or just display
            st.markdown(f"### {t('Plant Health Report')}")
            st.markdown(report_md)
            
            # In a real app, we'd offer a download link here
            st.download_button(
                label=t("Download Report"),
                data=report_md,
                file_name=f"plant_health_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )

# Soil analysis page
def show_soil_analysis_page():
    """Display the soil analysis page"""
    st.markdown(f"<h2 class='slideIn'>{t('Get Crop Recommendations')}</h2>", unsafe_allow_html=True)
    
    # Initialize session state for farmer inputs if not exists
    if 'farmer_inputs' not in st.session_state:
        st.session_state.farmer_inputs = {}
    
    uploaded_file = st.file_uploader(t("Upload an image of your soil for analysis"), type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Save the uploaded image to session state
        image = Image.open(uploaded_file)
        st.session_state.uploaded_soil_image = image
        
        # Display the uploaded image
        st.image(image, caption=t("Uploaded Soil Image"), use_container_width=True)
    
    # Form for additional soil details and farmer inputs
    if st.session_state.uploaded_soil_image:
        st.markdown(f"### {t('Soil & Farmer Information')}")
        st.markdown(t("Provide details to get personalized crop recommendations."))
        
        # Create tabs for soil details and farmer preferences
        soil_tab, farmer_tab = st.tabs([t("Soil Details"), t("Farmer Preferences")])
        
        with soil_tab:
            # Create a three-column layout for soil form inputs
            col1, col2, col3 = st.columns(3)
            
            with col1:
                soil_depth = st.selectbox(
                    t("Soil Depth"),
                    options=[t("Surface (0-10cm)"), t("Subsurface (10-30cm)"), t("Deep (30cm+)"), t("Unknown")],
                    index=0,
                    key="soil_depth"
                )
            
            with col2:
                recent_rainfall = st.selectbox(
                    t("Recent Rainfall"),
                    options=[t("None"), t("Light"), t("Moderate"), t("Heavy"), t("Unknown")],
                    index=0,
                    key="recent_rainfall"
                )
            
            with col3:
                sampling_location = st.text_input(
                    t("Sampling Location"),
                    placeholder=t("Field name or coordinates"),
                    key="sampling_location"
                )
            
            # Previous crop grown
            previous_crop = st.selectbox(
                t("Previous Crop Grown"),
                options=[t("None"), t("Wheat"), t("Rice"), t("Corn"), t("Soybean"), 
                        t("Cotton"), t("Vegetables"), t("Fruits"), t("Other")],
                index=0,
                key="previous_crop"
            )
            
            # If "Other" is selected, show text input
            if previous_crop == t("Other"):
                previous_crop_other = st.text_input(t("Please specify previous crop"))
                previous_crop = previous_crop_other if previous_crop_other else previous_crop
        
        with farmer_tab:
            st.markdown(f"### {t('Farmer Preferences & Constraints')}")
            
            # Create two columns for farmer inputs
            fcol1, fcol2 = st.columns(2)
            
            with fcol1:
                # Crops interested in (multi-select)
                interested_crops = st.multiselect(
                    t("Crops you're interested in (optional)"),
                    options=[t("Tomato"), t("Potato"), t("Corn"), t("Wheat"), t("Rice"), t("Onion"), 
                             t("Soybean"), t("Cotton"), t("Cabbage"), t("Watermelon"), t("Pomegranate"), 
                             t("Cluster Beans"), t("Grapes"), t("Cucumber"), t("Bitter Gourd"), 
                             t("Pumpkin"), t("Bottle Gourd"), t("Cauliflower"), t("Lady Finger")],
                    default=[],
                    help=t("Select crops you're considering. Leave empty for all suggestions.")
                )
                
                # Budget for cultivation (per acre/hectare)
                budget_amount = st.number_input(
                    t("Budget (in your local currency)"),
                    min_value=0,
                    value=0,
                    step=1000,
                    help=t("Approximate budget you can invest per acre/hectare")
                )
                
                budget_unit = st.radio(
                    t("Budget unit"),
                    options=[t("Per Acre"), t("Per Hectare")],
                    horizontal=True
                )
            
            with fcol2:
                # Attention level/Time commitment
                attention_level = st.select_slider(
                    t("Attention Level/Time Commitment"),
                    options=[
                        t("Very Low (minimal care)"),
                        t("Low (weekly check-ins)"),
                        t("Medium (regular attention)"),
                        t("High (daily care)"),
                        t("Very High (intensive management)")
                    ],
                    value=t("Medium (regular attention)"),
                    help=t("How much time and effort you can dedicate to crop management")
                )
                
                # Risk tolerance
                risk_tolerance = st.select_slider(
                    t("Risk Tolerance"),
                    options=[
                        t("Very Low (can't afford failure)"),
                        t("Low (prefer safe options)"),
                        t("Medium (balanced approach)"),
                        t("High (willing to take chances)"),
                        t("Very High (experimental)")
                    ],
                    value=t("Medium (balanced approach)"),
                    help=t("Your tolerance for crop failure or market volatility")
                )
            
            # Time duration for cultivation
            st.markdown(f"### {t('Time Duration')}")
            duration_col1, duration_col2 = st.columns(2)
            
            with duration_col1:
                duration_value = st.number_input(
                    t("Duration"),
                    min_value=1,
                    value=3,
                    step=1
                )
            
            with duration_col2:
                duration_unit = st.selectbox(
                    t("Unit"),
                    options=[t("Weeks"), t("Months"), t("Seasons")],
                    index=1
                )
            
            # Additional preferences
            st.markdown(f"### {t('Additional Preferences (Optional)')}")
            
            add_col1, add_col2 = st.columns(2)
            
            with add_col1:
                # Organic farming preference
                organic_preference = st.checkbox(
                    t("Prefer organic farming methods"),
                    help=t("If checked, recommendations will prioritize organic-friendly crops")
                )
                
                # Irrigation availability
                irrigation_available = st.radio(
                    t("Irrigation Availability"),
                    options=[t("None - Rainfed only"), t("Limited"), t("Good"), t("Excellent")],
                    index=1
                )
            
            with add_col2:
                # Market preference
                market_preference = st.selectbox(
                    t("Market Preference"),
                    options=[t("Local market"), t("Distant market"), t("Export quality"), t("No preference")],
                    index=3
                )
                
                labor_availability = st.select_slider(
                    t("Labor Availability"),
                    options=[t("Very Limited"), t("Limited"), t("Adequate"), t("Abundant")],
                    value=t("Adequate")
                )
                
        
        # Save all inputs to session state
        st.session_state.farmer_inputs = {
            "soil_depth": soil_depth,
            "recent_rainfall": recent_rainfall,
            "sampling_location": sampling_location,
            "previous_crop": previous_crop,
            "interested_crops": interested_crops,
            "budget": {
                "amount": budget_amount,
                "unit": budget_unit
            },
            "attention_level": attention_level,
            "risk_tolerance": risk_tolerance,
            "time_duration": {
                "value": duration_value,
                "unit": duration_unit
            },
            "organic_preference": organic_preference if 'organic_preference' in locals() else False,
            "irrigation_available": irrigation_available if 'irrigation_available' in locals() else t("Limited"),
            "market_preference": market_preference if 'market_preference' in locals() else t("No preference"),
            "labor_availability": labor_availability if 'labor_availability' in locals() else t("Adequate"),
            "weather_api_key": weather_api_key_input if 'weather_api_key_input' in locals() else None
        }
        
        # Analyze button
        if st.button(t("Analyze Soil & Get Recommendations"), key="analyze_soil_btn"):
            if st.session_state.uploaded_soil_image:
                with st.spinner(t("Analyzing soil and generating recommendations... Please wait")):
                    try:
                        # Preprocess the image
                        image = st.session_state.uploaded_soil_image
                        preprocessed_soil_image = preprocess_image(image)
                        
                        # Get soil analysis results
                        soil_results = analyze_soil(None, np.array(preprocessed_soil_image))
                        
                        # Ensure results are in proper dictionary format
                        if isinstance(soil_results, str):
                            # If it's just a string (soil type), convert to full structure
                            soil_results = {
                                "soil_type": soil_results,
                                "properties": {
                                    "ph": t("Unknown"),
                                    "organic_matter": t("Unknown"),
                                    "drainage": t("Unknown"),
                                    "nitrogen": t("Unknown"),
                                    "phosphorus": t("Unknown"),
                                    "potassium": t("Unknown")
                                },
                                "characteristics": t("Basic analysis completed"),
                                "suitability": {},
                                "recommendations": t("Consult local agricultural expert for specific advice")
                            }
                        elif not isinstance(soil_results, dict):
                            # Fallback for unexpected formats
                            soil_results = {
                                "soil_type": t("Unknown"),
                                "properties": {
                                    "ph": t("Unknown"),
                                    "organic_matter": t("Unknown"),
                                    "drainage": t("Unknown"),
                                    "nitrogen": t("Unknown"),
                                    "phosphorus": t("Unknown"),
                                    "potassium": t("Unknown")
                                },
                                "characteristics": t("Analysis completed"),
                                "suitability": {},
                                "recommendations": t("Results format unexpected")
                            }
                        
                        # Add NPK values if not present
                        if "nitrogen" not in soil_results["properties"]:
                            soil_results["properties"]["nitrogen"] = t("Medium")
                        if "phosphorus" not in soil_results["properties"]:
                            soil_results["properties"]["phosphorus"] = t("Medium")
                        if "potassium" not in soil_results["properties"]:
                            soil_results["properties"]["potassium"] = t("Medium")
                        
                        # Update session state
                        st.session_state.soil_results = soil_results
                        st.session_state.soil_analysis_complete = True
                        
                        # Reset saved flag
                        st.session_state.soil_analysis_saved = False
                        
                        # Show success message
                        st.success(t("Analysis complete! Scroll down to see your personalized recommendations."))
                    
                    except Exception as e:
                        st.error(f"{t('Error during soil analysis')}: {str(e)}")
                        st.session_state.soil_analysis_complete = False
                
                st.rerun()
    
    # Display soil analysis results and recommendations
    if st.session_state.soil_analysis_complete and st.session_state.soil_results:
        st.markdown("---")
        st.markdown(f"<h2 class='fadeIn'>{t('Soil Analysis & Crop Recommendations')}</h2>", unsafe_allow_html=True)
        
        soil_results = st.session_state.soil_results
        farmer_inputs = st.session_state.farmer_inputs
        
        # Create columns for results display
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display the soil image
            if st.session_state.uploaded_soil_image is not None:
                st.image(st.session_state.uploaded_soil_image, caption=t("Soil Sample"), use_container_width=True)
            
            # Soil type and characteristics
            st.markdown(f"### {t('Soil Classification')}")
            
            # Get soil type safely
            soil_type = soil_results.get("soil_type") if isinstance(soil_results, dict) else str(soil_results)
            st.markdown(f"**{t('Identified Soil Type')}:** {t(soil_type) if isinstance(soil_type, str) else soil_type}")
            
            # Display soil properties
            st.markdown(f"### {t('Soil Properties')}")
            
            properties = soil_results.get("properties", {}) if isinstance(soil_results, dict) else {
                "ph": t("Unknown"),
                "organic_matter": t("Unknown"),
                "drainage": t("Unknown"),
                "nitrogen": t("Unknown"),
                "phosphorus": t("Unknown"),
                "potassium": t("Unknown")
            }
            
            # Create a two-column layout for properties
            prop_col1, prop_col2 = st.columns(2)
            
            with prop_col1:
                st.markdown(f"**{t('pH Value')}:** {t(properties.get('ph', 'Unknown')) if isinstance(properties.get('ph'), str) else properties.get('ph', 'Unknown')}")
                st.markdown(f"**{t('Organic Matter')}:** {t(properties.get('organic_matter', 'Unknown')) if isinstance(properties.get('organic_matter'), str) else properties.get('organic_matter', 'Unknown')}")
                st.markdown(f"**{t('Nitrogen (N)')}:** {t(properties.get('nitrogen', 'Unknown')) if isinstance(properties.get('nitrogen'), str) else properties.get('nitrogen', 'Unknown')}")
            
            with prop_col2:
                st.markdown(f"**{t('Drainage')}:** {t(properties.get('drainage', 'Unknown')) if isinstance(properties.get('drainage'), str) else properties.get('drainage', 'Unknown')}")
                st.markdown(f"**{t('Phosphorus (P)')}:** {t(properties.get('phosphorus', 'Unknown')) if isinstance(properties.get('phosphorus'), str) else properties.get('phosphorus', 'Unknown')}")
                st.markdown(f"**{t('Potassium (K)')}:** {t(properties.get('potassium', 'Unknown')) if isinstance(properties.get('potassium'), str) else properties.get('potassium', 'Unknown')}")
        
        with col2:
            # Farmer inputs summary
            st.markdown(f"### {t('Your Preferences Summary')}")
            
            # Create a summary card
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
                <p><strong>{t('Previous Crop')}:</strong> {farmer_inputs['previous_crop']}</p>
                <p><strong>{t('Budget')}:</strong> {farmer_inputs['budget']['amount']} {farmer_inputs['budget']['unit']}</p>
                <p><strong>{t('Attention Level')}:</strong> {farmer_inputs['attention_level']}</p>
                <p><strong>{t('Risk Tolerance')}:</strong> {farmer_inputs['risk_tolerance']}</p>
                <p><strong>{t('Time Duration')}:</strong> {farmer_inputs['time_duration']['value']} {farmer_inputs['time_duration']['unit']}</p>
                <p><strong>{t('Irrigation')}:</strong> {farmer_inputs['irrigation_available']}</p>
                <p><strong>{t('Interested Crops')}:</strong> {', '.join(farmer_inputs['interested_crops']) if farmer_inputs['interested_crops'] else t('All suitable crops')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Soil characteristics
            st.markdown(f"### {t('Soil Characteristics')}")
            
            if isinstance(soil_results, dict):
                characteristics = soil_results.get("characteristics", t("Information not available."))
            else:
                characteristics = t("Basic analysis completed. Detailed characteristics not available.")
            
            st.markdown(t(characteristics) if isinstance(characteristics, str) else characteristics)
        
        # Generate recommendations based on all inputs
        st.markdown("---")
        st.markdown(f"## {t('🌱 Personalized Crop Recommendations')}")
        
        # This is where we'll integrate with weather API and crop data
        # Get recommendations and other data
        recommendations, weather_data, market_data = generate_crop_recommendations(soil_results, farmer_inputs)
        
        # Save complete results to history if not already saved
        if not st.session_state.soil_analysis_saved:
            full_results = {
                **soil_results,
                "farmer_inputs": farmer_inputs,
                "recommendations": recommendations[:5] if recommendations else [],  # Save top 5
                "weather_data": weather_data,
                "market_data": market_data
            }
            save_to_history("soil", full_results)
            st.session_state.soil_analysis_saved = True
            

        
        # Visualize soil properties
        st.markdown("---")
        st.markdown(f"## {t('Soil Analysis Visualization')}")
        
        # Create a simple visualization of soil properties
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Parse pH value safely
        try:
            ph_str = str(properties.get('ph', '7.0'))
            # Extract numeric part if it contains text
            import re
            ph_match = re.search(r'(\d+\.?\d*)', ph_str)
            ph_value = float(ph_match.group(1)) if ph_match else 7.0
        except (ValueError, AttributeError):
            ph_value = 7.0
        
        # Create pH scale visualization
        ph_range = np.linspace(4, 10, 100)
        colors = []
        
        for ph in ph_range:
            if ph < 5.5:  # Acidic
                colors.append('#FF6B6B')  # Red
            elif ph < 6.5:  # Slightly acidic
                colors.append('#FFD166')  # Yellow
            elif ph < 7.5:  # Neutral
                colors.append('#06D6A0')  # Green
            elif ph < 8.5:  # Slightly alkaline
                colors.append('#118AB2')  # Blue
            else:  # Alkaline
                colors.append('#073B4C')  # Dark blue
        
        # Plot the pH scale
        ax.scatter(ph_range, [1] * len(ph_range), c=colors, s=100, marker='|')
        ax.scatter(ph_value, 1, c='red', s=300, marker='v', zorder=5)
        
        # Add labels
        ax.text(4.5, 1.05, t("Acidic"), fontsize=10, ha='center')
        ax.text(6.0, 1.05, t("Slightly Acidic"), fontsize=10, ha='center')
        ax.text(7.0, 1.05, t("Neutral"), fontsize=10, ha='center')
        ax.text(8.0, 1.05, t("Slightly Alkaline"), fontsize=10, ha='center')
        ax.text(9.5, 1.05, t("Alkaline"), fontsize=10, ha='center')
        
        # Customize the plot
        ax.set_xlim(4, 10)
        ax.set_ylim(0.9, 1.1)
        ax.set_xlabel(t('pH Scale'))
        ax.set_title(f"{t('Soil pH Analysis')}: {ph_value:.1f} ({t(properties.get('ph', 'Unknown')) if isinstance(properties.get('ph'), str) else properties.get('ph', 'Unknown')})")
        ax.get_yaxis().set_visible(False)
        
        # Show the plot
        st.pyplot(fig)
        
        # NPK visualization
        st.markdown(f"### {t('NPK Levels Visualization')}")
        
        # Create a horizontal bar chart for NPK levels
        fig_npk, ax_npk = plt.subplots(figsize=(10, 4))
        
        nutrients = ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)']
        
        # Map qualitative levels to numeric values for plotting
        level_map = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Very High': 5}
        level_colors = {'Very Low': '#FF6B6B', 'Low': '#FFD166', 'Medium': '#06D6A0', 'High': '#118AB2', 'Very High': '#073B4C'}
        
        values = []
        colors = []
        labels = []
        
        for nutrient_key, display_name in zip(['nitrogen', 'phosphorus', 'potassium'], nutrients):
            val_str = properties.get(nutrient_key, 'Medium')
            # Handle if value is a string needing translation or raw
            val_display = t(val_str) if isinstance(val_str, str) else str(val_str)
            
            numeric_val = level_map.get(val_str, 3) # Default to Medium if unknown
            values.append(numeric_val)
            colors.append(level_colors.get(val_str, '#06D6A0'))
            labels.append(f"{val_display}")

        # Create bars
        y_pos = np.arange(len(nutrients))
        bars = ax_npk.barh(y_pos, values, color=colors, height=0.5)
        
        # Customize the chart
        ax_npk.set_yticks(y_pos)
        ax_npk.set_yticklabels(nutrients, fontsize=12)
        ax_npk.set_xlim(0, 5.5)
        ax_npk.set_xticks([1, 2, 3, 4, 5])
        ax_npk.set_xticklabels([t('Very Low'), t('Low'), t('Medium'), t('High'), t('Very High')])
        ax_npk.set_xlabel(t('Level'))
        
        # Add value labels on/next to bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax_npk.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                        labels[i], 
                        ha='left', va='center', fontweight='bold')
            
        # Remove spines
        for spine in ['top', 'right']:
            ax_npk.spines[spine].set_visible(False)
            
        plt.tight_layout()
        st.pyplot(fig_npk)
            

        
        # Generate report button
        if st.button(t("Generate Detailed Soil & Recommendations Report")):
            generate_detailed_report(soil_results, farmer_inputs)


def generate_detailed_report(soil_results, farmer_inputs):
    """Generate a detailed report with all analysis and recommendations"""
    from datetime import datetime
    
    report_md = f"""
    # {t('Comprehensive Soil Analysis & Crop Recommendation Report')}
    
    ## {t('Report Information')}
    - **{t('Date')}:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
    - **{t('Report ID')}:** SOIL-{datetime.now().strftime('%Y%m%d%H%M%S')}
    
    ## {t('Soil Analysis Results')}
    
    ### {t('Soil Classification')}
    - **{t('Soil Type')}:** {soil_results.get('soil_type', 'Unknown')}
    
    ### {t('Soil Properties')}
    - **{t('pH Value')}:** {soil_results.get('properties', {}).get('ph', 'Unknown')}
    - **{t('Organic Matter')}:** {soil_results.get('properties', {}).get('organic_matter', 'Unknown')}
    - **{t('Nitrogen (N)')}:** {soil_results.get('properties', {}).get('nitrogen', 'Unknown')}
    - **{t('Phosphorus (P)')}:** {soil_results.get('properties', {}).get('phosphorus', 'Unknown')}
    - **{t('Potassium (K)')}:** {soil_results.get('properties', {}).get('potassium', 'Unknown')}
    - **{t('Drainage')}:** {soil_results.get('properties', {}).get('drainage', 'Unknown')}
    
    ### {t('Soil Characteristics')}
    {soil_results.get('characteristics', 'Information not available.')}
    
    ## {t('Farmer Input Summary')}
    - **{t('Previous Crop')}:** {farmer_inputs.get('previous_crop', 'Not specified')}
    - **{t('Budget')}:** {farmer_inputs.get('budget', {}).get('amount', 0)} {farmer_inputs.get('budget', {}).get('unit', '')}
    - **{t('Attention Level')}:** {farmer_inputs.get('attention_level', 'Not specified')}
    - **{t('Risk Tolerance')}:** {farmer_inputs.get('risk_tolerance', 'Not specified')}
    - **{t('Time Duration')}:** {farmer_inputs.get('time_duration', {}).get('value', '')} {farmer_inputs.get('time_duration', {}).get('unit', '')}
    - **{t('Irrigation Availability')}:** {farmer_inputs.get('irrigation_available', 'Not specified')}
    - **{t('Organic Preference')}:** {'Yes' if farmer_inputs.get('organic_preference') else 'No'}
    
    ## {t('Recommendations')}
    {soil_results.get('recommendations', 'No specific recommendations available.')}
    
    ## {t('Next Steps')}
    1. **{t('Soil Preparation')}:** Based on the analysis, prepare your soil with appropriate amendments
    2. **{t('Crop Selection')}:** Choose from the recommended crops above
    3. **{t('Weather Monitoring')}:** Check local weather forecasts before planting
    4. **{t('Market Research')}:** Verify current market prices for your chosen crops
    5. **{t('Consult Local Experts')}:** Discuss these recommendations with local agricultural extension officers
    
    ---
    *{t('This report is generated by AI and should be used as a guideline. Always consult with local agricultural experts for final decisions.')}*
    """
    
    st.markdown(f"### {t('Detailed Report')}")
    st.markdown(report_md)
    
    # Offer report download
    st.download_button(
        label=t("Download Complete Report"),
        data=report_md,
        file_name=f"soil_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        mime="text/markdown"
    )

# History page
def show_history_page():
    """Display the user's analysis history"""
    st.markdown(f"<h2 class='slideIn'>{t('Analysis History')}</h2>", unsafe_allow_html=True)
    
    # Get user ID
    user_id = st.session_state.current_user['id'] if isinstance(st.session_state.current_user, dict) else st.session_state.current_user.id
    
    # Get user's analysis history
    history = get_user_analyses(user_id, limit=50)  # Get up to 50 analyses
    
    if not history:
        st.info(t("No analysis history found. Start by analyzing your crops or soil!"))
        return
    
    # Create filter options
    st.markdown(f"### {t('Filter Results')}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Use raw strings for options to allow correct filtering, translate via format_func
        analysis_types = ["All Types"] + list(set(a["analysis_type"] for a in history))
        selected_type = st.selectbox(t("Analysis Type"), options=analysis_types, format_func=t)
    
    with col2:
        # Extract all dates (YYYY-MM-DD) from timestamps
        dates = ["All Dates"] + sorted(list(set(a["timestamp"][:10] for a in history)), reverse=True)
        selected_date = st.selectbox(t("Date"), options=dates, format_func=t)
    
    with col3:
        # For plant analyses, get list of plants
        plant_types = ["All Plants"]
        for a in history:
            if a["analysis_type"] == "plant" and "results" in a and "plant_info" in a["results"]:
                plant_name = a["results"]["plant_info"].get("name", "Unknown")
                if plant_name not in plant_types and plant_name != "Unknown":
                    plant_types.append(plant_name)
        
        # Translate plant names in dropdown
        selected_plant = st.selectbox(t("Plant Type"), options=plant_types, format_func=t)
    
    # Filter history based on selections
    filtered_history = history
    
    if selected_type != "All Types":
        filtered_history = [a for a in filtered_history if a["analysis_type"] == selected_type]
    
    if selected_date != "All Dates":
        filtered_history = [a for a in filtered_history if a["timestamp"][:10] == selected_date]
    
    if selected_plant != "All Plants":
        filtered_history = [a for a in filtered_history if a["analysis_type"] == "plant" and 
                          "results" in a and 
                          "plant_info" in a["results"] and 
                          a["results"]["plant_info"].get("name") == selected_plant]
    
    # Display filtered history
    st.markdown(f"### {t('Results')} ({len(filtered_history)} {t('analyses')})")
    
    if not filtered_history:
        st.info(t("No analyses match your filter criteria."))
        return
    
    # Check if we need to show details for a specific analysis
    if "selected_analysis_id" in st.session_state:
        selected_analysis = next((a for a in filtered_history if a["id"] == st.session_state.selected_analysis_id), None)
        if selected_analysis:
            show_analysis_details(selected_analysis)
            if st.button(t("Back to History")):
                del st.session_state.selected_analysis_id
                st.rerun()
            return
    
    # Create tabs for different view types
    tab1, tab2 = st.columns(2)  # Changed from tabs to columns for better layout
    
    with tab1:
        # Simple list view
        st.markdown(f"#### {t('Analysis List')}")
        for i, analysis in enumerate(filtered_history):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    if analysis["analysis_type"] == "plant":
                        icon = "🌱"
                        title = t("Plant Health Analysis")
                        if "results" in analysis and "plant_info" in analysis["results"]:
                            plant_name = analysis['results']['plant_info'].get('name', 'Unknown')
                            subtitle = f"{t('Plant')}: {t(plant_name)}"
                        else:
                            subtitle = t("Plant analysis")
                    elif analysis["analysis_type"] == "soil":
                        icon = "🌍"
                        title = t("Soil Analysis")
                        if "results" in analysis and "soil_type" in analysis["results"]:
                            soil_type = analysis['results']['soil_type']
                            subtitle = f"{t('Soil')}: {t(soil_type) if isinstance(soil_type, str) else soil_type}"
                        else:
                            subtitle = t("Soil analysis")
                    else:
                        icon = "📋"
                        # Translate the analysis type name
                        title = f"{t(analysis['analysis_type'].title())} {t('Analysis')}"
                        subtitle = ""
                    
                    st.markdown(f"**{i+1}. {icon} {title}** - {analysis['timestamp'][:10]}")
                    st.markdown(f"{subtitle}")
                
                with col2:
                    if st.button(t("View Details"), key=f"view_details_{analysis['id']}"):
                        st.session_state.selected_analysis_id = analysis["id"]
                        st.rerun()
                
                st.markdown("---")

def show_analysis_details(analysis):
    """Display detailed view of a single analysis"""
    st.markdown(f"## {t('Detailed Analysis')} - {analysis['timestamp'][:10]}")
    
    # Display analysis details based on type
    if analysis["analysis_type"] == "plant":
        st.markdown(f"### 🌱 {t('Plant Health Analysis')}")
        
        # Get results
        results = analysis.get("results", {})
        plant_info = results.get("plant_info", {})
        diseases = results.get("diseases", {})
        pests = results.get("pests", {})
        water_content = results.get("water_content", {})
        preventive_measures = results.get("preventive_measures", [])
        fertilizer_recommendations = results.get("fertilizer_recommendations", [])
        
        # Display image if available
        if "image_path" in analysis and analysis["image_path"]:
            try:
                image = Image.open(analysis["image_path"])
                st.image(image, caption=t("Plant Image"), width=300)
            except Exception as e:
                st.error(f"{t('Could not load image')}: {e}")
        
        # Create columns for information display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {t('Plant Information')}")
            st.markdown(f"**{t('Plant')}:** {plant_info.get('name', t('Unknown'))}")
            if "scientific_name" in plant_info and plant_info["scientific_name"]:
                st.markdown(f"**{t('Scientific Name')}:** {plant_info['scientific_name']}")
            st.markdown(f"**{t('Confidence')}:** {format_probability(plant_info.get('probability', 0))}%")
            
            st.markdown(f"### {t('Water Content')}")
            st.markdown(f"**{t('Status')}:** {t(water_content.get('status', 'Unknown'))}")
            st.markdown(f"**{t('Percentage')}:** {water_content.get('percentage', t('Unknown'))}%")
        
        with col2:
            st.markdown(f"### {t('Disease & Pest Information')}")
            
            if diseases.get("detected", False):
                st.markdown(f"**{t('Diseases Detected')}:** {t('Yes')}")
                for disease in diseases.get("diseases", []):
                    st.markdown(f"- {t(disease.get('name', 'Unknown'))} ({format_probability(disease.get('confidence', 0))}%)")
                    if "treatment" in disease:
                        st.markdown(f"  - {t('Treatment')}: {t(disease['treatment'])}")
            else:
                st.markdown(f"**{t('Diseases Detected')}:** {t('No')}")
            
            if pests.get("detected", False):
                st.markdown(f"**{t('Pests Detected')}:** {t('Yes')}")
                for pest in pests.get("pests", []):
                    st.markdown(f"- {t(pest.get('name', 'Unknown'))} ({t('Level')}: {t(pest.get('infestation_level', 'Unknown'))})")
                    if "treatment" in pest:
                        st.markdown(f"  - {t('Treatment')}: {t(pest['treatment'])}")
            else:
                st.markdown(f"**{t('Pests Detected')}:** {t('No')}")
        
        # Recommendations
        st.markdown(f"### {t('Recommendations')}")
        
        if preventive_measures:
            st.markdown(f"**{t('Preventive Measures')}:**")
            for measure in preventive_measures:
                st.markdown(f"- {t(measure) if isinstance(measure, str) else measure}")
        
        if fertilizer_recommendations:
            st.markdown(f"### {t('Fertilizer Recommendations')}")
            
            # Create tabs for different fertilizer types if they exist
            fertilizer_types = set()
            for rec in fertilizer_recommendations:
                if isinstance(rec, dict) and 'type' in rec:
                    fertilizer_types.add(rec['type'].title())
            
            if fertilizer_types:
                tabs = st.tabs([f"{t(ftype)}" for ftype in sorted(fertilizer_types)] + [t("All")])
            else:
                tabs = [st.container()]
            
            # Organize recommendations by type
            typed_recommendations = {}
            for rec in fertilizer_recommendations:
                if isinstance(rec, dict):
                    ftype = rec.get('type', 'other').title()
                    if ftype not in typed_recommendations:
                        typed_recommendations[ftype] = []
                    typed_recommendations[ftype].append(rec)
                else:
                    if 'other' not in typed_recommendations:
                        typed_recommendations['other'] = []
                    typed_recommendations['other'].append(rec)
            
            # Display in tabs
            for i, (ftype, tab) in enumerate(zip(sorted(typed_recommendations.keys()), tabs)):
                with tab:
                    for rec in typed_recommendations[ftype]:
                        if isinstance(rec, dict):
                            with st.expander(f"🔹 {t(rec.get('name', 'Fertilizer'))}"):
                                # Create a nice card-like display
                                col1, col2 = st.columns([1, 3])
                                
                                with col1:
                                    # Display NPK ratio with colored badges
                                    if 'npk' in rec:
                                        npk = rec['npk'].split('-')
                                        if len(npk) == 3:
                                            st.markdown("""
                                            <style>
                                                .npk-badge {
                                                    display: inline-block;
                                                    padding: 2px 8px;
                                                    border-radius: 12px;
                                                    font-weight: bold;
                                                    font-size: 0.8em;
                                                    margin: 2px;
                                                }
                                                .npk-N { background-color: #4CAF50; color: white; }
                                                .npk-P { background-color: #2196F3; color: white; }
                                                .npk-K { background-color: #FF9800; color: black; }
                                            </style>
                                            """, unsafe_allow_html=True)
                                            
                                            st.markdown(f"""
                                            <div style="margin-bottom: 10px;">
                                                <span class="npk-badge npk-N">{t('N')}: {npk[0]}</span>
                                                <span class="npk-badge npk-P">{t('P')}: {npk[1]}</span>
                                                <span class="npk-badge npk-K">{t('K')}: {npk[2]}</span>
                                            </div>
                                            """, unsafe_allow_html=True)
                                
                                with col2:
                                    st.markdown(f"**{t('Type')}:** {t(rec.get('type', 'N/A')).title()}")
                                    
                                    if 'description' in rec:
                                        st.markdown(f"**{t('Description')}:** {t(rec['description'])}")
                                    
                                    if 'application' in rec:
                                        st.markdown(f"**{t('Application')}:** {t(rec['application'])}")
                                    
                                    if 'conditions' in rec:
                                        st.markdown(f"**{t('Best For')}:** {t(rec['conditions'])}")
                                    
                                    if 'scientific_backing' in rec:
                                        st.markdown(f"*{t('Scientific Backing')}:* {t(rec['scientific_backing'])}", unsafe_allow_html=True)
                        else:
                            st.markdown(f"- {t(rec)}")
            
            # If there's only one type, don't show tabs
            if len(fertilizer_types) <= 1:
                tabs[0].empty()  # Clear the single tab
                for rec in fertilizer_recommendations:
                    if isinstance(rec, dict):
                        with st.expander(f"🔹 {t(rec.get('name', 'Fertilizer'))}"):
                            # Same card display as above
                            col1, col2 = st.columns([1, 3])
                            
                            with col1:
                                if 'npk' in rec:
                                    npk = rec['npk'].split('-')
                                    if len(npk) == 3:
                                        st.markdown(f"""
                                        <div style="margin-bottom: 10px;">
                                            <span class="npk-badge npk-N">{t('N')}: {npk[0]}</span>
                                            <span class="npk-badge npk-P">{t('P')}: {npk[1]}</span>
                                            <span class="npk-badge npk-K">{t('K')}: {npk[2]}</span>
                                        </div>
                                        """, unsafe_allow_html=True)
                            
                            with col2:
                                st.markdown(f"**{t('Type')}:** {t(rec.get('type', 'N/A')).title()}")
                                
                                if 'description' in rec:
                                    st.markdown(f"**{t('Description')}:** {t(rec['description'])}")
                                
                                if 'application' in rec:
                                    st.markdown(f"**{t('Application')}:** {t(rec['application'])}")
                                
                                if 'conditions' in rec:
                                    st.markdown(f"**{t('Best For')}:** {t(rec['conditions'])}")
                                
                                if 'scientific_backing' in rec:
                                    st.markdown(f"*{t('Scientific Backing')}:* {t(rec['scientific_backing'])}", unsafe_allow_html=True)
                    else:
                        st.markdown(f"- {t(rec)}")
    
    elif analysis["analysis_type"] == "soil":
        st.markdown(f"### 🌍 {t('Soil Analysis & Crop Recommendations')}")
        
        results = analysis.get("results", {})
        
        # Display simplified view of results if available
        if "recommendations" in results:
            recommendations = results["recommendations"]
            st.markdown(f"#### {t('Top Recommended Crops')}")
            for i, crop in enumerate(recommendations):
                with st.expander(f"#{i+1} {crop['name']} - Score: {crop['score']}%"):
                    # Display saved reasons
                    if "reasons" in crop:
                        st.markdown(f"**{t('Why this matches')}:**")
                        for reason in crop["reasons"]:
                            st.markdown(f"- {reason}")
                    
                    if "warnings" in crop:
                        st.markdown(f"**{t('Considerations')}:**")
                        for warning in crop["warnings"]:
                            st.markdown(f"- {warning}")
                    
                    if "price_prediction" in crop and crop["price_prediction"]:
                        pred = crop["price_prediction"]
                        st.markdown(f"**{t('Price Forecast')}:** ₹{pred['predicted_price']} ({pred['trend']})")
        
        # Display weather summary if available
        if "weather_data" in results:
             w = results["weather_data"]
             st.markdown(f"#### {t('Weather Context')}")
             st.info(w.get("summary", t("No summary available")))

    # Generate report button
    if st.button(t("Generate Report")):
        if analysis["analysis_type"] == "plant":
            report_md = generate_report_markdown(
                plant_info=analysis.get("results", {}).get("plant_info", {}),
                water_content=analysis.get("results", {}).get("water_content", {}),
                diseases=analysis.get("results", {}).get("diseases", {}),
                pests=analysis.get("results", {}).get("pests", {}),
                preventive_measures=analysis.get("results", {}).get("preventive_measures", []),
                fertilizer_recommendations=analysis.get("results", {}).get("fertilizer_recommendations", []),
                local_recommendations=analysis.get("results", {}).get("local_recommendations", {}),
                plant_details=analysis.get("results", {}).get("plant_details", {})
            )
            
            st.download_button(
                label=t("Download Plant Report"),
                data=report_md,
                file_name=f"plant_report_{analysis['timestamp'][:10]}.md",
                mime="text/markdown"
            )
        elif analysis["analysis_type"] == "soil":
            # Create soil report
            soil_results = analysis.get("results", {})
            soil_type = soil_results.get("soil_type", t("Unknown"))
            
            report_md = f"""
            # {t('Soil Analysis Report')}
            
            ## {t('Analysis Date')}: {analysis['timestamp'][:10]}
            
            ## {t('Soil Classification')}
            - **{t('Identified Soil Type')}:** {t(soil_type) if isinstance(soil_type, str) else soil_type}
            
            ## {t('Soil Properties')}
            """
            
            if "properties" in soil_results:
                properties = soil_results["properties"]
                report_md += f"- **{t('pH Value')}:** {t(properties.get('ph', 'Unknown')) if isinstance(properties.get('ph'), str) else properties.get('ph', 'Unknown')}\n"
                report_md += f"- **{t('Organic Matter')}:** {t(properties.get('organic_matter', 'Unknown')) if isinstance(properties.get('organic_matter'), str) else properties.get('organic_matter', 'Unknown')}\n"
                report_md += f"- **{t('Drainage')}:** {t(properties.get('drainage', 'Unknown')) if isinstance(properties.get('drainage'), str) else properties.get('drainage', 'Unknown')}\n"
            
            if "characteristics" in soil_results:
                report_md += f"\n## {t('Characteristics')}\n{t(soil_results['characteristics']) if isinstance(soil_results['characteristics'], str) else soil_results['characteristics']}\n"
            
            if "suitability" in soil_results:
                report_md += f"\n## {t('Crop Suitability')}\n"
                for crop, suitability in soil_results["suitability"].items():
                    report_md += f"- **{t(crop.title())}:** {t(suitability) if isinstance(suitability, str) else suitability}\n"
            
            if "recommendations" in soil_results:
                if isinstance(soil_results["recommendations"], list) and len(soil_results["recommendations"]) > 0 and isinstance(soil_results["recommendations"][0], dict):
                     # New format with detailed crop recommendations
                     report_md += f"\n## {t('Detailed Crop Recommendations')}\n"
                     for i, crop in enumerate(soil_results["recommendations"]):
                         report_md += f"### {i+1}. {crop['name']} (Score: {crop['score']}%)\n"
                         if "reasons" in crop:
                             report_md += "#### Matches because:\n" + "\n".join([f"- {r}" for r in crop["reasons"]]) + "\n"
                         
                         if "price_prediction" in crop and crop["price_prediction"]:
                             pred = crop["price_prediction"]
                             report_md += f"**Price Outlook:** {pred['predicted_price']} ({pred['trend']})\n"
                else:
                    # Legacy format
                    report_md += f"\n## {t('Recommendations')}\n{t(soil_results['recommendations']) if isinstance(soil_results['recommendations'], str) else soil_results['recommendations']}\n"
            
            st.download_button(
                label=t("Download Soil Report"),
                data=report_md,
                file_name=f"soil_report_{analysis['timestamp'][:10]}.md",
                mime="text/markdown"
            )

# Resources page (placeholder - would be implemented with actual resources)
def show_resources_page():
    """Display agricultural resources and guides"""
    st.markdown(f"<h2 class='slideIn'>{t('Agricultural Resources')}</h2>", unsafe_allow_html=True)
    
    # Resource types tabs
    tab1, tab2, tab3, tab4 = st.tabs([t("Guides"), t("Best Practices"), t("Local Resources"), t("Government Schemes")])
    
    with tab1:
        st.markdown(f"### {t('Farming Guides')}")
        
        # Create expandable sections for different guides
        with st.expander(t("Crop Rotation Guide")):
            st.markdown(f"""
            # {t('Crop Rotation Guide')}
            
            {t('Crop rotation is the practice of growing different types of crops in the same area across a sequence of growing seasons. It reduces reliance on one set of nutrients, pest and weed pressure, and the probability of developing resistant pests and weeds.')}
            
            ## {t('Benefits of Crop Rotation')}
            
            - {t('Improved soil structure through different root structures working the soil')}
            - {t('Enhanced soil fertility with legumes adding nitrogen')}
            - {t('Reduced pest pressure by breaking pest cycles')}
            - {t('Improved weed control through varying control methods')}
            - {t('Increased biodiversity on your farm')}
            
            ## {t('Simple Crop Rotation Plan (4-Year)')}
            
            1. **{t('Year 1: Leafy Crops')}** ({t('lettuce, spinach, cabbage')})
            2. **{t('Year 2: Fruit Crops')}** ({t('tomatoes, peppers, eggplant')})
            3. **{t('Year 3: Root Crops')}** ({t('carrots, onions, garlic')})
            4. **{t('Year 4: Legumes')}** ({t('beans, peas, lentils')})
            
            ## {t('Maharashtra-Specific Rotations')}
            
            | {t('Previous Crop')} | {t('Suitable Following Crops')} |
            |---------------|--------------------------|
            | {t('Cotton')}        | {t('Groundnut, Pulses, Millet')} |
            | {t('Rice')}          | {t('Pulses, Vegetables, Oilseeds')} |
            | {t('Sugarcane')}     | {t('Soybean, Pulses, Vegetables')} |
            | {t('Sorghum')}       | {t('Legumes, Oilseeds')} |
            | {t('Wheat')}         | {t('Green manure, Legumes, Oilseeds')} |
            """)
        
        with st.expander(t("Integrated Pest Management (IPM) Guide")):
            st.markdown(f"""
            # {t('Integrated Pest Management Guide')}
            
            {t('IPM is an ecosystem-based strategy that focuses on long-term prevention of pests through a combination of techniques such as biological control, habitat manipulation, and resistant crop varieties.')}
            
            ## {t('IPM Steps')}
            
            1. **{t('Identify and Monitor Pests')}**: {t('Know your enemy before taking action')}
            2. **{t('Set Action Thresholds')}**: {t('Determine at what point pest control action is necessary')}
            3. **{t('Prevention')}**: {t('Implement cultural practices to prevent pest problems')}
            4. **{t('Control')}**: {t('Use appropriate control methods starting with least risky options')}
            
            ## {t('Natural Pest Control Methods')}
            
            | {t('Pest Type')} | {t('Natural Controls')} |
            |-----------|------------------|
            | {t('Aphids')}    | {t('Ladybugs, lacewings, neem oil spray')} |
            | {t('Caterpillars')} | {t('Bacillus thuringiensis (Bt), encourage birds')} |
            | {t('Mites')}     | {t('Predatory mites, sulfur dust')} |
            | {t('Fungal diseases')} | {t('Proper spacing, morning watering, neem oil')} |
            
            ## {t('Maharashtra-Specific Pest Pressures')}
            
            - **{t('Cotton')}**: {t('Pink bollworm - Use pheromone traps, early plowing after harvest')}
            - **{t('Rice')}**: {t('Brown planthopper - Use resistant varieties, maintain water levels')}
            - **{t('Sugarcane')}**: {t('Pyrilla - Release Epiricania parasites, avoid excess nitrogen')}
            - **{t('Vegetables')}**: {t('Fruit flies - Use traps with methyl eugenol')}
            """)
        
        with st.expander(t("Water Conservation Techniques")):
            st.markdown(f"""
            # {t('Water Conservation Techniques for Farmers')}
            
            {t('Water conservation is especially important in regions with limited rainfall or drought conditions. Implementing efficient water management practices helps maintain crop productivity while conserving this precious resource.')}
            
            ## {t('Irrigation Methods')}
            
            | {t('Method')} | {t('Efficiency')} | {t('Best For')} |
            |--------|------------|----------|
            | {t('Drip irrigation')} | 90% | {t('Row crops, trees, vines')} |
            | {t('Micro-sprinklers')} | 80-85% | {t('Tree crops, berries')} |
            | {t('Furrow irrigation')} | 60-80% | {t('Row crops, heavy soils')} |
            | {t('Flood irrigation')} | 40-50% | {t('Rice, heavy soils')} |
            
            ## {t('Conservation Practices')}
            
            1. **{t('Mulching')}**: {t('Apply 2-3 inches of organic mulch to reduce evaporation by 25-50%')}
            2. **{t('Soil Management')}**: {t('Add organic matter to increase water-holding capacity')}
            3. **{t('Timing')}**: {t('Irrigate early morning or evening to reduce evaporation')}
            4. **{t('Weather Monitoring')}**: {t('Use weather data to optimize irrigation scheduling')}
            5. **{t('Rainwater Harvesting')}**: {t('Capture rainwater in ponds or tanks for later use')}
            
            ## {t('Maharashtra Drought Mitigation')}
            
            - {t('Construction of farm ponds (5mx5mx3m) can provide critical irrigation during dry spells')}
            - {t('Contour bunding on sloped lands to prevent runoff and erosion')}
            - {t('Watershed development programs have shown 30-60% increase in water availability')}
            """)
        
        with st.expander(t("Soil Health Management")):
            st.markdown(f"""
            # {t('Soil Health Management')}
            
            {t('Healthy soil is the foundation of productive farming. Managing soil health involves maintaining soil physical, chemical, and biological properties for optimal plant growth.')}
            
            ## {t('Key Soil Health Principles')}
            
            1. **{t('Minimize Disturbance')}**: {t('Reduce tillage to protect soil structure')}
            2. **{t('Maximize Soil Cover')}**: {t('Keep living plants or residue on soil')}
            3. **{t('Maximize Biodiversity')}**: {t('Use diverse crop rotations and cover crops')}
            4. **{t('Maximize Living Roots')}**: {t('Keep living roots in soil as long as possible')}
            
            ## {t('Soil Amendments')}
            
            | {t('Amendment')} | {t('Benefits')} | {t('Application Rate')} |
            |-----------|----------|------------------|
            | {t('Compost')} | {t('Improves structure, adds nutrients')} | {t('5-10 tons/ha')} |
            | {t('Vermicompost')} | {t('Rich in microbes, balanced nutrients')} | {t('2.5-5 tons/ha')} |
            | {t('Green manure')} | {t('Adds nitrogen, improves biology')} | {t('Plant 45-60 days before main crop')} |
            | {t('Biochar')} | {t('Carbon sequestration, water retention')} | {t('5-10 tons/ha')} |
            
            ## {t('Maharashtra Soil Types and Management')}
            
            - **{t('Black cotton soil (Regur)')}**: {t('Add gypsum (500 kg/ha) to improve structure')}
            - **{t('Red soil')}**: {t('Add organic matter and maintain neutral pH')}
            - **{t('Lateritic soil')}**: {t('Focus on pH correction with lime and adding organic matter')}
            """)
    
    with tab2:
        st.markdown(f"### {t('Best Practices')}")
        
        # Seasonal best practices
        st.markdown(f"#### {t('Seasonal Best Practices')}")
        
        # Determine current season (simplified)
        now = datetime.now()
        month = now.month
        
        if 3 <= month <= 5:  # Spring (March-May)
            season = t("Spring")
        elif 6 <= month <= 8:  # Summer (June-August)
            season = t("Summer")
        elif 9 <= month <= 11:  # Fall (September-November)
            season = t("Fall")
        else:  # Winter (December-February)
            season = t("Winter")
        
        # Display practices for current season
        st.markdown(f"**{t('Current Season')}:** {season}")
        
        with st.expander(f"{season} {t('Best Practices')}"):
            if season == t("Spring"):
                st.markdown(f"""
                ## {t('Spring Best Practices (March-May)')}
                
                ### {t('Field Preparation')}
                - {t('Complete soil testing 30-45 days before planting')}
                - {t('Apply recommended amendments based on soil test results')}
                - {t('Perform primary and secondary tillage operations')}
                - {t('Clean irrigation channels and check pumping equipment')}
                
                ### {t('Planting')}
                - {t('Select appropriate varieties for your region')}
                - {t('Treat seeds with fungicides and bio-agents')}
                - {t('Ensure proper seed rate and spacing')}
                - {t('Plant when soil temperature reaches optimal level')}
                
                ### {t('Irrigation')}
                - {t('Pre-irrigation 10-15 days before sowing')}
                - {t('Light but frequent irrigation for young seedlings')}
                - {t('Monitor soil moisture regularly')}
                
                ### {t('Pest & Disease Management')}
                - {t('Set up monitoring systems (sticky traps, pheromone traps)')}
                - {t('Scout fields weekly for early pest detection')}
                - {t('Apply preventive measures before pest pressure builds up')}
                
                ### {t('Other Activities')}
                - {t('Prepare nurseries for transplanted crops')}
                - {t('Clean and repair farm equipment and tools')}
                - {t('Plan your season\'s crop layout and rotation')}
                """)
            elif season == t("Summer"):
                st.markdown(f"""
                ## {t('Summer Best Practices (June-August)')}
                
                ### {t('Crop Management')}
                - {t('Apply mulch to reduce water evaporation and suppress weeds')}
                - {t('Provide shade for sensitive crops during extreme heat')}
                - {t('Increase irrigation frequency but maintain appropriate volume')}
                - {t('Implement trellising/staking systems for vine crops')}
                
                ### {t('Pest & Disease Management')}
                - {t('Scout fields twice weekly during peak pest season')}
                - {t('Watch for fungal diseases during humid conditions')}
                - {t('Use biological controls whenever possible')}
                - {t('Apply pesticides in evening hours for better efficacy')}
                
                ### {t('Irrigation')}
                - {t('Irrigate during early morning or evening to reduce evaporation')}
                - {t('Practice deficit irrigation during critical growth stages')}
                - {t('Monitor for signs of water stress even with regular irrigation')}
                - {t('Consider temporary shade structures for sensitive crops')}
                
                ### {t('Soil Management')}
                - {t('Apply side dressing of nutrients for long-season crops')}
                - {t('Protect soil from erosion during heavy monsoon rains')}
                - {t('Maintain drainage channels to prevent waterlogging')}
                
                ### {t('Other Activities')}
                - {t('Prepare for harvest of early season crops')}
                - {t('Begin planning for fall planting')}
                - {t('Maintain records of all farming activities')}
                """)
            elif season == t("Fall"):
                st.markdown(f"""
                ## {t('Fall Best Practices (September-November)')}
                
                ### {t('Harvest Management')}
                - {t('Harvest crops at optimal maturity for best quality')}
                - {t('Ensure proper drying and storage of harvested crops')}
                - {t('Clean and sanitize storage facilities before use')}
                - {t('Grade and sort produce for better market prices')}
                
                ### {t('Field Preparation')}
                - {t('Collect and analyze soil samples after harvest')}
                - {t('Plant cover crops in harvested fields')}
                - {t('Incorporate crop residues to add organic matter')}
                - {t('Apply lime if needed (based on soil test results)')}
                
                ### {t('Planting (Rabi Crops)')}
                - {t('Select appropriate varieties for winter growing conditions')}
                - {t('Plant at recommended depth and spacing')}
                - {t('Provide irrigation immediately after planting if soil is dry')}
                
                ### {t('Pest & Disease Management')}
                - {t('Clean up crop residues that may harbor pests')}
                - {t('Apply preventive measures for winter pests')}
                - {t('Monitor stored crops regularly for pest issues')}
                
                ### {t('Other Activities')}
                - {t('Service irrigation systems before winter')}
                - {t('Review the season\'s records and plan improvements')}
                - {t('Attend agricultural training programs during off-season')}
                """)
            else:  # Winter
                st.markdown(f"""
                ## {t('Winter Best Practices (December-February)')}
                
                ### {t('Crop Management')}
                - {t('Protect sensitive crops from frost with covers or smoke')}
                - {t('Provide windbreaks for vulnerable fields')}
                - {t('Adjust irrigation timing to warmer parts of the day')}
                - {t('Apply recommended winter fertilization')}
                
                ### {t('Pest & Disease Management')}
                - {t('Monitor for rodent activity in fields and storage')}
                - {t('Check dormant trees for scale insects and apply dormant oil')}
                - {t('Clean and sanitize greenhouse structures')}
                
                ### {t('Water Management')}
                - {t('Check and repair water harvesting structures')}
                - {t('Maintain drainage systems to handle winter rains')}
                - {t('Apply limited irrigation to prevent dehydration during dry spells')}
                
                ### {t('Soil Management')}
                - {t('Apply organic matter to fields for slow decomposition')}
                - {t('Protect bare soil with cover crops or mulch')}
                - {t('Test soil in preparation for spring planting')}
                
                ### {t('Other Activities')}
                - {t('Maintain and repair farm equipment and tools')}
                - {t('Attend agricultural workshops and trainings')}
                - {t('Review previous year\'s records and plan for coming season')}
                - {t('Order seeds and supplies for spring planting')}
                """)
        
        # Crop-specific best practices
        st.markdown(f"#### {t('Crop-Specific Best Practices')}")
        
        # Create sections for common crops
        crops = [t("Tomato"), t("Rice"), t("Cotton"), t("Sugarcane"), t("Onion"), t("Wheat")]
        crop_selection = st.selectbox(t("Select Crop"), options=crops)
        
        with st.expander(f"{crop_selection} {t('Best Practices')}"):
            if crop_selection == t("Tomato"):
                st.markdown(f"""
                ## {t('Tomato Best Practices')}
                
                ### {t('Varieties for Maharashtra')}
                - **{t('Summer')}**: {t('Pusa Ruby, Punjab Chhuhara, Arka Vikas')}
                - **{t('Winter')}**: {t('Pusa Early Dwarf, Sioux, Punjab Kesri')}
                - **{t('Hybrid Options')}**: {t('Lakshmi, Naveen, Avinash-2')}
                
                ### {t('Spacing & Planting')}
                - **{t('Row-to-row')}**: {t('60-75 cm')}
                - **{t('Plant-to-plant')}**: {t('30-45 cm')}
                - {t('Transplant 4-6 week old seedlings')}
                - **{t('Optimum soil temperature')}**: {t('18-24°C')}
                
                ### {t('Nutrient Management')}
                - **{t('Base Application')}**: {t('FYM @ 25 tons/ha')}
                - **{t('NPK Requirements')}**: {t('100:50:50 kg/ha')}
                - **{t('Schedule')}**: 
                  - {t('50% N and full P & K at transplanting')}
                  - {t('25% N at flowering')}
                  - {t('25% N at fruiting')}
                
                ### {t('Water Management')}
                - **{t('Critical stages')}**: {t('Flowering and fruit development')}
                - **{t('Drip irrigation recommended')}**: {t('3-5 liters/day/plant')}
                - **{t('Mulching reduces water requirement by 30%')}**
                
                ### {t('Common Issues & Solutions')}
                | {t('Problem')} | {t('Symptoms')} | {t('Solution')} |
                |---------|----------|----------|
                | {t('Blossom end rot')} | {t('Black sunken area on fruit bottom')} | {t('Apply calcium nitrate, maintain even moisture')} |
                | {t('Fusarium wilt')} | {t('Yellowing of lower leaves, stunting')} | {t('Use resistant varieties, crop rotation')} |
                | {t('Tomato leaf curl virus')} | {t('Curling and yellowing of leaves')} | {t('Control whitefly vector, use resistant varieties')} |
                | {t('Early blight')} | {t('Dark concentric rings on leaves')} | {t('Fungicide application, avoid overhead irrigation')} |
                """)
            elif crop_selection == t("Rice"):
                st.markdown(f"""
                ## {t('Rice Best Practices')}
                
                ### {t('Varieties for Maharashtra')}
                - **{t('Kharif Season')}**: {t('Ratna, Jaya, Indrayani, Sahyadri series')}
                - **{t('Rabi Season')}**: {t('Krishna, Jai Shriram, Pawana')}
                - **{t('Drought Tolerant')}**: {t('Phule Radha, Phule Maval')}
                
                ### {t('Field Preparation & Planting')}
                - {t('Thorough puddling to reduce percolation losses')}
                - {t('Maintain 2-3 cm water level during puddling')}
                - **{t('Seed rate')}**: {t('20-25 kg/ha for transplanting, 60-80 kg/ha for broadcasting')}
                - **{t('Spacing')}**: {t('20 cm × 15 cm for transplanted rice')}
                
                ### {t('Nutrient Management')}
                - **{t('Base Application')}**: {t('FYM @ 10 tons/ha')}
                - **{t('NPK Requirements')}**: {t('100:50:50 kg/ha')}
                - **{t('Application Schedule')}**:
                  - {t('50% N, 100% P & K as basal')}
                  - {t('25% N at tillering')}
                  - {t('25% N at panicle initiation')}
                
                ### {t('Water Management')}
                - {t('Maintain 5 cm water throughout vegetative phase')}
                - {t('Practice alternate wetting and drying after panicle initiation')}
                - **{t('Critical stages')}**: {t('Tillering, panicle initiation, flowering')}
                
                ### {t('Common Issues & Solutions')}
                | {t('Problem')} | {t('Symptoms')} | {t('Solution')} |
                |---------|----------|----------|
                | {t('Blast')} | {t('Diamond-shaped lesions on leaves')} | {t('Apply tricyclazole, maintain water level')} |
                | {t('Bacterial leaf blight')} | {t('Yellow to white stripes on leaves')} | {t('Use resistant varieties, balanced fertilization')} |
                | {t('Brown planthopper')} | {t('Wilting, yellowing in patches (hopper burn)')} | {t('Drain fields, use resistant varieties')} |
                | {t('Stem borer')} | {t('Dead heart (vegetative), white head (reproductive)')} | {t('Apply carbofuran granules, monitor with pheromone traps')} |
                """)
            elif crop_selection == t("Cotton"):
                st.markdown(f"""
                ## {t('Cotton Best Practices')}
                
                ### {t('Varieties for Maharashtra')}
                - **{t('Non-Bt Cotton')}**: {t('NH 615, AKH 081, PKV Rajat')}
                - **{t('Bt Cotton Hybrids')}**: {t('Bollgard-II, RCH-2, JKCH-1947')}
                - **{t('Early Maturing')}**: {t('NH 615, PKVHY-2, AKH-9916')}
                
                ### {t('Spacing & Planting')}
                - **{t('Row-to-row')}**: {t('90-120 cm')}
                - **{t('Plant-to-plant')}**: {t('45-60 cm')}
                - **{t('Seed rate')}**: {t('2.5-3 kg/ha')}
                - **{t('Planting time')}**: {t('June-July with onset of monsoon')}
                
                ### {t('Nutrient Management')}
                - **{t('Base Application')}**: {t('FYM @ 10-15 tons/ha')}
                - **{t('NPK Requirements')}**: {t('100:50:50 kg/ha')}
                - **{t('Application Schedule')}**:
                  - {t('50% N, 100% P & K at sowing')}
                  - {t('25% N at squaring')}
                  - {t('25% N at flowering')}
                - **{t('Micronutrients')}**: {t('Foliar spray of 0.5% ZnSO₄ and 0.2% Boron at flowering')}
                
                ### {t('Water Management')}
                - **{t('Critical stages')}**: {t('Squaring, flowering, boll development')}
                - **{t('Water requirement')}**: {t('500-700 mm')}
                - {t('Protective irrigation during dry spells essential')}
                
                ### {t('Common Issues & Solutions')}
                | {t('Problem')} | {t('Symptoms')} | {t('Solution')} |
                |---------|----------|----------|
                | {t('Pink bollworm')} | {t('Rosette flowers, damaged bolls with red larvae')} | {t('Use pheromone traps (5/ha), timely harvest')} |
                | {t('Jassids')} | {t('Yellowing of leaf margins (hopper burn)')} | {t('Apply imidacloprid, use resistant varieties')} |
                | {t('Bollworms')} | {t('Floral bud and boll damage')} | {t('Use Bt cotton, apply NPV or chemical control')} |
                | {t('Bacterial blight')} | {t('Angular water-soaked lesions on leaves')} | {t('Use acid delinted seeds, copper fungicides')} |
                """)
            elif crop_selection == t("Sugarcane"):
                st.markdown(f"""
                ## {t('Sugarcane Best Practices')}
                
                ### {t('Varieties for Maharashtra')}
                - **{t('Early Maturing')}**: {t('Co 86032, CoM 0265')}
                - **{t('Mid-Late Maturing')}**: {t('Co 94012, CoM 9702')}
                - **{t('Drought Tolerant')}**: {t('Co 91010, CoM 88121')}
                
                ### {t('Planting Methods')}
                - **{t('Conventional')}**: {t('2-3 bud setts, 30,000-35,000/ha')}
                - **{t('Wide row')}**: {t('150 cm paired rows, suitable for mechanization')}
                - **{t('Sustainable Sugarcane Initiative (SSI)')}**: {t('Single bud, wider spacing')}
                - **{t('Planting Time')}**: {t('October-November (Adsali), January-February (Suru)')}
                
                ### {t('Nutrient Management')}
                - **{t('Base Application')}**: {t('FYM @ 25 tons/ha or press mud @ 10 tons/ha')}
                - **{t('NPK Requirements')}**: {t('250:115:115 kg/ha')}
                - **{t('Application Schedule')}**:
                  - {t('40% N, 100% P & K at planting')}
                  - {t('30% N at tillering (45-60 days)')}
                  - {t('30% N at grand growth stage (90-120 days)')}
                
                ### {t('Water Management')}
                - **{t('Total water requirement')}**: {t('1500-2500 mm')}
                - **{t('Critical growth stages')}**: {t('Germination, tillering, grand growth')}
                - {t('Drip irrigation can save 30-40% water')}
                
                ### {t('Common Issues & Solutions')}
                | {t('Problem')} | {t('Symptoms')} | {t('Solution')} |
                |---------|----------|----------|
                | {t('Early shoot borer')} | {t('Dead heart in young shoots')} | {t('Apply carbofuran granules, remove dead hearts')} |
                | {t('Top borer')} | {t('Bunchy top appearance')} | {t('Apply fipronil or chlorantraniliprole')} |
                | {t('Red rot')} | {t('Internal reddening of stalk')} | {t('Use disease-free setts, resistant varieties')} |
                | {t('Pyrilla')} | {t('Honeydew secretion, sooty mold')} | {t('Release Epiricania parasites, spray buprofezin')} |
                """)
            elif crop_selection == t("Onion"):
                st.markdown(f"""
                ## {t('Onion Best Practices')}
                
                ### {t('Varieties for Maharashtra')}
                - **{t('Kharif Season')}**: {t('N-53, Baswant 780')}
                - **{t('Rabi Season')}**: {t('Phule Samarth, Agrifound Dark Red, Bhima Super')}
                - **{t('Late Kharif')}**: {t('Phule Suvarna, Baswant 780')}
                
                ### {t('Nursery & Transplanting')}
                - **{t('Seed rate')}**: {t('8-10 kg/ha')}
                - **{t('Nursery bed size')}**: {t('3m × 1m × 15cm (raised)')}
                - {t('Transplant 6-8 week old seedlings')}
                - **{t('Spacing')}**: {t('15 cm × 10 cm')}
                
                ### {t('Nutrient Management')}
                - **{t('Base Application')}**: {t('FYM @ 20-25 tons/ha')}
                - **{t('NPK Requirements')}**: {t('100:50:50 kg/ha')}
                - **{t('Application Schedule')}**:
                  - {t('50% N, 100% P & K before transplanting')}
                  - {t('25% N at 30 days after transplanting')}
                  - {t('25% N at 45 days after transplanting')}
                - **{t('Micronutrients')}**: {t('Foliar spray of 0.5% ZnSO₄ at 45 days')}
                
                ### {t('Water Management')}
                - {t('Light but frequent irrigation')}
                - **{t('Critical stages')}**: {t('Bulb formation, bulb development')}
                - {t('Stop irrigation 15-20 days before harvest')}
                
                ### {t('Common Issues & Solutions')}
                | {t('Problem')} | {t('Symptoms')} | {t('Solution')} |
                |---------|----------|----------|
                | {t('Purple blotch')} | {t('Purple lesions on leaves')} | {t('Spray mancozeb or chlorothalonil')} |
                | {t('Thrips')} | {t('Silvery patches, curling of leaves')} | {t('Apply fipronil or spinosad')} |
                | {t('Basal rot')} | {t('Yellowing from leaf tips, rotting at base')} | {t('Treat seed with Trichoderma, crop rotation')} |
                | {t('Stemphylium blight')} | {t('Small whitish spots on leaves')} | {t('Apply azoxystrobin or difenoconazole')} |
                """)
            elif crop_selection == t("Wheat"):
                st.markdown(f"""
                ## {t('Wheat Best Practices')}
                
                ### {t('Varieties for Maharashtra')}
                - **{t('Timely Sown')}**: {t('MACS 6478, HD 2189, LOK-1')}
                - **{t('Late Sown')}**: {t('HD 2932, NIAW 34, NIAW 917')}
                - **{t('Heat Tolerant')}**: {t('NIAW 301, HD 3090')}
                
                ### {t('Sowing & Spacing')}
                - **{t('Seed rate')}**: {t('100 kg/ha (timely), 125 kg/ha (late)')}
                - **{t('Spacing')}**: {t('22.5 cm between rows')}
                - **{t('Sowing depth')}**: {t('5 cm')}
                - **{t('Optimum sowing time')}**: {t('November 1-15')}
                
                ### {t('Nutrient Management')}
                - **{t('Base Application')}**: {t('FYM @ 10 tons/ha')}
                - **{t('NPK Requirements')}**: {t('120:60:40 kg/ha')}
                - **{t('Application Schedule')}**:
                  - {t('50% N, 100% P & K at sowing')}
                  - {t('25% N at first irrigation (21 days)')}
                  - {t('25% N at second irrigation (40-45 days)')}
                
                ### {t('Water Management')}
                - **{t('Critical stages')}**: {t('Crown root initiation, tillering, flowering, grain filling')}
                - **{t('Total water requirement')}**: {t('450-650 mm')}
                - **{t('Typical irrigation schedule')}**:
                  - {t('First: 21-25 days (CRI stage)')}
                  - {t('Second: 40-45 days (tillering)')}
                  - {t('Third: 60-65 days (late jointing)')}
                  - {t('Fourth: 80-85 days (flowering)')}
                  - {t('Fifth: 100-105 days (milk stage)')}
                
                ### {t('Common Issues & Solutions')}
                | {t('Problem')} | {t('Symptoms')} | {t('Solution')} |
                |---------|----------|----------|
                | {t('Leaf rust')} | {t('Orange-brown pustules on leaves')} | {t('Use resistant varieties, apply propiconazole')} |
                | {t('Powdery mildew')} | {t('White powdery patches on leaves')} | {t('Apply sulfur or tebuconazole')} |
                | {t('Aphids')} | {t('Clusters on young leaves and ears')} | {t('Spray imidacloprid or thiamethoxam')} |
                | {t('Termites')} | {t('Wilting, drying of plants')} | {t('Apply chlorpyriphos or fipronil in irrigation')} |
                """)
    
    with tab3:
        st.markdown(f"### {t('Maharashtra Local Resources')}")
        
        st.markdown(f"""
        ## {t('Maharashtra Agricultural Resources')}
        
        ### {t('Government Institutions')}
        
        | {t('Institution')} | {t('Location')} | {t('Services')} | {t('Contact')} |
        |-------------|----------|----------|---------|
        | {t('Mahatma Phule Krishi Vidyapeeth')} | {t('Rahuri, Ahmednagar')} | {t('Research, Training, Seed Production')} | mpkv.ac.in |
        | {t('Dr. Balasaheb Sawant Konkan Krishi Vidyapeeth')} | {t('Dapoli, Ratnagiri')} | {t('Coastal Agriculture Research')} | dbskkv.org |
        | {t('Vasantrao Naik Marathwada Agricultural University')} | {t('Parbhani')} | {t('Dryland Agriculture Research')} | vnmau.ac.in |
        | {t('Dr. Panjabrao Deshmukh Krishi Vidyapeeth')} | {t('Akola')} | {t('Cotton, Pulses Research')} | pdkv.ac.in |
        
        ### {t('State Government Support Schemes')}
        
        - **{t('Mahatma Jyotirao Phule Debt Waiver Scheme')}**: {t('Loan waiver for eligible farmers')}
        - **{t('Nano Urea Subsidy Scheme')}**: {t('50% subsidy on nano urea for increasing productivity')}
        - **{t('PM Kisan Samman Nidhi')}**: {t('₹6,000 annual income support in three equal installments')}
        - **{t('Maharashtra Agri-Tech Infrastructure Fund')}**: {t('Support for developing post-harvest infrastructure')}
        
        ### {t('Farmer Producer Organizations (FPOs)')}
        
        | {t('FPO Name')} | {t('Region')} | {t('Specialization')} | {t('Contact')} |
        |----------|--------|----------------|---------|
        | {t('Sahyadri Farmer Producer Company')} | {t('Nashik')} | {t('Grapes, Vegetables, Export')} | sahyadrifpo.com |
        | {t('Devnadi Valley Farmer Producer Company')} | {t('Sinnar, Nashik')} | {t('Onions, Pomegranates')} | devnadivalley@gmail.com |
        | {t('Ankur Farmer Producer Company')} | {t('Akola')} | {t('Cotton, Soybean')} | ankurfpc@gmail.com |
        | {t('Maha Farmers Producer Company')} | {t('Pune')} | {t('Fruits, Vegetables')} | maha.fpc@gmail.com |
        
        ### {t('Local Input Suppliers')}
        
        - **{t('Maharashtra Agro Industries Development Corporation (MAIDC)')}**: {t('Fertilizers, seeds, implements')}
        - **{t('Maharashtra State Seeds Corporation (Mahabeej)')}**: {t('Quality seeds of improved varieties')}
        - **{t('Krishi Vigyan Kendras (KVKs)')}**: {t('Technology assessment, demonstration, capacity development')}
        
        ### {t('Markets & Wholesale Centers')}
        
        | {t('Market')} | {t('Location')} | {t('Specialization')} | {t('Market Day')} |
        |--------|----------|----------------|------------|
        | {t('Lasalgaon APMC')} | {t('Nashik')} | {t("Asia's largest onion market")} | {t('Daily')} |
        | {t('Vashi APMC')} | {t('Navi Mumbai')} | {t('Vegetables, fruits, grains')} | {t('Daily')} |
        | {t('Kalamna Market')} | {t('Nagpur')} | {t('Oranges, cotton, soybeans')} | {t('Daily')} |
        | {t('Pune Market Yard')} | {t('Pune')} | {t('Vegetables, fruits')} | {t('Daily')} |
        
        ### {t('Weather Resources')}
        
        - **{t('Indian Meteorological Department (IMD)')}**: mausam.imd.gov.in
        - **{t('Maharashtra Remote Sensing Application Centre')}**: mrsac.gov.in
        - **{t('District Agromet Units (DAMUs)')}**: {t('Located at KVKs, provide district-level forecasts')}
        
        ### {t('Mobile Apps for Maharashtra Farmers')}
        
        - **{t('Kisan Suvidha')}**: {t('Weather, market prices, agro-advisories')}
        - **{t('Pusa Krishi')}**: {t('Crop specific information from ICAR')}
        - **{t('Shetkari Masik App')}**: {t('Marathi agricultural magazine')}
        - **{t('mKisan')}**: {t('SMS portal for farmers')}
        """)
    
    
    with tab4:
        st.markdown(f"### {t('Government Schemes for Farmers')}")
        st.markdown(t("Explore various government initiatives designed to support farmers."))

        schemes = [
            {
                "title": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
                "icon": "🇮🇳 1️⃣",
                "content": """
**Official Portal:** [pmkisan.gov.in](https://pmkisan.gov.in)

**Launched:** 2019  
**Ministry:** Ministry of Agriculture & Farmers Welfare

### 📌 Objective
To provide income support to small and marginal farmers for meeting agricultural and household expenses.

### 💰 Financial Structure
• ₹6,000 per year  
• Paid in 3 equal instalments of ₹2,000  
• Direct Benefit Transfer (DBT)  
• 100% funded by Government of India

### 🎯 Detailed Benefits
✔ Reduces dependence on moneylenders  
✔ Helps purchase seeds, fertilizers, pesticides  
✔ Supports small farmers during crop season  
✔ Financial stability in lean agricultural periods

### 👨🌾 Detailed Eligibility
**Eligible:**
• Small & marginal farmers  
• Landholding farmer families (husband, wife, minor children)

**Not Eligible:**
• Institutional landholders  
• Income tax payers  
• Government employees (except Class IV)  
• Professionals like doctors, engineers, lawyers

### 📄 Required Documents
• Aadhaar Card (mandatory)  
• Land ownership record (7/12 extract, Jamabandi etc.)  
• Bank account (Aadhaar linked)  
• Mobile number

### 🛠 Complete Application Process
**Online:**
1. Visit portal -> Farmer Corner -> New Registration
2. Enter Aadhaar & captcha
3. Fill land & bank details
4. Complete e-KYC (OTP or biometric)
5. Submit

**Offline:**
• Visit Common Service Centre (CSC)
• Provide documents
• Operator registers on portal

### ⏳ Timeline
• Instalments released every 4 months
• e-KYC mandatory for payment release

### 📞 Grievance
**PM-KISAN Helpline:** 155261 / 011-24300606  
**Email:** pmkisan-ict@gov.in

### 🎥 YouTube Registration Guide
[Hindi Guide](https://www.youtube.com/results?search_query=PM+Kisan+registration+online+step+by+step+Hindi) | [Marathi Guide](https://www.youtube.com/results?search_query=PM+Kisan+registration+process+Marathi)
"""
            },
            {
                "title": "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
                "icon": "🇮🇳 2️⃣",
                "content": """
**Official Portal:** [pmfby.gov.in](https://pmfby.gov.in)

**Launched:** 2016

### 📌 Objective
To provide financial protection against crop failure.

### 💰 Premium Structure
**Farmer Pays:**
• Kharif crops → 2%  
• Rabi crops → 1.5%  
• Commercial crops → 5%  
*Remaining premium paid by Govt (Centre + State).*

### 🌾 Risks Covered
✔ Drought  
✔ Flood  
✔ Cyclone  
✔ Pest attack  
✔ Landslides  
✔ Post-harvest losses (up to 14 days)

### 📄 Documents
• Aadhaar  
• Land records  
• Bank passbook  
• Sowing certificate (if required)

### 🛠 Application
• Bank branch  
• CSC centre  
• PMFBY portal

**Last Date:**
• Kharif → July/August  
• Rabi → December/January

### 📌 Claim Process
1. Inform within 72 hours of crop loss
2. Survey conducted
3. Yield data collected
4. Claim settled directly to bank

### 🎥 YouTube Registration Guide
[Hindi Guide](https://www.youtube.com/results?search_query=PMFBY+online+registration+Hindi) | [Marathi Guide](https://www.youtube.com/results?search_query=PMFBY+registration+process+Marathi)
"""
            },
            {
                "title": "PMKSY (Pradhan Mantri Krishi Sinchayee Yojana)",
                "icon": "🇮🇳 3️⃣",
                "content": """
**Official:** [pmksy.gov.in](https://pmksy.gov.in)

**Launched:** 2015

### 📌 Objective
Improve irrigation efficiency & water conservation.

### 💧 Components
1. **Har Khet Ko Pani**
2. **Per Drop More Crop**
3. **Watershed Development**

### 💰 Subsidy
• Small farmers → Up to 55%  
• Other farmers → 45%  
*(Varies by state)*

### 📄 Documents
• Aadhaar  
• Land documents  
• Bank details  
• Passport photo

### 🛠 Process
1. Apply via State Agriculture Department
2. Field inspection
3. Approval issued
4. Install drip/sprinkler
5. Subsidy credited

### 🎥 YouTube Registration Guide
[Hindi Guide](https://www.youtube.com/results?search_query=PMKSY+drip+irrigation+subsidy+apply+Hindi) | [Marathi Guide](https://www.youtube.com/results?search_query=PMKSY+drip+subsidy+registration+Marathi)
"""
            },
            {
                "title": "PM-KUSUM Scheme",
                "icon": "🇮🇳 4️⃣",
                "content": """
**Official:** [mnre.gov.in](https://mnre.gov.in)

### 📌 Objective
Promote solar energy in agriculture.

### ☀ Components
A – Solar plants  
B – Standalone solar pumps  
C – Solarisation of grid-connected pumps

### 💰 Financial Pattern
• 60% Govt subsidy  
• 30% bank loan  
• 10% farmer contribution

### 🎯 Benefits
✔ Free irrigation power  
✔ Sell surplus electricity  
✔ Reduce diesel cost

### 🎥 YouTube Registration Guide
[Hindi Guide](https://www.youtube.com/results?search_query=PM+KUSUM+scheme+apply+online+Hindi) | [Marathi Guide](https://www.youtube.com/results?search_query=PM+KUSUM+solar+pump+registration+Marathi)
"""
            },
            {
                "title": "Soil Health Card Scheme",
                "icon": "🇮🇳 5️⃣",
                "content": """
**Official:** [soilhealth.dac.gov.in](https://soilhealth.dac.gov.in)

### 📌 Objective
Promote balanced use of fertilizers.

### 🧪 Soil Testing Includes:
• Nitrogen  
• Phosphorus  
• Potassium  
• Micronutrients

**Validity:** Soil Health Card valid for 2 years.

### 🎥 YouTube Registration Guide
[Hindi Guide](https://www.youtube.com/results?search_query=Soil+Health+Card+registration+Hindi) | [Marathi Guide](https://www.youtube.com/results?search_query=Soil+Health+Card+process+Marathi)
"""
            },
            {
                "title": "Agriculture Infrastructure Fund (AIF)",
                "icon": "🇮🇳 7️⃣",
                "content": """
**Official:** [agriinfra.dac.gov.in](https://agriinfra.dac.gov.in)

### 📌 Loan Support
• Up to ₹2 crore  
• Interest subvention 3%  
• Credit guarantee

### Infrastructure Covered
• Warehouses  
• Cold storages  
• Processing units  
• Sorting/grading units

### 🎥 YouTube Registration Guide
[Hindi Guide](https://www.youtube.com/results?search_query=AIF+loan+apply+online+Hindi) | [Marathi Guide](https://www.youtube.com/results?search_query=Agriculture+Infrastructure+Fund+registration+Marathi)
"""
            },
            {
                "title": "SMAM (Farm Machinery Subsidy)",
                "icon": "🇮🇳 8️⃣",
                "content": """
**Official:** [agricoop.nic.in](https://agricoop.nic.in)

### Machines Covered
• Tractors  
• Seed drills  
• Power tillers  
• Harvesters  
• Sprayers

### Subsidy Range
40–50% (varies by category)

### 🎥 YouTube Registration Guide
[Hindi Guide](https://www.youtube.com/results?search_query=SMAM+tractor+subsidy+apply+Hindi) | [Marathi Guide](https://www.youtube.com/results?search_query=Farm+machinery+subsidy+registration+Marathi)
"""
            },
            {
                "title": "Paramparagat Krishi Vikas Yojana (PKVY)",
                "icon": "🇮🇳 9️⃣",
                "content": """
**Official:** [pgsindia-ncof.gov.in](https://pgsindia-ncof.gov.in)

### 📌 Organic Farming Cluster
• Minimum 20 farmers  
• 50-acre cluster

### Financial Assistance
₹50,000 per hectare for 3 years.

### 🎥 YouTube Registration Guide
[Hindi Guide](https://www.youtube.com/results?search_query=PKVY+organic+farming+registration+Hindi) | [Marathi Guide](https://www.youtube.com/results?search_query=PKVY+registration+process+Marathi)
"""
            }
        ]

        for scheme in schemes:
            with st.expander(f"{scheme['icon']} {t(scheme['title'])}"):
                st.markdown(scheme['content'])


# Weather page
def show_weather_page():
    """Display the full weather analysis page"""
    # Get location from profile or user input
    profile = st.session_state.user_profile or {}
    location = get_profile_field(profile, "farm_location")
    
    # Fallback to current_user if not in profile
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
    
    # Simply call the weather service's full page display
    from weather_service import show_weather_page as show_weather_service_page
    show_weather_service_page(location)

# Main app logic
def main():
    """Main application logic"""
    # Show header for all pages
    show_header()
    
    # Language selector in sidebar (removed as it's now in header/login pages)
    # if st.session_state.page not in ["login", "signup"]:
    #     with st.sidebar:
    #         show_language_selector()
    
    # Display current page
    if st.session_state.page == "login":
        show_login_page()
    elif st.session_state.page == "forgot_password":
        show_forgot_password_page()
    elif st.session_state.page == "signup":
        show_signup_page()
    elif st.session_state.page == "profile_setup":
        show_profile_setup_page()
    elif st.session_state.page == "dashboard":
        show_dashboard_page()
    elif st.session_state.page == "chatbot":
        show_chatbot_page()
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
    else:
        st.error("Unknown page")
        go_to_login()

    # Footer
    if st.session_state.page not in ["login", "signup"]:
        st.markdown(f"""
<footer>
    <p>{t("PhytoSense v2.0 - AI-Powered Plant Health Monitoring System")}</p>
    <p>{t("© 2024 PhytoSense Team. All rights reserved.")}</p>
</footer>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
