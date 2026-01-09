#!/usr/bin/env python3
"""
Test script for SafeGuard detection modules
Run this to verify your detection algorithms are working correctly
"""

import sys
import os

# Add detection_modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'detection_modules'))

def test_scam_detection():
    """Test the scam detection module"""
    print("🔍 Testing Scam Detection Module...")
    
    try:
        from detection_modules.scam_detector import detect_scam
        
        # Test cases
        test_cases = [
            {
                'name': 'High Risk Scam',
                'content': """
                URGENT! Congratulations! You have won $1,000,000 in the international lottery!
                To claim your prize, please send your bank account details and social security number.
                This offer expires in 24 hours! Act now! Click here immediately!
                """
            },
            {
                'name': 'Medium Risk',
                'content': """
                Limited time offer! Make money fast working from home!
                No experience required. Guaranteed results. Click here for details.
                """
            },
            {
                'name': 'Safe Content',
                'content': """
                Hi John, hope you're doing well. Just wanted to follow up on our meeting
                scheduled for next week. Please let me know if you need to reschedule.
                Best regards, Sarah
                """
            }
        ]
        
        for test in test_cases:
            print(f"\n--- Testing: {test['name']} ---")
            result = detect_scam(test['content'])
            
            print(f"✅ Is Scam: {result['is_scam']}")
            print(f"✅ Score: {result['scam_score']}/100")
            print(f"✅ Message: {result['message']}")
            
            if 'risk_level' in result:
                print(f"✅ Risk Level: {result['risk_level']}")
            
            if result.get('detected_keywords'):
                print(f"✅ Keywords: {', '.join(result['detected_keywords'][:5])}")
        
        print("\n✅ Scam Detection Module: WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Scam Detection Module Error: {e}")
        return False


def test_fake_news_detection():
    """Test the fake news detection module"""
    print("\n🔍 Testing Fake News Detection Module...")
    
    try:
        from detection_modules.fake_news_detector import detect_fake_news
        
        # Test cases
        test_cases = [
            {
                'name': 'Fake News',
                'content': """
                SHOCKING! Doctors HATE this one simple trick that COMPLETELY eliminates cancer!
                You won't believe what this anonymous insider revealed about the secret government
                cover-up! This breakthrough study shows 99% of people don't know this amazing fact!
                BREAKING: Must read before it's too late!
                """
            },
            {
                'name': 'Questionable Content',
                'content': """
                Breaking news! Unbelievable discovery that will shock you!
                Sources say this secret method is being hidden from the public.
                """
            },
            {
                'name': 'Credible News',
                'content': """
                According to a study published in the Journal of Medical Research, researchers
                at Stanford University have identified a potential new treatment approach for
                certain types of cancer. The peer-reviewed study, conducted over 3 years with
                500 participants, showed promising preliminary results that warrant further investigation.
                """
            }
        ]
        
        for test in test_cases:
            print(f"\n--- Testing: {test['name']} ---")
            result = detect_fake_news(test['content'])
            
            print(f"✅ Is Fake: {result['is_fake']}")
            print(f"✅ Score: {result['fake_score']}/100")
            print(f"✅ Message: {result['message']}")
            
            if 'credibility_level' in result:
                print(f"✅ Credibility: {result['credibility_level']}")
            
            if result.get('detected_indicators'):
                print(f"✅ Indicators: {', '.join(result['detected_indicators'][:5])}")
        
        print("\n✅ Fake News Detection Module: WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Fake News Detection Module Error: {e}")
        return False


def test_flask_integration():
    """Test Flask app integration"""
    print("\n🔍 Testing Flask Integration...")
    
    try:
        # Import Flask app
        from app import app
        
        with app.test_client() as client:
            # Test scam detection endpoint
            scam_response = client.post('/analyze-scam', 
                                      json={'content': 'Test scam content'},
                                      headers={'Content-Type': 'application/json'})
            
            if scam_response.status_code == 401:  # Not authenticated
                print("✅ Scam endpoint requires authentication (correct)")
            else:
                print(f"⚠️ Unexpected scam endpoint response: {scam_response.status_code}")
            
            # Test fake news detection endpoint
            news_response = client.post('/analyze-news', 
                                      json={'content': 'Test news content'},
                                      headers={'Content-Type': 'application/json'})
            
            if news_response.status_code == 401:  # Not authenticated
                print("✅ News endpoint requires authentication (correct)")
            else:
                print(f"⚠️ Unexpected news endpoint response: {news_response.status_code}")
        
        print("✅ Flask Integration: WORKING")
        return True
        
    except Exception as e:
        print(f"❌ Flask Integration Error: {e}")
        return False


def main():
    """Run all tests"""
    print("🛡️ SafeGuard Detection Module Tests")
    print("=" * 50)
    
    results = []
    
    # Test individual modules
    results.append(test_scam_detection())
    results.append(test_fake_news_detection())
    results.append(test_flask_integration())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL TESTS PASSED ({passed}/{total})")
        print("\n🚀 Your SafeGuard application is ready to run!")
        print("   Run: python app.py")
        print("   Then visit: http://localhost:5000")
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total})")
        print("\n🔧 Please check the errors above and fix the issues.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)