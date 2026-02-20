"""
Crop data module for PhytoSense application.
Contains information about crop diseases, pests, and related agricultural data.
"""

# Onion diseases and related information
onion_diseases = {
    "Purple Blotch": {
        "scientific_name": "Alternaria porri",
        "symptoms": "Small, water-soaked lesions that quickly develop purple centers and yellow margins",
        "favorable_conditions": "Temperatures between 21-30°C, high humidity, frequent rains",
        "management": "Crop rotation, fungicide applications, proper plant spacing",
        "chemicals": ["Mancozeb", "Chlorothalonil", "Azoxystrobin"],
        "organic_controls": ["Garlic extract spray", "Neem oil", "Trichoderma harzianum"]
    },
    "Downy Mildew": {
        "scientific_name": "Peronospora destructor",
        "symptoms": "Pale-green to yellow elongated patches on leaves with gray-violet fuzzy growth",
        "favorable_conditions": "Cool temperatures (10-20°C), high humidity, long leaf wetness periods",
        "management": "Plant resistant varieties, minimize leaf wetness, copper-based fungicides",
        "chemicals": ["Metalaxyl", "Chlorothalonil", "Cymoxanil"],
        "organic_controls": ["Copper hydroxide", "Potassium bicarbonate", "Compost tea"]
    },
    "Basal Rot": {
        "scientific_name": "Fusarium oxysporum f.sp. cepae",
        "symptoms": "Yellowing and death of leaf tips, rotting of the basal plate with white mycelium",
        "favorable_conditions": "Warm soil temperatures (25-30°C), soil pH below 6.0",
        "management": "Crop rotation (4+ years), resistant varieties, proper curing of bulbs",
        "chemicals": ["Thiram", "Carbendazim", "Thiophanate-methyl"],
        "organic_controls": ["Trichoderma spp.", "Plant extract of marigold", "Hot water treatment of seeds"]
    },
    "White Rot": {
        "scientific_name": "Sclerotium cepivorum",
        "symptoms": "White fluffy mycelium at the base, black sclerotia, yellowing and wilting of leaves",
        "favorable_conditions": "Soil temperatures of 10-20°C, sclerotia can survive in soil for decades",
        "management": "Long crop rotations, careful water management, disease-free transplants",
        "chemicals": ["Tebuconazole", "Fludioxonil", "Boscalid"],
        "organic_controls": ["Allium extracts", "Trichoderma spp.", "Biofumigation"]
    }
}

# Tomato diseases and related information
tomato_diseases = {
    "Late Blight": {
        "scientific_name": "Phytophthora infestans",
        "symptoms": "Dark, water-soaked lesions on leaves, stems and fruits with white fuzzy growth",
        "favorable_conditions": "Moderate temperatures (10-24°C), high humidity, long leaf wetness periods",
        "management": "Fungicide applications, resistant varieties, proper plant spacing and pruning",
        "chemicals": ["Chlorothalonil", "Mancozeb", "Azoxystrobin"],
        "organic_controls": ["Copper formulations", "Bacillus subtilis", "Potassium bicarbonate"]
    },
    "Early Blight": {
        "scientific_name": "Alternaria solani",
        "symptoms": "Dark brown lesions with concentric rings (target-like) on lower leaves spreading upward",
        "favorable_conditions": "Temperatures of 24-29°C, high humidity, older plant tissue more susceptible",
        "management": "Crop rotation, removal of infected plants, fungicide applications",
        "chemicals": ["Chlorothalonil", "Azoxystrobin", "Difenoconazole"],
        "organic_controls": ["Copper hydroxide", "Neem oil", "Bacillus subtilis"]
    },
    "Septoria Leaf Spot": {
        "scientific_name": "Septoria lycopersici",
        "symptoms": "Small, circular spots with dark brown margins and gray centers with tiny black fruiting bodies",
        "favorable_conditions": "Warm, wet weather, temperatures of 20-27°C, splashing water",
        "management": "Crop rotation, avoid overhead irrigation, fungicide applications, sanitation",
        "chemicals": ["Chlorothalonil", "Mancozeb", "Copper hydroxide"],
        "organic_controls": ["Copper formulations", "Potassium bicarbonate", "Compost tea"]
    },
    "Bacterial Spot": {
        "scientific_name": "Xanthomonas campestris pv. vesicatoria",
        "symptoms": "Small, dark, water-soaked spots on leaves, stems, and fruits that enlarge and turn brownish-red",
        "favorable_conditions": "Warm (24-30°C), humid conditions, overhead irrigation, splashing water",
        "management": "Crop rotation, sanitation, drip irrigation, copper-based bactericides",
        "chemicals": ["Copper hydroxide", "Streptomycin (limited use)", "Acibenzolar-S-methyl"],
        "organic_controls": ["Copper formulations", "Bacillus subtilis", "Neem oil"]
    },
    "Fusarium Wilt": {
        "scientific_name": "Fusarium oxysporum f.sp. lycopersici",
        "symptoms": "Yellowing and wilting of lower leaves, often on one side of the plant, vascular discoloration",
        "favorable_conditions": "Warm soil temperatures (28°C optimal), low soil moisture, acidic soil pH",
        "management": "Resistant varieties, crop rotation, soil solarization, balanced fertilization",
        "chemicals": ["Propiconazole", "Thiophanate-methyl", "Carbendazim"],
        "organic_controls": ["Trichoderma spp.", "Pseudomonas fluorescens", "Mycorrhizal fungi"]
    }
}

