"""
Test script to verify both servers can start and communicate
"""
import subprocess
import requests
import time
import sys
import os

def test_django_server():
    """Test if Django server is running"""
    try:
        response = requests.get('http://localhost:8000/admin/', timeout=3)
        print("✅ Django Server: CONNECTED (HTTP 200)")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Django Server: NOT RUNNING")
        return False
    except Exception as e:
        print(f"⚠️  Django Server: {str(e)}")
        return False

def test_rasa_server():
    """Test if RASA actions server is running"""
    try:
        response = requests.post(
            'http://localhost:5005/webhook',
            json={'action': 'action_listen'},
            timeout=3
        )
        print("✅ RASA Server: CONNECTED")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ RASA Server: NOT RUNNING")
        return False
    except Exception as e:
        print(f"⚠️  RASA Server: {str(e)}")
        return False

def main():
    print("\n" + "=" * 60)
    print("  SERVER CONNECTIVITY TEST")
    print("=" * 60 + "\n")
    
    print("⏳ Waiting 5 seconds for servers to initialize...")
    time.sleep(5)
    
    print("\n📊 Testing connections...\n")
    
    django_ok = test_django_server()
    rasa_ok = test_rasa_server()
    
    print("\n" + "=" * 60)
    if django_ok and rasa_ok:
        print("✨ All servers are running and communicating!")
        print("\n📍 Access points:")
        print("   🌐 Main Portal: http://localhost:8000")
        print("   🤖 RASA API: http://localhost:5005")
        print("   🔧 Admin Panel: http://localhost:8000/admin")
    elif django_ok:
        print("⚠️  Django is running but RASA is not responding")
        print("   Make sure RASA actions server started successfully")
    elif rasa_ok:
        print("⚠️  RASA is running but Django is not responding")
        print("   Make sure Django server started successfully")
    else:
        print("❌ Neither server is responding")
        print("   Make sure both servers are running")
    
    print("=" * 60 + "\n")

if __name__ == '__main__':
    # Try to import requests, if not available, inform user
    try:
        import requests
    except ImportError:
        print("\n⚠️  'requests' module not found!")
        print("   Install it with: pip install requests")
        sys.exit(1)
    
    main()
