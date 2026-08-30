import time
import io
import base64
import json
import os
import streamlit as st
from image_processing import preprocess_image, extract_features
from model_handler import identify_plant, detect_water_content, detect_diseases, detect_pests
from maharashtra import get_local_recommendations
from crop_database import get_crop_info, get_crop_disease_info, get_crop_pest_info, get_crop_deficiency_info

# Groq Wrapper
try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

def encode_image_to_base64(pil_image):
    buffered = io.BytesIO()
    pil_image.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def refine_analysis_with_llm(image, heuristic_results, plant_details):
    """
    Use Groq's multimodal llama-3.2-11b-vision-preview model to analyze:
    1. The visual image content
    2. The user-provided symptoms, location, and soil
    3. The rule-based heuristic prediction results
    And return a refined set of predictions.
    """
    if not HAS_GROQ:
        return heuristic_results
        
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return heuristic_results
        
    try:
        base64_image = encode_image_to_base64(image)
        
        user_symptoms = plant_details.get("symptoms") or "None reported" if plant_details else "None reported"
        crop_type = plant_details.get("crop_type") or "Unknown" if plant_details else "Unknown"
        location = plant_details.get("farm_location") if plant_details else None
        soil_type = plant_details.get("soil_type") if plant_details else None
        irrigation = plant_details.get("irrigation_method") or "Unknown" if plant_details else "Unknown"
        prev_treatment = plant_details.get("previous_treatments") or "None" if plant_details else "None"
        
        # Fallback to lookup location from profile if not provided in plant details
        if not location:
            current_user = st.session_state.get("current_user")
            if current_user:
                username = current_user.get("username") if isinstance(current_user, dict) else getattr(current_user, "username", None)
                if username:
                    try:
                        from db_adapter import get_user_profile
                        from profile_utils import get_profile_field
                        profile = get_user_profile(username)
                        location = get_profile_field(profile, 'farm_location', 'Unknown')
                    except Exception:
                        pass
        if not location:
            location = "Unknown"

        if not soil_type:
            soil_type = "Unknown"

        
        heuristic_desc = f"""
- Identified Plant: {heuristic_results['plant_info']['name']} (Confidence: {heuristic_results['plant_info']['probability']}%)
- Water content: {heuristic_results['water_content']['percentage']}% (Status: {heuristic_results['water_content']['status']})
- Diseases detected: {json.dumps(heuristic_results['diseases'])}
- Pests detected: {json.dumps(heuristic_results['pests'])}
"""
        
        prompt = f"""
Please audit and refine the following plant analysis results:

=== USER INPUT DETAILS ===
- Crop Type Selected: {crop_type}
- Farm Location: {location}
- Soil Type: {soil_type}
- Irrigation Method: {irrigation}
- User Reported Symptoms: {user_symptoms}
- Previous Treatments: {prev_treatment}

=== HEURISTIC MODEL PREDICTIONS ===
{heuristic_desc}

Compare the visual evidence in the image (lesions, leaf spots, wilting, leaf shape, color abnormalities, insect damage) with the user symptoms and the heuristic predictions. 
Refine the findings. If the heuristic missed a disease/pest or incorrectly labeled it, correct it. Detail visual symptoms, suggest active treatments/preventions, and diagnose potential nutrient deficiencies (e.g. Nitrogen, Phosphorus, Potassium, Zinc, Iron).

Return the response strictly as a JSON object matching this schema:
{{
  "diseases": [
     {{
       "name": "Disease Name",
       "scientific_name": "Scientific Name",
       "confidence": 0-100 score (integer),
       "description": "Symptoms observed in the image",
       "treatment": "Treatment recommendations",
       "detailed_info": {{
          "symptoms": "Detailed symptoms",
          "causes": "Causes of disease",
          "treatment": "Detailed treatment steps",
          "prevention": "Prevention steps"
       }}
     }}
  ],
  "pests": [
     {{
       "name": "Pest Name",
       "scientific_name": "Scientific Name",
       "confidence": 0-100 score (integer),
       "description": "Visual evidence of pests",
       "treatment": "Control actions",
       "detailed_info": {{
          "symptoms": "Damage symptoms",
          "description": "About the pest",
          "treatment": "Treatment steps"
       }}
     }}
  ],
  "water_content": {{
     "percentage": 0-100 score (integer),
     "status": "Optimal/Low/Critical"
  }},
  "deficiencies": {{
     "NutrientName": {{
       "symptoms": "Visual signs observed",
       "treatment": "Fertilizer/Cure application steps"
     }}
  }},
  "healthy": true/false,
  "advisor_summary": "Professional diagnosis summary and prioritized action plan."
}}

Do not write anything else. Return only the JSON object.
"""

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[

                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        refined_data = json.loads(content)
        
        if refined_data:
            heuristic_results["water_content"] = refined_data.get("water_content", heuristic_results["water_content"])
            
            refined_diseases = refined_data.get("diseases", [])
            heuristic_results["diseases"] = {
                "detected": len(refined_diseases) > 0,
                "diseases": refined_diseases
            }
            
            refined_pests = refined_data.get("pests", [])
            heuristic_results["pests"] = {
                "detected": len(refined_pests) > 0,
                "pests": refined_pests
            }
            
            refined_deficiencies = refined_data.get("deficiencies", {})
            if refined_deficiencies:
                heuristic_results["deficiencies"] = refined_deficiencies
                
            heuristic_results["advisor_summary"] = refined_data.get("advisor_summary", "")
            
    except Exception as e:
        print(f"Error refining analysis with LLM: {e}")
        
    return heuristic_results

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
    
    # Refine results with Groq vision model
    analysis_results = refine_analysis_with_llm(image, analysis_results, plant_details)
    
    return analysis_results