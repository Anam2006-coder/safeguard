#!/usr/bin/env python3
"""
SafeGuard Folder Setup Assistant
This script helps you integrate your existing detection folders
"""

import os
import sys
import glob

def find_python_files(folder_path):
    """Find all Python files in a folder"""
    python_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                python_files.append(os.path.join(root, file))
    return python_files

def scan_for_functions(file_path):
    """Scan a Python file for function definitions"""
    functions = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if line.strip().startswith('def ') and not line.strip().startswith('def __'):
                    func_name = line.strip().split('def ')[1].split('(')[0]
                    functions.append((func_name, i+1))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return functions

def detect_folders():
    """Detect potential detection folders in the current directory"""
    current_dir = os.getcwd()
    folders = []
    
    # Look for folders that might contain detection code
    for item in os.listdir(current_dir):
        if os.path.isdir(item) and item not in ['templates', 'detection_modules', '__pycache__', '.git']:
            # Check if folder contains Python files
            python_files = find_python_files(item)
            if python_files:
                folders.append({
                    'name': item,
                    'path': os.path.join(current_dir, item),
                    'python_files': python_files
                })
    
    return folders

def analyze_folder(folder_info):
    """Analyze a folder to find potential detection functions"""
    print(f"\n📁 Analyzing folder: {folder_info['name']}")
    print("=" * 50)
    
    potential_functions = []
    
    for py_file in folder_info['python_files']:
        rel_path = os.path.relpath(py_file, folder_info['path'])
        functions = scan_for_functions(py_file)
        
        if functions:
            print(f"\n📄 File: {rel_path}")
            for func_name, line_num in functions:
                print(f"   🔧 Function: {func_name} (line {line_num})")
                
                # Try to guess if this might be a detection function
                if any(keyword in func_name.lower() for keyword in 
                      ['detect', 'classify', 'predict', 'analyze', 'check', 'scan']):
                    potential_functions.append({
                        'file': rel_path,
                        'function': func_name,
                        'full_path': py_file
                    })
    
    if potential_functions:
        print(f"\n🎯 Potential detection functions found:")
        for i, func in enumerate(potential_functions, 1):
            print(f"   {i}. {func['function']} in {func['file']}")
    
    return potential_functions

