"""
Database adapter module for PhytoSense application.
Provides functions for interacting with the database for user management and analysis storage.
"""

import os
import json
import hashlib
from datetime import datetime

# Attempt to import SQLAlchemy for database operations
try:
    from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship
    from sqlalchemy.pool import NullPool
    import sqlalchemy.exc
    
    # Check if database URL is available
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Set up SQLAlchemy if database URL is available
    if DATABASE_URL:
        # Fix for Heroku's postgres:// vs postgresql:// issue
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
        # Create engine with NullPool to avoid pool timeout issues
        engine = create_engine(DATABASE_URL, poolclass=NullPool)
        
        # Create base class for SQLAlchemy models
        Base = declarative_base()
        
        # Create session maker
        Session = sessionmaker(bind=engine)
        
        # Define SQLAlchemy models
        class User(Base):
            """User model for authentication and profile information"""
            __tablename__ = 'users'
            
            id = Column(Integer, primary_key=True)
            username = Column(String(50), unique=True, nullable=False)
            password = Column(String(128), nullable=False)  # Stores hashed password
            email = Column(String(100))
            farm_location = Column(String(100))
            profile_complete = Column(Boolean, default=False)
            created_at = Column(DateTime, default=datetime.utcnow)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            # Relationships
            analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
            profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
        
        class UserProfile(Base):
            """Extended user profile information"""
            __tablename__ = 'user_profiles'
            
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
            name = Column(String(100))
            farm_size = Column(String(50))
            farming_type = Column(String(50))
            irrigation = Column(String(50))
            primary_crops = Column(String(200))
            secondary_crops = Column(String(200))
            receive_weather_alerts = Column(Boolean, default=True)
            preferred_language = Column(String(20), default='English')
            additional_info = Column(JSON)
            created_at = Column(DateTime, default=datetime.utcnow)
            updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            
            # Relationships
            user = relationship("User", back_populates="profile")
        
        class Analysis(Base):
            """Store analysis results"""
            __tablename__ = 'analyses'
            
            id = Column(Integer, primary_key=True)
            user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
            analysis_type = Column(String(50), nullable=False)  # 'plant', 'soil', etc.
            image_path = Column(String(255))
            results = Column(JSON)
            timestamp = Column(DateTime, default=datetime.utcnow)
            
            # Relationships
            user = relationship("User", back_populates="analyses")
        
        # Create tables if they don't exist
        try:
            Base.metadata.create_all(engine)
            USE_SQLALCHEMY = True
        except (sqlalchemy.exc.OperationalError, sqlalchemy.exc.ProgrammingError) as e:
            print(f"Could not create database tables: {e}")
            USE_SQLALCHEMY = False
    else:
        USE_SQLALCHEMY = False
except ImportError:
    USE_SQLALCHEMY = False

# Fall back to JSON-based storage if SQLAlchemy is not available
# Fall back to MongoDB if SQLAlchemy is not available
try:
    from mongo_db import (
        create_user as mongo_create_user,
        verify_user as mongo_verify_user,
        update_user_profile as mongo_update_user_profile,
        save_analysis as mongo_save_analysis,
        get_user_analyses as mongo_get_user_analyses,
        get_user_by_id as mongo_get_user_by_id,
        get_user_profile as mongo_get_user_profile,
        hash_password,
        verify_forgot_password as mongo_verify_forgot_password,
        reset_password as mongo_reset_password
    )
    USE_MONGO = True
except ImportError:
    USE_MONGO = False

# Fall back to JSON-based storage if Mongo is not available
from local_db import (
    create_user as json_create_user,
    verify_user as json_verify_user,
    update_user_profile as json_update_user_profile,
    save_analysis as json_save_analysis,
    get_user_analyses as json_get_user_analyses,
    get_user_by_id as json_get_user_by_id,
    get_user_profile as json_get_user_profile,
    hash_password as json_hash_password,
    save_session,
    get_active_session,
    clear_session,
    verify_forgot_password as json_verify_forgot_password,
    reset_password as json_reset_password
)

if not USE_MONGO:
    # re-export hash_password if mongo didn't load
    hash_password = json_hash_password

