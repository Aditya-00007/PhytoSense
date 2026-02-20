import numpy as np
import random
from model import SOIL_CLASSES

def analyze_soil(model, image):
    """
    Analyze soil from an image
    
    Args:
        model: Loaded soil analysis model
        image: Preprocessed image as numpy array
        
    Returns:
        Dictionary containing soil analysis results
    """
    # In a real system, we would use the model for inference
    # For now, we'll simulate predictions based on image characteristics
    
    # Calculate color features
    avg_color = np.mean(image, axis=(0, 1))
    r, g, b = avg_color[0], avg_color[1], avg_color[2]
    
    # Calculate texture features (simplistic approach)
    std_color = np.std(image, axis=(0, 1))
    texture_complexity = np.mean(std_color)
    
    # Simulate soil type prediction based on color and texture
    # This is just for demonstration - a real system would use the trained model
    
    # Use simplified rules for soil type classification
    if r > 0.6 and g < 0.4:  # Reddish
        soil_type_index = 1  # Red Soil
    elif r > 0.4 and g > 0.4 and b < 0.3:  # Brownish-yellow
        soil_type_index = 3  # Alluvial Soil
    elif r < 0.3 and g < 0.3 and b < 0.3:  # Dark
        soil_type_index = 0  # Black Soil
    elif r > 0.5 and g > 0.5 and b > 0.4:  # Light colored
        soil_type_index = 4  # Coastal Sandy Soil
    else:  # Other
        soil_type_index = 2  # Laterite Soil
    
    # Add some randomness for demonstration
    if random.random() < 0.3:
        soil_type_index = random.randint(0, len(SOIL_CLASSES) - 1)
    
    soil_type = SOIL_CLASSES[soil_type_index]
    
    # Process soil analysis based on predicted soil type
    return get_soil_details(soil_type)