# Common crop pests and related information
common_pests = {
    "Aphids": {
        "scientific_name": "Various species (e.g., Aphis gossypii, Myzus persicae)",
        "identification": "Small (1-3mm), soft-bodied insects, often clustered on new growth, various colors",
        "damage": "Stunted growth, leaf curling, transmission of plant viruses, honeydew secretion",
        "management": "Natural predators, insecticidal soaps, neem oil, appropriate chemical insecticides",
        "chemicals": ["Imidacloprid", "Acetamiprid", "Flonicamid"],
        "organic_controls": ["Neem oil", "Insecticidal soap", "Ladybugs", "Lacewings"]
    },
    "Thrips": {
        "scientific_name": "Various species (e.g., Thrips tabaci, Frankliniella occidentalis)",
        "identification": "Tiny (1-2mm), slender insects with fringed wings, difficult to see without magnification",
        "damage": "Silvery stippling on leaves, leaf distortion, scarring of fruits, transmission of viruses",
        "management": "Blue/yellow sticky traps, insecticides, remove weed hosts, reflective mulches",
        "chemicals": ["Spinosad", "Spinetoram", "Abamectin"],
        "organic_controls": ["Spinosad", "Neem oil", "Predatory mites", "Minute pirate bugs"]
    },
    "Whiteflies": {
        "scientific_name": "Various species (e.g., Bemisia tabaci, Trialeurodes vaporariorum)",
        "identification": "Tiny (1-2mm) white insects that fly when disturbed, congregate on leaf undersides",
        "damage": "Yellowing of leaves, stunted growth, honeydew secretion, transmission of viruses",
        "management": "Yellow sticky traps, natural enemies, neem oil, appropriate insecticides",
        "chemicals": ["Pyriproxyfen", "Dinotefuran", "Spiromesifen"],
        "organic_controls": ["Neem oil", "Insecticidal soap", "Beauveria bassiana", "Encarsia formosa wasps"]
    },
    "Spider Mites": {
        "scientific_name": "Various species (e.g., Tetranychus urticae)",
        "identification": "Tiny (0.5mm) arachnids, often forming webbing on plants, various colors",
        "damage": "Fine stippling on leaves, yellowing or bronzing of foliage, webbing on plants",
        "management": "High humidity, water sprays, predatory mites, miticides when necessary",
        "chemicals": ["Abamectin", "Bifenazate", "Etoxazole"],
        "organic_controls": ["Predatory mites", "Neem oil", "Insecticidal soap", "Sulfur"]
    },
    "Tomato Hornworm": {
        "scientific_name": "Manduca quinquemaculata",
        "identification": "Large (up to 10cm) green caterpillars with diagonal white stripes and a horn-like projection",
        "damage": "Extensive defoliation, feeding on fruits, significant damage to tomato plants",
        "management": "Handpicking, natural enemies (parasitic wasps), Bacillus thuringiensis",
        "chemicals": ["Carbaryl", "Permethrin", "Spinosad"],
        "organic_controls": ["Bacillus thuringiensis (Bt)", "Handpicking", "Parasitic wasps"]
    }
}

# Maharashtra-specific crop varieties and recommendations
maharashtra_crop_varieties = {
    "Rice": {
        "recommended_varieties": [
            "Indrayani", "Kundalika", "Ratna", "Jaya", "Karjat-184", "Karjat-7", 
            "Sahyadri-1", "Sahyadri-2", "Sahyadri-3", "Sahyadri-4"
        ],
        "planting_seasons": ["Kharif (June-July)", "Summer (Jan-Feb)"],
        "special_recommendations": "For Konkan region, prefer salt-tolerant varieties like Karjat series. For drought conditions, use Sahyadri series."
    },
    "Cotton": {
        "recommended_varieties": [
            "AKH-081", "NHH-44", "PKV Rajat", "PKVHY-2", "Phule Dhanwantari", 
            "AKA-7", "AKA-8", "JLA-794", "Suraj"
        ],
        "planting_seasons": ["Kharif (June-July after onset of monsoon)"],
        "special_recommendations": "Bt cotton hybrids suitable for Vidarbha and Marathwada regions. For rainfed conditions, prefer early maturing varieties."
    },
    "Sugarcane": {
        "recommended_varieties": [
            "Co 86032", "Co 94012", "CoM 0265", "CoC 671", "CoVSI 9805", 
            "Co 86032", "Co 86249", "Co 92005", "CoM 88121"
        ],
        "planting_seasons": ["Adsali (Jul-Aug)", "Pre-seasonal (Oct-Nov)", "Suru (Jan-Feb)"],
        "special_recommendations": "Co 86032 performs well across Maharashtra. For drought conditions, prefer CoM 88121."
    },
    "Tomato": {
        "recommended_varieties": [
            "Pusa Ruby", "Punjab Chhuhara", "Arka Vikas", "Pusa Early Dwarf", 
            "Sioux", "Punjab Kesri", "Hisar Arun", "Hisar Lalit"
        ],
        "planting_seasons": ["Kharif (June-July)", "Rabi (Oct-Nov)"],
        "special_recommendations": "For processing, prefer Punjab Chhuhara. For fresh market, Pusa Ruby and Arka Vikas are suitable."
    },
    "Onion": {
        "recommended_varieties": [
            "Phule Samarth", "Bhima Super", "Bhima Red", "Agrifound Dark Red", 
            "Agrifound Light Red", "N-53", "Baswant 780", "Phule Suvarna"
        ],
        "planting_seasons": ["Kharif (May-June)", "Late Kharif (Aug-Sep)", "Rabi (Oct-Nov)"],
        "special_recommendations": "For Kharif season, prefer N-53, Baswant 780. For Rabi, prefer Agrifound Dark Red, Bhima Super."
    },
    "Wheat": {
        "recommended_varieties": [
            "MACS 6478", "HD 2189", "LOK-1", "NIAW 301", "NIAW 917", 
            "HD 2932", "NIAW 34", "HD 3090", "GW 322", "PBW 550"
        ],
        "planting_seasons": ["Rabi (Nov-Dec)"],
        "special_recommendations": "For timely sowing, prefer MACS 6478, HD 2189. For late sowing, prefer HD 2932, NIAW 34."
    }
}

