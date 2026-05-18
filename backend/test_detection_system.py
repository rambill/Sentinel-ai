"""
Comprehensive test script for SentinelAI detection system
Tests various threat levels and validates AI accuracy
"""
import requests
import json
from typing import Dict, List
import sys

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://localhost:8000/api"

# Test messages with expected threat levels
TEST_MESSAGES = {
    "HIGH_RISK_1": {
        "text": "URGENT: Your bank account has been suspended due to suspicious activity! Click here immediately to verify your identity: http://bit.ly/verify-now or your account will be permanently closed within 24 hours. Enter your credit card details to confirm.",
        "expected": "high",
        "min_confidence": 70
    },
    "HIGH_RISK_2": {
        "text": "CONGRATULATIONS! You've won $1,000,000 in the international lottery! Act now to claim your prize. Send processing fee of $500 via wire transfer immediately. Limited time offer expires today! Call now: +1-555-SCAM",
        "expected": "high",
        "min_confidence": 70
    },
    "HIGH_RISK_3": {
        "text": "FINAL NOTICE: Unauthorized access detected on your PayPal account. Immediate action required! Your account will be terminated in 48 hours. Click this link to reset password and update payment information: https://paypal-security.tk/verify",
        "expected": "high",
        "min_confidence": 70
    },
    "MEDIUM_RISK_1": {
        "text": "Hello, we noticed unusual activity on your account. Please verify your information at your earliest convenience by visiting our website. Contact customer support if you have questions.",
        "expected": "medium",
        "min_confidence": 40
    },
    "MEDIUM_RISK_2": {
        "text": "Limited time offer! Get 50% off your next purchase. Click here to claim your discount before it expires. Don't miss out on this exclusive deal.",
        "expected": "medium",
        "min_confidence": 35
    },
    "LOW_RISK_1": {
        "text": "Hi John, thanks for your email yesterday. I've reviewed the project proposal and it looks great. Let's schedule a meeting next week to discuss the timeline. Looking forward to working with you.",
        "expected": "low",
        "max_confidence": 40
    },
    "LOW_RISK_2": {
        "text": "Your order #12345 has been shipped and will arrive in 3-5 business days. You can track your package using the tracking number provided in your confirmation email. Thank you for your purchase.",
        "expected": "low",
        "max_confidence": 40
    },
    "LOW_RISK_3": {
        "text": "Hey! How was your weekend? I went hiking with some friends and the weather was perfect. We should plan a trip together sometime. Let me know when you're free!",
        "expected": "low",
        "max_confidence": 30
    }
}


def test_text_analysis(test_id: str, test_data: Dict) -> Dict:
    """Test a single text message"""
    print(f"\n{'='*80}")
    print(f"TEST: {test_id}")
    print(f"{'='*80}")
    print(f"Message: {test_data['text'][:100]}...")
    print(f"Expected: {test_data['expected'].upper()} risk")
    
    try:
        response = requests.post(
            f"{API_URL}/analyze-text",
            json={"text": test_data["text"]},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ RESULT:")
            print(f"   Is Scam: {result['isScam']}")
            print(f"   Confidence: {result['confidence']}%")
            print(f"   Threat Level: {result['threatLevel'].upper()}")
            print(f"   Explanation: {result['explanation'][:150]}...")
            print(f"\n   Indicators ({len(result['indicators'])}):")
            for indicator in result['indicators'][:5]:
                print(f"   - {indicator}")
            
            # Validate results
            passed = True
            issues = []
            
            # Check threat level
            if result['threatLevel'] != test_data['expected']:
                passed = False
                issues.append(f"Expected {test_data['expected']} but got {result['threatLevel']}")
            
            # Check confidence range
            if 'min_confidence' in test_data:
                if result['confidence'] < test_data['min_confidence']:
                    passed = False
                    issues.append(f"Confidence {result['confidence']}% below minimum {test_data['min_confidence']}%")
            
            if 'max_confidence' in test_data:
                if result['confidence'] > test_data['max_confidence']:
                    passed = False
                    issues.append(f"Confidence {result['confidence']}% above maximum {test_data['max_confidence']}%")
            
            if passed:
                print(f"\n✅ TEST PASSED")
            else:
                print(f"\n❌ TEST FAILED:")
                for issue in issues:
                    print(f"   - {issue}")
            
            return {
                "test_id": test_id,
                "passed": passed,
                "issues": issues,
                "result": result
            }
        else:
            print(f"\n❌ API ERROR: {response.status_code}")
            print(f"   {response.text}")
            return {
                "test_id": test_id,
                "passed": False,
                "issues": [f"API error: {response.status_code}"],
                "result": None
            }
    
    except Exception as e:
        print(f"\n❌ EXCEPTION: {str(e)}")
        return {
            "test_id": test_id,
            "passed": False,
            "issues": [f"Exception: {str(e)}"],
            "result": None
        }


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("SENTINELAI DETECTION SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*80)
    
    # Check if backend is running
    try:
        response = requests.get(f"http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print("❌ Backend returned error")
            return
    except:
        print("❌ Backend is not running. Start it with: cd backend && python -m app.main")
        return
    
    # Run all tests
    results = []
    for test_id, test_data in TEST_MESSAGES.items():
        result = test_text_analysis(test_id, test_data)
        results.append(result)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results if r['passed'])
    failed = len(results) - passed
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    
    if failed > 0:
        print(f"\n❌ FAILED TESTS:")
        for result in results:
            if not result['passed']:
                print(f"\n{result['test_id']}:")
                for issue in result['issues']:
                    print(f"  - {issue}")
    
    # Detailed statistics
    print(f"\n" + "="*80)
    print("CONFIDENCE SCORES BY CATEGORY")
    print("="*80)
    
    high_risk_scores = []
    medium_risk_scores = []
    low_risk_scores = []
    
    for result in results:
        if result['result']:
            conf = result['result']['confidence']
            if 'HIGH_RISK' in result['test_id']:
                high_risk_scores.append(conf)
            elif 'MEDIUM_RISK' in result['test_id']:
                medium_risk_scores.append(conf)
            elif 'LOW_RISK' in result['test_id']:
                low_risk_scores.append(conf)
    
    if high_risk_scores:
        print(f"\nHigh Risk Messages:")
        print(f"  Average: {sum(high_risk_scores)/len(high_risk_scores):.1f}%")
        print(f"  Range: {min(high_risk_scores):.1f}% - {max(high_risk_scores):.1f}%")
    
    if medium_risk_scores:
        print(f"\nMedium Risk Messages:")
        print(f"  Average: {sum(medium_risk_scores)/len(medium_risk_scores):.1f}%")
        print(f"  Range: {min(medium_risk_scores):.1f}% - {max(medium_risk_scores):.1f}%")
    
    if low_risk_scores:
        print(f"\nLow Risk Messages:")
        print(f"  Average: {sum(low_risk_scores)/len(low_risk_scores):.1f}%")
        print(f"  Range: {min(low_risk_scores):.1f}% - {max(low_risk_scores):.1f}%")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
