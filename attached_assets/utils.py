import os
import base64
import numpy as np
import matplotlib.pyplot as plt
import io
import datetime
import json
from PIL import Image
import uuid

def load_svg(path):
    """
    Load an SVG file and return it as a data URI
    
    Args:
        path (str): Path to SVG file
        
    Returns:
        str: SVG content as data URI
    """
    # Check if file exists
    if not os.path.exists(path):
        # Create a simple placeholder SVG if file doesn't exist
        svg_content = """<svg width="80" height="80" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
            <circle cx="40" cy="40" r="38" fill="#E8F5E9" stroke="#4CAF50" stroke-width="2" />
            <path d="M40,15 C55,15 65,25 65,40 C65,55 55,65 40,65 C25,65 15,55 15,40 L15,25 C30,25 40,15 40,15 Z" fill="#66BB6A" />
            <circle cx="40" cy="40" r="8" fill="#FFFFFF" stroke="#2196F3" stroke-width="1" />
            <circle cx="40" cy="40" r="4" fill="#2196F3" />
        </svg>"""
        
        # Return the inline SVG
        return f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}"
    
    # Read SVG file
    with open(path, 'r') as f:
        svg_content = f.read()
    
    # Convert to data URI
    return f"data:image/svg+xml;base64,{base64.b64encode(svg_content.encode()).decode()}"

def get_example_images():
    """
    Get list of example plant images
    
    Returns:
        list: List of example image paths
    """
    # Check for example directory
    example_dir = "assets/examples"
    if not os.path.exists(example_dir):
        os.makedirs(example_dir)
    
    # Get list of example images
    example_images = []
    for file in os.listdir(example_dir):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            example_images.append(os.path.join(example_dir, file))
    
    return example_images

