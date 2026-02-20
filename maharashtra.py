"""
Maharashtra-specific agricultural data and recommendations for PhytoSense application.
Contains information about regional agricultural practices, seasonal guidelines, and local crop varieties.
"""

import random
from datetime import datetime
from crop_data import maharashtra_crop_varieties, maharashtra_soil_types, crop_water_requirements

def get_local_recommendations(crop_name):
    """
    Get Maharashtra-specific recommendations for a given crop
    
    Args:
        crop_name: Name of the crop
        
    Returns:
        dict: Maharashtra-specific recommendations
    """
    # Handle case sensitivity
    crop_name = crop_name.capitalize()
    
    # Create recommendations
    recommendations = {}
    
    # Check if crop data exists
    if crop_name in maharashtra_crop_varieties:
        # Get seasonal recommendations based on current month
        month = datetime.now().month
        
        if 3 <= month <= 5:  # Summer (March-May)
            season = "summer"
        elif 6 <= month <= 9:  # Monsoon/Kharif (June-September)
            season = "monsoon"
        elif 10 <= month <= 11:  # Post-monsoon (October-November)
            season = "post_monsoon"
        else:  # Winter (December-February)
            season = "winter"
        
        # Seasonal recommendations
        seasonal_recommendations = {
            "Tomato": {
                "summer": "Apply mulch to conserve moisture and use shade nets during peak summer.",
                "monsoon": "Use staking and raise seedlings in protected nurseries. Watch for fungal diseases.",
                "post_monsoon": "Ideal planting season. Monitor for jassids and fruit borers.",
                "winter": "Protect from frost in North Maharashtra. Reduce irrigation frequency."
            },
            "Onion": {
                "summer": "Not recommended for planting. For stored onions, ensure proper ventilation.",
                "monsoon": "Kharif onion planting time. Use raised beds for good drainage.",
                "post_monsoon": "Ideal for rabi onion planting. Treat seeds with fungicides.",
                "winter": "Apply light irrigation. Watch for purple blotch disease."
            },
            "Wheat": {
                "summer": "Post-harvest storage period. Ensure proper drying before storage.",
                "monsoon": "Not a wheat growing season in Maharashtra.",
                "post_monsoon": "Ideal sowing time. Apply pre-sowing irrigation.",
                "winter": "Apply irrigation at critical stages. Watch for aphid infestation."
            },
            "Rice": {
                "summer": "Summer rice harvesting period. Ensure proper post-harvest handling.",
                "monsoon": "Main growing season. Use SRI technique for better yields.",
                "post_monsoon": "Harvesting period for kharif rice. Monitor for grain discoloration.",
                "winter": "Not a major rice growing season except in irrigated areas."
            },
            "Cotton": {
                "summer": "Land preparation time. Apply organic matter.",
                "monsoon": "Sowing season. Adopt high-density planting for better yields.",
                "post_monsoon": "Flowering and boll formation stage. Monitor for pink bollworm.",
                "winter": "Harvesting season. Focus on clean picking."
            },
            "Sugarcane": {
                "summer": "Pre-seasonal cane requires adequate irrigation. Watch for early shoot borer.",
                "monsoon": "Ideal for Adsali planting. Ensure proper drainage.",
                "post_monsoon": "Good for pre-seasonal planting. Apply Trichoderma to setts.",
                "winter": "Suru planting season. Treat setts with fungicides."
            },
            "Soybean": {
                "summer": "Land preparation time. Apply lime if soil is acidic.",
                "monsoon": "Sowing season. Use rhizobium culture as seed treatment.",
                "post_monsoon": "Harvesting period. Ensure proper drying to avoid aflatoxin.",
                "winter": "Not a soybean growing season in Maharashtra."
            },
            "Potato": {
                "summer": "Not a potato growing season in Maharashtra.",
                "monsoon": "Not recommended due to high disease pressure.",
                "post_monsoon": "Ideal planting time. Use certified seed potatoes.",
                "winter": "Apply light irrigation. Watch for late blight disease."
            }
        }
        
        # Add seasonal recommendation if available
        if crop_name in seasonal_recommendations and season in seasonal_recommendations[crop_name]:
            recommendations["seasonal"] = seasonal_recommendations[crop_name][season]
        else:
            recommendations["seasonal"] = f"Consult local agricultural extension for {season} recommendations for {crop_name}."
        
        # Irrigation recommendations
        if crop_name in crop_water_requirements:
            water_req = crop_water_requirements[crop_name]
            
            recommendations["irrigation"] = f"Total water requirement: {water_req['total_water_requirement']}. " + \
                                          f"Critical stages: {', '.join(water_req['critical_stages'])}. " + \
                                          f"{water_req['irrigation_schedule']}."
        else:
            recommendations["irrigation"] = "Irrigate based on soil moisture status and crop stage."
        
        # Add Maharashtra-specific variety recommendations
        crop_varieties = maharashtra_crop_varieties[crop_name]["recommended_varieties"]
        planting_seasons = maharashtra_crop_varieties[crop_name]["planting_seasons"]
        special_recommendations = maharashtra_crop_varieties[crop_name]["special_recommendations"]
        
        recommendations["varieties"] = random.sample(crop_varieties, min(3, len(crop_varieties)))
        recommendations["planting_seasons"] = planting_seasons
        recommendations["special_advice"] = special_recommendations
        
        # Add region-specific practices
        maharashtra_regions = {
            "Konkan": ["Rice", "Mango", "Cashew", "Coconut"],
            "Vidarbha": ["Cotton", "Soybean", "Orange", "Tur"],
            "Marathwada": ["Cotton", "Soybean", "Sugarcane", "Jowar"],
            "Western Maharashtra": ["Sugarcane", "Grapes", "Pomegranate", "Onion"],
            "Khandesh": ["Banana", "Cotton", "Jowar"]
        }
        
        # Find regions where this crop is commonly grown
        regions_for_crop = [region for region, crops in maharashtra_regions.items() if crop_name in crops]
        
        if regions_for_crop:
            recommendations["suitable_regions"] = regions_for_crop
        
        # Add recommended practices
        practices = []
        
        # General practices
        practices.append("Adopt crop-specific integrated nutrient management (INM) for Maharashtra soils")
        practices.append("Follow integrated pest management (IPM) practices to reduce chemical usage")
        
        # Special practices for Maharashtra
        if crop_name == "Rice":
            practices.append("Implement System of Rice Intensification (SRI) for better water efficiency")
            practices.append("Use Indrayani and Karjat series varieties developed specifically for Maharashtra")
        elif crop_name == "Cotton":
            practices.append("Implement high-density planting (1.5 lakh plants/ha) for better yields")
            practices.append("Use pheromone traps (5/ha) for pink bollworm monitoring")
        elif crop_name == "Sugarcane":
            practices.append("Adopt trench planting method for better water use efficiency")
            practices.append("Practice trash mulching to conserve soil moisture")
        elif crop_name == "Onion":
            practices.append("Use raised beds with drip irrigation for kharif onion")
            practices.append("Adopt INM package developed by DOGR, Rajgurunagar for Maharashtra conditions")
        
        # Add practices to recommendations
        recommendations["practices"] = practices
    else:
        # Generic recommendations for crops not in the database
        recommendations = {
            "seasonal": "Consult local Krishi Vigyan Kendra for seasonal advice.",
            "irrigation": "Follow irrigation scheduling based on crop stage and soil moisture.",
            "practices": [
                "Adopt integrated nutrient management for Maharashtra soils",
                "Implement water conservation practices appropriate for your region",
                "Follow integrated pest management to reduce chemical usage"
            ]
        }
    
    return recommendations

