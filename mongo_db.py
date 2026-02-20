from datetime import datetime
from mongo_config import get_database
from pymongo import DESCENDING

# Import hash_password from local_db (or utils if moved, but currently in local_db)
# We need to ensure we don't break if local_db is removed later, 
# but for now we can import it or duplicate the logic since it's simple sha256.
import hashlib

def hash_password(password):
    """Create a hash of a password"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_user(username, password, email=None, farm_location=None):
    """Create a new user with farm location"""
    db = get_database()
    if db is None:
        return False, "Database connection failed"
        
    # Check if username exists
    if db.users.find_one({"username": username}):
        return False, "Username already exists"
    
    user_doc = {
        "username": username,
        "password": hash_password(password),
        "email": email,
        "farm_location": farm_location,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "profile_complete": False
    }
    
    try:
        db.users.insert_one(user_doc)
        return True, "User created successfully"
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def verify_user(username, password):
    """Verify user credentials"""
    db = get_database()
    if db is None:
        return None
        
    user = db.users.find_one({"username": username})
    
    if user and user['password'] == hash_password(password):
        # Convert ObjectId to string if needed, or just use username as ID helper
        # The existing system uses username (or int ID) depending on adapter.
        # JSON adapter used username as ID. SQL used Int.
        # We will return a structure matching the JSON adapter's return for consistency.
        return {
            'id': user['username'], # Use username as ID for consistency with local_db and migration data
            'username': user['username'],
            'farm_location': user.get('farm_location'),
            'profile_complete': user.get('profile_complete', False)
        }
    return None

def update_user_profile(user_id, profile_data):
    """Update user profile"""
    db = get_database()
    if db is None:
        return False, "Database connection failed"
    
    # In JSON adapter, user_id is the username.
    # We should search by username if user_id is passed as such.
    # However, if we switched verify_user to return _id, we must query by _id.
    # Since we want to match local_db behavior (which uses username as key),
    # we'll assume user_id is the username for now, or handle both.
    
    # Strategy: Find user by username OR _id
    user = db.users.find_one({"username": user_id}) 
    # If not found by username, try _id (if valid ObjectId)
    if not user:
        # Check if user_id serves as a unique identifier compatible with our design
        # For this migration, we'll align with 'username' as the logical ID for consistency with local_db logic
        # if that is what was active.
        return False, "User not found"
        
    # Update farm_location in users collection if provided
    update_fields = {
        "profile_complete": True,
        "updated_at": datetime.utcnow()
    }
    if 'farm_location' in profile_data:
        update_fields['farm_location'] = profile_data['farm_location']
        
    db.users.update_one({"username": user_id}, {"$set": update_fields})
    
    # Update/Create profile in user_profiles collection
    profile_data['updated_at'] = datetime.utcnow()
    # Ensure user_id link is preserved
    profile_data['user_id'] = user_id 
    
    try:
        db.user_profiles.update_one(
            {"user_id": user_id},
            {"$set": profile_data},
            upsert=True
        )
        return True, "Profile updated successfully"
    except Exception as e:
        return False, f"Error updating profile: {str(e)}"

def save_analysis(user_id, analysis_type, image_path, results):
    """Save analysis results"""
    db = get_database()
    if db is None:
        return False, "Database connection failed"
        
    # Create analysis document
    # Note: timestamp is stored as Date object for TTL to work
    analysis_doc = {
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "analysis_type": analysis_type,
        "image_path": image_path,
        "results": results
    }
    
    try:
        result = db.analyses.insert_one(analysis_doc)
        return True, str(result.inserted_id)
    except Exception as e:
        return False, f"Error saving analysis: {str(e)}"

def get_user_analyses(user_id, limit=None):
    """Get user's analysis history"""
    db = get_database()
    if db is None:
        return []
        
    try:
        cursor = db.analyses.find({"user_id": user_id}).sort("timestamp", DESCENDING)
        
        if limit:
            cursor = cursor.limit(limit)
            
        analyses = []
        for doc in cursor:
            # Convert to structure expected by app (timestamp as ISO string)
            doc['id'] = str(doc['_id'])
            doc['timestamp'] = doc['timestamp'].isoformat()
            del doc['_id']
            analyses.append(doc)
            
        return analyses
    except Exception as e:
        print(f"Error fetching analyses: {e}")
        return []

def get_user_by_id(user_id):
    """Get user by ID (username)"""
    db = get_database()
    if db is None:
        return None
        
    user = db.users.find_one({"username": user_id})
    if not user:
        return None
        
    return {
        'id': user['username'],
        'username': user['username'],
        'farm_location': user.get('farm_location'),
        'profile_complete': user.get('profile_complete', False)
    }

def get_user_profile(user_id):
    """Get user profile"""
    db = get_database()
    if db is None:
        return None
        
    profile = db.user_profiles.find_one({"user_id": user_id})
    if not profile:
        # Check if user exists to return basic profile
        user = db.users.find_one({"username": user_id})
        if user:
            return {'user_id': user_id, 'farm_location': user.get('farm_location')}
        return None
    
    # Helper to merge farm_location from user if missing in profile (matches local_db logic)
    if 'farm_location' not in profile:
        user = db.users.find_one({"username": user_id})
        if user and user.get('farm_location'):
            profile['farm_location'] = user['farm_location']
            
    # Remove _id
    if '_id' in profile:
        del profile['_id']
        
    return profile

def verify_forgot_password(username, email, full_name):
    """
    Verify user details for password reset
    
    Args:
        username: Username
        email: Email address
        full_name: Full name of the user
        
    Returns:
        bool: True if details match, False otherwise
    """
    db = get_database()
    if db is None:
        return False
        
    # Find user by username
    user = db.users.find_one({"username": username})
    
    if not user:
        return False
        
    # Check email match
    if user.get("email") != email:
        return False
        
    # Check name match in user_profiles
    profile = db.user_profiles.find_one({"user_id": username})
    
    if not profile:
        # If no profile, check if name is stored in user doc (unlikely but safe fallback)
        return False
        
    if profile.get("name") != full_name:
        return False
        
    return True

def reset_password(username, new_password):
    """
    Reset user password
    
    Args:
        username: Username
        new_password: New password
        
    Returns:
        bool: True if successful, False otherwise
    """
    db = get_database()
    if db is None:
        return False
        
    try:
        hashed_password = hash_password(new_password)
        result = db.users.update_one(
            {"username": username},
            {"$set": {"password": hashed_password, "updated_at": datetime.utcnow()}}
        )
        return result.modified_count > 0
    except Exception:
        return False
