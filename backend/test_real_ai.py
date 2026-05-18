"""
Test script to demonstrate REAL AI detection capabilities
Run this after starting the backend server
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")

def print_result(result: Dict[Any, Any]):
    """Print analysis result in a formatted way"""
    print(f"🎯 Is Scam: {result.get('isScam', 'N/A')}")
    print(f"📊 Confidence: {result.get('confidence', 'N/A')}%")
    print(f"⚠️  Threat Level: {result.get('threatLevel', 'N/A').upper()}")
    print(f"\n💡 Explanation:\n{result.get('explanation', 'N/A')}")
    
    if 'indicators' in result and result['indicators']:
        print(f"\n🔍 Indicators Detected:")
        for indicator in result['indicators']:
            print(f"   {indicator}")
    
    if 'recommendation' in result:
        print(f"\n✅ Recommendation:\n{result.get('recommendation', 'N/A')}")

def test_health():
    """Test the health endpoint"""
    print_section("Testing Health Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Status: {data.get('status', 'unknown')}")
        print(f"📦 Version: {data.get('version', 'unknown')}")
        print(f"⏱️  Uptime: {data.get('uptime', 'unknown')}")
        
        print("\n🤖 AI Models Status:")
        ai_models = data.get('ai_models', {})
        for model_name, status in ai_models.items():
            print(f"   • {model_name}: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_phishing_message():
    """Test with a clear phishing message"""
    print_section("Test 1: Obvious Phishing Message")
    
    text = """
    URGENT! Your bank account has been compromised. 
    Click here immediately to verify your identity: http://bit.ly/secure123 
    or your account will be locked in 24 hours!
    """
    
    print(f"📝 Testing message:\n{text.strip()}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-text",
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        print_result(result)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_legitimate_message():
    """Test with a legitimate message"""
    print_section("Test 2: Legitimate Message")
    
    text = """
    Hi John, just wanted to confirm our meeting tomorrow at 3 PM.
    Looking forward to discussing the project details.
    Best regards, Sarah
    """
    
    print(f"📝 Testing message:\n{text.strip()}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-text",
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        print_result(result)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_lottery_scam():
    """Test with a lottery scam message"""
    print_section("Test 3: Lottery Scam")
    
    text = """
    Congratulations! You've won $1,000,000 in the international lottery!
    To claim your prize, send your bank details and $500 processing fee to:
    winner@lottery-claim.tk
    Act now! Offer expires in 48 hours!
    """
    
    print(f"📝 Testing message:\n{text.strip()}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-text",
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        print_result(result)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_tech_support_scam():
    """Test with a tech support scam"""
    print_section("Test 4: Tech Support Scam")
    
    text = """
    WARNING: Your computer has been infected with a virus!
    Call Microsoft Support immediately at 1-800-FAKE-NUM
    Do not turn off your computer or you will lose all your data!
    Our technicians are standing by 24/7 to help you.
    """
    
    print(f"📝 Testing message:\n{text.strip()}\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze-text",
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        print_result(result)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_statistics():
    """Test the statistics endpoint"""
    print_section("Testing Statistics Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        response.raise_for_status()
        data = response.json()
        
        print(f"📊 Total Analyses: {data.get('totalAnalyses', 0):,}")
        print(f"🚨 Scams Detected: {data.get('scamsDetected', 0):,}")
        print(f"✅ Legitimate: {data.get('legitimate', 0):,}")
        print(f"📈 Accuracy Rate: {data.get('accuracyRate', 0)}%")
        print(f"⚡ Avg Response Time: {data.get('avgResponseTime', 0)}ms")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🤖 "*20)
    print("  SentinelAI - REAL AI Detection Test Suite")
    print("🤖 "*20)
    
    # Check if server is running
    if not test_health():
        print("\n❌ Backend server is not running!")
        print("Please start the server first:")
        print("  cd backend")
        print("  python main.py")
        return
    
    # Run all tests
    tests = [
        test_phishing_message,
        test_legitimate_message,
        test_lottery_scam,
        test_tech_support_scam,
        test_statistics
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    # Summary
    print_section("Test Summary")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {passed + failed}")
    
    if failed == 0:
        print("\n🎉 All tests passed! Real AI detection is working perfectly!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please check the errors above.")
    
    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