def create_visualization(image, analysis_result, analysis_type):
    """
    Create a visualization based on analysis result
    
    Args:
        image: Original image
        analysis_result: Result of analysis
        analysis_type: Type of analysis performed
        
    Returns:
        matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Display the original image
    ax.imshow(np.array(image))
    ax.axis('off')
    
    # Add visualizations based on analysis type
    if analysis_type == "plant":
        # Highlight diseased areas or add markers
        if "diseases" in analysis_result and analysis_result["diseases"]:
            disease = analysis_result["diseases"][0]
            disease_name = disease.get("name", "Unknown")
            probability = disease.get("probability", 0)
            
            # Add a text annotation
            ax.text(10, 30, f"{disease_name}: {probability:.1f}%", 
                   color='white', fontsize=12, backgroundcolor='#4CAF50',
                   bbox=dict(facecolor='#4CAF50', alpha=0.8, pad=5))
    
    elif analysis_type == "soil":
        # Add soil type and properties
        if "type" in analysis_result:
            soil_type = analysis_result["type"]
            
            # Add a text annotation
            ax.text(10, 30, f"Soil Type: {soil_type}", 
                   color='white', fontsize=12, backgroundcolor='#795548',
                   bbox=dict(facecolor='#795548', alpha=0.8, pad=5))
    
    # Convert figure to image
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)
    buf.seek(0)
    
    return buf

def generate_report_markdown(analysis_results, user_data=None):
    """
    Generate a markdown report from analysis results
    
    Args:
        analysis_results (dict): Analysis results data
        user_data (dict): Optional user data to include
        
    Returns:
        str: Markdown formatted report
    """
    # Initialize markdown content
    md = "# Plant Health Analysis Report\n\n"
    
    # Add date and time
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    md += f"**Date:** {current_datetime}\n\n"
    
    # Add user information if available
    if user_data:
        md += "## User Information\n\n"
        md += f"**Name:** {user_data.get('full_name', 'Not provided')}\n\n"
        if user_data.get('farm_name'):
            md += f"**Farm:** {user_data.get('farm_name')}\n\n"
        if user_data.get('location'):
            md += f"**Location:** {user_data.get('location')}\n\n"
    
    # Add plant identification information
    if "plant_info" in analysis_results and analysis_results["plant_info"]:
        plant_info = analysis_results["plant_info"]
        md += "## Plant Identification\n\n"
        md += f"**Plant:** {plant_info.get('name', 'Unknown')}\n\n"
        md += f"**Scientific Name:** {plant_info.get('scientific_name', 'Not available')}\n\n"
        md += f"**Confidence:** {format_probability(plant_info.get('probability', 0))}\n\n"
        
        # Add plant details if available
        if "details" in plant_info:
            details = plant_info["details"]
            md += "### Plant Details\n\n"
            md += f"**Family:** {details.get('family', 'Unknown')}\n\n"
            md += f"**Growing Season:** {details.get('growing_season', 'Unknown')}\n\n"
            md += f"**Days to Maturity:** {details.get('days_to_maturity', 'Unknown')}\n\n"
            md += f"**Sunlight Needs:** {details.get('sunlight', 'Unknown')}\n\n"
            md += f"**Watering Needs:** {details.get('watering', 'Unknown')}\n\n"
    
    # Add disease analysis
    if "diseases" in analysis_results and analysis_results["diseases"]:
        md += "## Disease Analysis\n\n"
        
        # Primary disease
        primary_disease = analysis_results["diseases"][0]
        disease_name = primary_disease.get("name", "Unknown")
        probability = primary_disease.get("probability", 0)
        description = primary_disease.get("description", "")
        
        md += f"### Primary Condition: {disease_name}\n\n"
        md += f"**Confidence:** {format_probability(probability)}\n\n"
        md += f"{description}\n\n"
        
        # Add treatments if available
        if "treatments" in primary_disease and primary_disease["treatments"]:
            md += "#### Treatment Recommendations\n\n"
            for treatment in primary_disease["treatments"]:
                md += f"- {treatment}\n"
            md += "\n"
        
        # Add secondary diseases if any
        if len(analysis_results["diseases"]) > 1:
            md += "### Other Potential Conditions\n\n"
            for disease in analysis_results["diseases"][1:]:
                sec_name = disease.get("name", "Unknown")
                sec_probability = disease.get("probability", 0)
                md += f"**{sec_name}** ({format_probability(sec_probability)})\n\n"
                if "description" in disease:
                    md += f"{disease['description']}\n\n"
    
    # Add water content analysis
    if "water_content" in analysis_results and analysis_results["water_content"]:
        water_content = analysis_results["water_content"]
        md += "## Water Content Analysis\n\n"
        
        percentage = water_content.get("percentage", 0)
        status = water_content.get("status", "")
        recommendation = water_content.get("recommendation", "")
        
        md += f"**Status:** {status}\n\n"
        md += f"**Water Content:** {percentage}%\n\n"
        md += f"**Recommendation:** {recommendation}\n\n"
    
    # Add pest analysis
    if "pests" in analysis_results and analysis_results["pests"]:
        pests = analysis_results["pests"]
        md += "## Pest Analysis\n\n"
        
        pest_name = pests.get("name", "Unknown")
        infestation_level = pests.get("infestation_level", "None")
        
        md += f"**Pest Detected:** {pest_name}\n\n"
        md += f"**Infestation Level:** {infestation_level}\n\n"
        
        if "description" in pests:
            md += f"{pests['description']}\n\n"
        
        if "damage" in pests and pests["damage"] and infestation_level != "None":
            md += f"**Potential Damage:** {pests['damage']}\n\n"
        
        if "control_methods" in pests and pests["control_methods"]:
            md += "### Control Methods\n\n"
            for method in pests["control_methods"]:
                md += f"- {method}\n"
            md += "\n"
    
    # Add preventive measures
    if "preventive_measures" in analysis_results and analysis_results["preventive_measures"]:
        md += "## Preventive Measures\n\n"
        for measure in analysis_results["preventive_measures"]:
            md += f"- {measure}\n"
        md += "\n"
    
    # Add fertilizer recommendations
    if "fertilizer_recommendations" in analysis_results and analysis_results["fertilizer_recommendations"]:
        md += "## Fertilizer Recommendations\n\n"
        for fertilizer in analysis_results["fertilizer_recommendations"]:
            name = fertilizer.get("name", "Unknown")
            npk = fertilizer.get("npk", "N/A")
            
            md += f"### {name} (NPK: {npk})\n\n"
            
            if "description" in fertilizer:
                md += f"{fertilizer['description']}\n\n"
            
            if "application" in fertilizer:
                md += f"**Application:** {fertilizer['application']}\n\n"
    
    # Add footer
    md += "---\n\n"
    md += "Generated by PhytoSense - AI Plant Health Monitoring System"
    
    return md

def format_probability(probability):
    """Format probability as a percentage with one decimal place"""
    return f"{probability:.1f}%" if isinstance(probability, (int, float)) else "N/A"

def save_uploaded_image(uploaded_file, directory="uploads"):
    """Save an uploaded image to disk and return the path"""
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Generate a unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id = str(uuid.uuid4())[:8]
    
    # Extract the file extension from the original filename
    original_filename = uploaded_file.name if hasattr(uploaded_file, 'name') else "image.jpg"
    file_ext = os.path.splitext(original_filename)[1].lower()
    
    # Build the new filename
    filename = f"{timestamp}_{file_id}{file_ext}"
    file_path = os.path.join(directory, filename)
    
    # Open the uploaded file and save it
    try:
        # If it's a file-like object from Streamlit
        image = Image.open(uploaded_file)
        image.save(file_path)
    except Exception as e:
        print(f"Error saving image: {e}")
        return None
    
    return file_path