def create_user(username, password, email=None, farm_location=None):
    """
    Create a new user
    
    Args:
        username: User's username
        password: User's password
        email: Optional email address
        farm_location: Optional farm location
        
    Returns:
        tuple: (success, message)
    """
    if USE_SQLALCHEMY:
        try:
            session = Session()
            
            # Check if username already exists
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                session.close()
                return False, "Username already exists"
            
            # Hash password
            hashed_password = hash_password(password)
            
            # Create new user
            new_user = User(
                username=username,
                password=hashed_password,
                email=email,
                farm_location=farm_location,
                profile_complete=False
            )
            
            session.add(new_user)
            session.commit()
            session.close()
            
            return True, "User created successfully"
        except Exception as e:
            try:
                session.rollback()
            except:
                pass
            finally:
                session.close()
            return False, f"Error creating user: {str(e)}"
    elif USE_MONGO:
        return mongo_create_user(username, password, email, farm_location)
    else:
        # Fall back to JSON-based storage
        return json_create_user(username, password, email, farm_location)

def verify_user(username, password):
    """
    Verify user credentials
    
    Args:
        username: User's username
        password: User's password
        
    Returns:
        User object if credentials are valid, None otherwise
    """
    if USE_SQLALCHEMY:
        try:
            session = Session()
            
            # Find user by username
            user = session.query(User).filter_by(username=username).first()
            
            if user and user.password == hash_password(password):
                # Credentials are valid
                result = {
                    'id': user.id,
                    'username': user.username,
                    'farm_location': user.farm_location,
                    'profile_complete': user.profile_complete
                }
                session.close()
                return result
            
            session.close()
            return None
        except Exception as e:
            try:
                session.close()
            except:
                pass
            return None
    elif USE_MONGO:
        return mongo_verify_user(username, password)
    else:
        # Fall back to JSON-based storage
        return json_verify_user(username, password)

def update_user_profile(user_id, profile_data):
    """
    Update user profile information
    
    Args:
        user_id: User ID
        profile_data: Dictionary containing profile information
        
    Returns:
        tuple: (success, message)
    """
    if USE_SQLALCHEMY:
        try:
            session = Session()
            
            # Find user by ID
            user = session.query(User).filter_by(id=user_id).first()
            
            if not user:
                session.close()
                return False, "User not found"
            
            # Update farm_location if provided
            if 'farm_location' in profile_data:
                user.farm_location = profile_data['farm_location']
            
            # Mark profile as complete
            user.profile_complete = True
            
            # Find existing profile or create new one
            profile = session.query(UserProfile).filter_by(user_id=user_id).first()
            
            if not profile:
                profile = UserProfile(user_id=user_id)
                session.add(profile)
            
            # Update profile fields
            for key, value in profile_data.items():
                if key != 'farm_location' and hasattr(profile, key):
                    setattr(profile, key, value)
            
            # Store additional fields in JSON column
            additional_info = {}
            for key, value in profile_data.items():
                if not hasattr(profile, key) and key != 'farm_location':
                    additional_info[key] = value
            
            if additional_info:
                profile.additional_info = additional_info
            
            session.commit()
            session.close()
            
            return True, "Profile updated successfully"
        except Exception as e:
            try:
                session.rollback()
            except:
                pass
            return False, f"Error updating profile: {str(e)}"
    elif USE_MONGO:
        return mongo_update_user_profile(user_id, profile_data)
    else:
        # Fall back to JSON-based storage
        return json_update_user_profile(user_id, profile_data)

def save_analysis(user_id, analysis_type, image_path, results):
    """
    Save analysis results
    
    Args:
        user_id: User ID
        analysis_type: Type of analysis ('plant', 'soil', etc.)
        image_path: Path to the uploaded image
        results: Analysis results (will be stored as JSON)
        
    Returns:
        tuple: (success, analysis_id)
    """
    if USE_SQLALCHEMY:
        try:
            session = Session()
            
            # Find user by ID
            user = session.query(User).filter_by(id=user_id).first()
            
            if not user:
                session.close()
                return False, "User not found"
            
            # Create new analysis
            new_analysis = Analysis(
                user_id=user_id,
                analysis_type=analysis_type,
                image_path=image_path,
                results=results
            )
            
            session.add(new_analysis)
            session.commit()
            
            analysis_id = new_analysis.id
            
            session.close()
            
            return True, analysis_id
        except Exception as e:
            try:
                session.rollback()
            except:
                pass
            return False, f"Error saving analysis: {str(e)}"
    elif USE_MONGO:
        return mongo_save_analysis(user_id, analysis_type, image_path, results)
    else:
        # Fall back to JSON-based storage
        success = json_save_analysis(user_id, analysis_type, image_path, results)
        return success, "Analysis saved successfully"

