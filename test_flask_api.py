import requests
import os

def test_api_with_audio():
    """Test the Flask API with an audio file"""
    
    # API endpoint
    url = "http://127.0.0.1:5000/api/transcribe"
    
    # Check if you have an audio file to test with
    audio_files = []
    for ext in ['.wav', '.mp3', '.m4a', '.mp4']:
        for file in os.listdir('.'):
            if file.endswith(ext):
                audio_files.append(file)
    
    if not audio_files:
        print("❌ No audio files found in current directory")
        print("📁 Please add an audio file (.wav, .mp3, .m4a, .mp4) to test with")
        return False
    
    # Use the first audio file found
    audio_file = audio_files[0]
    print(f"🎵 Testing with audio file: {audio_file}")
    
    try:
        # Send POST request with audio file
        with open(audio_file, 'rb') as f:
            files = {'file': (audio_file, f, 'audio/wav')}
            response = requests.post(url, files=files)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! API Response:")
            print("=" * 50)
            print(f"📝 Transcript: {result.get('transcript', 'N/A')}")
            print(f"📄 Summary: {result.get('summary', 'N/A')}")
            print(f"✅ Action Items: {result.get('action_items', 'N/A')}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
        return False

def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get("http://127.0.0.1:5000/")
        if response.status_code == 200:
            print(f"✅ Health check: {response.text}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to Flask app: {str(e)}")
        print("Make sure your Flask app is running with: .\\venv\\Scripts\\python.exe app.py")
        return False

if __name__ == "__main__":
    print("🧪 Testing Flask Audio Transcription API")
    print("=" * 50)
    
    # Test 1: Health check
    print("1️⃣ Testing health endpoint...")
    health_ok = test_health_endpoint()
    
    if not health_ok:
        print("\n❌ Flask app is not running. Please start it first:")
        print("   .\\venv\\Scripts\\python.exe app.py")
        exit(1)
    
    print("\n" + "=" * 50)
    
    # Test 2: Audio transcription
    print("2️⃣ Testing audio transcription...")
    test_api_with_audio()
