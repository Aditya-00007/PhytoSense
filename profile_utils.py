"""
Profile utility functions for PhytoSense application.
Provides helper functions for working with user profiles.
"""

def get_profile_field(profile_data, field_name, default=""):
    """
    Safely get a field from profile data, handling missing keys.
    
    Args:
        profile_data: Dictionary containing profile data
        field_name: Name of the field to retrieve
        default: Default value to return if field is not found
        
    Returns:
        Value of the field or default if not found
    """
    if not profile_data:
        return default
    return profile_data.get(field_name, default)

def get_select_index(current_value, options):
    """
    Get the index of the current value in the options list.
    
    Args:
        current_value: Current value to find in options
        options: List of options
        
    Returns:
        int: Index of the current value in options, or 0 if not found
    """
    try:
        return options.index(current_value) if current_value in options else 0
    except ValueError:
        return 0

def get_farm_size_category(farm_size_str):
    """
    Convert farm size string to category.
    
    Args:
        farm_size_str: String representation of farm size (e.g., "5 acres")
        
    Returns:
        string: Category of farm size ("Marginal", "Small", "Medium", "Large")
    """
    try:
        # Extract numeric value
        size_value = float(''.join(c for c in farm_size_str if c.isdigit() or c == '.'))
        
        # Determine category based on size
        if size_value < 2.5:
            return "Marginal"
        elif size_value < 5:
            return "Small"
        elif size_value < 10:
            return "Medium"
        else:
            return "Large"
    except:
        return "Unknown"

def parse_crop_list(crops_str):
    """
    Parse comma-separated crop list into a list of crops.
    
    Args:
        crops_str: Comma-separated string of crops
        
    Returns:
        list: List of crops
    """
    if not crops_str:
        return []
    
    return [crop.strip() for crop in crops_str.split(',') if crop.strip()]

def get_main_crop(profile_data):
    """
    Determine the main crop from the user's profile.
    
    Args:
        profile_data: Dictionary containing profile data
        
    Returns:
        string: The main crop or None if not found
    """
    primary_crops = get_profile_field(profile_data, 'primary_crops')
    crops = parse_crop_list(primary_crops)
    
    return crops[0] if crops else None

def get_region_from_location(location):
    """
    Determine the Maharashtra region from a location string.
    
    Args:
        location: Location string
        
    Returns:
        string: Region name ("Konkan", "Vidarbha", "Marathwada", etc.) or None if not found
    """
    # Define regions and their districts/cities
    regions = {
        "Konkan": ["Mumbai", "Thane", "Palghar", "Raigad", "Ratnagiri", "Sindhudurg"],
        "Western Maharashtra": ["Pune", "Satara", "Sangli", "Kolhapur", "Solapur"],
        "Khandesh": ["Nashik", "Dhule", "Nandurbar", "Jalgaon"],
        "Marathwada": ["Aurangabad", "Jalna", "Parbhani", "Hingoli", "Nanded", "Beed", "Latur", "Osmanabad"],
        "Vidarbha": ["Nagpur", "Wardha", "Bhandara", "Gondia", "Chandrapur", "Gadchiroli", "Yavatmal", "Akola", "Amravati", "Buldhana", "Washim"]
    }
    
    # Check location against regions
    if not location:
        return None
    
    location_lower = location.lower()
    
    # Check if location contains region name directly
    for region in regions:
        if region.lower() in location_lower:
            return region
    
    # Check if location contains any district/city name
    for region, districts in regions.items():
        for district in districts:
            if district.lower() in location_lower:
                return region
    
    return None

def get_weather_risk_factors(profile_data):
    """
    Determine weather risk factors based on user's profile.
    
    Args:
        profile_data: Dictionary containing profile data
        
    Returns:
        dict: Weather risk factors
    """
    risk_factors = {
        "drought_risk": "Low",
        "flood_risk": "Low",
        "frost_risk": "Low"
    }
    
    # Get region from location
    farm_location = get_profile_field(profile_data, 'farm_location')
    region = get_region_from_location(farm_location)
    
    # Determine risks based on region
    if region == "Marathwada" or region == "Vidarbha":
        risk_factors["drought_risk"] = "High"
    elif region == "Konkan":
        risk_factors["flood_risk"] = "High"
        risk_factors["drought_risk"] = "Low"
    elif region == "Western Maharashtra":
        risk_factors["frost_risk"] = "Medium"
    
    # Adjust based on crops
    primary_crops = parse_crop_list(get_profile_field(profile_data, 'primary_crops'))
    
    if "Rice" in primary_crops:
        risk_factors["drought_risk"] = "High" if risk_factors["drought_risk"] != "Low" else "Medium"
    if "Sugarcane" in primary_crops:
        risk_factors["frost_risk"] = "Medium" if risk_factors["frost_risk"] == "Low" else risk_factors["frost_risk"]
    
    return risk_factors

