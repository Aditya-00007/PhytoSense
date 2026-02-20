"""
Crop database module for PhytoSense application.
Contains detailed information about crops, diseases, symptoms, and treatments.
"""

CROP_DATABASE = {
    "Tomato": {
        "info": {
            "scientific_name": "Solanum lycopersicum",
            "best_season": "Tomatoes can be cultivated throughout the year in Maharashtra. Optimal planting times are: Rainy Season (June to July), Winter Season (October to November), Summer Season (January to February)",
            "best_soil": "Well-drained loamy soils rich in organic matter with a pH range of 6.5–7.5",
            "time_period": "Approximately 120 days from transplanting to harvesting",
            "estimated_cost": "₹30,150 per acre",
            "varieties": [
                "Phule Raja", "Phule Tejas", "Vaishali", "Dhanashree", "Abhinav", 
                "Pusa Ruby", "Naveen", "Rashmi", "Megha", "Sankranti"
            ]
        },
        "diseases": {
            "Leaf Curl Virus": {
                "symptoms": "Upward curling of leaves, reduction in leaf size, stunted growth, and flower drop",
                "causes": "Transmitted by whiteflies",
                "treatment": "Apply insecticides such as Imidacloprid (70% WG) at 0.1 g per liter of water to control whitefly populations",
                "prevention": "Remove and destroy infected plants; use reflective mulches to deter whiteflies"
            },
            "Early Blight": {
                "symptoms": "Dark brown spots with concentric rings on older leaves ('target board' appearance). Yellowing of leaves leading to defoliation",
                "causes": "Fungus (Alternaria solani) persists in soil and plant debris. Spread facilitated by splashing water and wind",
                "treatment": "Spray Chlorothalonil or Mancozeb @ 2–2.5 g/L. Use Azoxystrobin as systemic option",
                "prevention": "Practice crop rotation, remove plant debris after harvest, ensure balanced fertilization (especially nitrogen and potassium)"
            },
            "Late Blight": {
                "symptoms": "Water-soaked lesions on leaves, stems, and fruits. White mold growth under leaves in humid conditions",
                "causes": "Oomycete pathogen Phytophthora infestans thrives in cool, wet weather. Spores spread via wind and rain",
                "treatment": "Apply fungicides like Mancozeb + Metalaxyl, Phosphoric acid-based foliar fertilizers",
                "prevention": "Remove and destroy infected plants immediately, avoid overhead watering to reduce leaf wetness"
            },
            "Fusarium Wilt": {
                "symptoms": "Yellowing and wilting of leaves, often on one side of the plant. Brown discoloration of vascular tissue when stems are cut",
                "causes": "Soil-borne fungus Fusarium oxysporum enters through roots and blocks water transport",
                "treatment": "Use biofertilizers like Pseudomonas fluorescens, Neem Cake + Farm Yard Manure (FYM)",
                "prevention": "Plant resistant tomato varieties, practice crop rotation with non-host plants, remove and destroy infected plants"
            }
        },
        "pests": {
            "Fruit Borer": {
                "symptoms": "Holes in fruits with excreta, caterpillar often found inside fruit",
                "description": "Greenish-brown caterpillar; feeds on developing fruits",
                "treatment": "Install pheromone traps, release Trichogramma chilonis (egg parasitoid), use Spinosad 45 SC (0.3 ml/l), Emamectin Benzoate 5 SG (0.4 g/l), or Novaluron 10 EC (1 ml/l)"
            },
            "Whitefly": {
                "symptoms": "Yellowing and curling of leaves, sticky honeydew on leaves; sooty mold formation",
                "description": "Tiny white insects on the undersides of leaves, also transmits Tomato Leaf Curl Virus",
                "treatment": "Use yellow sticky traps, apply Imidacloprid or Thiamethoxam, spray neem oil as an organic alternative"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Older leaves turn pale yellow or light green, stunted growth, poor fruit development",
                "treatment": "Apply Urea (46% N), Ammonium Sulphate, organic compost or well-decomposed FYM"
            },
            "Phosphorus": {
                "symptoms": "Leaves appear dull dark green with purplish veins, slow growth and poor root development",
                "treatment": "Apply Single Super Phosphate (SSP), Di-Ammonium Phosphate (DAP), or bone meal (organic)"
            },
            "Calcium": {
                "symptoms": "Blossom End Rot on fruits, young leaves may be distorted, reduced root and shoot growth",
                "treatment": "Apply Calcium Nitrate, Gypsum (Calcium Sulphate), or Dolomite lime (if soil is acidic)"
            }
        }
    },
    "Cabbage": {
        "info": {
            "scientific_name": "Brassica oleracea var. capitata",
            "best_season": "Cabbage is a cool-season crop that prefers moderate temperatures. It thrives best in spring or fall, with temperatures ranging from 15°C to 20°C (59°F to 68°F)",
            "best_soil": "Loamy soil, which is well-drained and rich in organic matter. Soil pH between 6.0 to 6.5",
            "time_period": "Early varieties take around 70 to 85 days to mature. Late varieties may take 100 to 120 days",
            "estimated_cost": "₹35,000 to ₹50,000 per acre",
            "varieties": [
                "Green Cabbage", "Red Cabbage", "Savoy Cabbage", "Napa Cabbage (Chinese Cabbage)"
            ]
        },
        "diseases": {
            "Downy Mildew": {
                "symptoms": "Yellow patches on upper leaf surface, white to grey mold under the leaves, wilting in severe infections",
                "causes": "Fungal disease caused by Peronospora parasitica, favors high humidity and cool temperatures",
                "treatment": "Spray Metalaxyl + Mancozeb (0.25%), use Fosetyl-Al (Aliette)",
                "prevention": "Improve field drainage and aeration, avoid wetting foliage during irrigation"
            },
            "Clubroot": {
                "symptoms": "Root swelling, stunted growth, yellowing of leaves, wilting, premature leaf drop, reduced head formation",
                "causes": "Caused by the soil-borne protist Plasmodiophora brassicae, thrives in acidic, poorly-drained soils",
                "treatment": "Apply lime to raise soil pH to 7.0–7.5, use phosphorus and potassium fertilizers, organic compost, biological control with Trichoderma harzianum",
                "prevention": "Crop rotation for 3-4 years, use resistant varieties, maintain neutral to alkaline pH, ensure good drainage"
            },
            "Black Rot": {
                "symptoms": "Yellowing of leaf edges, V-shaped lesions spreading inward, blackening of veins and rotting of heads",
                "causes": "Bacterial infection caused by Xanthomonas campestris pv. campestris, spread through seeds, water, and contaminated tools",
                "treatment": "Spray Copper Oxychloride @ 2.5 g/liter + Streptocycline @ 100 ppm, use bioagents like Pseudomonas fluorescens",
                "prevention": "Use disease-free seeds, practice crop rotation (3–4 years), avoid overhead irrigation"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Curled leaves, yellowing of leaves, sticky residue on plants",
                "description": "Small soft-bodied insects that cluster on leaves and stems",
                "treatment": "Use Neem oil or insecticidal soaps for control"
            },
            "Cabbage Worms": {
                "symptoms": "Holes in the leaves, chewed edges, and visible caterpillars",
                "description": "Green caterpillars that feed on leaves",
                "treatment": "Treat plants with Bacillus thuringiensis (Bt) or pyrethrin-based insecticides"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves (chlorosis), stunted growth and small leaves, reduced head size and poor yield",
                "treatment": "Apply Nitrogen-rich fertilizers, such as Urea or Ammonium Nitrate, or incorporate well-rotted manure or compost"
            },
            "Phosphorus": {
                "symptoms": "Dark green leaves with a reddish-purple tinge, stunted growth and poor root development",
                "treatment": "Use phosphorus-based fertilizers like Single Superphosphate (SSP) or Diammonium Phosphate (DAP), bone meal or rock phosphate"
            }
        }
    },
    "Cauliflower": {
        "info": {
            "scientific_name": "Brassica oleracea var. botrytis",
            "best_season": "Cool-season crop that prefers moderate temperatures, ideally between 15°C and 20°C (59°F to 68°F). Most successfully grown in spring or fall",
            "best_soil": "Well-drained, fertile soil rich in organic matter. Ideal pH range is 6.0 to 6.8",
            "time_period": "Early varieties mature in 50 to 75 days from transplanting. Late varieties typically require around 80 to 120 days",
            "estimated_cost": "Between ₹1,66,000 to ₹3,32,000 per acre",
            "varieties": [
                "Snowball", "Great White", "Graffiti", "Cheddar", "Romanesco"
            ]
        },
        "diseases": {
            "Downy Mildew": {
                "symptoms": "Yellowish patches on the upper side of leaves, white fungal growth on the underside, wilting in severe cases",
                "causes": "Caused by fungus Peronospora parasitica, favors cool, moist conditions",
                "treatment": "Spray Metalaxyl + Mancozeb (0.25%) every 10–15 days, use fungicides like Ridomil Gold",
                "prevention": "Avoid overhead irrigation, maintain plant spacing, use resistant varieties, ensure good air circulation"
            },
            "Black Rot": {
                "symptoms": "Yellowing leaf margins with V-shaped lesions, black veins on leaves and stems, bad odor in advanced stages",
                "causes": "Caused by Xanthomonas campestris pv. campestris (a bacterium), spread via infected seeds, tools, and water",
                "treatment": "Spray Copper Oxychloride (0.25%) + Streptocycline (100 ppm)",
                "prevention": "Use disease-free certified seeds, practice crop rotation, avoid overhead irrigation"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Soft-bodied green/black insects cluster on new leaves, curling and yellowing of leaves, sticky honeydew attracts ants",
                "description": "Small, soft-bodied insects that suck plant sap",
                "treatment": "Spray Neem oil (2%), Imidacloprid 17.8 SL @ 0.3 ml/liter water, Verticillium lecanii (biopesticide) as an eco-friendly option"
            },
            "Diamondback Moth": {
                "symptoms": "Small caterpillars make holes in leaves, larvae feed on leaf undersides and curds",
                "description": "Small caterpillars that feed on leaves and heads",
                "treatment": "Use Bacillus thuringiensis (Bt) formulations, Spinosad 45 SC @ 1 ml/liter, introduce natural enemies like Trichogramma spp."
            }
        },
        "deficiencies": {
            "Boron": {
                "symptoms": "Brown curd spots, hollow stems, distorted curd and stem cracking",
                "treatment": "Apply Borax (10–15 kg/ha), use boron-rich organic compost, foliar spray: 0.1% boric acid solution at 30 and 50 days after planting"
            },
            "Molybdenum": {
                "symptoms": "Whiptail condition – narrow, strap-like leaves, poor curd development",
                "treatment": "Apply Ammonium Molybdate (0.05%) as foliar spray, enrich compost with molybdenum-containing minerals"
            }
        }
    },
    "Potato": {
        "info": {
            "scientific_name": "Solanum tuberosum",
            "best_season": "Cool-season crop, grows best in spring and early summer. In temperate climates, spring planting is common. In tropical areas, potatoes can be grown in fall",
            "best_soil": "Well-drained, loose, and fertile soil with pH 5.0 to 6.0. Well-drained loamy soils are ideal",
            "time_period": "Early varieties mature in 70 to 90 days. Mid-season: 90 to 120 days. Late varieties: 120 to 150 days",
            "estimated_cost": "₹1,28,450 to ₹3,92,650 or more per acre",
            "varieties": [
                "Russet Burbank", "Yukon Gold", "Red Potatoes", "Fingerling Potatoes", "New Potatoes"
            ]
        },
        "diseases": {
            "Late Blight": {
                "symptoms": "Water-soaked brown to black lesions on leaves and stems, white fungal growth under leaves, tubers show brownish rot with foul smell",
                "causes": "Fungal disease caused by Phytophthora infestans, favored by cool, moist conditions",
                "treatment": "Spray Mancozeb + Metalaxyl (e.g., Ridomil Gold) at 10–15 day intervals, use Copper Oxychloride for tuber protection",
                "prevention": "Use resistant varieties (like Kufri Jyoti, Kufri Bahar), avoid overhead irrigation, destroy infected crop residues"
            },
            "Bacterial Wilt / Brown Rot": {
                "symptoms": "Sudden wilting of entire plant, browning of vascular tissues in stems, brown ooze from infected stem or tuber when cut",
                "causes": "Caused by Ralstonia solanacearum (bacteria), survives in soil and infected crop residue",
                "treatment": "No effective chemical treatment. Uproot and destroy infected plants immediately. Soil treatment with Pseudomonas fluorescens as biocontrol",
                "prevention": "Use certified disease-free seed, avoid waterlogging, rotate with non-host crops like cereals"
            }
        },
        "pests": {
            "Potato Tuber Moth": {
                "symptoms": "Caterpillars bore into tubers and create tunnels, dry powdery frass inside tuber, secondary fungal/bacterial rot",
                "description": "Moths that lay eggs on tubers, and the larvae bore into the potato",
                "treatment": "Spray Spinosad 45 SC @ 1 ml/l, store tubers under cool, dark, and ventilated conditions, use neem oil spray for eco-friendly control"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, poor tuber development",
                "treatment": "Apply nitrogen fertilizers like urea or ammonium nitrate, organic options include composted manure"
            },
            "Potassium": {
                "symptoms": "Bronzing and scorching of leaf edges, weak stems, reduced tuber size",
                "treatment": "Apply potassium-rich fertilizers like muriate of potash or sulfate of potash"
            }
        }
    },
    "Watermelon": {
        "info": {
            "scientific_name": "Citrullus lanatus",
            "best_season": "Warm, dry climates. Spring Season: January to March. Summer Season: November to February (in areas with mild winters). Best when temperatures are between 22°C and 35°C",
            "best_soil": "Well-drained, sandy loam soils rich in organic matter. Soil pH between 6.0 and 7.5 is ideal",
            "time_period": "Approximately 75–120 days from sowing to harvesting, depending on the variety",
            "estimated_cost": "₹50,000–₹80,000 per acre",
            "varieties": [
                "Sugar Baby", "Arka Manik", "Crimson Sweet", "Black Diamond", "Kiran", "Seedless Watermelon"
            ]
        },
        "diseases": {
            "Anthracnose": {
                "symptoms": "Circular, sunken lesions on leaves, stems, and fruits. Fruits may develop cracks and rot",
                "causes": "Caused by the fungus Colletotrichum orbiculare, thrives in warm, humid conditions",
                "treatment": "Apply fungicides like chlorothalonil, mancozeb, or azoxystrobin at regular intervals during the growing season",
                "prevention": "Use disease-resistant varieties, practice crop rotation, avoid overhead irrigation"
            },
            "Fusarium Wilt": {
                "symptoms": "Yellowing and wilting of leaves, vascular discoloration, and eventual plant death",
                "causes": "Caused by the fungus Fusarium oxysporum f. sp. niveum, thrives in warm, sandy soils with low pH",
                "treatment": "Apply fungicides like prothioconazole through drip irrigation to reduce disease severity",
                "prevention": "Rotate with non-cucurbit crops for 5-6 years, plant resistant varieties, maintain soil pH above 6.5"
            },
            "Powdery Mildew": {
                "symptoms": "White powdery spots on leaves and stems, leads to leaf distortion and reduced photosynthesis",
                "causes": "Caused by the fungus Podosphaera xanthii, thrives in warm, dry conditions with high humidity",
                "treatment": "Use sulfur-based fungicides or systemic fungicides like azoxystrobin or myclobutanil",
                "prevention": "Plant resistant varieties, ensure proper spacing for airflow, avoid overhead irrigation"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Sticky honeydew secretions on leaves, curled or distorted leaves",
                "description": "Small soft-bodied insects that suck plant sap",
                "treatment": "Apply neem-based organic fertilizers, systemic insecticides like imidacloprid, introduce beneficial insects"
            },
            "Spider Mites": {
                "symptoms": "Fine webbing on leaves, yellow speckling or bronzing of leaves, leaf drop in severe cases",
                "description": "Tiny spider-like pests that suck plant juices, often found on leaf undersides",
                "treatment": "Apply miticides, horticultural oils, or insecticidal soaps, maintain adequate humidity"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, and reduced foliage",
                "treatment": "Apply nitrogen-rich fertilizers like urea or ammonium nitrate, or organic options like composted manure"
            },
            "Potassium": {
                "symptoms": "Browning or scorching of leaf edges and tips, weak stems, and poor fruit quality",
                "treatment": "Use potassium sulfate or muriate of potash, or organic alternatives like wood ash or banana peels"
            },
            "Calcium": {
                "symptoms": "Distorted young leaves, yellow or brown spots, and cracking of fruits",
                "treatment": "Add lime, gypsum, or crushed eggshells to the soil, use calcium-rich compost"
            }
        }
    },
    "Pomegranate": {
        "info": {
            "scientific_name": "Punica granatum",
            "best_season": "Thrives in semi-arid and tropical climates. Best planted during monsoon (June to August) or spring (February to March) with irrigation",
            "best_soil": "Grows well in sandy loam to black soil with pH 6.0-7.5. Well-drained soil is essential to avoid waterlogging",
            "time_period": "Starts bearing fruits 2-3 years after planting. Fruits are harvested 5-7 months after flowering",
            "estimated_cost": "₹80,000–₹1,60,000 per acre",
            "varieties": [
                "Bhagwa", "Ganesh", "Arakta", "Mridula", "Kandhari", "Wonderful"
            ]
        },
        "diseases": {
            "Cercospora Fruit Spot": {
                "symptoms": "Yellowish spots with halos on leaves and fruits, which turn black and corky. Severe infections cause defoliation",
                "causes": "Caused by the fungus Cercospora punicae, thrives in warm, humid conditions",
                "treatment": "Apply fungicides like Hexaconazole (0.1%) or Carbendazim (0.1%), use Mancozeb (0.25%) or Propiconazole (0.1%)",
                "prevention": "Use pathogen-free planting material, prune infected parts, ensure proper spacing and airflow"
            },
            "Anthracnose": {
                "symptoms": "Leaf blight, dark brown lesions on fruits with concentric rings, dieback of twigs",
                "causes": "Caused by the fungus Colletotrichum gloeosporioides, spreads through wind, rain, and infected plant debris",
                "treatment": "Apply copper fungicides, use Mancozeb (0.25%) or Propiconazole (0.1%)",
                "prevention": "Use disease-free planting material, remove infected plant parts, improve airflow"
            },
            "Alternaria Leaf Spot": {
                "symptoms": "Circular brown spots with concentric rings on leaves, leading to defoliation",
                "causes": "Caused by the fungus Alternaria alternata, thrives in warm, humid conditions",
                "treatment": "Apply fungicides like Mancozeb or Chlorothalonil at recommended doses",
                "prevention": "Use certified disease-free material, avoid overhead irrigation, remove infected debris"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Curled leaves, stunted growth, honeydew secretion on leaves",
                "description": "Small soft-bodied insects that suck plant sap",
                "treatment": "Apply neem oil, insecticidal soap, or imidacloprid. Encourage natural predators like ladybugs"
            },
            "Fruit Borer": {
                "symptoms": "Holes in fruits, larval feeding damage, fruit drop",
                "description": "Caterpillars that bore into fruits and feed on the pulp",
                "treatment": "Apply Bacillus thuringiensis (Bt), spinosad, or carbaryl. Use pheromone traps for monitoring"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, reduced foliage and fruit yield",
                "treatment": "Apply nitrogen-rich fertilizers like urea or ammonium nitrate, or organic alternatives like compost"
            },
            "Zinc": {
                "symptoms": "Small, narrow leaves, shortened internodes, chlorosis between veins",
                "treatment": "Apply zinc sulfate as foliar spray or soil application, use organic composts with zinc additives"
            },
            "Iron": {
                "symptoms": "Interveinal chlorosis in young leaves while veins remain green",
                "treatment": "Apply iron chelates or ferrous sulfate as foliar spray, improve soil organic matter"
            }
        }
    },
    "Bottle Gourd": {
        "info": {
            "scientific_name": "Lagenaria siceraria",
            "best_season": "Summer season crop that grows well in warm temperatures between 25°C to 35°C. Best planted from February to July in most regions",
            "best_soil": "Well-drained sandy loam to loamy soil with good organic matter content. Soil pH of 6.5-7.5 is ideal",
            "time_period": "Flowering begins 40-45 days after planting. Fruits are ready for harvest in 60-70 days from sowing",
            "estimated_cost": "₹40,000 to ₹60,000 per acre",
            "varieties": [
                "Pusa Naveen", "Pusa Sandesh", "Pusa Summer Prolific Long", "Punjab Komal", "Arka Bahar"
            ]
        },
        "diseases": {
            "Powdery Mildew": {
                "symptoms": "White powdery patches on leaves and stems that gradually cover entire surfaces. Leads to leaf yellowing, withering, and reduced yield",
                "causes": "Fungal disease caused by Erysiphe cichoracearum, favored by warm, dry days and cool, humid nights",
                "treatment": "Apply sulfur-based fungicides or systemic fungicides like Myclobutanil. Organic options include neem oil or potassium bicarbonate sprays",
                "prevention": "Proper plant spacing, avoid overhead irrigation, remove infected plants, and practice crop rotation"
            },
            "Downy Mildew": {
                "symptoms": "Yellow or pale green spots on upper leaf surfaces with grayish-white fungal growth on the undersides. Leaves eventually turn brown and die",
                "causes": "Caused by Pseudoperonospora cubensis, favored by cool, wet conditions with high humidity",
                "treatment": "Apply copper-based fungicides or specific downy mildew fungicides like Mancozeb or Metalaxyl",
                "prevention": "Provide good air circulation, avoid overhead irrigation, remove crop debris after harvest"
            },
            "Fusarium Wilt": {
                "symptoms": "Yellowing and wilting of leaves, brown discoloration of vascular tissue, stunted growth, and eventual plant death",
                "causes": "Soil-borne fungal pathogen Fusarium oxysporum that invades through roots and blocks water transport",
                "treatment": "No effective chemical treatment once infected. Use resistant varieties and soil solarization",
                "prevention": "Use disease-free seeds, practice crop rotation with non-host crops, manage soil pH and drainage"
            }
        },
        "pests": {
            "Red Pumpkin Beetle": {
                "symptoms": "Holes in leaves, damaged seedlings, reduced plant vigor",
                "description": "Small red-brown beetles that feed on leaves and flowers",
                "treatment": "Apply neem oil, spinosad, or carbaryl. Use row covers for young plants"
            },
            "Fruit Fly": {
                "symptoms": "Small punctures on fruits, maggots inside fruits, fruit rotting",
                "description": "Small flies that lay eggs in young fruits, larvae feed inside fruit causing rot",
                "treatment": "Use fruit fly traps with methyl eugenol, cover young fruits with paper bags, apply malathion or spinosad as needed"
            },
            "Aphids": {
                "symptoms": "Curled leaves, stunted growth, sticky honeydew on leaves",
                "description": "Small soft-bodied insects that suck plant sap, often clustered on new growth",
                "treatment": "Spray insecticidal soap, neem oil, or imidacloprid. Encourage natural predators like ladybugs"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves, stunted growth, thin stems, and poor fruit development",
                "treatment": "Apply nitrogen-rich fertilizers like urea or ammonium sulfate. Organic alternatives include compost or well-rotted manure"
            },
            "Calcium": {
                "symptoms": "Blossom end rot in fruits, distorted new leaves, poor root development",
                "treatment": "Apply calcium nitrate as foliar spray or soil application. Add lime or gypsum to calcium-deficient soils"
            },
            "Boron": {
                "symptoms": "Cracked fruits, hollow stems, stunted growth, and thickened leaves",
                "treatment": "Apply borax or solubor as foliar spray at very low concentrations (0.1-0.2%)"
            }
        }
    },
    "Cluster Beans": {
        "info": {
            "scientific_name": "Cyamopsis tetragonoloba",
            "best_season": "Summer season crop, preferably grown from March to July. Requires warm weather with temperatures between 25°C to 35°C",
            "best_soil": "Well-drained sandy loam to medium black soils. Tolerates slight salinity and alkalinity. Ideal pH range of 7.0-8.0",
            "time_period": "First picking starts 45-60 days after sowing. Harvesting period extends for about 3-4 months",
            "estimated_cost": "₹25,000 to ₹35,000 per acre",
            "varieties": [
                "Pusa Navbahar", "Pusa Sadabahar", "Durgapura Safed", "Durgapura Kanti", "HG-75"
            ]
        },
        "diseases": {
            "Bacterial Blight": {
                "symptoms": "Water-soaked lesions on leaves that turn brown with yellow halos. Severe infections cause defoliation",
                "causes": "Caused by Xanthomonas axonopodis pv. cyamopsidis, spreads through wind, rain, and infected seeds",
                "treatment": "Apply copper-based bactericides like copper oxychloride. Streptocycline can be effective when applied early",
                "prevention": "Use disease-free seeds, practice crop rotation, avoid overhead irrigation, remove infected plants"
            },
            "Powdery Mildew": {
                "symptoms": "White powdery growth on leaves, stems, and pods. Affected leaves become yellow and may fall prematurely",
                "causes": "Fungal disease caused by Leveillula taurica or Erysiphe polygoni, favored by moderate temperatures and high humidity",
                "treatment": "Apply sulfur-based fungicides or wettable sulfur. Organic options include neem oil or potassium bicarbonate",
                "prevention": "Provide adequate spacing between plants, avoid excessive nitrogen fertilization"
            },
            "Alternaria Leaf Spot": {
                "symptoms": "Brown circular spots with concentric rings on leaves. Severe cases lead to defoliation",
                "causes": "Caused by Alternaria cucumerina, thrives in warm, humid conditions with alternating wet and dry periods",
                "treatment": "Apply mancozeb or copper oxychloride at recommended doses",
                "prevention": "Crop rotation, proper field sanitation, use of disease-free seeds"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Curled leaves, stunted growth, honeydew secretion, and black sooty mold",
                "description": "Small soft-bodied insects that suck plant sap from tender shoots and leaves",
                "treatment": "Apply neem oil, insecticidal soap, or imidacloprid. Encourage natural predators like ladybugs"
            },
            "Pod Borer": {
                "symptoms": "Holes in pods, damaged seeds, frass (excrement) visible near entry holes",
                "description": "Caterpillars that bore into pods and feed on developing seeds",
                "treatment": "Apply Bacillus thuringiensis (Bt), spinosad, or neem-based insecticides. Use pheromone traps for monitoring"
            },
            "Jassids": {
                "symptoms": "Yellowing of leaf margins, leaf curling, 'hopper burn' where leaf edges turn brown",
                "description": "Small, wedge-shaped green insects that hop or fly when disturbed",
                "treatment": "Apply imidacloprid, thiamethoxam, or neem oil. Avoid water stress as it increases susceptibility"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Pale green or yellow older leaves, stunted growth, reduced branching and yield",
                "treatment": "Apply nitrogen fertilizers like urea, ammonium sulfate, or organic sources like compost and well-rotted manure"
            },
            "Iron": {
                "symptoms": "Interveinal chlorosis (yellowing between veins) in young leaves while veins remain green",
                "treatment": "Apply ferrous sulfate as foliar spray or use iron chelates for soil application"
            },
            "Zinc": {
                "symptoms": "Small, narrow leaves, shortened internodes, rosetting of terminal leaves",
                "treatment": "Apply zinc sulfate as foliar spray or soil application. Organic alternatives include composted manure with zinc additives"
            }
        }
    },
   "Cucumber": {
        "info": {
            "scientific_name": "Cucumis sativus",
            "best_season": "Zaid season (February to April), Kharif season (June to July), and Rabi season (October to December) in some regions. Requires temperatures between 24°C and 32°C",
            "best_soil": "Well-drained sandy loam to loamy soils rich in organic matter with pH 6.0-7.5",
            "time_period": "70 to 90 days from sowing to harvest",
            "estimated_cost": "₹22,300 to ₹34,700 per acre",
            "varieties": [
                "Pusa Uday", "Kashi Abhijeet", "Pant Khira-1", "Pant Khira-2", 
                "NS 408", "VNS Hybrid-202", "Pusa Barkha", "Kashi Bahar",
                "Japanese Long Green", "Green Long", "Pusa Sanyog", "Punjab Naveen",
                "Kashi Nayan", "Pusa Samridhi"
            ]
        },
        "diseases": {
            "Powdery Mildew": {
                "symptoms": "White powdery patches on leaves, stems, and buds. Leaves may curl, yellow, dry, and fall off prematurely",
                "causes": "Fungal spores spread through wind, especially in dry, warm climates",
                "treatment": "Spray with wettable sulfur, karathane (dinocap), or hexaconazole. Use potassium bicarbonate as organic option",
                "prevention": "Use resistant varieties, maintain good air circulation, avoid overhead irrigation, remove infected plant parts"
            },
            "Downy Mildew": {
                "symptoms": "Yellow angular spots on upper side of leaves; undersides show grayish mold. Leads to rapid leaf death and stunted growth",
                "causes": "Spreads through airborne spores, favored by high humidity and wet leaves",
                "treatment": "Spray with metalaxyl + mancozeb, cymoxanil + mancozeb, or chlorothalonil",
                "prevention": "Avoid water stagnation and overcrowding, grow resistant varieties, practice early morning irrigation"
            },
            "Anthracnose": {
                "symptoms": "Water-soaked round spots on leaves and fruits; spots turn black with sunken centers. Can lead to fruit rot",
                "causes": "Fungal spores spread by rain splash and tools. Persists in crop residues",
                "treatment": "Spray with carbendazim, copper oxychloride, or chlorothalonil at 10-14-day intervals",
                "prevention": "Avoid water splashing and overhead irrigation, remove plant debris and rotate crops"
            },
            "Fusarium Wilt": {
                "symptoms": "Lower leaves turn yellow and droop; whole plant wilts, especially during midday. Brown streaks visible in vascular tissues",
                "causes": "Soil-inhabiting fungus enters through roots; survives in soil for many years",
                "treatment": "Apply Trichoderma viride with compost or as soil drench. Use carbendazim or thiophanate-methyl as soil fungicide",
                "prevention": "Use resistant varieties and certified seeds, practice crop rotation with non-cucurbit crops, avoid overwatering"
            },
            "Bacterial Wilt": {
                "symptoms": "Sudden wilting of entire plant or individual vines; white sticky bacterial ooze may come out when stem is cut",
                "causes": "Spread by feeding activity of cucumber beetles carrying bacteria in their mouthparts",
                "treatment": "No direct chemical treatment. Control cucumber beetles using imidacloprid or neem oil sprays",
                "prevention": "Use floating row covers, monitor and control beetle population early, remove and destroy infected plants"
            },
            "Cucumber Mosaic Virus": {
                "symptoms": "Mosaic or mottled pattern on leaves, stunted growth, leaf deformation, fruit yellowing, blistering, and curling",
                "causes": "Spread by aphids in a non-persistent manner; also through infected seed or sap",
                "treatment": "No direct treatment for viruses. Spray imidacloprid, acetamiprid, or neem oil to control aphid vectors",
                "prevention": "Use virus-free seeds and resistant varieties, remove and destroy infected plants, use reflective mulches"
            }
        },
        "pests": {
            "Aphids": {
                "symptoms": "Tiny soft-bodied insects found on the underside of leaves. Leaves curl, wrinkle, and become sticky. May transmit viral diseases",
                "description": "Green/black aphids that suck plant sap",
                "treatment": "Spray imidacloprid (0.3 ml/l) or acetamiprid (0.2 g/l). Neem oil (5 ml/l) as organic option. Introduce ladybird beetles"
            },
            "Whiteflies": {
                "symptoms": "Tiny white insects fly off when disturbed. Yellowing and stunted growth; leaves become sticky. Transmit viral diseases",
                "description": "Small white flying insects",
                "treatment": "Spray with buprofezin, imidacloprid, or pyriproxyfen. Use sticky traps and neem oil spray"
            },
            "Red Spider Mites": {
                "symptoms": "Fine webbing on leaves. Leaves appear yellow or bronze and may drop. Common in hot, dry climates",
                "description": "Tiny spider-like pests",
                "treatment": "Spray miticides like propargite, dicofol, or abamectin. Neem oil at higher doses can suppress populations"
            },
            "Fruit Fly": {
                "symptoms": "Eggs laid inside young fruits; fruits show puncture marks. Affected fruits rot or drop prematurely",
                "description": "Small flies that lay eggs in fruits",
                "treatment": "Use methyl eugenol traps (pheromone traps). Spray malathion (2 ml/l) with jaggery solution as bait. Remove infested fruits"
            },
            "Cucumber Beetle": {
                "symptoms": "Chew leaves and stems; transmit bacterial wilt disease",
                "description": "Yellow-green beetles with black spots or stripes",
                "treatment": "Spray carbaryl, chlorpyrifos, or spinosad. Apply neem oil to deter feeding. Use row covers early in season"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Pale yellowing of older leaves (bottom of plant). Stunted growth, thin vines, fewer flowers and fruits",
                "treatment": "Apply Urea (46% N) - 40-50 kg/acre in split doses. Use composted farmyard manure (FYM) or vermicompost"
            },
            "Phosphorus": {
                "symptoms": "Dark green or purplish discoloration on older leaves. Poor root development and delayed flowering/fruiting",
                "treatment": "Apply Single Super Phosphate (SSP) or DAP (Di-Ammonium Phosphate). Use bone meal or rock phosphate in organic farming"
            },
            "Potassium": {
                "symptoms": "Yellowing and browning of leaf edges (leaf scorching). Weak stems, poor fruit development, low disease resistance",
                "treatment": "Apply Muriate of Potash (MOP) - 20-25 kg/acre. Organic option: wood ash, banana peel tea, or sulphate of potash (SOP)"
            },
            "Calcium": {
                "symptoms": "Young leaves curl and appear distorted. Blossom end rot in fruits (black sunken spot at fruit tip)",
                "treatment": "Apply calcium nitrate as foliar spray (1%) or soil drench. Use dolomite lime, eggshell compost, or bone meal organically"
            },
            "Magnesium": {
                "symptoms": "Interveinal chlorosis (yellowing between veins) on older leaves. Leaf edges may curl upwards",
                "treatment": "Apply magnesium sulfate (Epsom salt) - 5 kg/acre or as 1% foliar spray. Organic: seaweed extract or wood ash"
            }
        }
    },
    "Bitter Gourd": {
        "info": {
            "scientific_name": "Momordica charantia",
            "best_season": "Warm-season crop. In Northern India: February-March (Summer), June-July (Monsoon), September (Autumn). In Southern India: Can be grown year-round.",
            "best_soil": "Well-drained sandy loam or loamy soils rich in organic matter with pH 6.0-6.7",
            "time_period": "Germination: 6-10 days. First harvest: 55-65 days after sowing. Harvesting continues for 1.5-2 months.",
            "estimated_cost": "₹40,000-₹55,000 per acre",
            "varieties": [
                "Pusa Do Mausami", "Arka Harit", "Phule Priyanka", "Coimbatore Long", 
                "Pusa Vishesh", "Hirkani", "Green Long", "Phule Ujjwala", "MDU 1",
                "Phule Green Gold", "Indam 111", "Kanchan", "Priya Hybrid"
            ]
        },
        "diseases": {
            "Downy Mildew": {
                "symptoms": "Yellow angular spots on upper leaf surface, purplish mold on underside, premature leaf drop",
                "causes": "Caused by Pseudoperonospora cubensis, favored by humid, wet conditions",
                "treatment": "Spray Mancozeb 75% WP at 2.0 g/liter of water or Metalaxyl",
                "prevention": "Ensure good air circulation, avoid overhead irrigation, plant resistant varieties"
            },
            "Powdery Mildew": {
                "symptoms": "White powdery spots on upper side of leaves, gradual leaf yellowing and drying",
                "causes": "Caused by Erysiphe cichoracearum, favored by warm and dry weather with high humidity",
                "treatment": "Apply Sulphur 80% WP at 2 g/liter or Hexaconazole",
                "prevention": "Avoid dense planting, use resistant cultivars"
            },
            "Anthracnose": {
                "symptoms": "Sunken dark spots on fruits and stems, dark brown to black lesions on leaves",
                "causes": "Caused by Colletotrichum lagenarium, favored by warm and wet weather",
                "treatment": "Spray Carbendazim 50% WP at 1 g/liter or Chlorothalonil",
                "prevention": "Practice crop rotation, avoid working in wet fields"
            },
            "Mosaic Virus": {
                "symptoms": "Light and dark green mottling on leaves, distorted wrinkled leaves, reduced fruit size",
                "causes": "Transmitted by aphids and whiteflies, caused by Cucumber mosaic virus",
                "treatment": "Spray Imidacloprid 17.8% SL at 0.3 ml/liter to control vectors",
                "prevention": "Control aphid/whitefly populations, use reflective mulches, remove infected plants"
            }
        },
        "pests": {
            "Fruit Fly": {
                "symptoms": "Fruit deformation and premature drop, oozing sap, maggots inside fruits",
                "description": "Bactrocera cucurbitae lays eggs inside developing fruits",
                "treatment": "Spray Malathion 50% EC at 1 ml/liter, use bait spray with jaggery + Malathion"
            },
            "Red Pumpkin Beetle": {
                "symptoms": "Holes in leaves, flowers and young shoots, wilting of seedlings",
                "description": "Aulacophora foveicollis beetles feed on plant parts",
                "treatment": "Spray Carbaryl (4 g/L) or Imidacloprid (0.5 ml/L), handpick adult beetles"
            },
            "Aphids": {
                "symptoms": "Clusters of small black/green insects under leaves, sticky honeydew, leaf curling",
                "description": "Aphis gossypii suck plant sap and transmit viruses",
                "treatment": "Spray Imidacloprid (0.5 ml/L) or Thiamethoxam, use Neem oil (3%)"
            },
            "Whiteflies": {
                "symptoms": "Tiny white insects flying from leaves, yellowing and wilting",
                "description": "Bemisia tabaci transmit viral diseases",
                "treatment": "Spray Imidacloprid, Acetamiprid or Neem oil (5 ml/L), use yellow sticky traps"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Yellowing of older leaves (bottom first), poor vine growth, small pale leaves",
                "treatment": "Apply Urea (46% N) @ 50-60 kg/acre, foliar spray of urea solution (1%)"
            },
            "Phosphorus": {
                "symptoms": "Stunted root/shoot growth, purplish/reddish leaf discoloration, delayed flowering",
                "treatment": "Apply Single Super Phosphate (SSP) @ 100 kg/acre, use bone meal or rock phosphate"
            },
            "Potassium": {
                "symptoms": "Leaf edges turn yellow and brown (scorching), small deformed fruits",
                "treatment": "Apply Muriate of Potash (MOP) @ 40-50 kg/acre, use wood ash or banana peel compost"
            },
            "Calcium": {
                "symptoms": "New leaves distorted/hook-shaped, blossom-end rot in fruits, shoot tip dieback",
                "treatment": "Spray Calcium Nitrate (1%) or Calcium Chloride (0.5%), use crushed egg shells or gypsum"
            }
        }
    },
    "Pumpkin" : {
        "info": {
            "scientific_name": "Cucurbita spp.",
            "best_season": "Summer (Feb-April) and monsoon (June-July)",
            "best_soil": "Well-drained sandy loam or loamy soil with pH 6.5-7.5",
            "time_period": "90-120 days from planting to harvest",
            "estimated_cost": "₹30,000-₹50,000 per acre",
            "varieties": [
                "Small Sugar", "Jack O'Lantern", "Cinderella", "Atlantic Giant", 
                "Baby Boo", "Jarrahdale", "Lumina", "Fairytale"
            ]
        },
        "diseases": {
            "Powdery Mildew": {
                "symptoms": "White powdery patches appear on leaves, leading to yellowing and drying",
                "causes": "Fungus Podosphaera xanthii thrives in dry and warm conditions",
                "treatment": "Spray sulfur-based fungicides or neem oil",
                "prevention": "Use resistant varieties, avoid overcrowding, maintain proper spacing",
                "fertilizers": "Potassium-rich fertilizers (Muriate of Potash)",
                "compost": "Neem cake compost and vermicompost"
            },
            "Downy Mildew": {
                "symptoms": "Yellow patches on leaves, with greyish mold underneath. Leaves eventually dry and die",
                "causes": "Fungus Pseudoperonospora cubensis spreads through moisture and high humidity",
                "treatment": "Apply Copper fungicides or Mancozeb spray",
                "prevention": "Rotate crops regularly, avoid overhead irrigation, water plants early morning",
                "fertilizers": "Calcium nitrate and Potassium sulfate",
                "compost": "Cow dung compost or bio-compost enriched with Trichoderma"
            },
            "Anthracnose": {
                "symptoms": "Dark sunken spots develop on leaves and fruits, leading to fruit rot",
                "causes": "Colletotrichum spp. spreads through infected seeds or splashing rainwater",
                "treatment": "Spray Chlorothalonil or Copper oxychloride",
                "prevention": "Avoid excessive moisture, remove infected plants, maintain field hygiene",
                "fertilizers": "Balanced NPK (Nitrogen-Phosphorus-Potassium)",
                "compost": "Bone meal and Neem cake compost"
            },
            "Fusarium Wilt": {
                "symptoms": "Leaves wilt suddenly, stems turn brown or reddish. Plant may die prematurely",
                "causes": "Soil-borne fungus Fusarium oxysporum infects through roots",
                "treatment": "Apply Trichoderma-enriched biofertilizers",
                "prevention": "Use disease-free seeds, practice crop rotation, conduct soil solarization",
                "fertilizers": "Phosphorus-rich fertilizers (Rock phosphate)",
                "compost": "Vermicompost, Neem cake, well-rotted farmyard manure"
            },
            "Bacterial Wilt": {
                "symptoms": "Sudden wilting of vines, yellow streaks on stems, plants eventually die",
                "causes": "Bacterium Erwinia tracheiphila spreads through insect vectors like beetles",
                "treatment": "No chemical cure - remove infected plants immediately",
                "prevention": "Control cucumber beetles, use resistant varieties, practice sanitation",
                "fertilizers": "Zinc sulfate and Boron",
                "compost": "Cow dung compost mixed with Neem cake"
            }
        },
        "pests": {
            "Squash Bugs": {
                "symptoms": "Yellow spots on leaves that turn brown, wilting plants",
                "description": "Grayish-brown bugs that suck plant juices",
                "treatment": "Handpick bugs and eggs, use insecticidal soap or neem oil"
            },
            "Cucumber Beetles": {
                "symptoms": "Holes in leaves, can transmit bacterial wilt",
                "description": "Yellow-green beetles with black spots or stripes",
                "treatment": "Use row covers, apply kaolin clay or pyrethrin"
            },
            "Squash Vine Borers": {
                "symptoms": "Sudden wilting of vines, sawdust-like frass at base",
                "description": "White caterpillars that bore into vines",
                "treatment": "Inject Bt into vines, wrap base with aluminum foil"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Older leaves turn pale yellow, stunted growth",
                "treatment": "Apply blood meal, fish emulsion, or composted manure"
            },
            "Phosphorus": {
                "symptoms": "Purplish discoloration on leaves, poor root development",
                "treatment": "Apply bone meal or rock phosphate"
            },
            "Potassium": {
                "symptoms": "Yellowing leaf edges, weak stems",
                "treatment": "Apply wood ash or kelp meal"
            },
            "Calcium": {
                "symptoms": "Blossom end rot in fruits, distorted new growth",
                "treatment": "Apply gypsum or calcium nitrate"
            }
        }
    },
    "Grape": {
        "info": {
            "scientific_name": "Vitis vinifera",
            "best_season": "Spring planting (March-April) after frost in temperate regions. Fall planting (October-November) in tropics. Ideal temperature: 15-35°C.",
            "best_soil": "Well-drained sandy loam with pH 5.5-6.5. Avoid clayey/waterlogged soils.",
            "time_period": "First harvest in 2-3 years after planting. Yield lifespan: 15-30 years with care.",
            "estimated_cost": "₹2,00,000--₹4,00,000 per acre",
            "varieties": [
                "Thompson Seedless", "Flame Seedless", "Cabernet Sauvignon", 
                "Shiraz", "Bangalore Blue", "Anab-e-Shahi"
            ]
        },
        "diseases": {
            "Powdery Mildew": {
                "symptoms": "White powdery patches on leaves resembling talcum powder, curled edges, brown scorched patches, corky scars on berries",
                "causes": "Fungus Uncinula necator, thrives in warm dry conditions",
                "treatment": "Sulfur sprays (2-3 g/L), Tebuconazole (0.5 mL/L), Myclobutanil (0.3 mL/L), Bacillus subtilis (2 g/L)",
                "prevention": "Prune for airflow, avoid dense canopies, avoid overhead irrigation"
            },
            "Downy Mildew": {
                "symptoms": "Yellow 'oil spots' on upper leaf surface, white cottony sporulation underneath, purple-brown discoloration on berries",
                "causes": "Fungus Plasmopara viticola, favors cool wet conditions",
                "treatment": "Copper-based fungicides (Bordeaux mixture), Metalaxyl + Mancozeb (2 g/L), Fosetyl-Al (2.5 g/L)",
                "prevention": "Remove infected leaves, use drip irrigation, maintain good air circulation"
            },
            "Anthracnose": {
                "symptoms": "Small circular spots with dark margins and gray centers on leaves, sunken black spots with pinkish spore masses on berries",
                "causes": "Fungus Elsinoë ampelina, spreads through rain splash",
                "treatment": "Mancozeb (2.5 g/L), Chlorothalonil (2 g/L), Azoxystrobin (0.5 mL/L)",
                "prevention": "Sanitation (burn infected prunings), avoid wounding berries"
            },
            "Black Rot": {
                "symptoms": "Red-brown circular spots with black pycnidia on leaves, shriveled black 'mummies' on berries",
                "causes": "Fungus Guignardia bidwellii, persists in infected plant material",
                "treatment": "Captan (3 g/L) at bud break, Pyraclostrobin + Boscalid (0.5 mL/L)",
                "prevention": "Remove mummies from vines post-harvest, canopy management"
            }
        },
        "pests": {
            "Grape Berry Moth": {
                "symptoms": "Larvae tunneling into berries, frass at entry holes",
                "description": "Small moth whose larvae feed on grape berries",
                "treatment": "Spinosad (0.5 mL/L) + pheromone traps, Bacillus thuringiensis"
            },
            "Aphids": {
                "symptoms": "Curled leaves, sticky honeydew, sooty mold growth",
                "description": "Small sap-sucking insects that transmit viruses",
                "treatment": "Imidacloprid (0.3 mL/L), neem oil, introduce ladybugs"
            }
        },
        "deficiencies": {
            "Nitrogen": {
                "symptoms": "Pale yellow leaves, reduced growth and yield",
                "treatment": "Urea (50 kg/acre), composted manure"
            },
            "Potassium": {
                "symptoms": "Brown leaf edges, weak stems, poor fruit quality",
                "treatment": "MOP (40 kg/acre), wood ash"
            },
            "Zinc": {
                "symptoms": "Small leaves, short internodes, rosetting",
                "treatment": "ZnSO₄ spray (0.5%), zinc chelates"
            }
        }
    },

}

