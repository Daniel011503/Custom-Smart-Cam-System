# notification_setup.py - Configuration helper for SmartCam notifications
import json
import os

def create_notification_config():
    """Interactive setup for notification configuration"""
    print("=== SmartCam Notification Setup ===")
    print("This will help you configure remote notifications for your SmartCam system.\n")
    
    config = {
        "email": {"enabled": False},
        "webhook": {"enabled": False},
        "discord": {"enabled": False},
        "pushover": {"enabled": False}
    }
    
    # Email Configuration
    print("1. EMAIL NOTIFICATIONS")
    email_enabled = input("Enable email notifications? (y/n): ").lower() == 'y'
    
    if email_enabled:
        config["email"] = {
            "enabled": True,
            "smtp_server": input("SMTP server (default: smtp.gmail.com): ") or "smtp.gmail.com",
            "smtp_port": int(input("SMTP port (default: 587): ") or "587"),
            "sender_email": input("Your email address: "),
            "sender_password": input("Email password (use app password for Gmail): "),
            "recipient_email": input("Recipient email address: ")
        }
        print("✅ Email notifications configured")
    else:
        print("❌ Email notifications disabled")
    
    print()
    
    # Discord Configuration
    print("2. DISCORD NOTIFICATIONS")
    discord_enabled = input("Enable Discord notifications? (y/n): ").lower() == 'y'
    
    if discord_enabled:
        print("To set up Discord notifications:")
        print("1. Go to your Discord server")
        print("2. Go to Server Settings > Integrations > Webhooks")
        print("3. Create a new webhook and copy the URL")
        
        webhook_url = input("Discord webhook URL: ")
        config["discord"] = {
            "enabled": True,
            "webhook_url": webhook_url
        }
        print("✅ Discord notifications configured")
    else:
        print("❌ Discord notifications disabled")
    
    print()
    
    # Pushover Configuration
    print("3. PUSHOVER NOTIFICATIONS")
    pushover_enabled = input("Enable Pushover notifications? (y/n): ").lower() == 'y'
    
    if pushover_enabled:
        print("To set up Pushover notifications:")
        print("1. Create account at https://pushover.net")
        print("2. Create an application to get API token")
        print("3. Get your user key from the dashboard")
        
        user_key = input("Pushover user key: ")
        api_token = input("Pushover API token: ")
        config["pushover"] = {
            "enabled": True,
            "user_key": user_key,
            "api_token": api_token
        }
        print("✅ Pushover notifications configured")
    else:
        print("❌ Pushover notifications disabled")
    
    print()
    
    # Webhook Configuration
    print("4. CUSTOM WEBHOOK")
    webhook_enabled = input("Enable custom webhook notifications? (y/n): ").lower() == 'y'
    
    if webhook_enabled:
        webhook_url = input("Webhook URL: ")
        config["webhook"] = {
            "enabled": True,
            "url": webhook_url,
            "headers": {"Content-Type": "application/json"}
        }
        print("✅ Custom webhook configured")
    else:
        print("❌ Custom webhook disabled")
    
    # Save configuration
    config_file = "notification_config.json"
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to {config_file}")
    print("\nTo use this configuration:")
    print("1. Edit SmartCam.py")
    print("2. Replace NOTIFICATION_CONFIG with:")
    print(f"   NOTIFICATION_CONFIG = json.load(open('{config_file}'))")
    print("\nOr copy the configuration manually from the generated file.")
    
    return config

def test_notifications(config_file="notification_config.json"):
    """Test notification setup"""
    if not os.path.exists(config_file):
        print(f"Configuration file {config_file} not found!")
        print("Run create_notification_config() first.")
        return
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Import the NotificationManager from SmartCam
    import sys
    sys.path.append('.')
    
    # Create a minimal test notification manager
    class TestNotificationManager:
        def __init__(self, config):
            self.config = config
        
        def send_test_email(self):
            if not self.config["email"]["enabled"]:
                return False
            
            try:
                import smtplib
                from email.mime.text import MIMEText
                
                msg = MIMEText("This is a test notification from SmartCam setup.")
                msg['Subject'] = "SmartCam Test Notification"
                msg['From'] = self.config["email"]["sender_email"]
                msg['To'] = self.config["email"]["recipient_email"]
                
                server = smtplib.SMTP(self.config["email"]["smtp_server"], self.config["email"]["smtp_port"])
                server.starttls()
                server.login(self.config["email"]["sender_email"], self.config["email"]["sender_password"])
                server.send_message(msg)
                server.quit()
                return True
            except Exception as e:
                print(f"Email test failed: {e}")
                return False
        
        def send_test_discord(self):
            if not self.config["discord"]["enabled"]:
                return False
            
            try:
                import requests
                payload = {
                    "content": "🧪 **Test notification from SmartCam setup!**",
                    "embeds": [{
                        "title": "SmartCam Test",
                        "description": "If you see this, Discord notifications are working correctly!",
                        "color": 0x00ff00
                    }]
                }
                response = requests.post(self.config["discord"]["webhook_url"], json=payload, timeout=10)
                return response.status_code == 204
            except Exception as e:
                print(f"Discord test failed: {e}")
                return False
        
        def send_test_pushover(self):
            if not self.config["pushover"]["enabled"]:
                return False
            
            try:
                import requests
                data = {
                    "token": self.config["pushover"]["api_token"],
                    "user": self.config["pushover"]["user_key"],
                    "message": "Test notification from SmartCam setup!",
                    "title": "SmartCam Test"
                }
                response = requests.post("https://api.pushover.net/1/messages.json", data=data, timeout=10)
                return response.status_code == 200
            except Exception as e:
                print(f"Pushover test failed: {e}")
                return False
    
    # Test notifications
    tester = TestNotificationManager(config)
    
    print("Testing notification configurations...\n")
    
    if config["email"]["enabled"]:
        print("Testing email... ", end="")
        if tester.send_test_email():
            print("✅ SUCCESS")
        else:
            print("❌ FAILED")
    
    if config["discord"]["enabled"]:
        print("Testing Discord... ", end="")
        if tester.send_test_discord():
            print("✅ SUCCESS")
        else:
            print("❌ FAILED")
    
    if config["pushover"]["enabled"]:
        print("Testing Pushover... ", end="")
        if tester.send_test_pushover():
            print("✅ SUCCESS")
        else:
            print("❌ FAILED")
    
    print("\nTest completed!")

if __name__ == "__main__":
    print("SmartCam Notification Setup")
    print("1. Create configuration")
    print("2. Test existing configuration")
    
    choice = input("Choose option (1 or 2): ")
    
    if choice == "1":
        create_notification_config()
    elif choice == "2":
        test_notifications()
    else:
        print("Invalid choice. Run the script again.")
