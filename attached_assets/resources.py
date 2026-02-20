import streamlit as st
import pandas as pd

def get_seasonal_crops():
    """
    Return information about seasonal crops
    """
    seasonal_data = {
        "Kharif (Monsoon)": {
            "Season": "June to October",
            "Crops": "Rice, Maize, Jowar, Bajra, Tur, Moong, Urad, Cotton, Jute, Groundnut, Soybean",
            "Requirements": "Requires warm, wet weather for growth and a dry spell during harvest",
            "Regions": "Throughout India, especially in regions with good rainfall"
        },
        "Rabi (Winter)": {
            "Season": "October to March",
            "Crops": "Wheat, Barley, Oats, Gram, Pea, Mustard, Linseed",
            "Requirements": "Cool weather during growth and warm weather during harvest",
            "Regions": "Northern and Central India"
        },
        "Zaid (Summer)": {
            "Season": "March to June",
            "Crops": "Watermelon, Cucumber, Muskmelon, Vegetables",
            "Requirements": "Warm dry weather, irrigation facilities necessary",
            "Regions": "Areas with irrigation facilities"
        }
    }
    return seasonal_data

def get_soil_types():
    """
    Return information about different soil types
    """
    soil_data = {
        "Alluvial Soil": {
            "Description": "Deposited by rivers, highly fertile",
            "Regions": "Indo-Gangetic plains, eastern coastal plains, deltas",
            "Suitable Crops": "Rice, wheat, sugarcane, cotton, jute",
            "Characteristics": "Rich in potash, phosphoric acid, lime",
            "Management": "Regular crop rotation, moderate irrigation"
        },
        "Black Soil (Regur)": {
            "Description": "Rich in clay, retains moisture",
            "Regions": "Deccan Plateau - Maharashtra, Gujarat, MP",
            "Suitable Crops": "Cotton, sugarcane, tobacco, wheat, jowar, linseed",
            "Characteristics": "Rich in calcium carbonate, magnesium, potash",
            "Management": "Careful irrigation to prevent waterlogging"
        },
        "Red Soil": {
            "Description": "Red due to iron oxide presence",
            "Regions": "Tamil Nadu, Karnataka, Andhra Pradesh, eastern Rajasthan",
            "Suitable Crops": "Pulses, millets, tobacco, oilseeds, potatoes",
            "Characteristics": "Sandy texture, porous",
            "Management": "Requires fertilizers, proper irrigation"
        },
        "Laterite Soil": {
            "Description": "Formed under high temperature and rainfall with alternating wet and dry periods",
            "Regions": "Karnataka, Kerala, Tamil Nadu, hills of Maharashtra and Orissa",
            "Suitable Crops": "Cashew, rubber, tea, coffee, coconut",
            "Characteristics": "Poor in organic matter, rich in iron",
            "Management": "Requires heavy fertilization, proper drainage"
        },
        "Arid/Desert Soil": {
            "Description": "Sandy with low organic matter",
            "Regions": "Rajasthan, western Gujarat, Haryana, Punjab",
            "Suitable Crops": "Drought-resistant crops like millets, barley, cotton, maize",
            "Characteristics": "Low humus content, high salt content",
            "Management": "Extensive irrigation, addition of organic matter"
        },
        "Mountain Soil": {
            "Description": "Varies in different altitudes",
            "Regions": "Himalayan region, Western and Eastern Ghats",
            "Suitable Crops": "Tea, coffee, spices, tropical and temperate fruits",
            "Characteristics": "Rich in humus, acidic at higher elevations",
            "Management": "Terracing, contour farming to prevent erosion"
        }
    }
    return soil_data

