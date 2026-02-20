"""
Utility functions for PhytoSense application.
"""

import os
import base64
import io
import glob
import json
import uuid
from datetime import datetime
from PIL import Image

def load_svg(file_path):
    """
    Load SVG file contents as a string
    
    Args:
        file_path: Path to SVG file
        
    Returns:
        string: SVG content or fallback SVG if file not found
    """
    # Try to read the SVG file
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except (FileNotFoundError, IOError):
        # If file not found, generate a simple SVG as fallback
        fallback_svg = f"""
        <svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
            <circle cx="50" cy="50" r="40" stroke="#4CAF50" stroke-width="3" fill="#E8F5E9" />
            <text x="50" y="55" font-family="Arial" font-size="12" text-anchor="middle" fill="#2E7D32">PhytoSense</text>
        </svg>
        """
        
        # Save the fallback SVG
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(fallback_svg)
        
        return fallback_svg

def get_example_images():
    """
    Get a dictionary of example images from the assets/examples directory
    
    Returns:
        dict: Dictionary mapping file paths to descriptions
    """
    # Check if example images directory exists
    example_dir = "assets/examples"
    if not os.path.exists(example_dir):
        os.makedirs(example_dir, exist_ok=True)
        return {}
    
    # Get all image files in the directory
    example_files = glob.glob(os.path.join(example_dir, "*.jpg")) + \
                   glob.glob(os.path.join(example_dir, "*.jpeg")) + \
                   glob.glob(os.path.join(example_dir, "*.png"))
    
    # Try to load descriptions from JSON file
    descriptions_file = os.path.join(example_dir, "descriptions.json")
    descriptions = {}
    
    try:
        if os.path.exists(descriptions_file):
            with open(descriptions_file, 'r') as f:
                descriptions = json.load(f)
    except (json.JSONDecodeError, IOError):
        descriptions = {}
    
    # Create dictionary mapping file paths to descriptions
    examples = {}
    for file_path in example_files:
        base_name = os.path.basename(file_path)
        examples[file_path] = descriptions.get(base_name, f"Example: {base_name}")
    
    return examples

def generate_report_markdown(plant_info, water_content, diseases, pests, 
                           preventive_measures, fertilizer_recommendations,
                           local_recommendations, plant_details):
    """
    Generate a Markdown report for plant health analysis
    
    Args:
        plant_info: Plant identification information
        water_content: Water content analysis
        diseases: Disease detection results
        pests: Pest detection results
        preventive_measures: Recommended preventive measures
        fertilizer_recommendations: Recommended fertilizers
        local_recommendations: Maharashtra-specific recommendations
        plant_details: Additional plant details provided by user
        
    Returns:
        string: Markdown-formatted report
    """
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Start building the report
    report = f"""
# Plant Health Analysis Report

**Date:** {timestamp}

## Plant Information

**Identified Plant:** {plant_info.get('name', 'Unknown')}
"""
    
    if plant_info.get('scientific_name'):
        report += f"**Scientific Name:** {plant_info['scientific_name']}\n"
    
    report += f"**Identification Confidence:** {plant_info.get('probability', 0):.1f}%\n"
    
    # Add user-provided details if available
    if any(plant_details.values()):
        report += "\n## Plant Details (User Provided)\n\n"
        
        if plant_details.get('crop_type'):
            report += f"**Crop Type:** {plant_details['crop_type']}\n"
        
        if plant_details.get('plant_age'):
            report += f"**Plant Age:** {plant_details['plant_age']}\n"
        
        if plant_details.get('planting_date'):
            report += f"**Planting Date:** {plant_details['planting_date']}\n"
        
        if plant_details.get('irrigation_method'):
            report += f"**Irrigation Method:** {plant_details['irrigation_method']}\n"
        
        if plant_details.get('symptoms'):
            report += f"**Observed Symptoms:** {plant_details['symptoms']}\n"
        
        if plant_details.get('previous_treatments'):
            report += f"**Previous Treatments:** {plant_details['previous_treatments']}\n"
    
    # Add water content analysis
    report += f"""
## Water Content Analysis

**Status:** {water_content.get('status', 'Unknown')}
**Estimated Water Content:** {water_content.get('percentage', 0)}%
"""
    
    # Add disease analysis
    report += "\n## Disease Analysis\n\n"
    
    if diseases.get('detected', False):
        report += "**Diseases Detected: Yes**\n\n"
        
        for disease in diseases.get('diseases', []):
            report += f"### {disease.get('name', 'Unknown Disease')}\n\n"
            report += f"**Confidence:** {disease.get('confidence', 0):.1f}%\n"
            
            if disease.get('scientific_name'):
                report += f"**Scientific Name:** {disease['scientific_name']}\n"
            
            if disease.get('description'):
                report += f"**Description:** {disease['description']}\n"
            
            if disease.get('treatment'):
                report += f"**Treatment Options:** {disease['treatment']}\n"
            
            report += "\n"
    else:
        report += "**Diseases Detected: No**\n\n"
        report += "The plant appears healthy with no significant disease symptoms detected.\n"
    
    # Add pest analysis
    report += "\n## Pest Analysis\n\n"
    
    if pests.get('detected', False):
        report += "**Pests Detected: Yes**\n\n"
        
        for pest in pests.get('pests', []):
            report += f"### {pest.get('name', 'Unknown Pest')}\n\n"
            report += f"**Infestation Level:** {pest.get('infestation_level', 'Unknown')}\n"
            
            if pest.get('scientific_name'):
                report += f"**Scientific Name:** {pest['scientific_name']}\n"
            
            if pest.get('description'):
                report += f"**Description:** {pest['description']}\n"
            
            if pest.get('treatment'):
                report += f"**Treatment Options:** {pest['treatment']}\n"
            
            report += "\n"
    else:
        report += "**Pests Detected: No**\n\n"
        report += "No significant pest infestations detected on the plant.\n"
    
    # Add recommendations
    report += "\n## Recommendations\n\n"
    
    # Preventive measures
    if preventive_measures:
        report += "### Preventive Measures\n\n"
        for measure in preventive_measures:
            report += f"- {measure}\n"
        report += "\n"
    
    # Fertilizer recommendations
    if fertilizer_recommendations:
        report += "### Fertilizer Recommendations\n\n"
        for recommendation in fertilizer_recommendations:
            report += f"- {recommendation}\n"
        report += "\n"
    
    # Add Maharashtra-specific recommendations
    if local_recommendations:
        report += "### Maharashtra-Specific Recommendations\n\n"
        
        if 'seasonal' in local_recommendations:
            report += f"**Seasonal Advice:** {local_recommendations['seasonal']}\n\n"
        
        if 'irrigation' in local_recommendations:
            report += f"**Irrigation Management:** {local_recommendations['irrigation']}\n\n"
        
        if 'varieties' in local_recommendations:
            report += f"**Recommended Varieties for Maharashtra:** {', '.join(local_recommendations['varieties'])}\n\n"
        
        if 'practices' in local_recommendations:
            report += "**Recommended Practices:**\n\n"
            for practice in local_recommendations['practices']:
                report += f"- {practice}\n"
    
    # Add disclaimer
    report += """
## Disclaimer

This analysis is based on computer vision and machine learning models and should be used as a guide only. For serious plant health issues, please consult with a qualified agricultural expert or extension officer. The recommendations provided are general and may need to be adapted to your specific growing conditions.

*Report generated by PhytoSense - AI Plant Health Monitoring System*
"""
    
    return report

