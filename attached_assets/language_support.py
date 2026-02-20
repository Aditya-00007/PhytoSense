"""
Language support for PhytoSense application
Provides translations for multiple languages
"""
import streamlit as st

# Define translations for key UI elements
TRANSLATIONS = {
    "english": {
        # General UI
        "welcome": "Welcome to PhytoSense",
        "dashboard": "Dashboard",
        "login": "Login",
        "signup": "Sign Up",
        "logout": "Logout",
        "username": "Username",
        "password": "Password",
        "email": "Email (Optional)",
        "confirm_password": "Confirm Password",
        "create_account": "Create Account",
        "login_button": "Login",
        "signup_button": "Sign Up",
        "language_settings": "Language Settings",
        
        # Navigation
        "test_crop": "Test Your Crop",
        "soil_analysis": "Soil Analysis",
        "history": "History",
        "resources": "Resources",
        
        # Profile
        "complete_profile": "Complete Your Profile",
        "personal_info": "Personal Information",
        "full_name": "Full Name",
        "farm_info": "Farm Information",
        "farm_name": "Farm Name",
        "location": "Location",
        "district": "District in Maharashtra",
        "farm_size": "Farm Size (e.g., '5 acres')",
        "crop_info": "Crop Information",
        "current_crops": "Current Crops (separated by commas)",
        "soil_type": "Primary Soil Type",
        "irrigation_method": "Primary Irrigation Method",
        "current_status": "Current Status",
        "crop_health": "Current Crop Health Status (Any issues you're facing?)",
        "required_fields": "Required fields*",
        "save_profile": "Save Profile",
        
        # Dashboard
        "your_profile": "Your Profile",
        "name": "Name:",
        "farm": "Farm:",
        "location_label": "Location:",
        "district_label": "District:",
        "farm_size_label": "Farm Size:",
        "crop_information": "Crop Information",
        "main_crops": "Main Crops:",
        "soil_type_label": "Soil Type:",
        "irrigation_method_label": "Irrigation Method:",
        "current_status_label": "Current Status:",
        "no_issues": "No issues reported",
        "quick_actions": "Quick Actions",
        "analyze_plant": "Analyze Plant",
        "analyze_plant_health": "Analyze Plant Health",
        "upload_plant_photo": "Upload a photo of your plant to detect diseases",
        "analyze_soil": "Analyze Soil",
        "upload_soil_photo": "Upload a photo of your soil to get composition analysis",
        "view_history": "View History",
        "check_analyses": "Check your previous analyses and track plant health",
        "farming_resources": "Farming Resources",
        "access_guides": "Access guides on crops, soil types, and farming advice",
        "recent_analyses": "Recent Analyses",
        "no_analyses": "You haven't performed any analyses yet. Try analyzing a plant or soil sample!",
        "view_all_history": "View All History",
        
        # Plant Analysis
        "plant_health_analysis": "Plant Health Analysis",
        "plant_analysis_description": "Upload a photo of your plant and provide additional details to get a comprehensive analysis:",
        "disease_detection": "Disease detection",
        "water_content": "Water content analysis",
        "pest_identification": "Pest identification",
        "treatment_recommendations": "Treatment recommendations",
        "local_crop_advice": "Maharashtra-specific crop advice",
        "plant_details": "Plant Details (helps improve analysis accuracy)",
        "tell_about_crop": "Tell us about your crop",
        "crop_type": "Crop Type",
        "select_crop_type": "Select Crop Type",
        "plant_age": "Plant Age/Growth Stage",
        "select_stage": "Select Stage",
        "planting_date": "Planting Date (approximate)",
        "select_irrigation": "Select Method",
        "treatments_applied": "Any treatments already applied?",
        "treatments_placeholder": "e.g., fungicides, pesticides, fertilizers...",
        "symptoms_observed": "Describe any symptoms or issues you've observed",
        "symptoms_placeholder": "e.g., yellowing leaves, spots, wilting, stunted growth...",
        "plant_details_recorded": "Plant details recorded. These will be used to improve analysis accuracy!",
        "select_crop_type_warning": "Please select a crop type to continue.",
        "upload_image": "Upload an Image",
        "choose_image": "Choose an image...",
        "uploaded_image": "Uploaded Image",
        "image_processed": "Image successfully uploaded and processed!",
        "error_processing": "Error processing image:",
        "or_choose_example": "Or Choose an Example",
        "no_example_images": "No example images available. Please upload your own image.",
        "use_this": "Use This",
        "analyze_plant_health_button": "Analyze Plant Health",
        "analyzing": "Analyzing plant health...",
        "select_crop_type_first": "Please select a crop type in the Plant Details section before analysis.",
        
        # Weather
        "weather_alert": "Weather Alert",
        "current_weather": "Current Weather",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "wind_speed": "Wind Speed",
        "conditions": "Conditions",
        "forecast": "Weather Forecast",
        "no_alerts": "No severe weather alerts at this time",
        "weather_location": "Weather for",
        "update_weather": "Update Weather",
        "weather_updated": "Weather information updated",
        "weather_error": "Error getting weather data:",
        "high_temp_alert": "High Temperature Alert: Ensure adequate irrigation for your crops.",
        "heavy_rain_alert": "Heavy Rain Alert: Consider protective measures for your crops.",
        "frost_alert": "Frost Alert: Protect sensitive crops from freezing temperatures.",
        "wind_alert": "High Wind Alert: Secure structures and protect fragile crops.",
        "humidity_alert": "High Humidity Alert: Monitor for potential fungal diseases."
    },
    "marathi": {
        # General UI
        "welcome": "फायटोसेन्समध्ये आपले स्वागत आहे",
        "dashboard": "डॅशबोर्ड",
        "login": "लॉगिन",
        "signup": "साइन अप",
        "logout": "लॉगआउट",
        "username": "वापरकर्तानाव",
        "password": "पासवर्ड",
        "email": "ईमेल (पर्यायी)",
        "confirm_password": "पासवर्ड पुष्टी करा",
        "create_account": "खाते तयार करा",
        "login_button": "लॉगिन",
        "signup_button": "साइन अप",
        "language_settings": "भाषा सेटिंग्ज",
        
        # Navigation
        "test_crop": "आपली पिके तपासा",
        "soil_analysis": "मातीचे विश्लेषण",
        "history": "इतिहास",
        "resources": "संसाधने",
        
        # Profile
        "complete_profile": "आपली प्रोफाइल पूर्ण करा",
        "personal_info": "वैयक्तिक माहिती",
        "full_name": "पूर्ण नाव",
        "farm_info": "शेती माहिती",
        "farm_name": "शेताचे नाव",
        "location": "स्थान",
        "district": "महाराष्ट्रातील जिल्हा",
        "farm_size": "शेताचा आकार (उदा. '५ एकर')",
        "crop_info": "पिकांची माहिती",
        "current_crops": "वर्तमान पिके (स्वल्पविरामाने वेगळे)",
        "soil_type": "प्राथमिक मातीचा प्रकार",
        "irrigation_method": "प्राथमिक सिंचन पद्धती",
        "current_status": "वर्तमान स्थिती",
        "crop_health": "वर्तमान पिकांची आरोग्य स्थिती (आपण कोणत्या समस्यांना सामोरे जात आहात?)",
        "required_fields": "आवश्यक फील्ड्स*",
        "save_profile": "प्रोफाइल जतन करा",
        
        # Dashboard
        "your_profile": "आपली प्रोफाइल",
        "name": "नाव:",
        "farm": "शेत:",
        "location_label": "स्थान:",
        "district_label": "जिल्हा:",
        "farm_size_label": "शेताचा आकार:",
        "crop_information": "पिकांची माहिती",
        "main_crops": "मुख्य पिके:",
        "soil_type_label": "मातीचा प्रकार:",
        "irrigation_method_label": "सिंचन पद्धती:",
        "current_status_label": "वर्तमान स्थिती:",
        "no_issues": "कोणत्याही समस्या नोंदवलेल्या नाहीत",
        "quick_actions": "त्वरित कृती",
        "analyze_plant": "रोपांचे विश्लेषण करा",
        "analyze_plant_health": "वनस्पती आरोग्य विश्लेषण करा",
        "upload_plant_photo": "रोगांचा शोध घेण्यासाठी आपल्या वनस्पतीची फोटो अपलोड करा",
        "analyze_soil": "मातीचे विश्लेषण करा",
        "upload_soil_photo": "रचना विश्लेषण मिळविण्यासाठी आपल्या मातीची फोटो अपलोड करा",
        "view_history": "इतिहास पहा",
        "check_analyses": "आपले मागील विश्लेषण तपासा आणि वनस्पती आरोग्याचा मागोवा घ्या",
        "farming_resources": "शेती संसाधने",
        "access_guides": "पिके, मातीचे प्रकार आणि शेती सल्ल्यांवर मार्गदर्शक पहा",
        "recent_analyses": "अलीकडील विश्लेषणे",
        "no_analyses": "आपण अद्याप कोणतेही विश्लेषण केलेले नाही. वनस्पती किंवा माती नमुना विश्लेषण करून पहा!",
        "view_all_history": "पूर्ण इतिहास पहा",
        
        # Plant Analysis
        "plant_health_analysis": "वनस्पती आरोग्य विश्लेषण",
        "plant_analysis_description": "सर्वसमावेशक विश्लेषण मिळविण्यासाठी आपल्या वनस्पतीची फोटो अपलोड करा आणि अतिरिक्त तपशील प्रदान करा:",
        "disease_detection": "रोग शोध",
        "water_content": "पाणी सामग्री विश्लेषण",
        "pest_identification": "कीड ओळख",
        "treatment_recommendations": "उपचार शिफारसी",
        "local_crop_advice": "महाराष्ट्र-विशिष्ट पीक सल्ला",
        "plant_details": "वनस्पती तपशील (विश्लेषण अचूकता सुधारण्यात मदत करते)",
        "tell_about_crop": "आपल्या पिकाबद्दल आम्हाला सांगा",
        "crop_type": "पिकाचा प्रकार",
        "select_crop_type": "पिकाचा प्रकार निवडा",
        "plant_age": "वनस्पती वय/वाढ टप्पा",
        "select_stage": "टप्पा निवडा",
        "planting_date": "लागवड तारीख (अंदाजे)",
        "select_irrigation": "पद्धत निवडा",
        "treatments_applied": "आधीपासूनच कोणतेही उपचार लागू केले आहेत?",
        "treatments_placeholder": "उदा., बुरशीनाशके, कीटकनाशके, खते...",
        "symptoms_observed": "आपण निरीक्षण केलेल्या कोणत्याही लक्षणे किंवा समस्यांचे वर्णन करा",
        "symptoms_placeholder": "उदा., पिवळी पाने, डाग, कोमेजणे, खुंटलेली वाढ...",
        "plant_details_recorded": "वनस्पती तपशील नोंदवले. हे विश्लेषण अचूकता सुधारण्यासाठी वापरले जातील!",
        "select_crop_type_warning": "कृपया सुरू ठेवण्यासाठी पिकाचा प्रकार निवडा.",
        "upload_image": "प्रतिमा अपलोड करा",
        "choose_image": "प्रतिमा निवडा...",
        "uploaded_image": "अपलोड केलेली प्रतिमा",
        "image_processed": "प्रतिमा यशस्वीरित्या अपलोड आणि प्रक्रिया केली!",
        "error_processing": "प्रतिमा प्रक्रिया करताना त्रुटी:",
        "or_choose_example": "किंवा उदाहरण निवडा",
        "no_example_images": "कोणतीही उदाहरण प्रतिमा उपलब्ध नाही. कृपया आपली स्वतःची प्रतिमा अपलोड करा.",
        "use_this": "हे वापरा",
        "analyze_plant_health_button": "वनस्पती आरोग्य विश्लेषण करा",
        "analyzing": "वनस्पती आरोग्याचे विश्लेषण करत आहे...",
        "select_crop_type_first": "कृपया विश्लेषणापूर्वी वनस्पती तपशील विभागात पिकाचा प्रकार निवडा.",
        
        # Weather
        "weather_alert": "हवामान अलर्ट",
        "current_weather": "वर्तमान हवामान",
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "wind_speed": "वाऱ्याचा वेग",
        "conditions": "परिस्थिती",
        "forecast": "हवामान अंदाज",
        "no_alerts": "याक्षणी कोणताही गंभीर हवामान अलर्ट नाही",
        "weather_location": "हवामान",
        "update_weather": "हवामान अद्यतनित करा",
        "weather_updated": "हवामान माहिती अद्यतनित केली",
        "weather_error": "हवामान डेटा मिळविण्यात त्रुटी:",
        "high_temp_alert": "उच्च तापमान अलर्ट: आपल्या पिकांसाठी पुरेशी सिंचन सुनिश्चित करा.",
        "heavy_rain_alert": "मुसळधार पाऊस अलर्ट: आपल्या पिकांसाठी संरक्षणात्मक उपाय विचारात घ्या.",
        "frost_alert": "थंडी अलर्ट: हिमांकित तापमानापासून संवेदनशील पिकांचे संरक्षण करा.",
        "wind_alert": "वारा तीव्रता अलर्ट: संरचना सुरक्षित करा आणि नाजूक पिकांचे संरक्षण करा.",
        "humidity_alert": "उच्च आर्द्रता अलर्ट: संभाव्य बुरशीजन्य रोगांसाठी निरीक्षण करा."
    },
    "hindi": {
        # General UI
        "welcome": "फायटोसेंस में आपका स्वागत है",
        "dashboard": "डैशबोर्ड",
        "login": "लॉगिन",
        "signup": "साइन अप",
        "logout": "लॉगआउट",
        "username": "उपयोगकर्ता नाम",
        "password": "पासवर्ड",
        "email": "ईमेल (वैकल्पिक)",
        "confirm_password": "पासवर्ड की पुष्टि करें",
        "create_account": "खाता बनाएं",
        "login_button": "लॉगिन",
        "signup_button": "साइन अप",
        "language_settings": "भाषा सेटिंग्स",
        
        # Navigation
        "test_crop": "अपनी फसल का परीक्षण करें",
        "soil_analysis": "मिट्टी का विश्लेषण",
        "history": "इतिहास",
        "resources": "संसाधन",
        
        # Profile
        "complete_profile": "अपनी प्रोफ़ाइल पूरी करें",
        "personal_info": "व्यक्तिगत जानकारी",
        "full_name": "पूरा नाम",
        "farm_info": "खेत की जानकारी",
        "farm_name": "खेत का नाम",
        "location": "स्थान",
        "district": "महाराष्ट्र में जिला",
        "farm_size": "खेत का आकार (जैसे '५ एकड़')",
        "crop_info": "फसल की जानकारी",
        "current_crops": "वर्तमान फसलें (अल्पविराम से अलग करें)",
        "soil_type": "प्राथमिक मिट्टी का प्रकार",
        "irrigation_method": "प्राथमिक सिंचाई विधि",
        "current_status": "वर्तमान स्थिति",
        "crop_health": "वर्तमान फसल स्वास्थ्य स्थिति (क्या आप किसी समस्या का सामना कर रहे हैं?)",
        "required_fields": "आवश्यक फ़ील्ड*",
        "save_profile": "प्रोफ़ाइल सहेजें",
        
        # Dashboard
        "your_profile": "आपकी प्रोफ़ाइल",
        "name": "नाम:",
        "farm": "खेत:",
        "location_label": "स्थान:",
        "district_label": "जिला:",
        "farm_size_label": "खेत का आकार:",
        "crop_information": "फसल की जानकारी",
        "main_crops": "मुख्य फसलें:",
        "soil_type_label": "मिट्टी का प्रकार:",
        "irrigation_method_label": "सिंचाई विधि:",
        "current_status_label": "वर्तमान स्थिति:",
        "no_issues": "कोई समस्या रिपोर्ट नहीं की गई",
        "quick_actions": "त्वरित कार्रवाई",
        "analyze_plant": "पौधे का विश्लेषण करें",
        "analyze_plant_health": "पौधे के स्वास्थ्य का विश्लेषण करें",
        "upload_plant_photo": "रोगों का पता लगाने के लिए अपने पौधे की फोटो अपलोड करें",
        "analyze_soil": "मिट्टी का विश्लेषण करें",
        "upload_soil_photo": "संरचना विश्लेषण प्राप्त करने के लिए अपनी मिट्टी की फोटो अपलोड करें",
        "view_history": "इतिहास देखें",
        "check_analyses": "अपने पिछले विश्लेषणों की जांच करें और पौधे के स्वास्थ्य को ट्रैक करें",
        "farming_resources": "कृषि संसाधन",
        "access_guides": "फसलों, मिट्टी के प्रकारों और कृषि सलाह पर गाइड प्राप्त करें",
        "recent_analyses": "हालिया विश्लेषण",
        "no_analyses": "आपने अभी तक कोई विश्लेषण नहीं किया है। पौधे या मिट्टी के नमूने का विश्लेषण करके देखें!",
        "view_all_history": "सभी इतिहास देखें",
        
        # Plant Analysis
        "plant_health_analysis": "पौधे के स्वास्थ्य का विश्लेषण",
        "plant_analysis_description": "व्यापक विश्लेषण प्राप्त करने के लिए अपने पौधे की फोटो अपलोड करें और अतिरिक्त विवरण प्रदान करें:",
        "disease_detection": "रोग का पता लगाना",
        "water_content": "पानी की मात्रा का विश्लेषण",
        "pest_identification": "कीट पहचान",
        "treatment_recommendations": "उपचार की सिफारिशें",
        "local_crop_advice": "महाराष्ट्र-विशिष्ट फसल सलाह",
        "plant_details": "पौधे का विवरण (विश्लेषण सटीकता में सुधार करने में मदद करता है)",
        "tell_about_crop": "हमें अपनी फसल के बारे में बताएं",
        "crop_type": "फसल का प्रकार",
        "select_crop_type": "फसल का प्रकार चुनें",
        "plant_age": "पौधे की आयु/विकास चरण",
        "select_stage": "चरण चुनें",
        "planting_date": "रोपण तिथि (अनुमानित)",
        "select_irrigation": "विधि चुनें",
        "treatments_applied": "क्या पहले से ही कोई उपचार लागू किया गया है?",
        "treatments_placeholder": "जैसे, कवकनाशी, कीटनाशक, उर्वरक...",
        "symptoms_observed": "आपके द्वारा देखे गए किसी भी लक्षण या समस्या का वर्णन करें",
        "symptoms_placeholder": "जैसे, पीले पत्ते, धब्बे, मुरझाना, विकास में रुकावट...",
        "plant_details_recorded": "पौधे का विवरण दर्ज किया गया। इनका उपयोग विश्लेषण सटीकता में सुधार के लिए किया जाएगा!",
        "select_crop_type_warning": "जारी रखने के लिए कृपया फसल का प्रकार चुनें।",
        "upload_image": "छवि अपलोड करें",
        "choose_image": "छवि चुनें...",
        "uploaded_image": "अपलोड की गई छवि",
        "image_processed": "छवि सफलतापूर्वक अपलोड और प्रोसेस की गई!",
        "error_processing": "छवि प्रोसेसिंग में त्रुटि:",
        "or_choose_example": "या उदाहरण चुनें",
        "no_example_images": "कोई उदाहरण छवि उपलब्ध नहीं है। कृपया अपनी छवि अपलोड करें।",
        "use_this": "इसका उपयोग करें",
        "analyze_plant_health_button": "पौधे के स्वास्थ्य का विश्लेषण करें",
        "analyzing": "पौधे के स्वास्थ्य का विश्लेषण कर रहा है...",
        "select_crop_type_first": "कृपया विश्लेषण से पहले पौधे के विवरण वाले अनुभाग में फसल का प्रकार चुनें।",
        
        # Weather
        "weather_alert": "मौसम अलर्ट",
        "current_weather": "वर्तमान मौसम",
        "temperature": "तापमान",
        "humidity": "आर्द्रता",
        "wind_speed": "हवा की गति",
        "conditions": "परिस्थितियां",
        "forecast": "मौसम का पूर्वानुमान",
        "no_alerts": "इस समय कोई गंभीर मौसम अलर्ट नहीं है",
        "weather_location": "के लिए मौसम",
        "update_weather": "मौसम अपडेट करें",
        "weather_updated": "मौसम की जानकारी अपडेट की गई",
        "weather_error": "मौसम डेटा प्राप्त करने में त्रुटि:",
        "high_temp_alert": "उच्च तापमान अलर्ट: अपनी फसलों के लिए पर्याप्त सिंचाई सुनिश्चित करें।",
        "heavy_rain_alert": "भारी वर्षा अलर्ट: अपनी फसलों के लिए सुरक्षात्मक उपायों पर विचार करें।",
        "frost_alert": "ठंढ अलर्ट: जमने वाले तापमान से संवेदनशील फसलों की रक्षा करें।",
        "wind_alert": "तेज हवा अलर्ट: संरचनाओं को सुरक्षित करें और नाजुक फसलों की रक्षा करें।",
        "humidity_alert": "उच्च आर्द्रता अलर्ट: संभावित कवक रोगों के लिए निगरानी करें।"
    }
}