def get_major_crops():
    """
    Return information about major crops
    """
    crops_data = {
        "Rice": {
            "Growing Season": "Kharif (mainly)",
            "Regions": "West Bengal, UP, Punjab, Andhra Pradesh, Bihar, Chhattisgarh",
            "Water Requirements": "High (100-120 cm)",
            "Temperature": "22-32°C",
            "Soil Type": "Clayey or loamy soil with good water retention",
            "Key Care": "Standing water needed for first few weeks, regular weeding"
        },
        "Wheat": {
            "Growing Season": "Rabi",
            "Regions": "UP, Punjab, Haryana, Rajasthan, MP, Bihar",
            "Water Requirements": "Moderate (40-50 cm)",
            "Temperature": "15-25°C",
            "Soil Type": "Well-drained loamy soil",
            "Key Care": "5-6 irrigations at critical growth stages"
        },
        "Maize": {
            "Growing Season": "Kharif, Rabi and Zaid",
            "Regions": "Karnataka, Andhra Pradesh, Tamil Nadu, Rajasthan, MP",
            "Water Requirements": "Moderate (50-75 cm)",
            "Temperature": "21-27°C",
            "Soil Type": "Well-drained sandy loam to clay loam",
            "Key Care": "Frequent light irrigation, protection from waterlogging"
        },
        "Cotton": {
            "Growing Season": "Kharif",
            "Regions": "Maharashtra, Gujarat, Telangana, Punjab, Haryana",
            "Water Requirements": "Moderate (60-100 cm)",
            "Temperature": "21-30°C",
            "Soil Type": "Black cotton soil, alluvial soil, red sandy loam",
            "Key Care": "Protection from bollworms, adequate drainage"
        },
        "Sugarcane": {
            "Growing Season": "Year-round crop (12-18 months)",
            "Regions": "UP, Maharashtra, Karnataka, Tamil Nadu, Gujarat",
            "Water Requirements": "High (150-250 cm)",
            "Temperature": "21-27°C",
            "Soil Type": "Deep, well-drained loamy soil",
            "Key Care": "Regular irrigation, protection from pests"
        },
        "Pulses": {
            "Growing Season": "Mainly Rabi (gram, peas) and Kharif (tur, moong, urad)",
            "Regions": "MP, Maharashtra, Rajasthan, UP, Karnataka",
            "Water Requirements": "Low to moderate (30-50 cm)",
            "Temperature": "20-30°C",
            "Soil Type": "Well-drained loamy soil",
            "Key Care": "Good drainage, protection from excess moisture"
        },
        "Oilseeds": {
            "Growing Season": "Varies by crop (groundnut: Kharif; mustard: Rabi)",
            "Regions": "Gujarat, Rajasthan, MP, Maharashtra, Telangana",
            "Water Requirements": "Low to moderate (30-60 cm)",
            "Temperature": "20-30°C",
            "Soil Type": "Well-drained light to medium soils",
            "Key Care": "Protection from pests, adequate soil fertility"
        }
    }
    return crops_data

def get_maharashtra_specific():
    """
    Return Maharashtra-specific farming information
    """
    maharashtra_data = {
        "Major Agricultural Zones": {
            "Western Maharashtra": "Sugarcane, grapes, pomegranate, banana",
            "Vidarbha": "Cotton, soybean, oranges",
            "Marathwada": "Jowar, bajra, cotton, pulses",
            "Konkan": "Rice, coconut, cashew, mango"
        },
        "Special Crops": {
            "Alphonso Mango": "Ratnagiri, Sindhudurg, Raigad",
            "Nagpur Orange": "Vidarbha region",
            "Grapes": "Nashik, Sangli, Solapur",
            "Cotton": "Vidarbha, Marathwada",
            "Sugarcane": "Western Maharashtra"
        },
        "Rainfall Patterns": {
            "Konkan": "Heavy (2000-3000 mm annually)",
            "Western Maharashtra": "Moderate (700-1000 mm annually)",
            "Marathwada": "Low (500-700 mm annually)",
            "Vidarbha": "Moderate (700-900 mm annually)"
        },
        "Major Water Resources": {
            "Rivers": "Godavari, Krishna, Tapi, Narmada, Bhima",
            "Major Dams": "Koyna, Jayakwadi, Ujani, Bhandardara"
        },
        "Agricultural Challenges": {
            "Drought": "Marathwada and parts of Vidarbha frequently affected",
            "Water Management": "Critical in drought-prone regions",
            "Soil Erosion": "Western Ghats and hilly regions",
            "Market Access": "Improving but still a challenge in remote areas"
        }
    }
    return maharashtra_data

def get_farming_techniques():
    """
    Return information about different farming techniques
    """
    techniques_data = {
        "Traditional Farming": {
            "Description": "Age-old farming methods using traditional tools and practices",
            "Advantages": "Low initial investment, locally adapted practices",
            "Disadvantages": "Labor intensive, lower yields",
            "Suitable For": "Small land holdings, resource-poor farmers"
        },
        "Organic Farming": {
            "Description": "Farming without synthetic fertilizers and pesticides",
            "Advantages": "Environment-friendly, premium prices, soil health improvement",
            "Disadvantages": "Initially lower yields, labor intensive, certification challenges",
            "Suitable For": "Health-conscious markets, export-oriented crops, areas with good organic matter availability"
        },
        "Precision Farming": {
            "Description": "Using technology to optimize inputs and maximize yields",
            "Advantages": "Resource efficient, higher yields, reduced wastage",
            "Disadvantages": "High initial cost, requires technical knowledge",
            "Suitable For": "Large farms, high-value crops, resource-scarce regions"
        },
        "Conservation Agriculture": {
            "Description": "Minimal soil disturbance, permanent soil cover, crop rotation",
            "Advantages": "Soil conservation, reduced erosion, better moisture retention",
            "Disadvantages": "Weed management challenges, specialized equipment needed",
            "Suitable For": "Erosion-prone areas, drought-prone regions"
        },
        "Integrated Farming": {
            "Description": "Combining crops with livestock, fisheries, or other enterprises",
            "Advantages": "Risk distribution, effective resource cycling, multiple income sources",
            "Disadvantages": "Complex management, diverse skill requirements",
            "Suitable For": "Small to medium farms, areas with diverse resources"
        },
        "Hydroponics": {
            "Description": "Growing plants without soil, using nutrient solutions",
            "Advantages": "Water efficient, higher yields, no soil-borne diseases",
            "Disadvantages": "High setup cost, technical complexity, energy dependent",
            "Suitable For": "Water-scarce regions, high-value vegetables and herbs, urban farming"
        }
    }
    return techniques_data

