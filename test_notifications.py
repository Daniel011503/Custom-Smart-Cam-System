import sys
import os
sys.path.append('.')

# Import the notification system from SmartCam
from datetime import datetime
import requests

# Your Discord webhook
webhook_url = "https://discord.com/api/webhooks/1408115176577699930/Xmv5vL1mYbGoxwEN6U6NGodDspFPrvQHdSOaQvrp65pEGRhCxL6WgAbC1qelLnLGOeGM"

def send_test_alert():
    """Send a test security alert to Discord"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a realistic security alert
    embed_data = {
        "title": "🚨 Unknown Person Detected",
        "description": "SmartCam has detected an unknown person",
        "color": 0xff0000,  # Red color
        "timestamp": datetime.now().isoformat(),
        "fields": [
            {"name": "Time", "value": timestamp, "inline": True},
            {"name": "Confidence", "value": "65.2", "inline": True},
            {"name": "Location", "value": "Front Camera", "inline": True},
            {"name": "Action", "value": "Alarm Activated", "inline": False}
        ],
        "footer": {
            "text": "SmartCam Security System"
        }
    }
    
    payload = {
        "content": "🚨 **SECURITY ALERT** - Unknown person detected!",
        "embeds": [embed_data]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ Security alert sent to Discord!")
            return True
        else:
            print(f"❌ Failed to send alert: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error sending alert: {e}")
        return False

def send_alarm_alert():
    """Send an alarm activation alert"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    embed_data = {
        "title": "🔴 Alarm Activated",
        "description": "Security alarm has been activated",
        "color": 0xff0000,
        "timestamp": datetime.now().isoformat(),
        "fields": [
            {"name": "Time", "value": timestamp, "inline": True},
            {"name": "Status", "value": "ON", "inline": True},
            {"name": "Reason", "value": "Unknown person detected", "inline": False}
        ]
    }
    
    payload = {
        "content": "🔴 **Alarm Activated**",
        "embeds": [embed_data]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 204
    except:
        return False

if __name__ == "__main__":
    print("SmartCam Notification Test")
    print("=" * 30)
    
    print("1. Sending unknown person alert...")
    if send_test_alert():
        print("   ✅ Check your Discord channel!")
    
    print("\n2. Sending alarm activation alert...")
    if send_alarm_alert():
        print("   ✅ Check your Discord channel!")
    
    print("\nIf you received these notifications, your SmartCam is configured correctly!")
    print("During actual operation, you'll get notifications when unknown persons are detected.")
