
import os
import json
from local_db import create_user, verify_user, get_user_profile, USERS_FILE, PROFILES_FILE

# Setup: Remove existing test files if any
if os.path.exists(USERS_FILE):
    os.remove(USERS_FILE)
if os.path.exists(PROFILES_FILE):
    os.remove(PROFILES_FILE)

# Test 1: Create user with location
print("Creating user with location 'Pune'...")
success, msg = create_user("testuser", "password123", "test@example.com", farm_location="Pune")
print(f"Create user result: {success}, {msg}")

# Test 2: Login (verify_user)
print("Verifying user...")
user = verify_user("testuser", "password123")
print(f"User data: {user}")

if user and user.get('farm_location') == 'Pune':
    print("SUCCESS: farm_location found in user object.")
else:
    print("FAILURE: farm_location missing or incorrect in user object.")

# Test 3: Get User Profile
print("Getting user profile...")
profile = get_user_profile("testuser")
print(f"Profile: {profile}")

if profile and profile.get('farm_location') == 'Pune':
    print("SUCCESS: farm_location found in profile.")
else:
    print("FAILURE: farm_location missing or incorrect in profile.")

# Cleanup
if os.path.exists(USERS_FILE):
    os.remove(USERS_FILE)
if os.path.exists(PROFILES_FILE):
    os.remove(PROFILES_FILE)
