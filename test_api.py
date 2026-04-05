import requests
import sys

BASE_URL = "http://127.0.0.1:8000/api"

def run_tests():
    print("Testing Auth...")
    # Register
    reg_data = {
        "full_name": "Test User",
    "email": f"test_{__import__('time').time()}@example.com",
        "password": "password123"
    }
    r = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
    if r.status_code != 200:
        print(f"Register failed: {r.text}")
        sys.exit(1)
    print("Register OK")

    # Login
    login_data = {"username": reg_data["email"], "password": reg_data["password"]}
    r = requests.post(f"{BASE_URL}/auth/login", data=login_data)
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        sys.exit(1)
    
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("Login OK")

    # Get Me
    r = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if r.status_code != 200:
        print(f"Me failed: {r.text}")
        sys.exit(1)
    print("Me OK")

    # Update Profile
    prof_data = {
        "profession": "Software Developer",
        "sleep_pattern": "Evening (10-11 PM)",
        "personality": "Ambivert",
        "cleanliness": "Organized",
        "noise_tolerance": "Quiet",
        "room_preference": "single-bedded",
        "bedtime": "11 PM",
        "wake_time": "7 AM",
        "sleep_type": "Light Sleeper",
        "social_energy_rating": 7
    }
    r = requests.put(f"{BASE_URL}/profile", headers=headers, json=prof_data)
    if r.status_code != 200:
        print(f"Profile Update failed: {r.text}")
        sys.exit(1)
    print("Profile Update OK")

    # Get Matches
    r = requests.get(f"{BASE_URL}/matches?limit=5", headers=headers)
    if r.status_code != 200:
        print(f"Matches failed: {r.text}")
        sys.exit(1)
    matches = r.json()
    print(f"Matches OK: fetched {len(matches)}")

    # Post Community Message
    r = requests.post(f"{BASE_URL}/community/messages", headers=headers, json={"text": "Hello Community!"})
    if r.status_code != 200:
        print(f"Community Post failed: {r.text}")
        sys.exit(1)
    print("Community Post OK")

    # Get Community Messages
    r = requests.get(f"{BASE_URL}/community/messages", headers=headers)
    if r.status_code != 200:
        print(f"Community Get failed: {r.text}")
        sys.exit(1)
    print("Community Get OK")

    # Private Chat (with first match if any)
    if matches:
        match_id = matches[0].get("id")
        r = requests.post(f"{BASE_URL}/chat/{match_id}/messages", headers=headers, json={"text": "Hi Roomie", "receiver_is_seeded": True})
        if r.status_code != 200:
            print(f"Private Post failed: {r.text}")
            sys.exit(1)
        print("Private Post OK")

        r = requests.get(f"{BASE_URL}/chat/{match_id}/messages", headers=headers)
        if r.status_code != 200:
            print(f"Private Get failed: {r.text}")
            sys.exit(1)
        print("Private Get OK")

    # Download Agreement
    r = requests.get(f"{BASE_URL}/agreement/download", headers=headers)
    if r.status_code != 200:
        print(f"Agreement failed: {r.text}")
        sys.exit(1)
    if "application/pdf" not in r.headers.get("Content-Type", ""):
        print(f"Agreement failed: Wrong content type {r.headers}")
        sys.exit(1)
    print("Agreement OK")

    print("ALL TESTS PASSED")

if __name__ == "__main__":
    run_tests()