def get_irrigation_methods():
    """
    Return information about different irrigation methods
    """
    irrigation_data = {
        "Flood Irrigation": {
            "Description": "Traditional method of flooding fields with water",
            "Efficiency": "40-50%",
            "Suitable Crops": "Rice, wheat in flat lands",
            "Advantages": "Simple, low initial cost",
            "Disadvantages": "Water wastage, uneven distribution, waterlogging"
        },
        "Drip Irrigation": {
            "Description": "Water applied slowly to the root zone of plants",
            "Efficiency": "90-95%",
            "Suitable Crops": "Fruit trees, vegetables, row crops",
            "Advantages": "Highly efficient, reduced weed growth, uniform application",
            "Disadvantages": "High initial cost, maintenance needs, clogging issues"
        },
        "Sprinkler Irrigation": {
            "Description": "Water sprayed through nozzles in a controlled manner",
            "Efficiency": "70-80%",
            "Suitable Crops": "Field crops, vegetables, lawns",
            "Advantages": "Suitable for rolling terrain, good for sandy soils",
            "Disadvantages": "Wind drift, higher evaporation loss, high energy requirement"
        },
        "Furrow Irrigation": {
            "Description": "Water flows through small channels between crop rows",
            "Efficiency": "50-60%",
            "Suitable Crops": "Row crops like corn, sugarcane",
            "Advantages": "Lower cost than drip/sprinkler, less land leveling needed",
            "Disadvantages": "Water loss through deep percolation, runoff"
        },
        "Micro-irrigation": {
            "Description": "Low volume application near plant roots",
            "Efficiency": "85-90%",
            "Suitable Crops": "High-value crops, orchards, plantations",
            "Advantages": "Very efficient, can apply fertilizers directly",
            "Disadvantages": "High technical knowledge, maintenance requirements"
        },
        "Subsurface Irrigation": {
            "Description": "Water applied below the soil surface",
            "Efficiency": "95-100%",
            "Suitable Crops": "Tree crops, field crops in areas with high water table",
            "Advantages": "Minimal evaporation loss, reduced weed growth",
            "Disadvantages": "Installation complexity, root intrusion issues"
        }
    }
    return irrigation_data

def show_resources_page():
    """
    Display agricultural resources and information
    """
    st.title("Farming Resources")
    st.write("This comprehensive guide provides essential information for farmers about crops, soils, and farming practices.")
    
    tabs = st.tabs(["Seasonal Crops", "Soil Types", "Major Crops", "Maharashtra Guide", "Farming Techniques", "Irrigation Methods"])
    
    with tabs[0]:
        st.header("Seasonal Farming Calendar")
        st.write("Understanding crop seasons is crucial for successful farming in India")
        
        seasonal_data = get_seasonal_crops()
        for season, data in seasonal_data.items():
            with st.expander(f"🌱 {season}"):
                for key, value in data.items():
                    st.markdown(f"**{key}:** {value}")
    
    with tabs[1]:
        st.header("Soil Types and Properties")
        st.write("Different soils have unique properties and are suitable for specific crops")
        
        soil_data = get_soil_types()
        for soil, data in soil_data.items():
            with st.expander(f"🌍 {soil}"):
                for key, value in data.items():
                    st.markdown(f"**{key}:** {value}")
                
    with tabs[2]:
        st.header("Major Crops of India")
        st.write("Information about key crops grown across India and their requirements")
        
        crops_data = get_major_crops()
        for crop, data in crops_data.items():
            with st.expander(f"🌾 {crop}"):
                for key, value in data.items():
                    st.markdown(f"**{key}:** {value}")
    
    with tabs[3]:
        st.header("Maharashtra Agriculture Guide")
        st.write("Region-specific agricultural information for Maharashtra farmers")
        
        maharashtra_data = get_maharashtra_specific()
        for category, data in maharashtra_data.items():
            with st.expander(f"📍 {category}"):
                for key, value in data.items():
                    st.markdown(f"**{key}:** {value}")
    
    with tabs[4]:
        st.header("Modern Farming Techniques")
        st.write("Different approaches to agriculture with their advantages and challenges")
        
        techniques_data = get_farming_techniques()
        for technique, data in techniques_data.items():
            with st.expander(f"🔧 {technique}"):
                for key, value in data.items():
                    st.markdown(f"**{key}:** {value}")
    
    with tabs[5]:
        st.header("Irrigation Methods")
        st.write("Different ways to irrigate crops with their efficiency and suitability")
        
        irrigation_data = get_irrigation_methods()
        for method, data in irrigation_data.items():
            with st.expander(f"💧 {method}"):
                for key, value in data.items():
                    st.markdown(f"**{key}:** {value}")
    
    st.info("This information is meant as a general guide. For specific recommendations, consult with your local agricultural extension service.")