# Soil type data for Maharashtra
maharashtra_soil_types = {
    "Black Cotton Soil (Regur)": {
        "characteristics": "Deep black, clayey, high water retention, poor drainage, high fertility",
        "distribution": "Deccan Plateau - Marathwada, parts of Vidarbha",
        "suitable_crops": ["Cotton", "Sugarcane", "Wheat", "Jowar", "Onion"],
        "management": "Requires good drainage, deep plowing, addition of organic matter"
    },
    "Red Soil": {
        "characteristics": "Reddish, sandy to loamy, well-drained, moderate fertility",
        "distribution": "Eastern Vidarbha, parts of Western Maharashtra",
        "suitable_crops": ["Millets", "Pulses", "Groundnut", "Citrus", "Vegetables"],
        "management": "Requires regular addition of organic matter, irrigation, mulching"
    },
    "Laterite Soil": {
        "characteristics": "Red to reddish-brown, acidic, poor fertility, high iron content",
        "distribution": "Konkan coastal region, Western Ghats",
        "suitable_crops": ["Rice", "Coconut", "Cashew", "Mango", "Spices"],
        "management": "Requires lime application, heavy manuring, micronutrient supplementation"
    },
    "Alluvial Soil": {
        "characteristics": "Loamy to clayey, rich in minerals, good fertility, well-drained",
        "distribution": "River valleys - Godavari, Krishna, Tapi, Purna",
        "suitable_crops": ["Rice", "Wheat", "Sugarcane", "Vegetables", "Fruits"],
        "management": "Requires balanced fertilization, crop rotation, regular irrigation"
    },
    "Coastal Sandy Soil": {
        "characteristics": "Sandy, poor water retention, low fertility, saline in nature",
        "distribution": "Coastal areas of Konkan",
        "suitable_crops": ["Coconut", "Betel nut", "Cashew", "Watermelon"],
        "management": "Requires heavy organic matter application, frequent irrigation, mulching"
    }
}

# Water requirement data for major crops (in mm throughout growing season)
crop_water_requirements = {
    "Rice": {
        "total_water_requirement": "1200-1500 mm",
        "critical_stages": ["Tillering", "Panicle initiation", "Flowering"],
        "irrigation_schedule": "Maintain 5 cm standing water until 2 weeks before harvest"
    },
    "Wheat": {
        "total_water_requirement": "450-650 mm",
        "critical_stages": ["Crown root initiation", "Tillering", "Jointing", "Flowering", "Grain filling"],
        "irrigation_schedule": "First at 21-25 days, then at 40-45, 60-65, 80-85, and 100-105 days"
    },
    "Cotton": {
        "total_water_requirement": "700-1200 mm",
        "critical_stages": ["Squaring", "Flowering", "Boll development"],
        "irrigation_schedule": "At 10-15 day intervals during critical stages"
    },
    "Sugarcane": {
        "total_water_requirement": "1500-2500 mm",
        "critical_stages": ["Germination", "Tillering", "Grand growth", "Maturity"],
        "irrigation_schedule": "At 7-10 day intervals in summer, 15-20 days in winter"
    },
    "Tomato": {
        "total_water_requirement": "600-800 mm",
        "critical_stages": ["Vegetative growth", "Flowering", "Fruit development"],
        "irrigation_schedule": "Regular intervals of 3-5 days, 5-7 liters per plant per day"
    },
    "Onion": {
        "total_water_requirement": "350-550 mm",
        "critical_stages": ["Vegetative growth", "Bulb formation", "Bulb development"],
        "irrigation_schedule": "Light but frequent irrigation, stop 15-20 days before harvest"
    }
}