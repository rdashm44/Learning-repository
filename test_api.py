"""
Quick API test to verify the setup works
"""
import requests
import json

BASE_URL = "http://localhost:5001"

print("Testing Hunt Club Manager API")
print("=" * 50)

# Test 1: API Info
print("\n1. Testing API Info Endpoint...")
response = requests.get(f"{BASE_URL}/api/")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print("✅ API Info endpoint works!")
    data = response.json()
    print(f"API Version: {data['version']}")
else:
    print(f"❌ Failed: {response.text}")

# Test 2: Login
print("\n2. Testing Login...")
login_data = {
    "username": "admin",
    "password": "admin123"
}
response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json=login_data,
    headers={"Content-Type": "application/json"}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data.get('token')
    print(f"✅ Login successful!")
    print(f"Token (first 20 chars): {token[:20]}...")
    print(f"User: {data['user']}")

    # Test 3: Get Stands with Token
    print("\n3. Testing Get Stands (with auth)...")
    response = requests.get(
        f"{BASE_URL}/api/stands",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Got {len(data['stands'])} stands")
        for stand in data['stands'][:3]:
            print(f"  - {stand['name']}: {stand['description']}")
    else:
        print(f"❌ Failed: {response.text}")

    # Test 4: Get My Checkin
    print("\n4. Testing Get My Check-in...")
    response = requests.get(
        f"{BASE_URL}/api/stands/my-checkin",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Checkin status: {data['checkin']}")
    else:
        print(f"❌ Failed: {response.text}")

else:
    print(f"❌ Login failed: {response.text}")

print("\n" + "=" * 50)
print("API Testing Complete!")
