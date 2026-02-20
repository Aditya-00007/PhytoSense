import time
from image_processing import preprocess_image, extract_features
from model_handler import identify_plant, detect_water_content, detect_diseases, detect_pests
from maharashtra import get_local_recommendations
from crop_database import get_crop_info, get_crop_disease_info, get_crop_pest_info, get_crop_deficiency_info

def enhanced_analysis(image, crop_type=None, plant_details=None):
    """
    Combined analysis function that integrates multiple forms of analysis
    
    Args:
        image: PIL Image object
        crop_type: Optional crop type override
        plant_details: Optional dictionary of user-provided details (symptoms, etc.)
        
    Returns:
        dict: Combined analysis results
    """
    # Preprocess image for analysis
    processed_image = preprocess_image(image)
    
    # Extract features for custom analysis
    features = extract_features(processed_image)
    
    # Advanced Image Analysis
    from image_processing import detect_color_anomalies, analyze_leaf_shape
    anomalies = detect_color_anomalies(processed_image)
    shape_analysis = analyze_leaf_shape(processed_image)
    
    # Build Analysis Context
    analysis_context = {
        "symptoms": plant_details.get("symptoms") if plant_details else None,
        "anomalies": anomalies,
        "shape_analysis": shape_analysis
    }
    
    # Simulate some processing time for a better user experience
    time.sleep(0.5)
    
    # Identify the plant if crop_type is not specified
    if crop_type is None:
        plant_info = identify_plant(processed_image, context=analysis_context)
        plant_name = plant_info["name"]
    else:
        # Use the provided crop type
        plant_name = crop_type
        plant_info = {
            "name": crop_type,
            "scientific_name": "",
            "probability": 100.0
        }
    
    # Analyze water content with context
    water_content = detect_water_content(processed_image, context=analysis_context)
    
    # Detect diseases with context
    diseases = detect_diseases(processed_image, plant_name, context=analysis_context)
    
    # Detect pests with context
    pests = detect_pests(processed_image, context=analysis_context)
    
    # Get Maharashtra-specific recommendations
    local_recommendations = get_local_recommendations(plant_name)
    
    # Get detailed crop information from database if available
    crop_info = get_crop_info(plant_name)
    if crop_info:
        # Enhance plant info with database information
        if "scientific_name" not in plant_info or not plant_info["scientific_name"]:
            if "info" in crop_info and "scientific_name" in crop_info["info"]:
                plant_info["scientific_name"] = crop_info["info"]["scientific_name"]
        
        # Add detailed crop information
        crop_details = {
            "varieties": crop_info["info"].get("varieties", []),
            "best_season": crop_info["info"].get("best_season", ""),
            "best_soil": crop_info["info"].get("best_soil", ""),
            "time_period": crop_info["info"].get("time_period", "")
        }
        
        # Get more detailed disease information if possible
        detailed_diseases = []
        if diseases and diseases.get("detected", False):
            for disease in diseases.get("diseases", []):
                disease_name = disease.get("name", "")
                db_disease_info = get_crop_disease_info(plant_name, disease_name)
                
                if db_disease_info:
                    # Get the first matching disease from the database
                    db_disease_name, db_disease_data = next(iter(db_disease_info.items()))
                    disease["detailed_info"] = {
                        "symptoms": db_disease_data.get("symptoms", ""),
                        "causes": db_disease_data.get("causes", ""),
                        "treatment": db_disease_data.get("treatment", ""),
                        "prevention": db_disease_data.get("prevention", "")
                    }
                
                detailed_diseases.append(disease)
            
            if detailed_diseases:
                diseases["diseases"] = detailed_diseases
        
        # Get more detailed pest information if possible
        detailed_pests = []
        if pests and pests.get("detected", False):
            for pest in pests.get("pests", []):
                pest_name = pest.get("name", "")
                db_pest_info = get_crop_pest_info(plant_name, pest_name)
                
                if db_pest_info:
                    # Get the first matching pest from the database
                    db_pest_name, db_pest_data = next(iter(db_pest_info.items()))
                    pest["detailed_info"] = {
                        "symptoms": db_pest_data.get("symptoms", ""),
                        "description": db_pest_data.get("description", ""),
                        "treatment": db_pest_data.get("treatment", "")
                    }
                
                detailed_pests.append(pest)
            
            if detailed_pests:
                pests["pests"] = detailed_pests
        
        # Get common deficiencies
        deficiencies = get_crop_deficiency_info(plant_name)
    else:
        crop_details = {}
        deficiencies = None
    
    # Combine all results
    analysis_results = {
        "plant_info": plant_info,
        "water_content": water_content,
        "diseases": diseases,
        "pests": pests,
        "features": features,
        "local_recommendations": local_recommendations,
        "crop_details": crop_details,
        "deficiencies": deficiencies
    }
    
    return analysis_results