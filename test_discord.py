import requests
import json

# Test Discord webhook
webhook_url = "https://discord.com/api/webhooks/1408115176577699930/Xmv5vL1mYbGoxwEN6U6NGodDspFPrvQHdSOaQvrp65pEGRhCxL6WgAbC1qelLnLGOeGM"

# Simple test message
payload = {
    "content": "🧪 **Test notification from SmartCam!**",
    "embeds": [{
        "title": "SmartCam Test",
        "description": "If you see this, Discord notifications are working correctly!",
        "color": 0x00ff00,
        "timestamp": "2025-08-21T11:45:00Z"
    }]
}

print("Testing Discord webhook...")
try:
    response = requests.post(webhook_url, json=payload, timeout=10)
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 204:
        print("✅ SUCCESS: Discord notification sent!")
    else:
        print(f"❌ FAILED: {response.text}")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
