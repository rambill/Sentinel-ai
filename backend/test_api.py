"""
Simple test script to verify the SentinelAI API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root():
    """Test root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_health():
    """Test health check endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_analyze_text():
    """Test text analysis endpoint"""
    print("Testing text analysis endpoint...")
    
    # Test with suspicious text
    data = {
        "text": "URGENT: Your account has been suspended! Click here immediately to verify your identity."
    }
    
    response = requests.post(f"{BASE_URL}/api/analyze-text", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_stats():
    """Test statistics endpoint"""
    print("Testing stats endpoint...")
    response = requests.get(f"{BASE_URL}/api/stats")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("SentinelAI API Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_root()
        test_health()
        test_analyze_text()
        test_stats()
        
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