def format_probability(probability):
    """
    Format probability value for display
    
    Args:
        probability: Probability value (0-100)
        
    Returns:
        float: Formatted probability value
    """
    try:
        return round(float(probability), 1)
    except (ValueError, TypeError):
        return 0.0

def save_uploaded_image(image):
    """
    Save an uploaded image to the uploads directory
    
    Args:
        image: PIL Image object
        
    Returns:
        string: Path to the saved image
    """
    # Create uploads directory if it doesn't exist
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Generate a unique filename
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(uploads_dir, filename)
    
    # Save the image
    image.save(filepath, "JPEG")
    
    return filepath

def image_to_base64(image):
    """
    Convert PIL Image to base64 string
    
    Args:
        image: PIL Image object
        
    Returns:
        string: Base64-encoded image data
    """
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def base64_to_image(base64_str):
    """
    Convert base64 string to PIL Image
    
    Args:
        base64_str: Base64-encoded image data
        
    Returns:
        PIL.Image: Image object
    """
    # Remove data URL prefix if present
    if ',' in base64_str:
        base64_str = base64_str.split(',', 1)[1]
    
    # Decode base64 data
    img_data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(img_data))

def get_current_growing_season():
    """
    Determine the current growing season based on the date
    
    Returns:
        string: Current growing season in Maharashtra
    """
    month = datetime.now().month
    
    if 6 <= month <= 9:
        return "Kharif (Monsoon)"
    elif 10 <= month <= 2:
        return "Rabi (Winter)"
    else:
        return "Zaid (Summer)"

def get_crop_calendar(crop_name):
    """
    Get the crop calendar for a specific crop in Maharashtra
    
    Args:
        crop_name: Name of the crop
        
    Returns:
        dict: Crop calendar information
    """
    # Basic crop calendars for Maharashtra
    calendars = {
        "Rice": {
            "Kharif": {
                "sowing": "June-July",
                "harvesting": "October-November"
            },
            "Rabi": {
                "sowing": "December-January",
                "harvesting": "April-May"
            }
        },
        "Cotton": {
            "Kharif": {
                "sowing": "June-July",
                "harvesting": "November-February"
            }
        },
        "Sugarcane": {
            "Adsali": {
                "sowing": "July-August",
                "harvesting": "December-March (next year)"
            },
            "Pre-seasonal": {
                "sowing": "October-November",
                "harvesting": "October-November (next year)"
            },
            "Suru": {
                "sowing": "January-February",
                "harvesting": "October-November"
            }
        },
        "Wheat": {
            "Rabi": {
                "sowing": "November-December",
                "harvesting": "March-April"
            }
        },
        "Onion": {
            "Kharif": {
                "sowing": "May-June",
                "harvesting": "September-October"
            },
            "Late Kharif": {
                "sowing": "August-September",
                "harvesting": "January-February"
            },
            "Rabi": {
                "sowing": "November-December",
                "harvesting": "April-May"
            }
        },
        "Tomato": {
            "Kharif": {
                "sowing": "June-July",
                "harvesting": "September-October"
            },
            "Rabi": {
                "sowing": "October-November",
                "harvesting": "February-March"
            },
            "Summer": {
                "sowing": "January-February",
                "harvesting": "April-May"
            }
        }
    }
    
    return calendars.get(crop_name, {})
