"""
Simple JSON-based database for local development
This file provides a fallback when SQLAlchemy is not available
"""
import os
import json
import hashlib
from datetime import datetime

# File to store user data
USERS_FILE = 'users.json'
ANALYSES_FILE = 'analyses.json'
PROFILES_FILE = 'profiles.json'

def _load_json(filename, default=None):
    """Load data from a JSON file"""
    if default is None:
        default = {}
    
    if not os.path.exists(filename):
        return default
    
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return default

def _save_json(filename, data):
    """Save data to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def hash_password(password):
    """Create a hash of a password"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(username, password, email=None, farm_location=None):
    """Create a new user with farm location"""
    users = _load_json(USERS_FILE, {})
    
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        'password': hash_password(password),
        'email': email,
        'farm_location': farm_location,  # Add farm location
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'profile_complete': False
    }
    
    _save_json(USERS_FILE, users)
    return True, "User created successfully"

def verify_user(username, password):
    """Verify user credentials"""
    users = _load_json(USERS_FILE, {})
    
    if username not in users:
        return None
    
    user = users[username]
    if user['password'] == hash_password(password):
        return {
            'id': username,
            'username': username,
            'farm_location': user.get('farm_location'),  # Include farm location
            'profile_complete': user.get('profile_complete', False)
        }
    
    return None

def update_user_profile(user_id, profile_data):
    """Update user profile"""
    users = _load_json(USERS_FILE, {})
    profiles = _load_json(PROFILES_FILE, {})
    
    if user_id not in users:
        return False, "User not found"
    
    # Update farm_location if provided in profile_data
    if 'farm_location' in profile_data:
        users[user_id]['farm_location'] = profile_data['farm_location']
    
    # Update profile complete flag
    users[user_id]['profile_complete'] = True
    users[user_id]['updated_at'] = datetime.utcnow().isoformat()
    
    # Update profile data
    profiles[user_id] = profile_data
    profiles[user_id]['updated_at'] = datetime.utcnow().isoformat()
    
    _save_json(USERS_FILE, users)
    _save_json(PROFILES_FILE, profiles)
    
    return True, "Profile updated successfully"

def save_analysis(user_id, analysis_type, image_path, results):
    """Save analysis results"""
    analyses = _load_json(ANALYSES_FILE, [])
    
    analysis = {
        'id': len(analyses) + 1,
        'user_id': user_id,
        'timestamp': datetime.utcnow().isoformat(),
        'analysis_type': analysis_type,
        'image_path': image_path,
        'results': results
    }
    
    analyses.append(analysis)
    _save_json(ANALYSES_FILE, analyses)
    
    return True, "Analysis saved successfully"

def get_user_analyses(user_id, limit=10):
    """Get user's analysis history"""
    analyses = _load_json(ANALYSES_FILE, [])
    
    # Filter by user_id and sort by timestamp (newest first)
    user_analyses = [a for a in analyses if a['user_id'] == user_id]
    user_analyses.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Limit results
    limited_results = user_analyses[:limit] if limit else user_analyses
    return limited_results

def get_user_by_id(user_id):
    """Get user by ID"""
    users = _load_json(USERS_FILE, {})
    
    if user_id not in users:
        return None
    
    user = users[user_id]
    return {
        'id': user_id,
        'username': user_id,
        'farm_location': user.get('farm_location'),  # Include farm location
        'profile_complete': user.get('profile_complete', False)
    }

def get_user_profile(user_id):
    """Get user profile"""
    profiles = _load_json(PROFILES_FILE, {})
    
    if user_id not in profiles:
        return None
    
    return profiles[user_id]