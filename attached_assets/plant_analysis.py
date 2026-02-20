import time
from image_processing import preprocess_image, extract_features
from model_handler import identify_plant, detect_water_content, detect_diseases, detect_pests
from maharashtra import get_local_recommendations

def enhanced_analysis(image, crop_type=None):
    """
    Combined analysis function that integrates multiple forms of analysis
    
    Args:
        image: PIL Image object
        crop_type: Optional crop type override
        
    Returns:
        dict: Combined analysis results
    """
    # Preprocess image for analysis
    processed_image = preprocess_image(image)
    
    # Extract features for custom analysis
    features = extract_features(processed_image)
    
    # Simulate some processing time for a better user experience
    time.sleep(0.5)
    
    # Identify the plant if crop_type is not specified
    if crop_type is None:
        plant_info = identify_plant(processed_image)
        plant_name = plant_info["name"]
    else:
        # Use the provided crop type
        plant_name = crop_type
        plant_info = {
            "name": crop_type,
            "scientific_name": "",
            "probability": 100.0
        }
    
    # Analyze water content
    water_content = detect_water_content(processed_image)
    
    # Detect diseases
    diseases = detect_diseases(processed_image, plant_name)
    
    # Detect pests
    pests = detect_pests(processed_image)
    
    # Get Maharashtra-specific recommendations
    local_recommendations = get_local_recommendations(plant_name)
    
    # Combine all results
    analysis_results = {
        "plant_info": plant_info,
        "water_content": water_content,
        "diseases": diseases,
        "pests": pests,
        "features": features,
        "local_recommendations": local_recommendations
    }
    
    return analysis_results