def get_crop_info(crop_name):
    """
    Get detailed information about a specific crop
    
    Args:
        crop_name: Name of the crop
        
    Returns:
        dict: Detailed information about the crop or None if not found
    """
    crop_name = standardize_crop_name(crop_name)
    return CROP_DATABASE.get(crop_name)

def get_crop_disease_info(crop_name, disease_name=None):
    """
    Get disease information for a specific crop
    
    Args:
        crop_name: Name of the crop
        disease_name: Optional specific disease to get info about
        
    Returns:
        dict: Disease information or None if not found
    """
    crop_name = standardize_crop_name(crop_name)
    crop_data = CROP_DATABASE.get(crop_name)
    
    if not crop_data or 'diseases' not in crop_data:
        return None
    
    if disease_name:
        # Try to find closest matching disease
        for d_name, d_info in crop_data['diseases'].items():
            if disease_name.lower() in d_name.lower():
                return {d_name: d_info}
        return None
    
    return crop_data['diseases']

def get_crop_pest_info(crop_name, pest_name=None):
    """
    Get pest information for a specific crop
    
    Args:
        crop_name: Name of the crop
        pest_name: Optional specific pest to get info about
        
    Returns:
        dict: Pest information or None if not found
    """
    crop_name = standardize_crop_name(crop_name)
    crop_data = CROP_DATABASE.get(crop_name)
    
    if not crop_data or 'pests' not in crop_data:
        return None
    
    if pest_name:
        # Try to find closest matching pest
        for p_name, p_info in crop_data['pests'].items():
            if pest_name.lower() in p_name.lower():
                return {p_name: p_info}
        return None
    
    return crop_data['pests']

