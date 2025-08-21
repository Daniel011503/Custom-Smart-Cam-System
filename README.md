# Smart Camera Security System

A comprehensive AI-powered security camera system with face recognition, motion detection, remote notifications, and data logging capabilities.

## 🚀 Features

### 🎯 Core Functionality
- **Face Recognition**: LBPH (Local Binary Pattern Histogram) algorithm for person identification
- **Motion Detection**: Background subtraction for motion analysis
- **Real-time Monitoring**: Live video feed with overlay information
- **Arduino Integration**: Hardware alarm system with LED and buzzer

### 📊 Data Logging & Analysis
- **CSV Logging**: Structured data logging for all events
- **Session Tracking**: JSON-based session data with statistics
- **Analysis Tools**: Comprehensive data analysis with visualizations
- **Performance Metrics**: Detection rates, confidence scores, and timing analysis

### 🚨 Remote Notifications
- **Discord Integration**: Rich embedded notifications with real-time alerts
- **Email Notifications**: SMTP-based email alerts with image attachments
- **Pushover Support**: Mobile push notifications
- **Custom Webhooks**: Integration with custom APIs and services

### 🔒 Security Features
- **Unknown Person Detection**: Automatic alerts for unrecognized individuals
- **Alarm System**: Arduino-controlled LED and buzzer alerts
- **Image Snapshots**: Automatic capture of security events
- **Configurable Thresholds**: Adjustable confidence and motion sensitivity

## 📁 Project Structure

```
Smart-Camera-System/
├── SmartCam.py                 # Main application
├── train.py                    # Face recognition training
├── analyze_logs.py             # Data analysis tool
├── notification_setup.py       # Notification configuration helper
├── notification_guide.py       # Setup instructions
├── config_template.py          # Configuration template
├── Smart_Camera_Arduino/       # Arduino code
│   └── Smart_Camera_Arduino.ino
├── models/                     # Trained models (created after training)
├── logs/                       # Data logs (created during operation)
├── snapshots/                  # Security images (created during operation)
└── training_data/              # Create this folder and add face training images
    └── person_name/            # Create folders for each person
        ├── image1.jpg
        ├── image2.jpg
        └── ...
```

## 🛠 Hardware Requirements

### Arduino Components
- Arduino Uno/Nano
- LED (any color)
- Passive buzzer
- Push button
- Resistors (220Ω for LED, 10kΩ for button)
- Breadboard and jumper wires

### Computer Requirements
- Webcam/Camera
- Python 3.11+ (recommended)
- Windows/macOS/Linux

## 📋 Installation

### 1. Clone Repository
```bash
git clone https://github.com/Daniel011503/Custom-Smart-Cam-System.git
cd Custom-Smart-Cam-System
```

### 2. Install Python Dependencies
```bash
pip install opencv-python opencv-contrib-python pyserial requests
```

Optional for data analysis:
```bash
pip install matplotlib
```

### 3. Arduino Setup
1. Open `Smart_Camera_Arduino/Smart_Camera_Arduino.ino` in Arduino IDE
2. Connect your Arduino with the circuit diagram below
3. Upload the code to your Arduino

### 4. Configuration Setup
```bash
# Copy the template and add your credentials
cp config_template.py config.py

# Edit config.py with your notification settings
# Never commit config.py to git!
```

## 🔌 Circuit Diagram

```
Arduino Uno:
- LED: Pin 7 → 220Ω resistor → LED → GND
- Buzzer: Pin 8 → Passive Buzzer → GND
- Button: Pin 2 → Button → GND (using internal pullup)
- Power: 5V and GND connections
```

## 🚀 Quick Start

### 1. Prepare Training Data
```bash
# Create training folders
mkdir -p training_data/person_name
# Add 10-20 photos of each person to their folder
# Example: training_data/john/photo1.jpg, training_data/jane/photo1.jpg, etc.
```

### 2. Train the Model
```bash
python train.py
```

### 3. Set Up Notifications (Optional)
```bash
python notification_setup.py
```

### 4. Run the System
```bash
python SmartCam.py
```

## 📱 Notification Setup

### Discord (Recommended - Free)
1. Create a Discord server or use existing one
2. Right-click channel → Edit Channel → Integrations → Create Webhook
3. Copy webhook URL to `config.py`

### Email (Gmail)
1. Enable 2-Step Verification in Google Account
2. Generate App Password: Security → App Passwords → Mail
3. Use 16-character app password in `config.py`

### Pushover (Mobile)
1. Create account at https://pushover.net
2. Create application for API token
3. Install Pushover app on phone
4. Add credentials to `config.py`

## 📊 Data Analysis

View detailed analytics of your security system:

```bash
python analyze_logs.py
```

Features:
- Detection patterns by hour
- Confidence score distributions
- Motion analysis
- Alarm frequency and duration
- Automatic report generation
- Visual charts and graphs

## 🔧 Configuration

### Motion Sensitivity
Adjust motion threshold in `SmartCam.py`:
```python
if m > 6000:  # Increase for less sensitivity
```

### Face Recognition Confidence
Adjust confidence threshold:
```python
label = labels[pred] if conf < 70 else "unknown"  # Lower = stricter
```

### Serial Port
Update Arduino connection:
```python
PORT = "COM3"  # Windows: COM3, COM4, etc.
               # Linux/Mac: /dev/ttyUSB0, /dev/ttyACM0
```

## 🏗 Arduino Commands

The Arduino accepts these serial commands:
- `<ARM:1>` / `<ARM:0>` - Arm/disarm system
- `<ALARM:ON>` / `<ALARM:OFF>` - Control alarm
- `<STATUS>` - Get current state

## 🔍 Troubleshooting

### Common Issues

**Camera not detected:**
```python
cap = cv2.VideoCapture(1)  # Try different camera indices
```

**Serial connection failed:**
- Check Arduino is connected
- Verify correct COM port
- Ensure Arduino IDE Serial Monitor is closed

**Face recognition not working:**
- Train with more diverse images
- Ensure good lighting conditions
- Check image quality and resolution

**Notifications not sending:**
- Verify internet connection
- Check credentials in `config.py`
- Test with `notification_setup.py`

## 📈 Performance Tips

- Use at least 10-20 training images per person
- Ensure varied lighting and angles in training data
- Restart system if performance degrades over time
- Monitor log files for debugging information

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Arduino community for hardware integration
- Contributors and testers

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review configuration guides

---

**⚠️ Security Note**: Never commit `config.py` or any files containing API keys, passwords, or webhook URLs to public repositories.
