def get_local_recommendations(crop):
    """
    Get crop-specific recommendations for Maharashtra region
    
    Args:
        crop (str): Crop name
        
    Returns:
        dict: Dictionary containing Maharashtra-specific recommendations
    """
    # Base recommendations applicable to most crops in Maharashtra
    base_recommendations = {
        "irrigation": {
            "title": "Irrigation Practices",
            "content": "Maharashtra frequently faces water scarcity. Consider drip irrigation to conserve water while improving crop yields."
        },
        "climate": {
            "title": "Climate Considerations",
            "content": "Maharashtra has diverse climate zones. Be aware of monsoon patterns and prepare for occasional drought conditions."
        },
        "soil": {
            "title": "Soil Management",
            "content": "Most Maharashtra soils benefit from organic matter addition to improve water retention and fertility."
        }
    }
    
    # Crop-specific recommendations for Maharashtra
    crop_specific = {
        "Tomato": {
            "varieties": {
                "title": "Recommended Varieties",
                "content": "For Maharashtra: Pusa Ruby, Arka Vikas, Arka Saurabh, and Pusa Early Dwarf perform well in local conditions."
            },
            "planting": {
                "title": "Planting Season",
                "content": "Best planted from June-July (kharif) or November-December (rabi) in Maharashtra."
            },
            "pests": {
                "title": "Local Pest Management",
                "content": "Fruit borer and leaf curl virus are common in Maharashtra tomato crops. Consider neem-based sprays and resistant varieties."
            },
            "markets": {
                "title": "Market Information",
                "content": "Major tomato markets in Maharashtra include Pimpalgaon, Nashik, and Pune APMC."
            }
        },
        "Onion": {
            "varieties": {
                "title": "Recommended Varieties",
                "content": "For Maharashtra: N-53, Agrifound Dark Red, Baswant 780, and Phule Samarth are well adapted to local conditions."
            },
            "planting": {
                "title": "Planting Season",
                "content": "In Maharashtra, kharif onions are planted in May-June, and rabi onions in October-November for best results."
            },
            "storage": {
                "title": "Storage Practices",
                "content": "Store in well-ventilated structures with proper curing. Maharashtra's Nashik district has specialized onion storage structures (chawls) that can be adapted."
            },
            "markets": {
                "title": "Market Information",
                "content": "Lasalgaon in Nashik district hosts India's largest onion market. Other major markets include Pune and Solapur APMC."
            }
        },
        "Potato": {
            "varieties": {
                "title": "Recommended Varieties",
                "content": "For Maharashtra: Kufri Jyoti, Kufri Pukhraj, and Kufri Surya perform well in local conditions."
            },
            "planting": {
                "title": "Planting Season",
                "content": "In Maharashtra, best planted from October to November as a rabi crop."
            },
            "irrigation": {
                "title": "Irrigation Needs",
                "content": "In Maharashtra's often water-scarce conditions, consider furrow irrigation with careful scheduling to conserve water."
            },
            "markets": {
                "title": "Market Information",
                "content": "Major potato markets in Maharashtra include Pune, Nashik, and Mumbai APMC."
            }
        },
        "Corn": {
            "varieties": {
                "title": "Recommended Varieties",
                "content": "For Maharashtra: African Tall (fodder), Ganga, Deccan, and Pro Agro 4212 hybrids perform well."
            },
            "planting": {
                "title": "Planting Season",
                "content": "Kharif corn is planted with the onset of monsoon (June-July) in Maharashtra."
            },
            "irrigation": {
                "title": "Irrigation Management",
                "content": "Critical irrigation periods are silking and tasseling stages. In Maharashtra's drought-prone areas, consider rainwater harvesting."
            },
            "markets": {
                "title": "Market Information",
                "content": "Major corn markets in Maharashtra include Jalgaon, Ahmednagar, and Pune APMC."
            }
        },
        "Bell Pepper": {
            "varieties": {
                "title": "Recommended Varieties",
                "content": "For Maharashtra: California Wonder, Bharat, and Indra are suitable varieties."
            },
            "planting": {
                "title": "Planting Season",
                "content": "In Maharashtra, best transplanted from October to November for winter season cultivation."
            },
            "protection": {
                "title": "Climate Protection",
                "content": "In Maharashtra's hotter regions, consider partial shade or row covers to protect from extreme heat."
            },
            "markets": {
                "title": "Market Information",
                "content": "Major markets for bell peppers in Maharashtra include Mumbai, Pune, and Nagpur."
            }
        }
    }
    
    # Get crop-specific recommendations or use default
    specific_recs = crop_specific.get(crop, {})
    
    # Combine base and crop-specific recommendations
    recommendations = {
        "general": base_recommendations,
        "specific": specific_recs,
        "resources": {
            "title": "Maharashtra Agricultural Resources",
            "content": [
                {
                    "name": "Maharashtra Krishi Vibhag (Agriculture Department)",
                    "link": "https://krishi.maharashtra.gov.in/"
                },
                {
                    "name": "Mahabeej (Maharashtra State Seeds Corporation)",
                    "link": "http://mahabeej.com/"
                },
                {
                    "name": "Maharashtra Agricultural Universities",
                    "link": "https://www.mcaer.org/"
                }
            ]
        }
    }
    
    return recommendations