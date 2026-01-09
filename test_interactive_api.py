import requests

BASE_URL = "http://127.0.0.1:5000"

def get_risk_color(score):
    if score >= 80:
        return "🔴"
    elif score >= 60:
        return "🟠"
    elif score >= 40:
        return "🟡"
    else:
        return "🟢"

def get_risk_bar(score):
    bar_length = 50
    filled = int((score / 100) * bar_length)
    empty = bar_length - filled
    return "[" + "█" * filled + "░" * empty + "]"

def get_confidence_level(confidence):
    conf_pct = confidence * 100
    if conf_pct >= 90:
        return "VERY HIGH ✓✓✓"
    elif conf_pct >= 80:
        return "HIGH ✓✓"
    elif conf_pct >= 70:
        return "GOOD ✓"
    elif conf_pct >= 50:
        return "MODERATE"
    else:
        return "LOW"

def analyze_message(message):
    try:
        response = requests.post(
            f"{BASE_URL}/api/detect-scam",
            json={"message": message},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            
            verdict = result['verdict']
            risk_score = result['risk_score']
            confidence = result['confidence']
            
            # Display results
            print("\n" + "="*90)
            print(f"VERDICT:                               {verdict. upper()}")
            print("="*90)
            
            risk_bar = get_risk_bar(risk_score)
            risk_color = get_risk_color(risk_score)
            print(f"\nRISK SCORE:                           {risk_score}% {risk_bar} {risk_color}")
            
            conf_pct = confidence * 100
            conf_bar = get_risk_bar(conf_pct)
            conf_level = get_confidence_level(confidence)
            print(f"\nCONFIDENCE:                           {conf_pct:. 2f}% {conf_bar} [{conf_level}]")
            print("\n" + "="*90 + "\n")
            
            return True
        else:
            print(f"\n✗ Error: {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Cannot connect to Flask server!")
        print("✗ Make sure Flask is running:   python app.py")
        return False
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return False

def main():
    print("\n" + "="*90)
    print("SCAM DETECTION SYSTEM - INTERACTIVE CLI")
    print("="*90)
    print("\nType 'quit' to exit.\n")
    
    counter = 1
    while True:
        try:
            print("-"*90)
            print(f"[Message {counter}] Enter text (or 'quit'):")
            message = input("> ").strip()
            
            if not message:
                print("✗ Message cannot be empty!")
                continue
            
            if message.lower() in ['quit', 'exit', 'q']:
                print("\n" + "="*90)
                print("Stay safe!")
                print("="*90 + "\n")
                break
            
            analyze_message(message)
            counter += 1
        
        except KeyboardInterrupt: 
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()