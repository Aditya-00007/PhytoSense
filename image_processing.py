"""
Image processing module for PhytoSense application.
Provides functions for preprocessing images and extracting features for analysis.
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2

def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess an image for analysis by resizing, enhancing, and normalizing.
    
    Args:
        image: PIL Image object
        target_size: Tuple of (width, height) for resizing
        
    Returns:
        PIL Image: Preprocessed image ready for analysis
    """
    # If the image is not a PIL Image, convert it
    if not isinstance(image, Image.Image):
        if isinstance(image, np.ndarray):
            image = Image.fromarray(np.uint8(image))
        else:
            raise TypeError("Input must be a PIL Image or numpy array")
    
    # Make a copy to avoid modifying the original
    processed_img = image.copy()
    
    # Resize image while maintaining aspect ratio
    processed_img.thumbnail(target_size, Image.LANCZOS)
    
    # Create a new image with the target size and paste the resized image centered
    new_img = Image.new("RGB", target_size, (0, 0, 0))
    paste_x = (target_size[0] - processed_img.width) // 2
    paste_y = (target_size[1] - processed_img.height) // 2
    new_img.paste(processed_img, (paste_x, paste_y))
    processed_img = new_img
    
    # Enhance image for better feature detection
    # Adjust contrast
    enhancer = ImageEnhance.Contrast(processed_img)
    processed_img = enhancer.enhance(1.2)
    
    # Adjust brightness
    enhancer = ImageEnhance.Brightness(processed_img)
    processed_img = enhancer.enhance(1.1)
    
    # Adjust sharpness
    enhancer = ImageEnhance.Sharpness(processed_img)
    processed_img = enhancer.enhance(1.3)
    
    # Apply a very mild Gaussian blur to reduce noise
    processed_img = processed_img.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    return processed_img

