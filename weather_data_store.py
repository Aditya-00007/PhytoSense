
# -----------------------------------------------------------------------------
# WEATHER INTELLIGENCE DATASETS (Crop-Specific)
# -----------------------------------------------------------------------------

TOMATO_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 12),
            "impact": "Slow growth and flower drop risk",
            "actions": [
                "Cover plants at night using plastic sheet or old cloth.",
                "Irrigate lightly in the morning to warm the soil.",
                "Apply 1% potassium nitrate foliar spray.",
                "Add straw mulch around root zone."
            ]
        },
        "optimal_growth": {
            "range": (18, 30),
            "impact": "Best growth and fruit setting",
            "actions": [
                "Run drip irrigation once daily in morning.",
                "Apply 19:19:19 fertilizer through drip every 10–12 days.",
                "Spray neem oil (3 ml/L) in evening for pest prevention.",
                "Remove lower leaves touching soil."
            ]
        },
        "heat_stress": {
            "range": (30, 38),
            "impact": "Flower drop and fruit cracking",
            "actions": [
                "Irrigate early morning before 9 AM.",
                "Spread straw mulch to reduce soil heat.",
                "Apply 00:00:50 (Potassium) through drip.",
                "Avoid pesticide spraying during afternoon."
            ]
        },
        "extreme_heat": {
            "range": (38, 50),
            "impact": "Severe wilting and fruit loss",
            "actions": [
                "Run drip irrigation morning and evening (light irrigation).",
                "Provide temporary shade using available green net.",
                "Apply amino acid anti-stress spray.",
                "Check leaves for spider mites."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 35),
            "impact": "Spider mite risk",
            "actions": [
                "Inspect underside of leaves for mites.",
                "Spray neem oil (3 ml/L) in evening.",
                "Maintain proper soil moisture via drip.",
                "Avoid excess nitrogen fertilizer."
            ]
        },
        "moderate_humidity": {
            "range": (35, 70),
            "impact": "Normal condition",
            "actions": [
                "Continue weekly pest scouting.",
                "Remove yellow or infected leaves.",
                "Apply preventive fungicide every 12–15 days.",
                "Keep field weed-free."
            ]
        },
        "high_humidity": {
            "range": (70, 100),
            "impact": "High fungal disease risk",
            "actions": [
                "Stop overhead irrigation.",
                "Spray Mancozeb or Copper fungicide.",
                "Remove infected leaves from field.",
                "Ensure proper drainage between rows."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Fully irrigation dependent",
            "actions": [
                "Run drip irrigation daily based on crop stage.",
                "Check emitters for clogging.",
                "Avoid water stress during flowering.",
                "Flush drip lines weekly."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Waterlogging and root rot risk",
            "actions": [
                "Open drainage channels immediately.",
                "Do not irrigate for 2–3 days.",
                "Spray fungicide to prevent root disease.",
                "Support fallen plants using bamboo sticks."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "Pest build-up risk",
            "actions": [
                "Install yellow sticky traps.",
                "Remove dense lower leaves.",
                "Inspect for whiteflies and aphids.",
                "Avoid over-irrigation."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal airflow",
            "actions": [
                "Ensure plants are tied properly to stakes.",
                "Continue normal irrigation schedule.",
                "Avoid spraying during windy hours.",
                "Monitor flower setting."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Plant damage risk",
            "actions": [
                "Tie plants firmly to bamboo stakes.",
                "Repair damaged stems immediately.",
                "Avoid pesticide spraying in strong wind.",
                "Install simple wind barriers using crop residue."
            ]
        }
    }
}

POTATO_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 10),
            "impact": "Slow sprouting and frost injury risk",
            "actions": [
                "Cover young plants at night using straw or light plastic sheet.",
                "Irrigate lightly in morning to reduce frost damage.",
                "Avoid nitrogen fertilizer during very cold days.",
                "Apply light earthing-up to protect developing tubers."
            ]
        },
        "optimal_growth": {
            "range": (15, 28),
            "impact": "Best vegetative growth and tuber development",
            "actions": [
                "Irrigate at 5–7 day intervals depending on soil moisture.",
                "Apply balanced fertilizer (NPK 12:32:16 or 19:19:19) in split doses.",
                "Do timely earthing-up to promote tuber formation.",
                "Remove weeds to avoid nutrient competition."
            ]
        },
        "heat_stress": {
            "range": (28, 35),
            "impact": "Reduced tuber formation and smaller size",
            "actions": [
                "Increase irrigation frequency but avoid waterlogging.",
                "Apply straw mulch to reduce soil temperature.",
                "Avoid heavy nitrogen fertilizer during heat.",
                "Harvest mature crop early if heat continues."
            ]
        },
        "extreme_heat": {
            "range": (35, 50),
            "impact": "Tuber damage and plant wilting",
            "actions": [
                "Provide light irrigation in morning and evening.",
                "Avoid new planting during extreme heat period.",
                "Harvest ready crop immediately to avoid quality loss.",
                "Check for red spider mite infestation."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 35),
            "impact": "Mite infestation and leaf drying risk",
            "actions": [
                "Inspect lower leaves for mite damage.",
                "Spray neem oil (3 ml/L) in evening.",
                "Maintain soil moisture through regular irrigation.",
                "Avoid excess nitrogen fertilizer."
            ]
        },
        "moderate_humidity": {
            "range": (35, 70),
            "impact": "Normal crop condition",
            "actions": [
                "Continue weekly field inspection.",
                "Remove diseased or yellow leaves.",
                "Maintain proper irrigation schedule.",
                "Keep field weed-free."
            ]
        },
        "high_humidity": {
            "range": (70, 100),
            "impact": "High Late Blight risk",
            "actions": [
                "Spray Mancozeb (2.5 g/L) immediately as preventive measure.",
                "Avoid overhead irrigation.",
                "Remove infected leaves immediately.",
                "Ensure proper spacing and airflow in field."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Fully irrigation dependent",
            "actions": [
                "Irrigate every 5–6 days based on soil condition.",
                "Avoid moisture stress during tuber formation stage.",
                "Check drip or furrow system for proper flow.",
                "Do not allow soil cracking."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Waterlogging and tuber rot risk",
            "actions": [
                "Open drainage channels immediately.",
                "Stop irrigation for 2–3 days.",
                "Spray fungicide to prevent late blight and rot.",
                "Avoid entering field when soil is very wet."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "High pest and fungal risk due to low airflow",
            "actions": [
                "Inspect crop closely for aphids and blight symptoms.",
                "Avoid dense plant growth by removing excess foliage.",
                "Do not over-irrigate.",
                "Install yellow sticky traps if aphids are seen."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal condition",
            "actions": [
                "Continue normal irrigation schedule.",
                "Monitor crop for early blight symptoms.",
                "Avoid spraying during strong gusts.",
                "Check soil moisture regularly."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Leaf damage and blight spread risk",
            "actions": [
                "Avoid spraying pesticides during strong wind.",
                "Check for broken stems or damaged foliage.",
                "Apply preventive fungicide if blight risk exists.",
                "Ensure ridges are firm to protect tubers."
            ]
        }
    }
}

CORN_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 12),
            "impact": "Poor germination and slow early growth",
            "actions": [
                "Avoid sowing in very cold soil conditions.",
                "Use well-drained raised beds for better root development.",
                "Apply light irrigation in morning if frost risk is present.",
                "Delay nitrogen top dressing until temperature improves."
            ]
        },
        "optimal_growth": {
            "range": (20, 32),
            "impact": "Best vegetative growth and cob development",
            "actions": [
                "Irrigate at 7–10 day intervals depending on soil moisture.",
                "Apply nitrogen fertilizer in split doses (basal + knee-high stage).",
                "Perform timely weeding at 20–25 days after sowing.",
                "Inspect crop regularly for fall armyworm in whorl stage."
            ]
        },
        "heat_stress": {
            "range": (32, 38),
            "impact": "Poor pollination and reduced grain filling",
            "actions": [
                "Irrigate during tasseling and silking stage without fail.",
                "Apply mulch to conserve soil moisture.",
                "Avoid heavy nitrogen application during peak heat.",
                "Monitor crop for leaf rolling symptoms."
            ]
        },
        "extreme_heat": {
            "range": (38, 50),
            "impact": "Flower drying and poor grain formation",
            "actions": [
                "Provide light irrigation in morning and evening if possible.",
                "Harvest early-maturing crop if grains are ready.",
                "Avoid new sowing during extreme heat.",
                "Inspect for spider mite infestation."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 35),
            "impact": "Mite and sucking pest risk",
            "actions": [
                "Inspect lower leaves for mite damage.",
                "Spray neem oil (3–5 ml/L) if sucking pests are observed.",
                "Maintain proper irrigation to avoid moisture stress.",
                "Avoid excessive nitrogen fertilizer."
            ]
        },
        "moderate_humidity": {
            "range": (35, 70),
            "impact": "Normal crop condition",
            "actions": [
                "Continue regular field monitoring.",
                "Remove weeds from field.",
                "Apply top dressing of nitrogen at knee-high stage.",
                "Check for stem borer damage."
            ]
        },
        "high_humidity": {
            "range": (70, 100),
            "impact": "High fungal disease risk (Leaf blight, Rust)",
            "actions": [
                "Spray Mancozeb (2.5 g/L) as preventive fungicide.",
                "Avoid water stagnation in field.",
                "Remove severely infected leaves.",
                "Ensure proper plant spacing for airflow."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Moisture stress during critical stages",
            "actions": [
                "Irrigate during tasseling and silking stage without fail.",
                "Avoid moisture stress at grain filling stage.",
                "Check irrigation channels for proper flow.",
                "Apply mulch to conserve soil moisture."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Waterlogging and root damage risk",
            "actions": [
                "Open drainage channels immediately.",
                "Do not apply fertilizer during heavy rain period.",
                "Inspect roots for lodging or rot.",
                "Reapply nitrogen if heavy leaching occurs."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "Pest build-up risk",
            "actions": [
                "Inspect whorl for fall armyworm.",
                "Install pheromone traps for monitoring.",
                "Avoid excess irrigation.",
                "Remove heavily infested plants."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal condition",
            "actions": [
                "Continue normal irrigation schedule.",
                "Monitor tasseling stage for proper pollination.",
                "Avoid spraying during strong gusts.",
                "Check crop for stem damage."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Lodging (plant falling) risk",
            "actions": [
                "Perform earthing-up at knee-high stage to strengthen roots.",
                "Avoid excess irrigation before storms.",
                "Support lodged plants quickly if possible.",
                "Avoid pesticide spraying during strong winds."
            ]
        }
    }
}

WHEAT_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 10),
            "impact": "Slow germination and frost injury",
            "actions": [
                "Irrigate lightly in early morning to reduce frost damage.",
                "Avoid nitrogen top dressing during extreme cold.",
                "Maintain proper soil moisture to support root growth.",
                "Avoid late sowing in very cold conditions."
            ]
        },
        "optimal_growth": {
            "range": (15, 28),
            "impact": "Best tillering and grain development",
            "actions": [
                "Irrigate at critical stages (CRI, tillering, flowering).",
                "Apply nitrogen fertilizer in split doses.",
                "Remove weeds at 20–25 days after sowing.",
                "Monitor crop for rust symptoms."
            ]
        },
        "heat_stress": {
            "range": (28, 35),
            "impact": "Reduced grain filling and yield loss",
            "actions": [
                "Provide irrigation during grain filling stage.",
                "Avoid additional nitrogen during high heat.",
                "Harvest early if crop matures faster due to heat.",
                "Check for leaf drying symptoms."
            ]
        },
        "extreme_heat": {
            "range": (35, 50),
            "impact": "Terminal heat causing shriveled grains",
            "actions": [
                "Provide one light irrigation if crop is in milk stage.",
                "Harvest crop as soon as grains harden.",
                "Avoid any fertilizer application.",
                "Protect harvested grains from sun exposure."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 35),
            "impact": "Moisture stress and mite risk",
            "actions": [
                "Irrigate at proper intervals to avoid stress.",
                "Inspect crop for mite infestation.",
                "Avoid excess nitrogen fertilizer.",
                "Maintain soil moisture during heading stage."
            ]
        },
        "moderate_humidity": {
            "range": (35, 70),
            "impact": "Normal crop growth",
            "actions": [
                "Continue routine field inspection.",
                "Maintain irrigation schedule.",
                "Apply nitrogen top dressing at tillering stage.",
                "Keep field weed-free."
            ]
        },
        "high_humidity": {
            "range": (70, 100),
            "impact": "High rust and fungal disease risk",
            "actions": [
                "Spray Propiconazole or Mancozeb at early rust symptoms.",
                "Avoid water stagnation in field.",
                "Inspect lower leaves for yellow or brown rust.",
                "Ensure proper spacing for airflow."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Dependence on irrigation",
            "actions": [
                "Irrigate at CRI stage (20–25 days after sowing).",
                "Provide irrigation during flowering and grain filling.",
                "Avoid skipping critical irrigation stages.",
                "Check field channels for proper water flow."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Waterlogging and lodging risk",
            "actions": [
                "Open drainage channels immediately.",
                "Avoid nitrogen application during heavy rain.",
                "Inspect crop for lodging.",
                "Spray fungicide if fungal symptoms appear."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "Fungal disease build-up risk",
            "actions": [
                "Inspect crop regularly for rust infection.",
                "Avoid over-irrigation.",
                "Maintain proper spacing.",
                "Monitor leaf moisture levels."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal airflow",
            "actions": [
                "Continue normal irrigation schedule.",
                "Monitor grain development.",
                "Avoid spraying during strong gusts.",
                "Inspect crop health weekly."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Lodging (plant falling) risk",
            "actions": [
                "Avoid excess nitrogen fertilizer.",
                "Ensure timely irrigation to strengthen roots.",
                "Harvest mature crop early to avoid losses.",
                "Inspect field after storm for fallen plants."
            ]
        }
    }
}

RICE_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 15),
            "impact": "Poor germination and slow tillering",
            "actions": [
                "Avoid transplanting during very low temperature period.",
                "Maintain shallow water layer (2–3 cm) to protect seedlings.",
                "Apply light nitrogen dose after temperature improves.",
                "Use well-decomposed FYM to strengthen plant growth."
            ]
        },
        "optimal_growth": {
            "range": (20, 35),
            "impact": "Best tillering and panicle development",
            "actions": [
                "Maintain 3–5 cm standing water in field.",
                "Apply nitrogen in split doses (basal, tillering, panicle stage).",
                "Perform timely weeding at 20–25 days after transplanting.",
                "Monitor crop regularly for stem borer and leaf folder."
            ]
        },
        "heat_stress": {
            "range": (35, 40),
            "impact": "Poor grain filling and spikelet sterility",
            "actions": [
                "Maintain proper water level during flowering stage.",
                "Avoid nitrogen application during extreme heat.",
                "Provide irrigation if field dries quickly.",
                "Monitor panicle development carefully."
            ]
        },
        "extreme_heat": {
            "range": (40, 50),
            "impact": "Flower drying and yield reduction",
            "actions": [
                "Ensure continuous thin water layer in field.",
                "Harvest mature crop early to avoid grain cracking.",
                "Avoid fertilizer application.",
                "Inspect field for drying patches."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 40),
            "impact": "Leaf drying and pest attack risk",
            "actions": [
                "Maintain adequate standing water.",
                "Inspect crop for brown plant hopper and stem borer.",
                "Avoid moisture stress during flowering stage.",
                "Apply neem-based spray if sucking pests appear."
            ]
        },
        "moderate_humidity": {
            "range": (40, 75),
            "impact": "Normal crop condition",
            "actions": [
                "Continue regular field inspection.",
                "Maintain recommended water level.",
                "Apply top dressing nitrogen at tillering stage.",
                "Keep bunds clean to avoid pest hiding."
            ]
        },
        "high_humidity": {
            "range": (75, 100),
            "impact": "High blast and sheath blight disease risk",
            "actions": [
                "Spray Tricyclazole or Mancozeb at early blast symptoms.",
                "Avoid excess nitrogen fertilizer.",
                "Maintain proper spacing for airflow.",
                "Drain excess water if water stagnation occurs."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Moisture stress if irrigation unavailable",
            "actions": [
                "Maintain minimum 3 cm standing water.",
                "Irrigate at critical stages (tillering and flowering).",
                "Repair bunds to prevent water loss.",
                "Avoid skipping irrigation at panicle initiation stage."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Water overflow and lodging risk",
            "actions": [
                "Open drainage outlets to remove excess water.",
                "Strengthen bunds immediately.",
                "Avoid fertilizer application during heavy rain.",
                "Inspect crop for lodging and fungal symptoms."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "Pest and fungal build-up risk",
            "actions": [
                "Inspect crop for blast and brown spot symptoms.",
                "Avoid excessive nitrogen application.",
                "Monitor lower leaves for fungal patches.",
                "Ensure proper water level in field."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal airflow",
            "actions": [
                "Continue standard irrigation management.",
                "Monitor flowering stage for proper grain setting.",
                "Avoid spraying during gusty periods.",
                "Inspect field weekly."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Lodging (crop falling) risk",
            "actions": [
                "Drain excess water to strengthen roots.",
                "Avoid excess nitrogen which increases lodging.",
                "Support lodged plants early if possible.",
                "Harvest mature crop early to avoid losses."
            ]
        }
    }
}

ONION_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 12),
            "impact": "Slow seedling growth and bulb development",
            "actions": [
                "Avoid transplanting seedlings during very low temperature.",
                "Irrigate lightly in morning to reduce frost damage.",
                "Apply light nitrogen dose after temperature improves.",
                "Use straw mulch to protect young seedlings."
            ]
        },
        "optimal_growth": {
            "range": (15, 30),
            "impact": "Best leaf growth and bulb formation",
            "actions": [
                "Irrigate at 5–7 day intervals based on soil moisture.",
                "Apply nitrogen in split doses (basal + 30 days after transplanting).",
                "Keep field weed-free during early growth stage.",
                "Inspect regularly for thrips infestation."
            ]
        },
        "heat_stress": {
            "range": (30, 38),
            "impact": "Poor bulb size and early bolting risk",
            "actions": [
                "Increase irrigation frequency but avoid waterlogging.",
                "Avoid excess nitrogen during bulb formation stage.",
                "Apply mulch to conserve soil moisture.",
                "Harvest mature bulbs early to prevent sunburn."
            ]
        },
        "extreme_heat": {
            "range": (38, 50),
            "impact": "Bulb cracking and drying",
            "actions": [
                "Provide light irrigation in early morning only.",
                "Avoid fertilizer application during extreme heat.",
                "Harvest mature crop immediately.",
                "Dry harvested bulbs in shade before storage."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 35),
            "impact": "Thrips attack and leaf drying risk",
            "actions": [
                "Inspect leaves for thrips damage (silver streaks).",
                "Spray neem oil (3–5 ml/L) in evening if needed.",
                "Maintain proper irrigation schedule.",
                "Avoid excess nitrogen fertilizer."
            ]
        },
        "moderate_humidity": {
            "range": (35, 70),
            "impact": "Normal crop growth",
            "actions": [
                "Continue weekly field inspection.",
                "Remove weeds regularly.",
                "Apply balanced fertilizer at bulb initiation stage.",
                "Monitor for early disease symptoms."
            ]
        },
        "high_humidity": {
            "range": (70, 100),
            "impact": "High Purple Blotch and Downy Mildew risk",
            "actions": [
                "Spray Mancozeb (2.5 g/L) or Copper fungicide preventively.",
                "Avoid overhead irrigation.",
                "Remove infected leaves from field.",
                "Ensure proper drainage between rows."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Moisture stress affecting bulb size",
            "actions": [
                "Irrigate every 5–7 days depending on soil moisture.",
                "Avoid moisture stress during bulb formation stage.",
                "Check irrigation channels for uniform water flow.",
                "Do not allow soil cracking."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Waterlogging and bulb rot risk",
            "actions": [
                "Open drainage channels immediately.",
                "Stop irrigation for 2–3 days.",
                "Spray fungicide to prevent basal rot.",
                "Avoid entering field when soil is very wet."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "High pest and fungal build-up risk",
            "actions": [
                "Inspect crop for thrips and fungal spots.",
                "Avoid over-irrigation.",
                "Maintain proper spacing for airflow.",
                "Remove infected leaves immediately."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal condition",
            "actions": [
                "Continue regular irrigation schedule.",
                "Monitor bulb development.",
                "Avoid spraying during gusty periods.",
                "Inspect crop weekly."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Leaf damage and lodging risk",
            "actions": [
                "Avoid pesticide spraying during strong winds.",
                "Check for uprooted plants.",
                "Repair damaged ridges if needed.",
                "Harvest mature crop early if heavy wind continues."
            ]
        }
    }
}

GRAPE_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 12),
            "impact": "Slow shoot growth and delayed bud break",
            "actions": [
                "Avoid heavy pruning during very low temperature.",
                "Provide light irrigation in morning to reduce frost impact.",
                "Apply light nitrogen dose after temperature improves.",
                "Inspect young shoots for cold injury."
            ]
        },
        "optimal_growth": {
            "range": (18, 32),
            "impact": "Best shoot growth and berry development",
            "actions": [
                "Irrigate at 7–10 day intervals depending on soil moisture.",
                "Apply nitrogen and potassium in split doses.",
                "Perform timely pruning and canopy management.",
                "Monitor crop weekly for powdery mildew."
            ]
        },
        "heat_stress": {
            "range": (32, 38),
            "impact": "Berry sunburn and poor fruit size",
            "actions": [
                "Irrigate regularly to avoid moisture stress.",
                "Maintain proper canopy cover to protect bunches.",
                "Avoid excessive nitrogen application.",
                "Harvest mature bunches early morning."
            ]
        },
        "extreme_heat": {
            "range": (38, 50),
            "impact": "Berry shriveling and sunburn damage",
            "actions": [
                "Provide light irrigation in morning and evening if needed.",
                "Avoid spraying during peak afternoon heat.",
                "Harvest ready bunches immediately.",
                "Protect harvested grapes from direct sunlight."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 35),
            "impact": "Powdery mildew risk and mite infestation",
            "actions": [
                "Inspect leaves for powdery white patches.",
                "Spray sulfur-based fungicide if symptoms appear.",
                "Monitor for red spider mites.",
                "Maintain proper irrigation schedule."
            ]
        },
        "moderate_humidity": {
            "range": (35, 70),
            "impact": "Normal crop condition",
            "actions": [
                "Continue weekly vineyard inspection.",
                "Maintain proper canopy ventilation.",
                "Apply balanced fertilizer as per growth stage.",
                "Remove diseased leaves if observed."
            ]
        },
        "high_humidity": {
            "range": (70, 100),
            "impact": "High downy mildew and bunch rot risk",
            "actions": [
                "Spray Mancozeb or Metalaxyl-based fungicide preventively.",
                "Avoid overhead irrigation.",
                "Remove infected leaves and bunches immediately.",
                "Improve airflow by light pruning."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Moisture stress affecting berry size",
            "actions": [
                "Irrigate at regular intervals based on soil moisture.",
                "Avoid moisture stress during berry development stage.",
                "Check drip lines for proper water distribution.",
                "Apply mulch to conserve soil moisture."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Bunch rot and root disease risk",
            "actions": [
                "Ensure proper drainage in vineyard.",
                "Spray fungicide to prevent downy mildew.",
                "Avoid nitrogen fertilizer during heavy rain.",
                "Inspect bunches for rot immediately after rain."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "Fungal build-up risk due to low airflow",
            "actions": [
                "Inspect canopy for mildew symptoms.",
                "Avoid excessive irrigation.",
                "Maintain proper spacing between vines.",
                "Remove excess foliage."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal vineyard condition",
            "actions": [
                "Continue regular irrigation schedule.",
                "Monitor bunch development.",
                "Avoid spraying during gusty periods.",
                "Inspect trellis system weekly."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Trellis damage and berry drop risk",
            "actions": [
                "Check and tighten trellis wires immediately.",
                "Remove broken shoots.",
                "Avoid spraying during strong winds.",
                "Harvest mature bunches early if wind continues."
            ]
        }
    }
}

CUCUMBER_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 15),
            "impact": "Poor germination and slow vine growth",
            "actions": [
                "Avoid sowing during very low temperature period.",
                "Use straw mulch to protect young seedlings.",
                "Irrigate lightly in morning to reduce cold injury.",
                "Delay nitrogen application until temperature improves."
            ]
        },
        "optimal_growth": {
            "range": (20, 32),
            "impact": "Best vine growth and fruit development",
            "actions": [
                "Irrigate every 3–5 days depending on soil moisture.",
                "Apply balanced fertilizer in split doses.",
                "Provide staking or support for better fruit quality.",
                "Inspect regularly for aphids and early disease symptoms."
            ]
        },
        "heat_stress": {
            "range": (32, 38),
            "impact": "Flower drop and bitter fruits",
            "actions": [
                "Irrigate early morning to reduce plant stress.",
                "Apply straw mulch to conserve soil moisture.",
                "Avoid fertilizer application during peak heat.",
                "Harvest fruits regularly to reduce plant load."
            ]
        },
        "extreme_heat": {
            "range": (38, 50),
            "impact": "Leaf wilting and poor fruit setting",
            "actions": [
                "Provide light irrigation in morning and evening.",
                "Avoid pesticide spraying during afternoon heat.",
                "Harvest mature fruits early morning.",
                "Check for red spider mite infestation."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 35),
            "impact": "Mite infestation and leaf drying risk",
            "actions": [
                "Inspect leaves for red spider mites.",
                "Spray neem oil (3–5 ml/L) if mites appear.",
                "Maintain proper irrigation schedule.",
                "Avoid excess nitrogen fertilizer."
            ]
        },
        "moderate_humidity": {
            "range": (35, 70),
            "impact": "Normal crop growth",
            "actions": [
                "Continue weekly field inspection.",
                "Remove yellow or diseased leaves.",
                "Apply balanced fertilizer at flowering stage.",
                "Keep field weed-free."
            ]
        },
        "high_humidity": {
            "range": (70, 100),
            "impact": "High Downy Mildew and Powdery Mildew risk",
            "actions": [
                "Spray Mancozeb or Copper fungicide preventively.",
                "Avoid overhead irrigation.",
                "Remove infected leaves immediately.",
                "Ensure proper spacing for airflow."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Moisture stress affecting fruit size",
            "actions": [
                "Irrigate at 3–4 day intervals.",
                "Avoid moisture stress during flowering stage.",
                "Check drip lines for proper water flow.",
                "Apply mulch to conserve soil moisture."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Root rot and fungal disease risk",
            "actions": [
                "Open drainage channels immediately.",
                "Stop irrigation for 2–3 days.",
                "Spray fungicide after rain to prevent disease.",
                "Avoid working in waterlogged field."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "Pest and fungal build-up risk",
            "actions": [
                "Inspect crop for aphids and whiteflies.",
                "Install yellow sticky traps.",
                "Avoid over-irrigation.",
                "Remove dense foliage if needed."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal condition",
            "actions": [
                "Continue regular irrigation schedule.",
                "Monitor fruit development.",
                "Avoid spraying during gusty periods.",
                "Inspect crop weekly."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Vine damage and fruit drop risk",
            "actions": [
                "Repair damaged vines immediately.",
                "Avoid pesticide spraying during strong winds.",
                "Support creeping vines properly.",
                "Harvest mature fruits early if wind continues."
            ]
        }
    }
}

CABBAGE_WEATHER_INTELLIGENCE = {
    "temperature_ranges": {
        "cold_stress": {
            "range": (0, 10),
            "impact": "Slow head formation and frost injury risk",
            "actions": [
                "Provide light irrigation in morning to reduce frost damage.",
                "Avoid transplanting seedlings during very low temperatures.",
                "Cover young seedlings with straw or crop residue at night.",
                "Avoid nitrogen top dressing during extreme cold."
            ]
        },
        "optimal_growth": {
            "range": (15, 25),
            "impact": "Best vegetative growth and head development",
            "actions": [
                "Irrigate at 5–7 day intervals depending on soil moisture.",
                "Apply urea in split doses for proper head formation.",
                "Remove yellow and damaged outer leaves.",
                "Monitor weekly for aphids and caterpillars."
            ]
        },
        "heat_stress": {
            "range": (25, 32),
            "impact": "Loose head formation and bolting risk",
            "actions": [
                "Irrigate early morning to reduce heat stress.",
                "Apply mulch to conserve soil moisture.",
                "Harvest mature heads immediately to avoid cracking.",
                "Avoid heavy nitrogen application."
            ]
        },
        "extreme_heat": {
            "range": (32, 45),
            "impact": "Head cracking and poor quality",
            "actions": [
                "Increase irrigation frequency (light irrigation).",
                "Harvest market-ready heads without delay.",
                "Avoid pesticide spraying during afternoon.",
                "Provide temporary shade for young seedlings if possible."
            ]
        }
    },
    "humidity_ranges": {
        "low_humidity": {
            "range": (0, 35),
            "impact": "Aphid infestation risk",
            "actions": [
                "Inspect underside of leaves for aphids.",
                "Spray neem oil (3–5 ml/L) in evening.",
                "Avoid excess nitrogen fertilizer.",
                "Install yellow sticky traps."
            ]
        },
        "moderate_humidity": {
            "range": (35, 70),
            "impact": "Normal crop condition",
            "actions": [
                "Continue weekly field inspection.",
                "Remove infected outer leaves immediately.",
                "Maintain proper spacing for airflow.",
                "Keep field weed-free."
            ]
        },
        "high_humidity": {
            "range": (70, 100),
            "impact": "High Downy Mildew and Black Rot risk",
            "actions": [
                "Spray Mancozeb or Copper fungicide preventively.",
                "Avoid overhead irrigation.",
                "Improve drainage between rows.",
                "Remove infected plants to prevent spread."
            ]
        }
    },
    "rainfall_ranges": {
        "no_rain": {
            "range": (0, 1),
            "impact": "Moisture stress affecting head size",
            "actions": [
                "Irrigate at 5–6 day intervals.",
                "Avoid moisture stress during head formation stage.",
                "Check drip lines for clogging.",
                "Apply mulch to conserve soil moisture."
            ]
        },
        "heavy_rain": {
            "range": (10, 200),
            "impact": "Root rot and leaf disease risk",
            "actions": [
                "Open drainage channels immediately.",
                "Avoid irrigation for 2–3 days.",
                "Spray fungicide after rain to prevent disease.",
                "Avoid working in waterlogged field."
            ]
        }
    },
    "wind_ranges": {
        "low_wind": {
            "range": (0, 2),
            "impact": "Pest build-up and fungal risk",
            "actions": [
                "Inspect crop for aphids and caterpillars.",
                "Remove dense outer leaves.",
                "Avoid excess irrigation.",
                "Install yellow sticky traps."
            ]
        },
        "moderate_wind": {
            "range": (2, 6),
            "impact": "Normal field condition",
            "actions": [
                "Continue regular irrigation schedule.",
                "Monitor head firmness weekly.",
                "Avoid spraying during gusty hours.",
                "Inspect crop for disease symptoms."
            ]
        },
        "high_wind": {
            "range": (6, 20),
            "impact": "Plant lodging and leaf damage risk",
            "actions": [
                "Support weak plants with soil earthing-up.",
                "Remove broken leaves.",
                "Avoid pesticide spraying during strong winds.",
                "Harvest mature heads early if wind persists."
            ]
        }
    }
}
