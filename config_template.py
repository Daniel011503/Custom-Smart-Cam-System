# Configuration file for SmartCam notifications
# Copy this file to 'config.py' and fill in your actual credentials
# DO NOT commit config.py to git - it should be in .gitignore

NOTIFICATION_CONFIG = {
    "email": {
        "enabled": False,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "sender_email": "your_email@gmail.com",
        "sender_password": "your_16_character_app_password",
        "recipient_email": "recipient@gmail.com"
    },
    "webhook": {
        "enabled": False,
        "url": "https://your-webhook-url.com/notify",
        "headers": {"Content-Type": "application/json"}
    },
    "discord": {
        "enabled": False,
        "webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
    },
    "pushover": {
        "enabled": False,
        "user_key": "your_pushover_user_key",
        "api_token": "your_pushover_api_token"
    }
}