def get_soil_details(soil_type):
    """
    Get detailed information about a soil type
    
    Args:
        soil_type: String indicating soil type
        
    Returns:
        Dictionary containing detailed soil information
    """
    soil_details = {
        "Black Soil": {
            "characteristics": """
            - High clay content (30-80%)
            - Good water retention capacity
            - Rich in calcium, magnesium, potassium, and lime
            - Poor drainage when wet
            - Deep cracks when dry
            - pH range: 7.5-8.5 (slightly alkaline)
            """,
            "suitability": {
                "onion": "Excellent for onion cultivation with proper drainage. Rich in nutrients required for bulb development.",
                "tomato": "Good for tomato cultivation, but may need drainage improvements and pH adjustment."
            },
            "recommendations": """
            ### Recommendations for Black Soil:
            
            1. **Drainage Management:**
               - Create raised beds to improve drainage
               - Add organic matter to improve soil structure
               - Implement drip irrigation to control water distribution
            
            2. **Soil Amendments:**
               - Add gypsum (500 kg/ha) to improve soil structure
               - Incorporate well-decomposed FYM (15-20 tonnes/ha)
               - Apply sulfur if pH is above 8.0
            
            3. **Crop-Specific Recommendations:**
               - **For Onions:** Add phosphorus-rich fertilizers before planting
               - **For Tomatoes:** Adjust pH using elemental sulfur if necessary
            """,
            "properties": {
                "ph": "7.8",
                "organic_matter": "Medium",
                "drainage": "Poor to Moderate"
            }
        },
        
        "Red Soil": {
            "characteristics": """
            - Sandy to loamy texture
            - Low water retention capacity
            - Rich in iron oxides (gives red color)
            - Low organic matter content
            - Good drainage
            - pH range: 5.5-6.8 (slightly acidic)
            """,
            "suitability": {
                "onion": "Moderately suitable for onions. Requires additional organic matter and regular irrigation.",
                "tomato": "Well-suited for tomatoes with proper fertilization and irrigation management."
            },
            "recommendations": """
            ### Recommendations for Red Soil:
            
            1. **Organic Matter Enhancement:**
               - Add compost or well-rotted manure (20-25 tonnes/ha)
               - Implement green manuring practices
               - Use mulching to conserve soil moisture
            
            2. **Nutrient Management:**
               - Apply balanced NPK fertilizers
               - Incorporate micronutrient mixtures containing zinc, boron, and manganese
               - Use split application of nitrogen fertilizers
            
            3. **Crop-Specific Recommendations:**
               - **For Onions:** Ensure regular water supply and add potassium fertilizers
               - **For Tomatoes:** Apply calcium-rich amendments to prevent blossom end rot
            """,
            "properties": {
                "ph": "6.2",
                "organic_matter": "Low",
                "drainage": "Good"
            }
        },
        
        "Laterite Soil": {
            "characteristics": """
            - Highly weathered soil with sesquioxides
            - Poor in organic matter and nutrients
            - Porous and well-drained
            - High iron and aluminum content
            - Acidic in nature
            - pH range: 4.5-6.0 (acidic)
            """,
            "suitability": {
                "onion": "Poor suitability for onions. Requires significant soil amendments and pH correction.",
                "tomato": "Moderate suitability with proper liming and nutrient management."
            },
            "recommendations": """
            ### Recommendations for Laterite Soil:
            
            1. **pH Correction:**
               - Apply agricultural lime (1-2 tonnes/ha)
               - Use dolomitic lime for magnesium supplementation
               - Retest soil pH after 3-4 months
            
            2. **Fertility Enhancement:**
               - Incorporate high rates of organic matter (25-30 tonnes/ha)
               - Apply rock phosphate for slow phosphorus release
               - Use balanced NPK fertilizers with micronutrients
            
            3. **Crop-Specific Recommendations:**
               - **For Onions:** Create raised beds with amended soil mixture
               - **For Tomatoes:** Apply vermicompost and use mulching
            """,
            "properties": {
                "ph": "5.3",
                "organic_matter": "Very Low",
                "drainage": "Excessive"
            }
        },
        
        "Alluvial Soil": {
            "characteristics": """
            - Deposited by rivers and streams
            - Varying texture (sandy to clayey)
            - Rich in potash and lime
            - Good fertility and moisture retention
            - Moderate to good drainage
            - pH range: 6.5-7.5 (neutral)
            """,
            "suitability": {
                "onion": "Excellent for onion cultivation. Naturally fertile with good physical properties.",
                "tomato": "Highly suitable for tomatoes with minimal amendments required."
            },
            "recommendations": """
            ### Recommendations for Alluvial Soil:
            
            1. **Maintenance Practices:**
               - Add organic matter annually (10-15 tonnes/ha)
               - Implement crop rotation with legumes
               - Use conservation tillage practices
            
            2. **Nutrient Management:**
               - Apply balanced fertilizers based on soil test results
               - Use micronutrient supplements if deficiency symptoms appear
               - Implement split application of nitrogen
            
            3. **Crop-Specific Recommendations:**
               - **For Onions:** Regular but controlled irrigation to prevent disease
               - **For Tomatoes:** Stake plants and maintain optimal spacing
            """,
            "properties": {
                "ph": "7.0",
                "organic_matter": "Medium to High",
                "drainage": "Good"
            }
        },
        
        "Coastal Sandy Soil": {
            "characteristics": """
            - High sand content (>70%)
            - Very low water retention
            - Poor in organic matter and nutrients
            - Excellent drainage (often excessive)
            - May have salinity issues
            - pH range: 7.0-8.5 (neutral to alkaline)
            """,
            "suitability": {
                "onion": "Poor suitability for onions without significant amendments. Requires intensive management.",
                "tomato": "Moderate suitability with irrigation, mulching, and nutrient management."
            },
            "recommendations": """
            ### Recommendations for Coastal Sandy Soil:
            
            1. **Water Management:**
               - Install drip irrigation systems
               - Use mulching extensively to conserve moisture
               - Apply hydrogels for improving water retention
            
            2. **Soil Improvement:**
               - Add clay or silt-rich soil to improve texture
               - Incorporate very high rates of organic matter (30-40 tonnes/ha)
               - Use cocopeat or vermiculite as soil amendments
            
            3. **Crop-Specific Recommendations:**
               - **For Onions:** Consider container or raised bed cultivation
               - **For Tomatoes:** Use salt-tolerant varieties and mulching
            """,
            "properties": {
                "ph": "7.7",
                "organic_matter": "Very Low",
                "drainage": "Excessive"
            }
        }
    }
    
    # Return details for the specific soil type or a default message
    return soil_details.get(soil_type, {
        "soil_type": soil_type,
        "characteristics": "Information not available for this soil type.",
        "suitability": {
            "onion": "Information not available.",
            "tomato": "Information not available."
        },
        "recommendations": "Specific recommendations not available for this soil type.",
        "properties": {
            "ph": "Unknown",
            "organic_matter": "Unknown",
            "drainage": "Unknown"
        }
    })