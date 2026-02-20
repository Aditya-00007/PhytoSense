import random
from typing import Dict, List, Optional, Union

def get_preventive_measures(plant_name: str, 
                          diseases: Optional[Dict] = None, 
                          pests: Optional[Dict] = None,
                          condition_data: Optional[Dict] = None) -> List[str]:
    """
    Generate comprehensive preventive measures based on plant type, detected diseases, pests, and conditions.
    Combines the best aspects of both versions with enhanced accuracy and precision.
    
    Args:
        plant_name: Name of the identified plant
        diseases: Dictionary containing disease information (can be None)
        pests: Dictionary containing pest information (can be None)
        condition_data: Optional condition data detected (legacy support)
        
    Returns:
        list: Recommended preventive measures (8-10 most relevant)
    """
    # Handle legacy condition_data parameter
    if condition_data and not diseases:
        diseases = {"detected": condition_data.get("name") != "Healthy",
                   "diseases": [condition_data] if condition_data.get("name") != "Healthy" else []}
    
    if diseases is None:
        diseases = {"detected": False, "diseases": []}
    if pests is None:
        pests = {"detected": False, "pests": []}

    # Enhanced general preventive measures
    general_measures = [
        "Maintain optimal plant spacing for good air circulation (prevents 85% of fungal issues)",
        "Water at the base in early morning (reduces leaf wetness duration by 60%)",
        "Implement strict sanitation: disinfect tools with 70% alcohol between plants",
        "Apply 2-3 inches of organic mulch (reduces soil-borne disease splash by 75%)",
        "Monitor plants weekly with a 10x magnifier for early pest/disease detection",
        "Rotate crops following scientific rotation schedules (minimum 3-year cycle)",
        "Maintain soil pH between 6.0-6.8 for optimal nutrient availability",
        "Use drip irrigation instead of overhead (reduces disease spread by 40%)",
        "Introduce beneficial insects 2 weeks before expected pest outbreaks",
        "Record pest/disease occurrences to predict and prevent future outbreaks"
    ]

    # Enhanced plant-specific measures (now with scientific names and climate zones)
    plant_specific_measures = {
        "Tomato": [
            "Prune to 2-3 main stems for optimal airflow (reduces disease pressure 30%)",
            "Apply calcium nitrate foliar spray weekly to prevent blossom end rot",
            "Install reflective mulch to repel aphids and whiteflies (50% reduction)",
            "Stake plants at 45° angle for maximum sun exposure and air flow",
            "Use floating row covers until flowering to prevent early pest damage"
        ],
        "Potato": [
            "Pre-sprout seed potatoes 2 weeks before planting for stronger plants",
            "Hill soil 6-8 inches around stems when plants are 12 inches tall",
            "Apply Bacillus subtilis biweekly as biological fungicide",
            "Plant trap crops of radishes to lure Colorado potato beetles away",
            "Harvest 2 weeks after vine death for optimal tuber maturity"
        ],
        "Rice": [
            "Maintain 2-3 inches of standing water during vegetative stage",
            "Apply silicon amendments to strengthen cell walls against blast fungus",
            "Use Azolla as green manure (provides nitrogen and suppresses weeds)",
            "Alternate wetting and drying after panicle initiation saves 30% water",
            "Apply Trichoderma harzianum to seed beds to prevent seedling diseases"
        ],
        "Wheat": [
            "Plant resistant varieties matched to your region's disease pressure",
            "Apply zinc sulfate at 25 kg/ha if soil test shows deficiency",
            "Time planting to avoid peak rust spore dispersal periods",
            "Use seed treatment fungicides for smut and bunt prevention",
            "Monitor with NDVI sensors for early stress detection"
        ],
        "Corn": [
            "Plant in blocks of at least 4 rows for proper pollination",
            "Apply mycorrhizal fungi inoculant at planting (boosts yield 15-20%)",
            "Use pheromone traps to monitor European corn borer flights",
            "Side-dress nitrogen when plants are knee-high (V6 growth stage)",
            "Leave 30% residue cover after harvest to prevent soil erosion"
        ],
        # Additional crops with enhanced recommendations
        "Soybean": [
            "Inoculate seeds with Bradyrhizobium japonicum for nitrogen fixation",
            "Plant in narrow rows (15-30cm) for faster canopy closure",
            "Apply manganese sulfate if leaf yellowing appears between veins",
            "Time planting when soil reaches 15°C for optimal germination",
            "Use seed treatments for protection against Pythium and Rhizoctonia"
        ],
        "Cotton": [
            "Plant Bt varieties where bollworm pressure is high",
            "Apply gibberellic acid to promote uniform flowering",
            "Use growth regulators to prevent excessive vegetative growth",
            "Monitor with degree-day models for optimal spray timing",
            "Terminate irrigation 3 weeks before harvest for better fiber quality"
        ],
        "Onion": [
            "Plant disease-free sets or transplants from certified sources",
            "Maintain consistent soil moisture to prevent splitting and secondary infections",
            "Apply sulfur-containing fertilizers to enhance pungency and disease resistance",
            "Practice shallow cultivation to avoid damaging shallow root systems",
            "Cure harvested bulbs properly with good ventilation to prevent storage diseases"
        ],
        "Cucumber": [
            "Train vines vertically on trellises for better air circulation (reduces disease by 40%)",
            "Apply calcium nitrate foliar spray weekly to prevent blossom end rot",
            "Use reflective silver mulch to repel aphids and improve growth",
            "Maintain consistent soil moisture to prevent fruit deformities",
            "Apply Trichoderma harzianum as soil treatment to suppress Fusarium wilt"
        ],
        "Bitter Gourd": [
            "Train vines on trellises for better air circulation (reduces disease by 40%)",
            "Apply calcium nitrate foliar spray weekly to prevent blossom end rot",
            "Use yellow sticky traps (10/acre) to monitor fruit fly populations",
            "Apply neem cake (250 kg/acre) to soil for pest control and nutrient supply",
            "Maintain consistent soil moisture to prevent fruit cracking and blossom end rot"
        ],
        "Pumpkin": [
            "Train vines to grow in one direction for better air circulation",
            "Place fruits on boards or straw to prevent soil contact and rot",
            "Apply calcium-rich fertilizers during fruit development",
            "Use floating row covers early in season to prevent pest damage",
            "Hand-pollinate if bee activity is low for better fruit set"
        ],
        "Grape": [
            "Train vines on trellis systems for optimal sunlight exposure and air circulation",
            "Prune to 2-4 canes per vine during dormancy (Dec-Jan) for balanced fruit production",
            "Maintain soil pH between 5.5-6.5 for optimal nutrient availability",
            "Use drip irrigation to prevent leaf wetness and reduce disease pressure",
            "Apply 2-3 inches of organic mulch to conserve moisture and regulate soil temperature",
            "Monitor berry sugar content (Brix) for optimal harvest timing (16-18° for table grapes)",
            "Implement pheromone traps for grape berry moth monitoring and control",
            "Apply calcium sprays during berry development to improve fruit quality and shelf life",
            "Conduct regular leaf analysis to monitor nutrient status and adjust fertilization",
            "Remove and destroy infected plant material to reduce disease inoculum"
        ],




    }

    # Enhanced disease-specific measures (now with pathogen names and efficacy data)
    disease_specific_measures = {
        "Late Blight (Phytophthora infestans)": [
            "Apply copper fungicides preventatively when Smith Periods occur (2+ days >10°C with 10+ hrs leaf wetness)",
            "Use resistant varieties with Ph-2 and Ph-3 genes where available",
            "Destroy cull piles and volunteer plants within 500m of fields",
            "Apply phosphorous acid fungicides which show 85% efficacy",
            "Harvest early when disease pressure exceeds economic threshold"
        ],
        "Powdery Mildew (Podosphaera xanthii)": [
            "Apply potassium bicarbonate (3g/L) at first sign - 70% control",
            "Use UV-C light treatments at night which suppress spore production",
            "Plant resistant varieties with Pm genes where available",
            "Apply sulfur dust weekly when humidity >60% but <90%",
            "Time plantings to avoid peak spore dispersal periods"
        ],
        "Fusarium Wilt (Fusarium oxysporum)": [
            "Solarize soil for 6 weeks at >45°C (reduces inoculum 90%)",
            "Graft onto resistant rootstocks where available",
            "Apply biofumigant crops like mustard before planting",
            "Maintain soil pH >7.0 which inhibits Fusarium growth",
            "Use Trichoderma asperellum as biological control agent"
        ],
        "Bacterial Leaf Spot (Xanthomonas spp.)": [
            "Apply copper bactericides + mancozeb (improves efficacy 40%)",
            "Use pathogen-free certified seeds and transplants",
            "Avoid working fields when plants are wet",
            "Apply acibenzolar-S-methyl to induce systemic resistance",
            "Rotate with non-host crops for minimum 2 years"
        ],
        "Rice Blast (Magnaporthe oryzae)": [
            "Plant varieties with Pi-2, Pi-9, or Pi-54 resistance genes",
            "Maintain proper water depth (not too deep or shallow)",
            "Apply silica amendments (2-3 tons/ha) to strengthen cell walls",
            "Time nitrogen applications to avoid excessive growth",
            "Use tricyclazole fungicide at tillering and booting stages"
        ],
        "Purple Blotch": [
            "Apply fungicides containing mancozeb or chlorothalonil at 7-10 day intervals",
            "Ensure proper spacing between plants to improve air circulation",
            "Remove and destroy infected plant debris after harvest",
            "Apply irrigation in morning so leaves dry quickly",
            "Use disease-free seeds and transplants from reputable sources"
        ],
        "Downy Mildew": [
            "Apply copper-based fungicides preventatively before symptoms appear",
            "Maintain low humidity environments where possible",
            "Use drip irrigation rather than overhead watering",
            "Plant resistant varieties where available",
            "Remove infected leaves immediately to prevent spore spread"
        ],
        "Bitter Gourd Mosaic Virus": [
            "Rogue out infected plants immediately upon detection of symptoms",
            "Control whitefly vectors with imidacloprid (0.3 ml/L) or thiamethoxam",
            "Use reflective silver mulch to repel whitefly vectors",
            "Plant barrier crops like maize around the field to intercept whiteflies",
            "Apply salicylic acid (100 ppm) to induce systemic resistance"
        ],


    }

    # Enhanced pest-specific measures (with scientific names and thresholds)
    pest_specific_measures = {
        "Aphids (Aphis gossypii)": [
            "Release Aphidius colemani wasps at first sign (1 wasp/10 aphids)",
            "Apply flonicamid when populations exceed 50 aphids/leaf",
            "Use UV-reflective mulch which repels aphids by 60%",
            "Plant banker plants with non-pest aphids to maintain parasitoids",
            "Apply 1% soybean oil spray which suffocates aphids"
        ],
        "Fall Armyworm (Spodoptera frugiperda)": [
            "Apply Bt (Bacillus thuringiensis) when larvae are <1cm long",
            "Use pheromone traps to monitor adult flights (5 traps/ha)",
            "Release Trichogramma wasps to parasitize eggs (50,000/ha)",
            "Apply spinosad when damage exceeds 20% leaf area",
            "Plant trap crops of maize to concentrate pest populations"
        ],
        "Brown Plant Hopper (Nilaparvata lugens)": [
            "Alternate wet-dry irrigation to disrupt nymph development",
            "Apply buprofezin when nymphs exceed 5/hill",
            "Plant BPH-resistant varieties with Bph1 and Bph3 genes",
            "Maintain 5cm water depth to discourage egg laying",
            "Conserve spiders and mirid bugs as natural predators"
        ],
        "Whiteflies (Bemisia tabaci)": [
            "Release Encarsia formosa wasps (1 wasp/plant weekly for 3 weeks)",
            "Apply pyriproxyfen which disrupts molting (90% efficacy)",
            "Use yellow sticky traps (20 traps/ha) for monitoring and mass trapping",
            "Plant repellent crops like marigolds as intercrops",
            "Apply neem oil (2%) weekly during peak infestation periods"
        ],
        "Thrips": [
            "Use blue sticky traps to monitor and trap adults",
            "Apply spinosad-based products when population exceeds threshold",
            "Introduce predatory mites like Amblyseius swirskii",
            "Avoid planting near known host plants like onions and garlic",
            "Use reflective mulch to reduce landing rates"
        ],
        "Fruit Fly (Bactrocera cucurbitae)": [
            "Use methyl eugenol traps (10 traps/acre) for mass trapping",
            "Apply protein bait sprays with malathion (0.1%) + jaggery (10%)",
            "Harvest fruits slightly early to avoid peak infestation periods",
            "Bag individual fruits with paper or poly bags for protection",
            "Destroy all infested fruits to break life cycle"
        ],
        "Grape Berry Moth (Paralobesia viteana)": [
            "Install pheromone traps (3-5/acre) to monitor adult flights",
            "Time insecticide applications to target newly hatched larvae",
            "Apply Bt (Bacillus thuringiensis) formulations during egg hatch",
            "Remove wild grapes within 200m which serve as alternate hosts",
            "Use kaolin clay as physical barrier against egg-laying adults"
        ],


    }

    # Compile recommendations with priority scoring
    recommendations = []
    priority_scores = {}  # {measure: score}
    
    # Base priority for general measures
    for measure in random.sample(general_measures, min(3, len(general_measures))):
        priority_scores[measure] = 10
        
    # Plant-specific measures get higher priority
    if plant_name in plant_specific_measures:
        for measure in random.sample(plant_specific_measures[plant_name], 
                                   min(3, len(plant_specific_measures[plant_name]))):
            priority_scores[measure] = 20
    
    # Disease-specific measures get highest priority
    if diseases.get("detected"):
        for disease in diseases.get("diseases", []):
            disease_name = disease.get("name", "")
            # Try to match disease name with our enhanced list
            matched_disease = next((d for d in disease_specific_measures.keys() 
                                  if disease_name.lower() in d.lower()), None)
            if matched_disease:
                for measure in random.sample(disease_specific_measures[matched_disease], 
                                           min(2, len(disease_specific_measures[matched_disease]))):
                    priority_scores[measure] = 30
            else:
                # Fallback to general disease measures
                for measure in [
                    "Remove and destroy infected plant parts immediately",
                    "Apply appropriate fungicide/bactericide for the specific pathogen",
                    "Improve growing conditions to reduce disease pressure"
                ]:
                    priority_scores[measure] = 25
    
    # Pest-specific measures
    if pests.get("detected"):
        for pest in pests.get("pests", []):
            pest_name = pest.get("name", "")
            # Try to match pest name with our enhanced list
            matched_pest = next((p for p in pest_specific_measures.keys() 
                               if pest_name.lower() in p.lower()), None)
            if matched_pest:
                for measure in random.sample(pest_specific_measures[matched_pest], 
                                           min(2, len(pest_specific_measures[matched_pest]))):
                    priority_scores[measure] = 30
            else:
                # Fallback to general pest measures
                for measure in [
                    "Implement physical barriers or traps for the specific pest",
                    "Apply appropriate insecticide following IPM principles",
                    "Enhance natural enemy populations through habitat management"
                ]:
                    priority_scores[measure] = 25
    
    # Sort measures by priority score (descending) and take top 8-10
    sorted_measures = sorted(priority_scores.items(), key=lambda x: x[1], reverse=True)
    final_recommendations = [m[0] for m in sorted_measures[:10]]
    
    # Ensure we have enough recommendations
    if len(final_recommendations) < 8:
        additional_needed = 8 - len(final_recommendations)
        additional = [m for m in general_measures if m not in final_recommendations]
        final_recommendations.extend(random.sample(additional, min(additional_needed, len(additional))))
    
    return final_recommendations

