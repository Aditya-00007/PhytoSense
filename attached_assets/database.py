import os
import hashlib
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import text, pool
import json
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# SQLAlchemy setup with connection retry and pool settings
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
    logger.warning("DATABASE_URL environment variable is not set!")
    # Don't raise an exception here, the db_adapter will handle the fallback
elif DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Retry connection if it fails
def create_engine_with_retry(url, max_retries=3, retry_interval=2):
    if url is None:
        logger.error("Cannot create engine with None URL")
        raise ValueError("Database URL is required but not provided")
        
    for attempt in range(max_retries):
        try:
            return sa.create_engine(
                url, 
                echo=False,
                pool_pre_ping=True,  # Check connections before using them
                pool_recycle=3600,   # Recycle connections after 1 hour
                pool_size=5,         # Maintain a pool of 5 connections
                max_overflow=10,     # Allow up to 10 overflow connections
                pool_timeout=30      # Timeout after 30 seconds
            )
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt+1} failed: {e}")
                time.sleep(retry_interval)
            else:
                logger.error(f"All database connection attempts failed: {e}")
                raise

# Only create engine if DATABASE_URL is available
if DATABASE_URL:
    try:
        engine = create_engine_with_retry(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        logger.error(f"Failed to create database engine: {e}")
        raise
else:
    # These will be defined but not used if no DATABASE_URL 
    # (will be handled by the adapter)
    engine = None
    SessionLocal = None

# Define Base for model definitions
Base = declarative_base()

# Define models
class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True, index=True)
    password = sa.Column(sa.String)  # In a real app, this would be hashed
    email = sa.Column(sa.String, nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    profile_complete = sa.Column(sa.Boolean, default=False)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    analyses = relationship("Analysis", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    full_name = sa.Column(sa.String, nullable=True)
    farm_name = sa.Column(sa.String, nullable=True)
    location = sa.Column(sa.String, nullable=True)
    district = sa.Column(sa.String, nullable=True)
    farm_size = sa.Column(sa.String, nullable=True)
    main_crops = sa.Column(sa.String, nullable=True)
    soil_type = sa.Column(sa.String, nullable=True)
    irrigation_method = sa.Column(sa.String, nullable=True)
    crop_status = sa.Column(sa.Text, nullable=True)

    user = relationship("User", back_populates="profile")

class Analysis(Base):
    __tablename__ = "analyses"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    timestamp = sa.Column(sa.DateTime, default=datetime.utcnow)
    analysis_type = sa.Column(sa.String)  # 'plant', 'soil', etc.
    image_path = sa.Column(sa.String, nullable=True)
    results = sa.Column(sa.JSON)  # Store JSON data

    user = relationship("User", back_populates="analyses")

# Create all tables if engine is available
if engine:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

def get_db():
    """Get a database session with retry mechanism"""
    if SessionLocal is None:
        logger.error("Attempted to get database session but no SessionLocal is available")
        raise ValueError("Database connection not available")
        
    max_retries = 3
    retry_interval = 2
    db = None
    
    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            # Test connection with a simple query
            db.execute(text("SELECT 1"))
            return db
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Database connection attempt {attempt+1} failed: {e}")
                time.sleep(retry_interval)
            else:
                # If all retries fail, close the connection and raise the exception
                if db:
                    try:
                        db.close()
                    except:
                        pass
                logger.error(f"All database connection attempts failed: {e}")
                raise

def hash_password(password):
    """Create a hash of a password"""
    salt = "phytosense"  # In a real app, this would be a random salt stored in the database
    return hashlib.sha256((password + salt).encode()).hexdigest()

def create_user(username, password, email=None):
    """Create a new user"""
    db = get_db()
    try:
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            db.close()
            return False, "Username already exists"
        
        # Create user
        hashed_password = hash_password(password)
        new_user = User(
            username=username,
            password=hashed_password,
            email=email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        return True, new_user
    except Exception as e:
        db.rollback()
        db.close()
        return False, str(e)

def verify_user(username, password):
    """Verify user credentials"""
    db = get_db()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            db.close()
            return None
        
        hashed_password = hash_password(password)
        if user.password == hashed_password:
            db.close()
            return user  # SQLAlchemy objects are used directly
        else:
            db.close()
            return None
    except Exception as e:
        db.close()
        return None

def update_user_profile(user_id, profile_data):
    """Update user profile"""
    db = get_db()
    try:
        # Check if profile exists
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        if not profile:
            # Create new profile
            profile = UserProfile(user_id=user_id)
            db.add(profile)
        
        # Update profile fields
        if 'full_name' in profile_data:
            profile.full_name = profile_data['full_name']
        if 'farm_name' in profile_data:
            profile.farm_name = profile_data['farm_name']
        if 'location' in profile_data:
            profile.location = profile_data['location']
        if 'district' in profile_data:
            profile.district = profile_data['district']
        if 'farm_size' in profile_data:
            profile.farm_size = profile_data['farm_size']
        if 'main_crops' in profile_data:
            profile.main_crops = profile_data['main_crops']
        if 'soil_type' in profile_data:
            profile.soil_type = profile_data['soil_type']
        if 'irrigation_method' in profile_data:
            profile.irrigation_method = profile_data['irrigation_method']
        if 'crop_status' in profile_data:
            profile.crop_status = profile_data['crop_status']
        
        # Mark user profile as complete
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.profile_complete = True
        
        db.commit()
        db.close()
        return True, "Profile updated successfully"
    except Exception as e:
        db.rollback()
        db.close()
        return False, str(e)

def save_analysis(user_id, analysis_type, image_path, results):
    """Save analysis results"""
    db = get_db()
    try:
        # Convert results to JSON-serializable format if needed
        if isinstance(results, dict):
            # Handle NumPy types which are not JSON serializable
            results_str = json.dumps(results, default=lambda x: float(x) if hasattr(x, 'item') else x)
            results = json.loads(results_str)
        
        analysis = Analysis(
            user_id=user_id,
            analysis_type=analysis_type,
            image_path=image_path,
            results=results
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        db.close()
        return True, analysis.id
    except Exception as e:
        db.rollback()
        db.close()
        return False, str(e)

def get_user_analyses(user_id, limit=10):
    """Get user's analysis history"""
    db = get_db()
    try:
        analyses = db.query(Analysis).filter(Analysis.user_id == user_id).order_by(Analysis.timestamp.desc()).limit(limit).all()
        db.close()
        return analyses
    except Exception as e:
        db.close()
        return []

def get_user_by_id(user_id):
    """Get user by ID"""
    db = get_db()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        return user
    except Exception as e:
        db.close()
        return None

def get_user_profile(user_id):
    """Get user profile"""
    db = get_db()
    try:
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        db.close()
        return profile
    except Exception as e:
        db.close()
        return None