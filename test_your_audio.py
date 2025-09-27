import requests
import json

def test_audio_file():
    """Test the audio file you added"""
    
    # Your audio file
    audio_file = "i-dont-care-where-i-go-movie-quote_78bpm_F_minor.wav"
    url = "http://127.0.0.1:5000/api/transcribe"
    
    print(f"🎵 Testing audio file: {audio_file}")
    print("=" * 60)
    
    try:
        # Send the audio file to your API
        with open(audio_file, 'rb') as f:
            files = {'file': (audio_file, f, 'audio/wav')}
            print("📤 Sending file to API...")
            response = requests.post(url, files=files)
        
        print(f"📊 Response Status: {response.status_code}")
        print("=" * 60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS! Here's what your API returned:")
            print("=" * 60)
            print(f"📝 TRANSCRIPT:")
            print(result.get('transcript', 'No transcript'))
            print("\n" + "=" * 60)
            print(f"📄 SUMMARY:")
            print(result.get('summary', 'No summary'))
            print("\n" + "=" * 60)
            print(f"✅ ACTION ITEMS:")
            print(result.get('action_items', 'No action items'))
            print("\n" + "=" * 60)
            print(f"🎯 DECISIONS:")
            print(result.get('decisions', 'No decisions'))
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_audio_file()