def get_translation(key, language="english"):
    """Get a translation for a specific key in the specified language"""
    if language not in TRANSLATIONS:
        language = "english"  # Default to English
    
    if key not in TRANSLATIONS[language]:
        # If translation not found, fall back to English
        return TRANSLATIONS["english"].get(key, key)
        
    return TRANSLATIONS[language][key]

def initialize_language():
    """Initialize language in session state if not already present"""
    if "language" not in st.session_state:
        st.session_state.language = "english"

def set_language(language):
    """Set the language in session state"""
    st.session_state.language = language

def get_current_language():
    """Get the current language from session state"""
    initialize_language()
    return st.session_state.language

def t(key):
    """Translate a key based on the current language"""
    return get_translation(key, get_current_language())

def show_language_selector():
    """Display language selector in the sidebar"""
    current_lang = get_current_language()
    
    # Language names in their native language
    lang_options = {
        "english": "English",
        "marathi": "मराठी (Marathi)",
        "hindi": "हिंदी (Hindi)"
    }
    
    # Create a horizontal line of language buttons
    cols = st.columns(3)
    
    with cols[0]:
        if current_lang == "english":
            st.button("English", key="lang_english", disabled=True, use_container_width=True)
        else:
            if st.button("English", key="lang_english", use_container_width=True):
                set_language("english")
                st.rerun()
                
    with cols[1]:
        if current_lang == "marathi":
            st.button("मराठी", key="lang_marathi", disabled=True, use_container_width=True)
        else:
            if st.button("मराठी", key="lang_marathi", use_container_width=True):
                set_language("marathi")
                st.rerun()
                
    with cols[2]:
        if current_lang == "hindi":
            st.button("हिंदी", key="lang_hindi", disabled=True, use_container_width=True)
        else:
            if st.button("हिंदी", key="lang_hindi", use_container_width=True):
                set_language("hindi")
                st.rerun()