def generate_wrapper_code(folder_name, file_name, function_name, detection_type):
    """Generate wrapper code for integration"""
    
    if detection_type == 'scam':
        template = f'''"""
Scam Detection Wrapper - Auto-generated
"""

import sys
import os

# Add your folder to Python path
folder_path = os.path.join(os.path.dirname(__file__), '..', '{folder_name}')
sys.path.append(folder_path)

try:
    from {file_name.replace('.py', '')} import {function_name}
    MODULE_LOADED = True
    print("✅ Scam detection module loaded successfully!")
except ImportError as e:
    print(f"⚠️ Could not import scam module: {{e}}")
    MODULE_LOADED = False

def detect_scam(content):
    """
    Wrapper function for your scam detection code
    """
    if not MODULE_LOADED:
        return fallback_detection(content, "scam")
    
    try:
        # Call your function
        result = {function_name}(content)
        
        # Convert your result to SafeGuard format
        # TODO: Modify this based on what your function actually returns
        
        if isinstance(result, dict):
            # If your function returns a dictionary
            is_scam = result.get('is_scam', False)
            score = result.get('score', 0.5)
            if score <= 1.0:
                score = int(score * 100)
            keywords = result.get('keywords', [])
            
        elif isinstance(result, (int, float)):
            # If your function returns a score
            if result <= 1.0:
                score = int(result * 100)
            else:
                score = int(result)
            is_scam = score > 50
            keywords = []
            
        elif isinstance(result, bool):
            # If your function returns True/False
            is_scam = result
            score = 80 if is_scam else 20
            keywords = []
            
        else:
            # Default handling
            is_scam = bool(result)
            score = 80 if is_scam else 20
            keywords = []
        
        return {{
            'is_scam': is_scam,
            'scam_score': min(max(score, 0), 100),
            'detected_keywords': keywords[:10],
            'message': f'Analysis complete. Risk score: {{score}}%',
            'risk_level': get_risk_level(score),
            'recommendations': get_recommendations(is_scam)
        }}
        
    except Exception as e:
        print(f"Error in scam detection: {{e}}")
        return fallback_detection(content, "scam")

def get_risk_level(score):
    if score >= 80: return "CRITICAL"
    elif score >= 60: return "HIGH"
    elif score >= 40: return "MEDIUM"
    else: return "LOW"

def get_recommendations(is_scam):
    if is_scam:
        return [
            "🚨 HIGH RISK: Do not respond to this message",
            "🚨 Do not click any links",
            "🚨 Report as spam/scam",
            "🚨 Do not provide personal information"
        ]
    else:
        return [
            "✅ Content appears safe",
            "✅ Still verify sender if unknown",
            "✅ Be cautious with requests"
        ]

def fallback_detection(content, type_):
    return {{
        'is_scam': False,
        'scam_score': 0,
        'detected_keywords': [],
        'message': 'Using fallback detection - please check your integration',
        'risk_level': 'LOW',
        'recommendations': ['⚠️ Detection module not properly loaded']
    }}
'''
    
    else:  # fake news
        template = f'''"""
Fake News Detection Wrapper - Auto-generated
"""

import sys
import os

# Add your folder to Python path
folder_path = os.path.join(os.path.dirname(__file__), '..', '{folder_name}')
sys.path.append(folder_path)

try:
    from {file_name.replace('.py', '')} import {function_name}
    MODULE_LOADED = True
    print("✅ Fake news detection module loaded successfully!")
except ImportError as e:
    print(f"⚠️ Could not import fake news module: {{e}}")
    MODULE_LOADED = False

def detect_fake_news(content):
    """
    Wrapper function for your fake news detection code
    """
    if not MODULE_LOADED:
        return fallback_detection(content, "news")
    
    try:
        # Call your function
        result = {function_name}(content)
        
        # Convert your result to SafeGuard format
        # TODO: Modify this based on what your function actually returns
        
        if isinstance(result, dict):
            # If your function returns a dictionary
            is_fake = result.get('is_fake', False)
            score = result.get('score', 0.5)
            if score <= 1.0:
                score = int(score * 100)
            indicators = result.get('indicators', [])
            
        elif isinstance(result, (int, float)):
            # If your function returns a score
            if result <= 1.0:
                score = int(result * 100)
            else:
                score = int(result)
            is_fake = score > 50
            indicators = []
            
        elif isinstance(result, bool):
            # If your function returns True/False
            is_fake = result
            score = 80 if is_fake else 20
            indicators = []
            
        else:
            # Default handling
            is_fake = bool(result)
            score = 80 if is_fake else 20
            indicators = []
        
        return {{
            'is_fake': is_fake,
            'fake_score': min(max(score, 0), 100),
            'detected_indicators': indicators[:10],
            'message': f'Analysis complete. Fake probability: {{score}}%',
            'credibility_level': get_credibility_level(score),
            'recommendations': get_recommendations(is_fake)
        }}
        
    except Exception as e:
        print(f"Error in fake news detection: {{e}}")
        return fallback_detection(content, "news")

def get_credibility_level(score):
    if score >= 80: return "HIGHLY UNRELIABLE"
    elif score >= 60: return "UNRELIABLE"
    elif score >= 40: return "QUESTIONABLE"
    elif score >= 20: return "MOSTLY RELIABLE"
    else: return "RELIABLE"

def get_recommendations(is_fake):
    if is_fake:
        return [
            "🚨 HIGH RISK: Verify with multiple sources",
            "🚨 Check fact-checking websites",
            "🚨 Look for original documentation",
            "🚨 Be cautious about sharing"
        ]
    else:
        return [
            "✅ Content appears credible",
            "✅ Still cross-reference sources",
            "✅ Check publication date"
        ]

def fallback_detection(content, type_):
    return {{
        'is_fake': False,
        'fake_score': 0,
        'detected_indicators': [],
        'message': 'Using fallback detection - please check your integration',
        'credibility_level': 'RELIABLE',
        'recommendations': ['⚠️ Detection module not properly loaded']
    }}
'''
    
    return template