def get_weather_based_recommendations(crop_name, weather_data):
    """
    Get weather-based agricultural recommendations for Maharashtra
    
    Args:
        crop_name: Name of the crop
        weather_data: Current weather data
        
    Returns:
        list: Weather-based recommendations
    """
    recommendations = []
    
    # Extract weather variables if available
    temperature = weather_data.get("main", {}).get("temp", 25)
    humidity = weather_data.get("main", {}).get("humidity", 50)
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    has_rain = "rain" in weather_data
    
    # Temperature-based recommendations
    if temperature > 35:
        recommendations.append(f"High temperature alert (>35°C). Apply irrigation to {crop_name} during evening hours.")
        recommendations.append("Use shade nets for sensitive crops and increase irrigation frequency.")
        
        if crop_name == "Tomato":
            recommendations.append("Use fruit setting hormones as high temperatures affect pollination in tomatoes.")
        elif crop_name in ["Rice", "Wheat"]:
            recommendations.append("Apply irrigation to mitigate heat stress during critical growth stages.")
    elif temperature < 10:
        recommendations.append(f"Low temperature alert (<10°C). Protect {crop_name} from frost damage.")
        recommendations.append("Create smoke in the field during early morning hours to protect from frost.")
        
        if crop_name in ["Tomato", "Chili"]:
            recommendations.append("Cover seedlings with plastic tunnels to protect from cold injury.")
    
    # Humidity-based recommendations
    if humidity > 80:
        recommendations.append(f"High humidity alert (>80%). Monitor {crop_name} for fungal diseases.")
        
        if crop_name == "Onion":
            recommendations.append("High humidity favors purple blotch and stemphylium blight in onions. Apply prophylactic fungicide sprays.")
        elif crop_name == "Tomato":
            recommendations.append("Watch for early/late blight development. Ensure good ventilation between plants.")
        elif crop_name == "Grapes":
            recommendations.append("High risk of downy mildew infection. Apply protective fungicide spray.")
    
    # Rain-based recommendations
    if has_rain:
        rain_amount = weather_data.get("rain", {}).get("1h", 0) or weather_data.get("rain", {}).get("3h", 0)
        
        if rain_amount > 10:
            recommendations.append(f"Heavy rainfall alert (>{rain_amount}mm). Ensure proper drainage in {crop_name} fields.")
            recommendations.append("Postpone fertilizer application to prevent leaching and runoff.")
            
            if crop_name in ["Onion", "Cotton", "Chili"]:
                recommendations.append("Apply foliar spray of 19:19:19 after rain stops to promote recovery from rain damage.")
        else:
            recommendations.append("Light rainfall occurred. Avoid irrigation for the next 1-2 days.")
    
    # Wind-based recommendations
    if wind_speed > 8:
        recommendations.append(f"Strong wind alert (>{wind_speed}m/s). Provide physical support to {crop_name} plants.")
        
        if crop_name in ["Banana", "Papaya"]:
            recommendations.append("Provide staking support to prevent lodging in high wind.")
        elif crop_name == "Sugarcane":
            recommendations.append("Use propping (tying together) of sugarcane plants to prevent lodging.")
    
    # If no specific conditions trigger recommendations
    if not recommendations:
        recommendations.append(f"Current weather conditions are favorable for {crop_name} cultivation in Maharashtra.")
        recommendations.append("Continue regular monitoring and scheduled farm operations.")
    
    return recommendations

