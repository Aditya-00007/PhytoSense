import numpy as np
import cv2
from PIL import Image
import io

def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess the uploaded image for use with machine learning models.
    
    Args:
        image: PIL Image object
        target_size: Target size for model input
        
    Returns:
        numpy array: Processed image ready for model input
    """
    # Resize the image
    image = image.resize(target_size)
    
    # Convert to numpy array
    img_array = np.array(image)
    
    # Check if the image is grayscale and convert to RGB if needed
    if len(img_array.shape) == 2:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    elif img_array.shape[2] == 4:  # Has alpha channel
        # Convert RGBA to RGB
        img_array = img_array[:, :, :3]
    
    # Normalize the image (scale pixels to range [0, 1])
    img_array = img_array.astype(np.float32) / 255.0
    
    return img_array

def extract_features(processed_image):
    """
    Extract features from the processed image for custom analysis.
    
    Args:
        processed_image: Numpy array of preprocessed image
        
    Returns:
        dict: Various features extracted from the image
    """
    # Convert to BGR for OpenCV functions if needed
    if len(processed_image.shape) == 3 and processed_image.shape[2] == 3:
        # Convert from normalized [0-1] to [0-255]
        img_for_cv = (processed_image * 255).astype(np.uint8)
        # Convert RGB to BGR
        bgr_img = cv2.cvtColor(img_for_cv, cv2.COLOR_RGB2BGR)
        # Convert BGR to HSV
        hsv_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2HSV)
        
        # Convert RGB to grayscale for texture analysis
        gray_img = cv2.cvtColor(img_for_cv, cv2.COLOR_RGB2GRAY)
    else:
        # If already grayscale, use as is
        img_for_cv = (processed_image * 255).astype(np.uint8)
        gray_img = img_for_cv
        hsv_img = None  # HSV not applicable for grayscale images
    
    # Extract color features
    color_features = {}
    if hsv_img is not None:
        # Average hue, saturation, value
        avg_hue = np.mean(hsv_img[:, :, 0])
        avg_saturation = np.mean(hsv_img[:, :, 1])
        avg_value = np.mean(hsv_img[:, :, 2])
        
        color_features = {
            "avg_hue": avg_hue,
            "avg_saturation": avg_saturation,
            "avg_value": avg_value,
        }
        
        # Calculate dominant colors
        # Reshape image to list of pixels
        pixels = hsv_img.reshape(-1, 3)
        # Convert to 8-bit representation for K-means
        pixels = np.float32(pixels)
        # Define criteria and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
        k = 3  # Number of dominant colors to extract
        _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        
        # Convert centers back to BGR
        centers = centers.astype(np.uint8)
        centers_bgr = cv2.cvtColor(centers.reshape(1, k, 3), cv2.COLOR_HSV2BGR)
        centers_rgb = cv2.cvtColor(centers_bgr, cv2.COLOR_BGR2RGB)
        
        # Count labels to find percentage of each dominant color
        unique_labels, counts = np.unique(labels, return_counts=True)
        color_percentages = counts / len(labels) * 100
        
        dominant_colors = []
        for i in range(k):
            dominant_colors.append({
                "rgb": centers_rgb[0, i].tolist(),
                "percentage": color_percentages[i]
            })
        
        # Sort by percentage
        dominant_colors.sort(key=lambda x: x["percentage"], reverse=True)
        color_features["dominant_colors"] = dominant_colors
    
    # Extract texture features
    texture_features = calculate_glcm(gray_img)
    
    # Extract shape features
    shape_features = extract_shape_features(gray_img)
    
    # Combine all features
    features = {
        "color": color_features,
        "texture": texture_features,
        "shape": shape_features
    }
    
    return features

def calculate_glcm(gray_img):
    """
    Calculate Gray-Level Co-occurrence Matrix for texture analysis.
    Simplified version for demo purposes.
    
    Args:
        gray_img: Grayscale image
        
    Returns:
        dict: Texture features
    """
    # Simplified texture analysis for compatibility
    # Resize for faster processing
    gray_img = cv2.resize(gray_img, (128, 128))
    
    # Calculate basic texture metrics without GLCM
    # Standard deviation of pixel values (measure of contrast)
    contrast = np.std(gray_img)
    
    # Mean of pixel values
    mean = np.mean(gray_img)
    
    # Calculate a pseudo-entropy (measure of randomness)
    hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
    hist = hist / np.sum(hist)
    non_zero_hist = hist[hist > 0]
    entropy = -np.sum(non_zero_hist * np.log2(non_zero_hist))
    
    # Calculate local variations (approximation of homogeneity)
    dx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
    dy = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(dx**2 + dy**2)
    edge_intensity = np.mean(gradient_magnitude)
    
    return {
        "contrast": float(contrast),
        "mean_intensity": float(mean),
        "entropy": float(entropy),
        "edge_intensity": float(edge_intensity)
    }

def extract_shape_features(gray_img):
    """
    Extract shape features from the image.
    
    Args:
        gray_img: Grayscale image
        
    Returns:
        dict: Shape features
    """
    # Apply thresholding to separate objects from background
    _, thresh = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY)
    
    # Find contours (handle OpenCV version differences)
    try:
        # OpenCV 4.x
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    except ValueError:
        # OpenCV 3.x
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return {
            "num_contours": 0,
            "avg_contour_area": 0,
            "avg_contour_perimeter": 0,
            "shape_complexity": 0
        }
    
    # Calculate shape metrics
    areas = [cv2.contourArea(contour) for contour in contours]
    perimeters = [cv2.arcLength(contour, True) for contour in contours]
    
    # Shape complexity (circularity) - 4*pi*area/perimeter^2
    # A perfect circle has a value of 1, more complex shapes have lower values
    complexities = []
    for area, perimeter in zip(areas, perimeters):
        if perimeter > 0:
            complexity = 4 * np.pi * area / (perimeter * perimeter)
            complexities.append(complexity)
    
    return {
        "num_contours": int(len(contours)),
        "avg_contour_area": float(np.mean(areas) if areas else 0),
        "avg_contour_perimeter": float(np.mean(perimeters) if perimeters else 0),
        "shape_complexity": float(np.mean(complexities) if complexities else 0)
    }