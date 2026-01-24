import os
import sys

print("Python version:", sys.version)
print("\nCurrent working directory:", os.getcwd())
print("\nContents of current directory:")
for item in os.listdir('.'):
    print(f"  - {item}")

if os.path.exists("main.py"):
    print("\nmain.py exists!")
else:
    print("\nmain.py NOT found!")
    

print("\nLooking for modules directory:")
if os.path.exists("modules"):
    print("modules directory exists!")
    print("Contents of modules:")
    for item in os.listdir('modules'):
        print(f"  - {item}")
else:
    print("modules directory NOT found!")

print("\nEnvironment check:")
try:
    import speech_recognition
    print("[OK] speech_recognition installed")
except ImportError:
    print("[FAIL] speech_recognition NOT installed")
    
try:
    import openai
    print("[OK] openai installed")
except ImportError:
    print("[FAIL] openai NOT installed")
    
try:
    import pyttsx3
    print("[OK] pyttsx3 installed")
except ImportError:
    print("[FAIL] pyttsx3 NOT installed")
    
try:
    import pyaudio
    print("[OK] pyaudio installed")
except ImportError:
    print("[FAIL] pyaudio NOT installed")

print("\nChecking .env file:")
if os.path.exists(".env"):
    print(".env file exists")
    try:
        with open(".env", "r") as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                print("OPENAI_API_KEY found in .env")
            else:
                print("WARNING: OPENAI_API_KEY not found in .env")
    except:
        print("Could not read .env file")
else:
    print(".env file NOT found!")