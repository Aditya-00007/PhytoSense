"""
Utility functions for safer profile field access that works with both object and dictionary access
"""

def get_profile_field(profile, field, default='Not set'):
    """
    Get a field from a profile, regardless of whether it's a dictionary or an object
    
    Args:
        profile: Profile object or dict
        field: Field name to access
        default: Default value if field is not found
        
    Returns:
        Field value or default
    """
    if not profile:
        return default
        
    # Try dictionary access first
    if isinstance(profile, dict):
        return profile.get(field, default)
    
    # Fall back to object attribute access
    try:
        return getattr(profile, field, default)
    except:
        return default