def extract_features(image):
    """
    Extract visual features from an image for analysis.
    
    Args:
        image: PIL Image or numpy array
        
    Returns:
        dict: Dictionary containing extracted features
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image
    
    # Convert to BGR if the image is RGB
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        # OpenCV uses BGR format
        if img_array.dtype != np.uint8:
            img_array = (img_array * 255).astype(np.uint8)
    
    # Convert to grayscale for certain feature extractions
    if len(img_array.shape) == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Calculate color statistics
    color_features = {}
    if len(img_array.shape) == 3:
        # Calculate mean and std for each channel
        for i, channel_name in enumerate(['red', 'green', 'blue']):
            channel = img_array[:, :, i]
            color_features[f"{channel_name}_mean"] = float(np.mean(channel))
            color_features[f"{channel_name}_std"] = float(np.std(channel))
        
        # Calculate ratios between channels
        color_features["green_to_red_ratio"] = float(
            color_features["green_mean"] / (color_features["red_mean"] + 1e-10)
        )
        color_features["green_to_blue_ratio"] = float(
            color_features["green_mean"] / (color_features["blue_mean"] + 1e-10)
        )
    
    # Texture features using Haralick texture
    try:
        # Calculate GLCM (Gray-Level Co-occurrence Matrix)
        if gray.dtype != np.uint8:
            gray = (gray * 255).astype(np.uint8)
        
        glcm = cv2.GaussianBlur(gray, (5, 5), 0)
        glcm = cv2.normalize(glcm, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # Calculate texture statistics
        texture_features = {
            "contrast": float(cv2.Laplacian(gray, cv2.CV_64F).var()),
            "uniformity": float(np.sum(np.square(cv2.calcHist([gray], [0], None, [256], [0, 256])) / (gray.size**2))),
            "homogeneity": float(1.0 / (1.0 + cv2.Laplacian(gray, cv2.CV_64F).var() + 1e-10))
        }
    except Exception as e:
        # Fallback if texture calculation fails
        texture_features = {
            "contrast": 0.0,
            "uniformity": 0.0,
            "homogeneity": 0.0
        }
    
    # Edge detection to measure leaf structure
    try:
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / edges.size
        
        edge_features = {
            "edge_density": float(edge_density)
        }
    except Exception as e:
        edge_features = {
            "edge_density": 0.0
        }
    
    # Combine all features
    features = {
        **color_features,
        **texture_features,
        **edge_features
    }
    
    return features

def segment_plant(image):
    """
    Segment the plant from the background
    
    Args:
        image: PIL Image or numpy array
        
    Returns:
        tuple: (segmented_image, mask)
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image
    
    # Convert to BGR if the image is RGB
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        # Make sure image is uint8
        if img_array.dtype != np.uint8:
            img_array = (img_array * 255).astype(np.uint8)
        
        # Convert to HSV color space
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
        
        # Define range for green color in HSV
        lower_green = np.array([25, 40, 40])
        upper_green = np.array([95, 255, 255])
        
        # Create mask for green areas
        mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Create segmented image by masking the original
        segmented = cv2.bitwise_and(img_array, img_array, mask=mask)
        
        return segmented, mask
    else:
        # If the image is grayscale, use thresholding
        if img_array.dtype != np.uint8:
            img_array = (img_array * 255).astype(np.uint8)
        
        # Apply Otsu's thresholding
        _, mask = cv2.threshold(img_array, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        # Create segmented image
        segmented = cv2.bitwise_and(img_array, img_array, mask=mask)
        
        return segmented, mask

def detect_color_anomalies(image, mask=None):
    """
    Detect color anomalies in the plant that might indicate diseases
    
    Args:
        image: PIL Image or numpy array
        mask: Optional binary mask of the plant regions
        
    Returns:
        dict: Information about detected color anomalies
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image
    
    # Ensure image is RGB
    if len(img_array.shape) != 3 or img_array.shape[2] != 3:
        return {"anomalies_detected": False, "message": "Image must be RGB for color anomaly detection"}
    
    # If no mask is provided, try to segment the plant
    if mask is None:
        _, mask = segment_plant(img_array)
    
    # Create mask as boolean array
    if mask.dtype != bool:
        mask_bool = mask > 0
    else:
        mask_bool = mask
    
    # If not enough plant pixels are detected, return early
    if np.sum(mask_bool) < 100:
        return {"anomalies_detected": False, "message": "Not enough plant pixels detected"}
    
    # Extract the plant pixels using the mask
    plant_pixels = img_array[mask_bool]
    
    # Calculate the mean color of the plant
    mean_color = np.mean(plant_pixels, axis=0)
    
    # Calculate the standard deviation of each color channel
    std_color = np.std(plant_pixels, axis=0)
    
    # Define anomaly thresholds
    green_deficiency = mean_color[1] < 1.1 * mean_color[0] and mean_color[1] < 1.1 * mean_color[2]
    
    # Check for yellow discoloration (high red and green, low blue)
    yellow_discoloration = (mean_color[0] > 150 and mean_color[1] > 150 and mean_color[2] < 100)
    
    # Check for brown spots (low green, moderate red and blue)
    r_g_ratio = mean_color[0] / (mean_color[1] + 1e-10)
    brown_spots = r_g_ratio > 1.2 and mean_color[2] < mean_color[0]
    
    # Determine if anomalies are present
    anomalies_detected = green_deficiency or yellow_discoloration or brown_spots
    
    # Construct result
    anomaly_info = {
        "anomalies_detected": anomalies_detected,
        "mean_color": mean_color.tolist(),
        "std_color": std_color.tolist(),
        "green_deficiency": bool(green_deficiency),
        "yellow_discoloration": bool(yellow_discoloration),
        "brown_spots": bool(brown_spots),
        "r_g_ratio": float(r_g_ratio)
    }
    
    return anomaly_info

def analyze_leaf_shape(image, mask=None):
    """
    Analyze leaf shape to detect abnormalities
    
    Args:
        image: PIL Image or numpy array
        mask: Optional binary mask of the plant regions
        
    Returns:
        dict: Information about leaf shape analysis
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        img_array = image
    
    # If no mask is provided, try to segment the plant
    if mask is None:
        _, mask = segment_plant(img_array)
    
    # Ensure mask is uint8
    if mask.dtype != np.uint8:
        if mask.dtype == bool:
            mask = mask.astype(np.uint8) * 255
        else:
            mask = (mask > 0).astype(np.uint8) * 255
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # If no contours are found, return early
    if not contours:
        return {"error": "No plant contours detected"}
    
    # Get the largest contour (assumed to be the main plant)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Calculate area and perimeter
    area = cv2.contourArea(largest_contour)
    perimeter = cv2.arcLength(largest_contour, True)
    
    # Calculate shape features
    # Circularity = 4π(area/perimeter²), 1 indicates a perfect circle
    circularity = 4 * np.pi * area / (perimeter * perimeter + 1e-10)
    
    # Convex hull analysis
    hull = cv2.convexHull(largest_contour)
    hull_area = cv2.contourArea(hull)
    
    # Solidity = area/convex_hull_area, measures the density of the shape
    solidity = area / (hull_area + 1e-10)
    
    # Extent = area/bounding_rect_area, measures how the shape fills its bounding box
    x, y, w, h = cv2.boundingRect(largest_contour)
    extent = area / (w * h + 1e-10)
    
    # Determine if the leaf shape is abnormal
    shape_abnormality = False
    abnormality_reasons = []
    
    # Low circularity might indicate irregular shape
    if circularity < 0.3:
        shape_abnormality = True
        abnormality_reasons.append("Low circularity indicates irregular shape")
    
    # Low solidity might indicate holes or bite marks
    if solidity < 0.7:
        shape_abnormality = True
        abnormality_reasons.append("Low solidity indicates holes or bite marks")
    
    # Low extent might indicate irregular or elongated shape
    if extent < 0.5:
        shape_abnormality = True
        abnormality_reasons.append("Low extent indicates irregular or elongated shape")
    
    return {
        "shape_abnormality": shape_abnormality,
        "abnormality_reasons": abnormality_reasons,
        "area": float(area),
        "perimeter": float(perimeter),
        "circularity": float(circularity),
        "solidity": float(solidity),
        "extent": float(extent)
    }