def get_crop_deficiency_info(crop_name, deficiency_name=None):
    """
    Get nutrient deficiency information for a specific crop
    
    Args:
        crop_name: Name of the crop
        deficiency_name: Optional specific deficiency to get info about
        
    Returns:
        dict: Deficiency information or None if not found
    """
    crop_name = standardize_crop_name(crop_name)
    crop_data = CROP_DATABASE.get(crop_name)
    
    if not crop_data or 'deficiencies' not in crop_data:
        return None
    
    if deficiency_name:
        # Try to find closest matching deficiency
        for d_name, d_info in crop_data['deficiencies'].items():
            if deficiency_name.lower() in d_name.lower():
                return {d_name: d_info}
        return None
    
    return crop_data['deficiencies']

def get_available_crops():
    """
    Get list of all available crops in the database
    
    Returns:
        list: Names of all available crops
    """
    return list(CROP_DATABASE.keys())

def standardize_crop_name(crop_name):
    """
    Standardize crop name to match database keys
    
    Args:
        crop_name: Input crop name
        
    Returns:
        string: Standardized crop name
    """
    crop_name = crop_name.strip()
    
    # Handle common aliases
    aliases = {
    "okra": "Ladyfinger (Okra)",
    "ladyfinger": "Ladyfinger (Okra)",
    "bhindi": "Ladyfinger (Okra)",
    "tinda": "Watermelon",
    "anar": "Pomegranate",
    "karela": "Bitter Gourd",
    "bitter melon": "Bitter Gourd",
    "bitter gourd": "Bitter Gourd",
    "kaddu": "Pumpkin",
    "sitaphal": "Pumpkin",
    "yellow gourd": "Pumpkin"
}
    
    if crop_name.lower() in aliases:
        return aliases[crop_name.lower()]
    
    # Try to find a match in the database
    for db_crop in CROP_DATABASE.keys():
        if crop_name.lower() in db_crop.lower():
            return db_crop
    
    return crop_name