def get_maharashtra_soil_recommendation(soil_type, crop_name=None):
    """
    Get Maharashtra-specific soil management recommendations
    
    Args:
        soil_type: Type of soil
        crop_name: Optional name of the crop
        
    Returns:
        dict: Soil management recommendations
    """
    recommendations = {}
    
    # Find matching soil type
    matched_soil = None
    for soil in maharashtra_soil_types:
        if soil_type.lower() in soil.lower():
            matched_soil = soil
            break
    
    if not matched_soil:
        # Default to black cotton soil if no match found
        matched_soil = "Black Cotton Soil (Regur)"
    
    # Get soil information
    soil_info = maharashtra_soil_types[matched_soil]
    
    recommendations["soil_type"] = matched_soil
    recommendations["characteristics"] = soil_info["characteristics"]
    recommendations["distribution"] = soil_info["distribution"]
    recommendations["suitable_crops"] = soil_info["suitable_crops"]
    
    # Basic soil management recommendations
    recommendations["management"] = soil_info["management"]
    
    # Add crop-specific recommendations if crop is provided
    if crop_name:
        crop_name = crop_name.capitalize()
        
        # Check if crop is suitable for this soil
        crop_suitability = "highly suitable" if crop_name in soil_info["suitable_crops"] else "moderately suitable"
        recommendations["crop_suitability"] = f"{crop_name} is {crop_suitability} for {matched_soil}."
        
        # Soil-specific crop recommendations
        if matched_soil == "Black Cotton Soil (Regur)":
            if crop_name == "Cotton":
                recommendations["crop_specific"] = "Apply gypsum (500 kg/ha) to improve soil structure. Create drainage channels to prevent waterlogging during monsoon."
            elif crop_name == "Sugarcane":
                recommendations["crop_specific"] = "Apply press mud (10 tons/ha) to improve soil structure. Adopt trash mulching to conserve moisture."
            elif crop_name == "Onion":
                recommendations["crop_specific"] = "Create raised beds to improve drainage. Apply well-decomposed FYM (20 tons/ha)."
            else:
                recommendations["crop_specific"] = "Avoid over-irrigation to prevent waterlogging. Apply organic matter to improve soil structure."
        
        elif matched_soil == "Red Soil":
            if crop_name in ["Groundnut", "Pulses"]:
                recommendations["crop_specific"] = "Apply gypsum (500 kg/ha) at flowering stage for groundnut. Use drip irrigation for efficient water use."
            elif crop_name == "Citrus":
                recommendations["crop_specific"] = "Apply micronutrients (Zn, B) as foliar spray. Use basin irrigation with mulching."
            else:
                recommendations["crop_specific"] = "Apply organic matter to improve water retention. Consider drip irrigation for efficient water use."
        
        elif matched_soil == "Laterite Soil":
            if crop_name == "Rice":
                recommendations["crop_specific"] = "Apply lime (2 tons/ha) to correct soil acidity. Use balanced NPK fertilizers."
            elif crop_name in ["Cashew", "Mango"]:
                recommendations["crop_specific"] = "Create large planting pits with organic matter. Apply lime to correct acidity."
            else:
                recommendations["crop_specific"] = "Apply lime based on soil test. Add organic matter to improve soil fertility."
        
        elif matched_soil == "Alluvial Soil":
            recommendations["crop_specific"] = "Follow balanced fertilization based on soil test. Maintain organic matter through crop residue incorporation."
        
        elif matched_soil == "Coastal Sandy Soil":
            recommendations["crop_specific"] = "Apply coir pith compost or organic matter to improve water retention. Use drip irrigation with fertigation."
    
    return recommendations
