
import os
import json
from local_db import create_user, verify_user, get_user_profile, USERS_FILE, PROFILES_FILE

# Setup: Remove existing test files if any
if os.path.exists(USERS_FILE):
    os.remove(USERS_FILE)
if os.path.exists(PROFILES_FILE):
    os.remove(PROFILES_FILE)

# Test 1: Create user without location (empty string)
print("Creating user with empty location...")
success, msg = create_user("testuser_empty", "password123", "test@example.com", farm_location="")
print(f"Create user result: {success}, {msg}")

# Test 2: Verify user
print("Verifying user...")
user = verify_user("testuser_empty", "password123")
print(f"User data: {user}")

if user and user.get('farm_location') == "":
    print("SUCCESS: Empty farm_location found in user object.")
else:
    print(f"FAILURE: farm_location is unexpected: {user.get('farm_location')}")

# Test 3: Get User Profile
print("Getting user profile...")
profile = get_user_profile("testuser_empty")
print(f"Profile: {profile}")

# profile should merge '' from user.json
if profile and profile.get('farm_location') == "":
    print("SUCCESS: Empty farm_location found in profile.")
else:
    print(f"FAILURE: farm_location missing or incorrect in profile: {profile.get('farm_location')}")

# Cleanup
if os.path.exists(USERS_FILE):
    os.remove(USERS_FILE)
if os.path.exists(PROFILES_FILE):
    os.remove(PROFILES_FILE)