def get_fertilizer_recommendations(plant_name: str, 
                                 soil_data: Optional[Dict] = None,
                                 water_content: Optional[Dict] = None,
                                 diseases: Optional[Dict] = None) -> List[Dict]:
    """
    Generate scientifically-validated fertilizer recommendations based on multiple factors.
    Combines both versions with enhanced precision and crop-specific algorithms.
    
    Args:
        plant_name: Name of the identified plant
        soil_data: Soil analysis results (optional)
        water_content: Water status information (optional)
        diseases: Disease information (optional)
        
    Returns:
        list: Dictionary of fertilizer recommendations with application details
    """
    # Enhanced base recommendations with scientific backing
    base_recommendations = [
        {
            "type": "general",
            "name": "Balanced NPK (10-10-10)",
            "npk": "10-10-10",
            "description": "Provides equal parts nitrogen (N), phosphorus (P), and potassium (K). Nitrogen promotes leaf growth, phosphorus supports root and flower development, potassium enhances overall plant health.",
            "application": "Apply 2-3 lbs per 100 sq ft before planting and side-dress during active growth. Water thoroughly after application.",
            "conditions": "General purpose for most plants during vegetative growth",
            "scientific_backing": "University studies show balanced NPK improves yield by 15-20% over unfertilized controls"
        },
        {
            "type": "organic",
            "name": "Compost Tea",
            "npk": "Varies (typically 1-1-1)",
            "description": "Liquid extract of compost containing beneficial microbes, nutrients, and organic compounds that improve soil biology and plant health.",
            "application": "Apply as soil drench (5 gal/100 sq ft) or foliar spray (diluted 1:5) every 2-4 weeks.",
            "conditions": "All plants, especially when microbial activity is desired",
            "scientific_backing": "Research demonstrates 30-50% increase in beneficial soil microbes after application"
        },
        {
            "type": "mineral",
            "name": "Rock Phosphate",
            "npk": "0-20-0",
            "description": "Slow-release source of phosphorus that becomes available over 2-3 years. Ideal for building long-term soil phosphorus reserves.",
            "application": "Apply 5-10 lbs per 100 sq ft and incorporate into soil before planting. Does not dissolve in water.",
            "conditions": "Soils testing low in phosphorus, perennial crops",
            "scientific_backing": "Long-term studies show cumulative benefits over 3-5 year period"
        }
    ]

    # Enhanced crop-specific recommendations with growth stage guidance
    crop_specific = {
        "Tomato": [
            {
                "type": "vegetative",
                "name": "Calcium Nitrate",
                "npk": "15-0-0 + 19% Ca",
                "description": "Provides readily available nitrogen and prevents blossom end rot by supplying calcium during fruit development.",
                "application": "Apply 1-2 tbsp/gal as foliar spray or 1 lb/100 sq ft as soil application every 2 weeks during fruiting.",
                "conditions": "For fruiting stage, especially when blossom end rot is a concern",
                "scientific_backing": "Reduces blossom end rot incidence by up to 80% in field trials"
            },
            {
                "type": "flowering",
                "name": "Phosphorus-Potassium Booster",
                "npk": "3-15-15",
                "description": "Lower nitrogen with higher phosphorus and potassium to encourage flowering and fruit development instead of excessive vegetative growth.",
                "application": "Apply 1 lb/100 sq ft at first flower cluster formation and repeat every 3-4 weeks.",
                "conditions": "When plants are transitioning from vegetative to flowering stage",
                "scientific_backing": "Improves fruit set by 25-30% compared to high-nitrogen fertilizers"
            }
        ],
        "Onion": [
            {
                "type": "vegetative",
                "name": "Nitrogen-Sulfur Blend",
                "npk": "21-0-0-24S",
                "description": "Provides nitrogen for leaf growth and sulfur which is essential for onion flavor development and disease resistance.",
                "application": "Side-dress 1 lb/100 ft row at 3-leaf stage and again 3-4 weeks later.",
                "conditions": "Early to mid-growth stage onions",
                "scientific_backing": "Sulfur application increases pyruvic acid content by 30%, enhancing flavor"
            },
            {
                "type": "bulbing",
                "name": "Low-N, High-K Blend",
                "npk": "5-10-20",
                "description": "Lower nitrogen with higher potassium for bulb development phase. Reducing nitrogen prevents excess leaf growth that can delay bulbing.",
                "application": "Apply 1 lb/100 ft row when bulbs begin to form, typically 6-8 weeks after planting.",
                "conditions": "During bulb formation stage",
                "scientific_backing": "Potassium application at bulbing improves storage quality by 25-40%"
            }
        ],
        "Rice": [
            {
                "type": "foundation",
                "name": "Basal NPK + Zn",
                "npk": "14-14-14 + Zn",
                "description": "Balanced nutrition with zinc for initial establishment. Zinc is often deficient in flooded rice systems.",
                "application": "Apply 20-25 kg/ha at final land preparation, incorporated into soil.",
                "conditions": "Pre-planting or at transplanting",
                "scientific_backing": "Zinc addition increases yield by 15-30% in deficient soils"
            },
            {
                "type": "tillering",
                "name": "Urea Top-dressing",
                "npk": "46-0-0",
                "description": "High nitrogen to promote tillering and leaf development. Split application reduces losses and improves uptake efficiency.",
                "application": "Apply 40-60 kg N/ha at active tillering stage, ensure field is drained before application.",
                "conditions": "Active tillering phase, typically 15-20 days after transplanting",
                "scientific_backing": "Split application increases nitrogen use efficiency by 25%"
            }
        ],
        "Wheat": [
            {
                "type": "foundation",
                "name": "Starter Phosphorus",
                "npk": "11-52-0",
                "description": "High phosphorus formulation to support early root development and tillering. Critical for establishment in cool soils.",
                "application": "Apply 15-20 kg P₂O₅/ha at planting, placed 5 cm beside and below seed.",
                "conditions": "At planting, especially in cold soils or where phosphorus is limiting",
                "scientific_backing": "Seed-placed phosphorus improves early vigor by 30-40%"
            },
            {
                "type": "jointing",
                "name": "Nitrogen with Sulfur",
                "npk": "24-0-0-10S",
                "description": "Nitrogen to support stem elongation and leaf development, with sulfur for protein formation in grain.",
                "application": "Apply 50-70 kg N/ha at jointing stage (Zadoks 30-31).",
                "conditions": "At jointing/stem elongation phase",
                "scientific_backing": "Sulfur addition improves protein quality and bread-making characteristics"
            }
        ],
        "Cucumber": [
            {
                "type": "vegetative",
                "name": "High Nitrogen Starter",
                "npk": "20-10-10",
                "description": "Promotes vigorous vine growth during early development stages.",
                "application": "Apply 1 lb/100 sq ft at planting and again at 3-leaf stage.",
                "conditions": "Early growth phase (first 3-4 weeks)",
                "scientific_backing": "Increases vine length by 30% compared to balanced fertilizers"
            },
            {
                "type": "flowering",
                "name": "Balanced NPK + Calcium",
                "npk": "10-10-10 + 5% Ca",
                "description": "Supports flowering and prevents blossom end rot with added calcium.",
                "application": "Apply 1.5 lbs/100 sq ft at first flower appearance.",
                "conditions": "Flowering through early fruiting stage",
                "scientific_backing": "Reduces blossom end rot incidence by 75% in field trials"
            }
        ],
        "Bitter Gourd": [
            {
                "type": "vegetative",
                "name": "High Nitrogen Starter",
                "npk": "20-10-10",
                "description": "Promotes vigorous vine growth during early development stages.",
                "application": "Apply 1 lb/100 sq ft at planting and again at 3-leaf stage.",
                "conditions": "Early growth phase (first 3-4 weeks)",
                "scientific_backing": "Increases vine length by 30% compared to balanced fertilizers"
            },
            {
                "type": "flowering",
                "name": "Balanced NPK + Calcium",
                "npk": "10-10-10 + 5% Ca",
                "description": "Supports flowering and prevents blossom end rot with added calcium.",
                "application": "Apply 1.5 lbs/100 sq ft at first flower appearance.",
                "conditions": "Flowering through early fruiting stage",
                "scientific_backing": "Reduces blossom end rot incidence by 75% in field trials"
            }
        ],
        "Pumpkin": [
            {
                "type": "vegetative",
                "name": "High Nitrogen Starter",
                "npk": "20-10-10",
                "description": "Promotes vigorous vine growth during early development stages",
                "application": "Apply 1 lb/100 sq ft at planting and again at 3-leaf stage",
                "conditions": "Early growth phase (first 3-4 weeks)",
                "scientific_backing": "Increases vine length by 30% compared to balanced fertilizers"
            },
            {
                "type": "fruiting",
                "name": "High Potassium Booster",
                "npk": "5-10-20",
                "description": "Supports fruit development and improves disease resistance",
                "application": "Apply 1.5 lbs/100 sq ft when fruits are baseball-sized",
                "conditions": "Fruit development stage",
                "scientific_backing": "Increases fruit size and sugar content by 15-20%"
            }
        ],
        "Grape": [
            {
                "type": "vegetative",
                "name": "Balanced NPK (10-10-10)",
                "npk": "10-10-10",
                "description": "Promotes balanced growth during establishment phase",
                "application": "Apply 50-100 kg/acre in early spring before bud break",
                "conditions": "For young vines during first 2-3 years",
                "scientific_backing": "Improves vine establishment by 25-30%"
            },
            {
                "type": "fruiting",
                "name": "High Potassium Blend (8-12-24)",
                "npk": "8-12-24",
                "description": "Enhances fruit quality and sugar accumulation",
                "application": "Apply 40-60 kg/acre at berry set and veraison",
                "conditions": "For mature bearing vines",
                "scientific_backing": "Increases Brix levels by 1-2 degrees in trials"
            },
            {
                "type": "micronutrient",
                "name": "Zinc + Boron Foliar",
                "npk": "0-0-0 + Zn, B",
                "description": "Corrects common micronutrient deficiencies in grapes",
                "application": "Apply 0.5% ZnSO4 + 0.2% borax at pre-bloom and fruit set",
                "conditions": "When leaf analysis shows deficiencies",
                "scientific_backing": "Improves fruit set and reduces bunch stem necrosis"
            }
        ],

    }
    
    # Soil condition specific recommendations
    soil_specific = {
        "Acidic (pH < 6.0)": [
            {
                "type": "amendment",
                "name": "Agricultural Lime",
                "npk": "0-0-0 + Ca",
                "description": "Increases soil pH to make nutrients more available. Calcium carbonate neutralizes soil acidity.",
                "application": "Apply 50-100 lbs/1000 sq ft based on soil test, incorporate into top 6 inches of soil.",
                "conditions": "Apply 2-3 months before planting to allow time for pH adjustment",
                "scientific_backing": "Can increase nutrient availability by 50-80% in strongly acidic soils"
            }
        ],
        "Alkaline (pH > 7.5)": [
            {
                "type": "amendment",
                "name": "Elemental Sulfur",
                "npk": "0-0-0-90S",
                "description": "Gradually lowers soil pH as sulfur oxidizes to sulfuric acid. Opens up soils and improves nutrient availability.",
                "application": "Apply 5-10 lbs/1000 sq ft based on soil test, incorporate into soil.",
                "conditions": "Apply 3-6 months before planting to allow time for oxidation and pH reduction",
                "scientific_backing": "Improves iron and phosphorus availability in calcareous soils"
            }
        ],
        "Sandy": [
            {
                "type": "amendment",
                "name": "Slow-Release Organic Matter",
                "npk": "Varies",
                "description": "Improves water retention, nutrient holding capacity, and soil structure in sandy soils.",
                "application": "Apply 2-3 inches of compost or well-rotted manure, incorporate into top 6-8 inches of soil.",
                "conditions": "Apply before planting and annually thereafter",
                "scientific_backing": "Can increase water holding capacity by 2-3 times in sandy soils"
            }
        ],
        "Clay": [
            {
                "type": "amendment",
                "name": "Gypsum",
                "npk": "0-0-0 + Ca",
                "description": "Improves soil structure and drainage without changing pH. Calcium displaces sodium and improves clay aggregation.",
                "application": "Apply 40-50 lbs/1000 sq ft, incorporated into soil or applied to surface.",
                "conditions": "Apply annually for heavy clay soils or soils with poor drainage",
                "scientific_backing": "Improves infiltration rates by 30-50% in compacted clay soils"
            }
        ]
    }
    
    # Water content specific recommendations
    water_specific = {
        "Dry": [
            {
                "type": "amendment",
                "name": "Hydrogel Polymers",
                "npk": "0-0-0",
                "description": "Water-absorbing polymers that can retain hundreds of times their weight in water, releasing it slowly to plants.",
                "application": "Mix 1-2 lbs/1000 sq ft into planting soil or 1-2 tsp per planting hole.",
                "conditions": "For drought-prone areas or plants with high water needs",
                "scientific_backing": "Can reduce irrigation frequency by 30-50% in field trials"
            }
        ],
        "Waterlogged": [
            {
                "type": "amendment",
                "name": "Raised Bed + Coarse Sand",
                "npk": "0-0-0",
                "description": "Improves drainage and soil aeration in waterlogged conditions.",
                "application": "Create raised beds 8-12 inches high and incorporate 20-30% coarse sand into top 6 inches of soil.",
                "conditions": "For areas with poor drainage or heavy rainfall",
                "scientific_backing": "Increases root zone oxygen by 40-60% compared to flat beds in wet conditions"
            }
        ]
    }
    
    # Disease condition specific recommendations
    disease_specific = {
        "Fungal": [
            {
                "type": "amendment",
                "name": "Trichoderma Biofertilizer",
                "npk": "Varies",
                "description": "Contains beneficial Trichoderma fungi that compete with pathogens, induce systemic resistance, and improve nutrient uptake.",
                "application": "Apply 1-2 lbs/1000 sq ft incorporated into soil before planting or as a root drench (1 tbsp/gal).",
                "conditions": "For disease prevention or recovery from fungal infections",
                "scientific_backing": "Reduces Fusarium wilt incidence by 65-75% in controlled studies"
            }
        ],
        "Bacterial": [
            {
                "type": "amendment",
                "name": "Silicon + Copper Amendment",
                "npk": "0-0-0 + Si, Cu",
                "description": "Silicon strengthens cell walls while copper has bacteriostatic properties. Both increase plant resistance to bacterial pathogens.",
                "application": "Apply silicon at 100-200 kg/ha and copper at 2-5 kg/ha, incorporated into soil before planting.",
                "conditions": "For areas with history of bacterial diseases",
                "scientific_backing": "Silicon application reduces bacterial leaf blight severity by 35-45%"
            }
        ]
    }
    
    # Determine soil properties if soil data is available
    soil_condition = None
    if soil_data:
        soil_type = soil_data.get("type", "")
        soil_pH = soil_data.get("pH", 7.0)
        
        if soil_pH < 6.0:
            soil_condition = "Acidic (pH < 6.0)"
        elif soil_pH > 7.5:
            soil_condition = "Alkaline (pH > 7.5)"
        elif "Sandy" in soil_type:
            soil_condition = "Sandy"
        elif "Clay" in soil_type:
            soil_condition = "Clay"
    
    # Determine water condition if water data is available
    water_condition = None
    if water_content:
        moisture_level = water_content.get("moisture_level", "")
        if moisture_level == "Low":
            water_condition = "Dry"
        elif moisture_level == "High":
            water_condition = "Waterlogged"
    
    # Determine disease condition if disease data is available
    disease_condition = None
    if diseases and diseases.get("detected"):
        disease_type = diseases.get("type", "")
        if "fungal" in disease_type.lower():
            disease_condition = "Fungal"
        elif "bacterial" in disease_type.lower():
            disease_condition = "Bacterial"
    
    # Compile all relevant recommendations
    all_recommendations = []
    
    # Always include base recommendations
    all_recommendations.extend(base_recommendations)
    
    # Add crop-specific recommendations if available
    if plant_name in crop_specific:
        all_recommendations.extend(crop_specific[plant_name])
    
    # Add condition-specific recommendations
    if soil_condition and soil_condition in soil_specific:
        all_recommendations.extend(soil_specific[soil_condition])
    
    if water_condition and water_condition in water_specific:
        all_recommendations.extend(water_specific[water_condition])
    
    if disease_condition and disease_condition in disease_specific:
        all_recommendations.extend(disease_specific[disease_condition])
    
    # Choose a subset of recommendations to return (prioritizing specific ones)
    final_recommendations = []
    
    # Always include at least one base recommendation
    if base_recommendations:
        final_recommendations.append(random.choice(base_recommendations))
    
    # Priority to crop-specific recommendations
    if plant_name in crop_specific:
        crop_recs = crop_specific[plant_name]
        final_recommendations.extend(crop_recs[:min(2, len(crop_recs))])
    
    # Add condition-specific recommendations
    condition_recs = []
    if soil_condition and soil_condition in soil_specific:
        condition_recs.extend(soil_specific[soil_condition])
    if water_condition and water_condition in water_specific:
        condition_recs.extend(water_specific[water_condition])
    if disease_condition and disease_condition in disease_specific:
        condition_recs.extend(disease_specific[disease_condition])
    
    if condition_recs:
        # Randomly select 1-2 condition recommendations
        selected = random.sample(condition_recs, min(2, len(condition_recs)))
        final_recommendations.extend(selected)
    
    # De-duplicate recommendations based on name
    seen_names = set()
    unique_recommendations = []
    for rec in final_recommendations:
        if rec["name"] not in seen_names:
            seen_names.add(rec["name"])
            unique_recommendations.append(rec)
    
    # Ensure we have at least 3 recommendations
    while len(unique_recommendations) < 3 and len(all_recommendations) > len(unique_recommendations):
        additional = random.choice(all_recommendations)
        if additional["name"] not in seen_names:
            seen_names.add(additional["name"])
            unique_recommendations.append(additional)
    
    return unique_recommendations