def get_user_analyses(user_id, limit=None):
    """
    Get analyses for a specific user
    
    Args:
        user_id: User ID
        limit: Optional maximum number of analyses to return
        
    Returns:
        list: User's analyses
    """
    if USE_SQLALCHEMY:
        try:
            session = Session()
            
            # Query user's analyses, ordered by timestamp (newest first)
            query = session.query(Analysis).filter_by(user_id=user_id).order_by(Analysis.timestamp.desc())
            
            if limit:
                query = query.limit(limit)
            
            analyses = query.all()
            
            # Convert SQLAlchemy objects to dictionaries
            result = []
            for analysis in analyses:
                result.append({
                    'id': analysis.id,
                    'user_id': analysis.user_id,
                    'analysis_type': analysis.analysis_type,
                    'image_path': analysis.image_path,
                    'results': analysis.results,
                    'timestamp': analysis.timestamp.isoformat()
                })
            
            session.close()
            
            return result
        except Exception as e:
            try:
                session.close()
            except:
                pass
            return []
    elif USE_MONGO:
        return mongo_get_user_analyses(user_id, limit)
    else:
        # Fall back to JSON-based storage
        return json_get_user_analyses(user_id, limit)

def get_user_by_id(user_id):
    """
    Get user by ID
    
    Args:
        user_id: User ID
        
    Returns:
        User object or None if not found
    """
    if USE_SQLALCHEMY:
        try:
            session = Session()
            
            user = session.query(User).filter_by(id=user_id).first()
            
            if not user:
                session.close()
                return None
            
            result = {
                'id': user.id,
                'username': user.username,
                'farm_location': user.farm_location,
                'profile_complete': user.profile_complete
            }
            
            session.close()
            
            return result
        except Exception as e:
            try:
                session.close()
            except:
                pass
            return None
    elif USE_MONGO:
        return mongo_get_user_by_id(user_id)
    else:
        # Fall back to JSON-based storage
        return json_get_user_by_id(user_id)

def get_user_profile(user_id):
    """
    Get user profile information
    
    Args:
        user_id: User ID
        
    Returns:
        Dictionary containing profile information or None if not found
    """
    if USE_SQLALCHEMY:
        try:
            session = Session()
            
            profile = session.query(UserProfile).filter_by(user_id=user_id).first()
            
            if not profile:
                session.close()
                return None
            
            # Extract profile attributes
            result = {
                'user_id': profile.user_id,
                'name': profile.name,
                'farm_size': profile.farm_size,
                'farming_type': profile.farming_type,
                'irrigation': profile.irrigation,
                'primary_crops': profile.primary_crops,
                'secondary_crops': profile.secondary_crops,
                'receive_weather_alerts': profile.receive_weather_alerts,
                'preferred_language': profile.preferred_language
            }
            
            # Add additional info if available
            if profile.additional_info:
                for key, value in profile.additional_info.items():
                    result[key] = value
            
            # Get farm_location from user
            user = session.query(User).filter_by(id=user_id).first()
            if user and user.farm_location:
                result['farm_location'] = user.farm_location
            
            session.close()
            
            return result
        except Exception as e:
            try:
                session.close()
            except:
                pass
            return None
    elif USE_MONGO:
        return mongo_get_user_profile(user_id)
    else:
        # Fall back to JSON-based storage
        return json_get_user_profile(user_id)

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
    if USE_SQLALCHEMY:
        # Placeholder for SQL implementation - not requested but good practice to have structure
        try:
            session = Session()
            user = session.query(User).filter_by(username=username).first()
            if not user or user.email != email:
                session.close()
                return False
                
            # Check profile name
            profile = session.query(UserProfile).filter_by(user_id=user.id).first()
            if not profile or profile.name != full_name:
                session.close()
                return False
                
            session.close()
            return True
        except:
            return False
    elif USE_MONGO:
        return mongo_verify_forgot_password(username, email, full_name)
    else:
        return json_verify_forgot_password(username, email, full_name)

def reset_password(username, new_password):
    """
    Reset user password
    
    Args:
        username: Username
        new_password: New password
        
    Returns:
        bool: True if successful, False otherwise
    """
    if USE_SQLALCHEMY:
        try:
            session = Session()
            user = session.query(User).filter_by(username=username).first()
            if not user:
                session.close()
                return False
                
            user.password = hash_password(new_password)
            user.updated_at = datetime.utcnow()
            session.commit()
            session.close()
            return True
        except:
            return False
    elif USE_MONGO:
        return mongo_reset_password(username, new_password)
    else:
        return json_reset_password(username, new_password)
