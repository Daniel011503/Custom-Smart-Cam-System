# SmartCam Notification Setup Guide
# =====================================

"""
COMPLETE GUIDE TO SETTING UP SMARTCAM NOTIFICATIONS
===================================================

This guide explains how to get all the required credentials for each notification method.

1. EMAIL NOTIFICATIONS (SMTP)
=============================

For Gmail (Recommended):
- smtp_server: "smtp.gmail.com"
- smtp_port: 587
- sender_email: "youremail@gmail.com"
- sender_password: "YOUR_APP_PASSWORD" (NOT your regular password!)
- recipient_email: "recipient@gmail.com"

HOW TO GET GMAIL APP PASSWORD:
1. Go to https://myaccount.google.com/
2. Click "Security" on the left
3. Under "How you sign in to Google", click "2-Step Verification"
4. Enable 2-Step Verification if not already enabled
5. Go back to Security settings
6. Click "App passwords" 
7. Select "Mail" and your device
8. Google will generate a 16-character password like "abcd efgh ijkl mnop"
9. Use this password in the configuration (remove spaces)

For Other Email Providers:
- Outlook/Hotmail: smtp-mail.outlook.com, port 587
- Yahoo: smtp.mail.yahoo.com, port 587
- Custom: Check your email provider's SMTP settings

2. DISCORD NOTIFICATIONS
========================

What you need:
- webhook_url: "https://discord.com/api/webhooks/123456789/abcdefghijklmnopqrstuvwxyz"

HOW TO GET DISCORD WEBHOOK:
1. Open Discord and go to your server
2. Right-click on the channel where you want notifications
3. Click "Edit Channel"
4. Go to "Integrations" tab
5. Click "Create Webhook"
6. Give it a name like "SmartCam"
7. Copy the "Webhook URL"
8. The URL should look like: https://discord.com/api/webhooks/[NUMBERS]/[LONG_STRING]

3. PUSHOVER NOTIFICATIONS (Mobile Push)
=======================================

What you need:
- user_key: "u2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7"
- api_token: "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"

HOW TO GET PUSHOVER CREDENTIALS:
1. Go to https://pushover.net/
2. Create a free account (30-day trial, then $5 one-time fee)
3. After logging in, your USER KEY is displayed on the main page
4. To get API TOKEN:
   - Click "Create an Application/API Token"
   - Name: "SmartCam"
   - Description: "Security camera notifications"
   - URL: (leave blank)
   - Icon: (optional)
   - Click "Create Application"
   - Copy the API Token/Key

5. Install Pushover app on your phone and login with same account

4. CUSTOM WEBHOOK
=================

What you need:
- url: "https://yourserver.com/webhook"
- headers: {"Content-Type": "application/json", "Authorization": "Bearer your_token"}

This is for advanced users who want to send notifications to their own server.
The webhook will receive JSON data with event details.

5. TESTING YOUR SETUP
=====================

Use the notification_setup.py script to test your configuration:

```bash
python notification_setup.py
```

Choose option 1 to create configuration, then option 2 to test it.

6. EXAMPLE CONFIGURATION
========================

Here's what your NOTIFICATION_CONFIG should look like with real values:

NOTIFICATION_CONFIG = {
    "email": {
        "enabled": True,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "mycamera@gmail.com",
        "sender_password": "abcdefghijklmnop",  # 16-char app password
        "recipient_email": "myphone@gmail.com"
    },
    "discord": {
        "enabled": True,
        "webhook_url": "https://discord.com/api/webhooks/123456789012345678/AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIjKlMnOpQrStUvWxYz"
    },
    "pushover": {
        "enabled": True,
        "user_key": "u2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7",
        "api_token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
    },
    "webhook": {
        "enabled": False,  # Only enable if you have your own server
        "url": "https://yourserver.com/smartcam/webhook",
        "headers": {"Content-Type": "application/json"}
    }
}

7. SECURITY TIPS
================

- Never share your app passwords or API tokens
- Use dedicated email accounts for notifications if possible
- Test notifications before relying on them for security
- Keep credentials in a separate config file if sharing code
- Consider using environment variables for sensitive data

8. TROUBLESHOOTING
==================

Common Issues:

EMAIL ERRORS:
- "Authentication failed" → Use app password, not regular password
- "SMTP connect failed" → Check smtp_server and smtp_port
- "Recipient rejected" → Verify recipient email address

DISCORD ERRORS:
- "404 Not Found" → Webhook URL is incorrect
- "401 Unauthorized" → Webhook was deleted or expired

PUSHOVER ERRORS:
- "Invalid user key" → Check user_key from Pushover dashboard
- "Invalid token" → Check api_token from your application

GENERAL:
- Check internet connection
- Verify all credentials are correct
- Look at terminal output for specific error messages
"""

# Quick setup function
def quick_setup():
    print("SMARTCAM NOTIFICATION QUICK SETUP")
    print("=" * 40)
    
    print("\n1. EMAIL SETUP:")
    print("   • Go to https://myaccount.google.com/security")
    print("   • Enable 2-Step Verification")
    print("   • Create App Password for Mail")
    print("   • Use the 16-character password (no spaces)")
    
    print("\n2. DISCORD SETUP:")
    print("   • Right-click your Discord channel")
    print("   • Edit Channel → Integrations → Create Webhook")
    print("   • Copy the webhook URL")
    
    print("\n3. PUSHOVER SETUP:")
    print("   • Go to https://pushover.net/")
    print("   • Create account and note your User Key")
    print("   • Create Application for API Token")
    print("   • Install Pushover app on phone")
    
    print("\n4. EDIT SmartCam.py:")
    print("   • Find NOTIFICATION_CONFIG section")
    print("   • Set enabled: True for services you want")
    print("   • Add your credentials")
    
    print("\n5. TEST:")
    print("   • Run: python notification_setup.py")
    print("   • Choose option 2 to test configuration")

if __name__ == "__main__":
    quick_setup()
