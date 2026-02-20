
# Crop database for PhytoSense App

crops = []

cabbage_data = {
    "name": "Cabbage",
    "scientific_name": "Brassica oleracea var. capitata",
    "best_season": "Spring and Fall (15°C to 20°C)",
    "soil": {
        "type": "Loamy, well-drained, rich in organic matter",
        "pH": "6.0 to 6.5"
    },
    "varieties": [
        "Golden Acre", "Early Jersey Wakefield", "Savoy", "Red Express", "Ruby Ball", "Wintergreen", "Michihili", "Pak Choi"
    ],
    "diseases": [
        {
            "name": "Downy Mildew",
            "symptoms": ["Yellow patches on leaves", "White/grey mold underside", "Wilting"],
            "causes": "Peronospora parasitica (fungus)",
            "cure": ["Metalaxyl + Mancozeb 0.25%", "Fosetyl-Al (Aliette)"],
            "prevention": ["Improve drainage", "Avoid wet foliage during irrigation"]
        },
        {
            "name": "Clubroot",
            "symptoms": ["Root swelling", "Stunted growth", "Yellowing", "Wilting", "Poor head formation"],
            "causes": "Plasmodiophora brassicae (soil-borne protist)",
            "cure": ["Lime to raise pH", "Phosphorus & Potassium", "Trichoderma harzianum"],
            "prevention": ["Crop rotation", "Use resistant varieties", "Neutral pH", "Good sanitation"]
        },
        {
            "name": "Black Rot",
            "symptoms": ["Leaf yellowing", "V-shaped lesions", "Black veins"],
            "causes": "Xanthomonas campestris (bacteria)",
            "cure": ["Copper Oxychloride + Streptocycline", "Pseudomonas fluorescens"],
            "prevention": ["Disease-free seeds", "Crop rotation", "Avoid overhead irrigation"]
        },
        {
            "name": "Alternaria Leaf Spot",
            "symptoms": ["Dark circular spots", "Leaf drop"],
            "causes": "Alternaria brassicae",
            "cure": ["Chlorothalonil or Mancozeb every 10–12 days"],
            "prevention": ["Remove debris", "Air circulation"]
        }
    ],
    "pests": [
        {
            "name": "Aphids",
            "symptoms": ["Curled/yellow leaves", "Sticky residue"],
            "cure": ["Neem oil", "Insecticidal soap"]
        },
        {
            "name": "Cabbage Worms",
            "symptoms": ["Holes in leaves", "Chewed edges"],
            "cure": ["Bacillus thuringiensis (Bt)", "Pyrethrin"]
        },
        {
            "name": "Root Maggot",
            "symptoms": ["Wilting", "Stunted growth"],
            "cure": ["Insecticide-treated soil", "Nematodes"]
        }
    ],
    "deficiencies": [
        {
            "nutrient": "Nitrogen",
            "symptoms": ["Yellow older leaves", "Stunted growth"],
            "cure": ["Urea", "Ammonium Nitrate", "Compost"]
        },
        {
            "nutrient": "Phosphorus",
            "symptoms": ["Reddish-purple leaves", "Poor root development"],
            "cure": ["SSP", "DAP", "Bone meal"]
        },
        {
            "nutrient": "Potassium",
            "symptoms": ["Edge yellowing", "Brown spots", "Weak stems"],
            "cure": ["MOP", "Potassium Sulfate", "Potassium-rich compost"]
        },
        {
            "nutrient": "Calcium",
            "symptoms": ["Tip burn", "Curled leaves"],
            "cure": ["Gypsum", "Lime", "Calcium-rich compost"]
        }
    ]
}
crops.append(cabbage_data)