def get_recommended_features(profile_data):
    """
    Determine recommended app features based on user's profile.
    
    Args:
        profile_data: Dictionary containing profile data
        
    Returns:
        list: Recommended features
    """
    recommended = []
    
    # Basic recommendations for all users
    recommended.append("plant_health_analysis")
    
    # Add soil analysis if farming type indicates need
    farming_type = get_profile_field(profile_data, 'farming_type')
    if farming_type in ["Conventional", "Organic", "Transitioning to Organic"]:
        recommended.append("soil_analysis")
    
    # Add weather alerts if user has requested them
    receive_weather_alerts = get_profile_field(profile_data, 'receive_weather_alerts', True)
    if receive_weather_alerts:
        recommended.append("weather_alerts")
    
    # Add crop-specific features
    primary_crops = parse_crop_list(get_profile_field(profile_data, 'primary_crops'))
    
    if any(crop in ["Tomato", "Potato", "Onion"] for crop in primary_crops):
        recommended.append("vegetable_crop_guide")
    
    if any(crop in ["Rice", "Wheat", "Cotton", "Sugarcane"] for crop in primary_crops):
        recommended.append("major_crop_guide")
    
    # Add organic farming resources if applicable
    if farming_type in ["Organic", "Transitioning to Organic"]:
        recommended.append("organic_farming_resources")
    
    return recommended


def is_location_india(location):
    """
    Determine if the location is in India.
    """
    if not location:
        # Default to India as the application focuses on Maharashtra-specific agricultural data
        return True
    
    location_lower = location.lower().strip()
    
    # Check for country name or code
    if any(country in location_lower for country in ["india", "bharat"]):
        return True
    
    # Check for country code suffix
    if location_lower.endswith(",in") or location_lower.endswith(", in") or location_lower.endswith(" in"):
        return True
        
    # Check if get_region_from_location returns a region (all of them are in Maharashtra, India)
    if get_region_from_location(location) is not None:
        return True
        
    # Check for major Indian states/cities
    indian_places = [
        "maharashtra", "pune", "mumbai", "nashik", "nagpur", "aurangabad", "latur", "delhi", "bangalore", 
        "hyderabad", "chennai", "kolkata", "rajasthan", "gujarat", "punjab", "haryana", "uttar pradesh",
        "madhya pradesh", "karnataka", "tamil nadu", "andhra pradesh", "telangana", "kerala", "bihar",
        "west bengal", "assam", "odisha", "goa", "thane", "palghar", "raigad", "ratnagiri", "sindhudurg",
        "satara", "sangli", "kolhapur", "solapur", "dhule", "nandurbar", "jalgaon", "jalna", "parbhani",
        "hingoli", "nanded", "beed", "osmanabad", "wardha", "bhandara", "gondia", "chandrapur", "gadchiroli",
        "yavatmal", "akola", "amravati", "buldhana", "washim"
    ]
    if any(place in location_lower for place in indian_places):
        return True
        
    return False


def is_location_southern_hemisphere(location):
    """
    Determine if the location is in the Southern Hemisphere.
    """
    if not location:
        return False
        
    location_lower = location.lower().strip()
    sh_countries = ["australia", "brazil", "south africa", "new zealand", "argentina", "chile", "peru", "angola", "mozambique", "indonesia"]
    sh_codes = [",au", ", au", " au", ",br", ", br", " br", ",za", ", za", " za", ",nz", ", nz", " nz", ",ar", ", ar", " ar", ",cl", ", cl", " cl"]
    
    if any(country in location_lower for country in sh_countries):
        return True
    if any(location_lower.endswith(code) for code in sh_codes):
        return True
        
    return False