def main():
    """Main setup function"""
    print("🛡️ SafeGuard Folder Setup Assistant")
    print("=" * 50)
    print("This tool will help you integrate your detection folders.\n")
    
    # Detect folders
    folders = detect_folders()
    
    if not folders:
        print("❌ No potential detection folders found in current directory.")
        print("Please make sure you've copied your folders into the safeguard_app directory.")
        return
    
    print(f"📁 Found {len(folders)} potential folder(s):")
    for i, folder in enumerate(folders, 1):
        print(f"   {i}. {folder['name']} ({len(folder['python_files'])} Python files)")
    
    # Analyze each folder
    scam_config = None
    news_config = None
    
    for folder in folders:
        potential_functions = analyze_folder(folder)
        
        if potential_functions:
            print(f"\n🎯 Configure {folder['name']} as:")
            print("   1. Scam Detection")
            print("   2. Fake News Detection")
            print("   3. Skip this folder")
            
            while True:
                try:
                    choice = input(f"\nEnter choice for {folder['name']} (1-3): ").strip()
                    if choice in ['1', '2', '3']:
                        break
                    print("Please enter 1, 2, or 3")
                except KeyboardInterrupt:
                    print("\nSetup cancelled.")
                    return
            
            if choice == '3':
                continue
            
            # Select function
            if len(potential_functions) == 1:
                selected_func = potential_functions[0]
                print(f"✅ Auto-selected: {selected_func['function']} in {selected_func['file']}")
            else:
                print(f"\nSelect the main detection function:")
                for i, func in enumerate(potential_functions, 1):
                    print(f"   {i}. {func['function']} in {func['file']}")
                
                while True:
                    try:
                        func_choice = int(input("Enter function number: ")) - 1
                        if 0 <= func_choice < len(potential_functions):
                            selected_func = potential_functions[func_choice]
                            break
                        print(f"Please enter a number between 1 and {len(potential_functions)}")
                    except (ValueError, KeyboardInterrupt):
                        print("Invalid input or setup cancelled.")
                        return
            
            # Store configuration
            config = {
                'folder_name': folder['name'],
                'file_name': selected_func['file'],
                'function_name': selected_func['function']
            }
            
            if choice == '1':
                scam_config = config
                print(f"✅ Configured {folder['name']} for scam detection")
            else:
                news_config = config
                print(f"✅ Configured {folder['name']} for fake news detection")
    
    # Generate wrapper files
    if scam_config:
        print(f"\n📝 Generating scam detection wrapper...")
        wrapper_code = generate_wrapper_code(
            scam_config['folder_name'],
            scam_config['file_name'],
            scam_config['function_name'],
            'scam'
        )
        
        with open('detection_modules/scam_detector.py', 'w') as f:
            f.write(wrapper_code)
        print("✅ Created detection_modules/scam_detector.py")
    
    if news_config:
        print(f"\n📝 Generating fake news detection wrapper...")
        wrapper_code = generate_wrapper_code(
            news_config['folder_name'],
            news_config['file_name'],
            news_config['function_name'],
            'news'
        )
        
        with open('detection_modules/fake_news_detector.py', 'w') as f:
            f.write(wrapper_code)
        print("✅ Created detection_modules/fake_news_detector.py")
    
    # Final instructions
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("=" * 50)
    
    if scam_config or news_config:
        print("\n📋 Next Steps:")
        print("1. Review and modify the generated wrapper files if needed")
        print("2. Add your dependencies to requirements.txt")
        print("3. Test the integration: python test_detection.py")
        print("4. Run the application: python app.py")
        print("5. Visit: http://localhost:5000")
        
        print("\n⚠️ Important Notes:")
        print("- The wrapper files contain TODO comments where you may need adjustments")
        print("- Check the result format conversion in the wrapper functions")
        print("- Make sure all your dependencies are installed")
    else:
        print("\n❌ No folders were configured.")
        print("Please run the setup again and select your detection folders.")

if __name__ == "__main__":
    main()