import os
import sys
import numpy as np
from PIL import Image

# Reconfigure stdout for utf-8 on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Import our modified modules
from soil_analyzer import extract_soil_texture_features, analyze_soil, get_soil_details, SOIL_TEXTURES
from crop_suggestion_helper import generate_crop_recommendations, get_simulated_weather_data, get_market_prices

def run_tests():
    print("=" * 70)
    print("STARTING AUTOMATED VERIFICATION SUITE")
    print("=" * 70)
    
    passed_tests = 0
    total_tests = 0

    # ---------------------------------------------------------
    # TEST 1: Texture Feature Extraction
    # ---------------------------------------------------------
    total_tests += 1
    print("\n[TEST 1] Testing Texture Feature Extraction...")
    
    # 1a. Coarse/Sandy synthetic image (high noise, pale brightness)
    np.random.seed(42)
    sandy_img = np.random.uniform(0.5, 0.9, (100, 100, 3)).astype(np.float32)
    sandy_res = extract_soil_texture_features(sandy_img)
    print(f"  -> Synthetic Sandy Image Texture: {sandy_res['detected_texture']}")
    print(f"  -> Roughness: {sandy_res['metrics']['roughness']}, Composition: {sandy_res['composition']}")
    assert sandy_res["detected_texture"] in SOIL_TEXTURES, "Detected texture must be in SOIL_TEXTURES"
    assert "sand" in sandy_res["composition"], "Composition must include sand"
    
    # 1b. Smooth/Clayey synthetic image (low noise, darker tone)
    clay_img = np.full((100, 100, 3), 0.25, dtype=np.float32)
    # Add very low variation
    clay_img += np.random.normal(0, 0.01, (100, 100, 3)).astype(np.float32)
    clay_img = np.clip(clay_img, 0.0, 1.0)
    clay_res = extract_soil_texture_features(clay_img)
    print(f"  -> Synthetic Clay Image Texture: {clay_res['detected_texture']}")
    assert clay_res["detected_texture"] in ["Clayey", "Clay Loam", "Loamy"], "Smooth dark image should classify as cohesive clay/loam"
    
    print("  ✓ PASS: Texture Feature Extraction verified.")
    passed_tests += 1

    # ---------------------------------------------------------
    # TEST 2: Soil Analyzer End-to-End & Backward Compatibility
    # ---------------------------------------------------------
    total_tests += 1
    print("\n[TEST 2] Testing Soil Analyzer Integration & Schema...")
    
    test_soil_img = np.random.uniform(0.15, 0.35, (128, 128, 3)).astype(np.float32)
    farmer_ctx = {
        "sampling_location": "Nagpur, Maharashtra",
        "soil_depth": "Surface (0-10cm)",
        "recent_rainfall": "Moderate",
        "previous_crop": "Soybean",
        "user_observed_texture": "Clayey (Heavy, very sticky)"
    }
    
    analysis = analyze_soil(None, test_soil_img, farmer_inputs=farmer_ctx)
    print(f"  -> Identified Soil Type: {analysis.get('soil_type')}")
    print(f"  -> Identified Soil Texture: {analysis.get('soil_texture')}")
    print(f"  -> pH: {analysis.get('properties', {}).get('ph')}")
    print(f"  -> AI Status: Enhanced={analysis.get('ai_enhanced')}, Provider={analysis.get('ai_provider')}")
    
    # Schema assertions
    assert "soil_type" in analysis, "Result must contain 'soil_type' key"
    assert "soil_texture" in analysis, "Result must contain 'soil_texture' key"
    assert analysis["soil_texture"] in SOIL_TEXTURES or "Clayey" in analysis["soil_texture"], "Soil texture must match detected or user feel"
    assert "properties" in analysis, "Result must contain 'properties'"
    assert "characteristics" in analysis, "Result must contain 'characteristics'"
    assert "recommendations" in analysis, "Result must contain 'recommendations'"
    assert "ai_enhanced" in analysis, "Result must indicate AI enhancement status"
    assert analysis.get("soil_type") == "Black Soil", "Nagpur location context must resolve to Black Soil"
    
    print("  ✓ PASS: Soil Analyzer schema and context logic verified.")
    passed_tests += 1

    # ---------------------------------------------------------
    # TEST 3: Weather Factor in Crop Scoring Engine
    # ---------------------------------------------------------
    total_tests += 1
    print("\n[TEST 3] Testing Weather Factor Impact in Crop Scores...")
    
    # Simulated weather forecast with high temperature and moderate rain
    mock_weather = {
        "current_temp": 32.0,
        "forecast_3month": [
            {"month": "2026-03", "avg_temp": 32.0, "total_rain": 25.0, "rain_days": 2},
            {"month": "2026-04", "avg_temp": 34.0, "total_rain": 30.0, "rain_days": 3},
            {"month": "2026-05", "avg_temp": 36.0, "total_rain": 15.0, "rain_days": 1}
        ],
        "extreme_events": ["Heatwave Alert"],
        "summary": "Expect hot temperatures and dry spells."
    }
    
    sandy_soil = {
        "soil_type": "Coastal Sandy Soil",
        "soil_texture": "Sandy",
        "properties": {
            "ph": "7.2",
            "organic_matter": "Low",
            "drainage": "Excessive",
            "nitrogen": "Low",
            "phosphorus": "Medium",
            "potassium": "Medium"
        }
    }
    
    farmer_sandy = {
        "budget": {"amount": 25000, "unit": "Per Acre"},
        "attention_level": "Medium",
        "risk_tolerance": "Medium",
        "time_duration": {"value": 3, "unit": "Months"},
        "previous_crop": "None",
        "interested_crops": ["Watermelon"],
        "irrigation_available": "Good",
        "labor_availability": "Adequate"
    }

    # Import streamlit mock session_state if running standalone
    import streamlit as st
    if not hasattr(st, "session_state") or st.session_state is None:
        class SessionStateMock(dict):
            pass
        st.session_state = SessionStateMock()
        
    scored_crops, w_data, m_data = generate_crop_recommendations(sandy_soil, farmer_sandy)
    
    top_crop_names = [c["name"] for c in scored_crops[:3]]
    print(f"  -> Top 3 Recommended Crops for Sandy Soil + Warm Weather: {top_crop_names}")
    
    # Assert Watermelon or Cluster Beans is in top recommended crops
    assert any(c in top_crop_names for c in ["Watermelon", "Cluster Beans"]), "Watermelon or Cluster Beans must rank top for Sandy Soil in hot weather"
    
    # Check top crop sub-scores
    top_pick = scored_crops[0]
    print(f"  -> Top Pick: {top_pick['name']} with Score: {top_pick['score']}%")
    print(f"  -> Sub-scores: {top_pick['sub_scores']}")
    assert "weather" in top_pick["sub_scores"], "Sub-scores must include 'weather'"
    assert "soil" in top_pick["sub_scores"], "Sub-scores must include 'soil'"
    assert 15 <= top_pick["score"] <= 100, "Score must be within 15-100"
    
    print("  ✓ PASS: Weather factor and Sandy soil prioritization verified.")
    passed_tests += 1

    # ---------------------------------------------------------
    # TEST 4: Crop Rotation Synergy Bonus & Irrigation Compensation
    # ---------------------------------------------------------
    total_tests += 1
    print("\n[TEST 4] Testing Crop Rotation Synergy & Irrigation Synergy...")
    
    black_soil = {
        "soil_type": "Black Soil",
        "soil_texture": "Clayey",
        "properties": {
            "ph": "7.8",
            "organic_matter": "Medium",
            "drainage": "Poor to Moderate",
            "nitrogen": "Low",
            "phosphorus": "Medium",
            "potassium": "High"
        }
    }
    
    # Scenario 4a: Previous crop Soybean (legume) -> Wheat should get rotation synergy bonus
    farmer_rotation = {
        "budget": {"amount": 35000, "unit": "Per Acre"},
        "attention_level": "Medium",
        "risk_tolerance": "Medium",
        "time_duration": {"value": 4, "unit": "Months"},
        "previous_crop": "Soybean",  # Legume!
        "interested_crops": ["Wheat"],
        "irrigation_available": "Good",
        "labor_availability": "Adequate"
    }
    
    st.session_state.clear()
    scored_rot, _, _ = generate_crop_recommendations(black_soil, farmer_rotation)
    wheat_match = next((c for c in scored_rot if c["name"] == "Wheat"), None)
    
    assert wheat_match is not None, "Wheat must be in scored crops"
    print(f"  -> Wheat Score following Soybean: {wheat_match['score']}%")
    print(f"  -> Rotation Sub-score: {wheat_match['sub_scores']['rotation']}%")
    
    # Verify rotation reason is present
    has_rot_reason = any("legume" in r.lower() or "rotation" in r.lower() for r in wheat_match["reasons"])
    assert has_rot_reason, "Wheat must have rotation synergy reason following legume"
    assert wheat_match["sub_scores"]["rotation"] == 100, "Legume rotation synergy should yield 100% rotation sub-score"

    # Scenario 4b: Rainfed + Low Rainfall vs Good Irrigation
    farmer_rainfed = {
        "budget": {"amount": 20000, "unit": "Per Acre"},
        "attention_level": "Medium",
        "risk_tolerance": "Low",
        "time_duration": {"value": 4, "unit": "Months"},
        "previous_crop": "Wheat",
        "interested_crops": [],
        "irrigation_available": "None - Rainfed only",
        "labor_availability": "Limited"
    }
    st.session_state.clear()
    scored_rainfed, _, _ = generate_crop_recommendations(black_soil, farmer_rainfed)
    
    rice_match = next((c for c in scored_rainfed if c["name"] == "Rice"), None)
    if rice_match:
        has_water_warn = any("drought" in w.lower() or "rainfed" in w.lower() or "waterlogging" in w.lower() for w in rice_match["warnings"])
        print(f"  -> Rice Water Alignment Warnings: {rice_match['warnings']}")
        assert has_water_warn, "Rice in rainfed condition with extreme rain/low rain must trigger water risk warning"
        
    print("  ✓ PASS: Crop rotation synergy and irrigation risk logic verified.")
    passed_tests += 1

    # ---------------------------------------------------------
    # TEST 5: Solanaceae Mono-cropping Warning Check
    # ---------------------------------------------------------
    total_tests += 1
    print("\n[TEST 5] Testing Disease Carryover Check for Monoculture...")
    
    farmer_monoculture = {
        "budget": {"amount": 30000, "unit": "Per Acre"},
        "attention_level": "High",
        "risk_tolerance": "High",
        "time_duration": {"value": 3, "unit": "Months"},
        "previous_crop": "Potato",  # Solanaceae!
        "interested_crops": ["Tomato"],
        "irrigation_available": "Good",
        "labor_availability": "Adequate"
    }
    st.session_state.clear()
    scored_mono, _, _ = generate_crop_recommendations(black_soil, farmer_monoculture)
    tomato_match = next((c for c in scored_mono if c["name"] == "Tomato"), None)
    
    assert tomato_match is not None, "Tomato must be scored"
    has_solanaceae_warn = any("solanaceous" in w.lower() or "carryover" in w.lower() or "disease" in w.lower() for w in tomato_match["warnings"])
    print(f"  -> Tomato after Potato Warnings: {tomato_match['warnings']}")
    assert has_solanaceae_warn, "Tomato after Potato must trigger Solanaceous disease carryover warning"
    assert tomato_match["sub_scores"]["rotation"] < 50, "Monoculture rotation score must be discounted"

    print("  ✓ PASS: Disease carryover and monoculture penalty verified.")
    passed_tests += 1

    print("\n" + "=" * 70)
    print(f"ALL TESTS PASSED: {passed_tests}/{total_tests} (100% Success)")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