def get_season_details(location, month=None):
    """
    Determine season details based on farmer's location and current month.
    
    Returns:
        dict: {
            'season': str,
            'color': str,
            'icon': str,
            'tips': list of str
        }
    """
    from datetime import datetime
    from language_support import t
    
    if month is None:
        month = datetime.now().month
        
    # Check region/hemisphere
    if is_location_india(location):
        # Indian Season mapping
        if 6 <= month <= 9:  # June - September
            return {
                "season": t("Monsoon (Kharif)"),
                "color": "#2196F3",
                "icon": "🌧️",
                "tips": [
                    t("Sow Kharif crops (Rice, Cotton, Soybean, Maize)"),
                    t("Ensure proper drainage in fields to prevent waterlogging"),
                    t("Use staking for vegetable crops to prevent rot"),
                    t("Monitor for fungal diseases due to high humidity")
                ]
            }
        elif 10 <= month <= 11:  # October - November
            return {
                "season": t("Post-monsoon (Autumn)"),
                "color": "#FF5722",
                "icon": "🍂",
                "tips": [
                    t("Harvest mature Kharif crops"),
                    t("Prepare land and treat seeds for Rabi crops"),
                    t("Apply pre-sowing irrigation"),
                    t("Clean and store harvesting equipment")
                ]
            }
        elif month == 12 or month <= 2:  # December - February
            return {
                "season": t("Winter (Rabi)"),
                "color": "#00BCD4",
                "icon": "❄️",
                "tips": [
                    t("Sow and manage Rabi crops (Wheat, Mustard, Potato)"),
                    t("Apply light but regular irrigation"),
                    t("Protect crops from cold waves or frost"),
                    t("Watch for aphid infestations and powdery mildew")
                ]
            }
        else:  # March - May (Zaid / Summer)
            return {
                "season": t("Summer (Zaid)"),
                "color": "#FF9800",
                "icon": "☀️",
                "tips": [
                    t("Apply mulch to conserve moisture and use shade nets"),
                    t("Maintain regular irrigation for Zaid crops (cucumber, melons)"),
                    t("Prepare fields for upcoming Kharif sowing"),
                    t("Monitor soil moisture frequently during high heat")
                ]
            }
            
    elif is_location_southern_hemisphere(location):
        # Southern Hemisphere temperate mapping
        if month == 12 or month <= 2:  # Dec - Feb
            return {
                "season": t("Summer"),
                "color": "#FF9800",
                "icon": "☀️",
                "tips": [
                    t("Monitor for heat stress"),
                    t("Increase irrigation frequency"),
                    t("Apply mulch to retain moisture"),
                    t("Watch for pest outbreaks")
                ]
            }
        elif 3 <= month <= 5:  # Mar - May
            return {
                "season": t("Autumn"),
                "color": "#FF5722",
                "icon": "🍂",
                "tips": [
                    t("Harvest mature crops"),
                    t("Plant cover crops"),
                    t("Test and amend soil"),
                    t("Clean and store equipment")
                ]
            }
        elif 6 <= month <= 8:  # Jun - Aug
            return {
                "season": t("Winter"),
                "color": "#2196F3",
                "icon": "❄️",
                "tips": [
                    t("Protect sensitive plants"),
                    t("Service farm equipment"),
                    t("Plan next season's crops"),
                    t("Take training courses")
                ]
            }
        else:  # Sep - Nov
            return {
                "season": t("Spring"),
                "color": "#6EDB3E",
                "icon": "🌱",
                "tips": [
                    t("Prepare soil for planting"),
                    t("Start summer crop seedlings"),
                    t("Apply pre-emergent herbicides"),
                    t("Check irrigation systems")
                ]
            }
            
    else:
        # Northern Hemisphere temperate mapping (Default)
        if 3 <= month <= 5:  # Mar - May
            return {
                "season": t("Spring"),
                "color": "#6EDB3E",
                "icon": "🌱",
                "tips": [
                    t("Prepare soil for planting"),
                    t("Start summer crop seedlings"),
                    t("Apply pre-emergent herbicides"),
                    t("Check irrigation systems")
                ]
            }
        elif 6 <= month <= 8:  # Jun - Aug
            return {
                "season": t("Summer"),
                "color": "#FF9800",
                "icon": "☀️",
                "tips": [
                    t("Monitor for heat stress"),
                    t("Increase irrigation frequency"),
                    t("Apply mulch to retain moisture"),
                    t("Watch for pest outbreaks")
                ]
            }
        elif 9 <= month <= 11:  # Sep - Nov
            return {
                "season": t("Fall"),
                "color": "#FF5722",
                "icon": "🍂",
                "tips": [
                    t("Harvest mature crops"),
                    t("Plant cover crops"),
                    t("Test and amend soil"),
                    t("Clean and store equipment")
                ]
            }
        else:  # Dec - Feb
            return {
                "season": t("Winter"),
                "color": "#2196F3",
                "icon": "❄️",
                "tips": [
                    t("Protect sensitive plants"),
                    t("Service farm equipment"),
                    t("Plan next season's crops"),
                    t("Take training courses")
                ]
            }

