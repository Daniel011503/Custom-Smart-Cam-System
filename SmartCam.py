# smartcam.py
import cv2, serial, time, os, json, csv, smtplib, requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import threading
PORT="COM3"; BAUD=115200   # change port if needed

# Import notification configuration from secure config file
try:
    from config import NOTIFICATION_CONFIG
    print("✅ Loaded configuration from config.py")
except ImportError:
    print("⚠️  config.py not found - using default configuration")
    print("   Copy config_template.py to config.py and add your credentials")
    # Default configuration with no real credentials
    NOTIFICATION_CONFIG = {
        "email": {"enabled": False, "smtp_server": "smtp.gmail.com", "smtp_port": 587, "sender_email": "", "sender_password": "", "recipient_email": ""},
        "webhook": {"enabled": False, "url": "", "headers": {"Content-Type": "application/json"}},
        "discord": {"enabled": False, "webhook_url": ""},
        "pushover": {"enabled": False, "user_key": "", "api_token": ""}
    }
face=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
rec=cv2.face.LBPHFaceRecognizer_create(); rec.read("models/lbph.yml")
labels=open("models/labels.txt").read().splitlines()
cap=cv2.VideoCapture(0)

class NotificationManager:
    def __init__(self, config):
        self.config = config
        self.last_notification_time = {}
        self.notification_cooldown = 30  # seconds between notifications
        
    def should_send_notification(self, event_type):
        """Check if enough time has passed since last notification of this type"""
        now = time.time()
        if event_type in self.last_notification_time:
            if now - self.last_notification_time[event_type] < self.notification_cooldown:
                return False
        self.last_notification_time[event_type] = now
        return True
    
    def send_email(self, subject, body, image_path=None):
        """Send email notification"""
        if not self.config["email"]["enabled"]:
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config["email"]["sender_email"]
            msg['To'] = self.config["email"]["recipient_email"]
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach image if provided
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                    image = MIMEImage(img_data)
                    image.add_header('Content-Disposition', 'attachment', filename='detection.jpg')
                    msg.attach(image)
            
            server = smtplib.SMTP(self.config["email"]["smtp_server"], self.config["email"]["smtp_port"])
            server.starttls()
            server.login(self.config["email"]["sender_email"], self.config["email"]["sender_password"])
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Email notification failed: {e}")
            return False
    
    def send_webhook(self, event_type, data):
        """Send webhook notification"""
        if not self.config["webhook"]["enabled"]:
            return False
            
        try:
            payload = {
                "event_type": event_type,
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            response = requests.post(
                self.config["webhook"]["url"],
                json=payload,
                headers=self.config["webhook"]["headers"],
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Webhook notification failed: {e}")
            return False
    
    def send_discord(self, message, embed_data=None):
        """Send Discord notification"""
        if not self.config["discord"]["enabled"]:
            return False
            
        try:
            payload = {"content": message}
            
            if embed_data:
                payload["embeds"] = [{
                    "title": embed_data.get("title", "SmartCam Alert"),
                    "description": embed_data.get("description", ""),
                    "color": embed_data.get("color", 0xff0000),  # Red color
                    "timestamp": datetime.now().isoformat(),
                    "fields": embed_data.get("fields", [])
                }]
            
            response = requests.post(self.config["discord"]["webhook_url"], json=payload, timeout=10)
            return response.status_code == 204
        except Exception as e:
            print(f"Discord notification failed: {e}")
            return False
    
    def send_pushover(self, message, title="SmartCam Alert", priority=0):
        """Send Pushover notification"""
        if not self.config["pushover"]["enabled"]:
            return False
            
        try:
            data = {
                "token": self.config["pushover"]["api_token"],
                "user": self.config["pushover"]["user_key"],
                "message": message,
                "title": title,
                "priority": priority
            }
            
            response = requests.post("https://api.pushover.net/1/messages.json", data=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Pushover notification failed: {e}")
            return False
    
    def notify_unknown_person(self, confidence, image_path=None):
        """Send notification for unknown person detection"""
        if not self.should_send_notification("unknown_person"):
            return
            
        # Run notifications in separate thread to avoid blocking
        threading.Thread(target=self._send_unknown_person_notifications, 
                        args=(confidence, image_path), daemon=True).start()
    
    def _send_unknown_person_notifications(self, confidence, image_path):
        """Internal method to send all unknown person notifications"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Email notification
        if self.config["email"]["enabled"]:
            subject = "🚨 SmartCam: Unknown Person Detected"
            body = f"""
SECURITY ALERT: Unknown person detected by SmartCam

Time: {timestamp}
Confidence Score: {confidence:.1f}
Location: Front Camera

This is an automated security notification from your SmartCam system.
Please check the attached image and verify if this person is authorized.

Best regards,
SmartCam Security System
            """
            self.send_email(subject, body, image_path)
        
        # Discord notification
        if self.config["discord"]["enabled"]:
            embed_data = {
                "title": "🚨 Unknown Person Detected",
                "description": "SmartCam has detected an unknown person",
                "color": 0xff0000,  # Red
                "fields": [
                    {"name": "Time", "value": timestamp, "inline": True},
                    {"name": "Confidence", "value": f"{confidence:.1f}", "inline": True},
                    {"name": "Location", "value": "Front Camera", "inline": True}
                ]
            }
            self.send_discord("🚨 **SECURITY ALERT** - Unknown person detected!", embed_data)
        
        # Webhook notification
        if self.config["webhook"]["enabled"]:
            data = {
                "confidence": confidence,
                "location": "front_camera",
                "image_path": image_path
            }
            self.send_webhook("unknown_person", data)
        
        # Pushover notification
        if self.config["pushover"]["enabled"]:
            message = f"Unknown person detected at {timestamp} (confidence: {confidence:.1f})"
            self.send_pushover(message, priority=1)  # High priority
    
    def notify_alarm_state(self, state, reason=""):
        """Send notification for alarm state changes"""
        if not self.should_send_notification(f"alarm_{state.lower()}"):
            return
            
        threading.Thread(target=self._send_alarm_notifications, 
                        args=(state, reason), daemon=True).start()
    
    def _send_alarm_notifications(self, state, reason):
        """Internal method to send alarm state notifications"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emoji = "🔴" if state == "ON" else "🟢"
        
        # Email notification
        if self.config["email"]["enabled"]:
            subject = f"{emoji} SmartCam: Alarm {state}"
            body = f"""
SmartCam Security System Alert

Alarm Status: {state}
Time: {timestamp}
{f'Reason: {reason}' if reason else ''}

Your security system alarm has been {'activated' if state == 'ON' else 'deactivated'}.

Best regards,
SmartCam Security System
            """
            self.send_email(subject, body)
        
        # Discord notification
        if self.config["discord"]["enabled"]:
            color = 0xff0000 if state == "ON" else 0x00ff00
            embed_data = {
                "title": f"{emoji} Alarm {state}",
                "description": f"Security alarm has been {'activated' if state == 'ON' else 'deactivated'}",
                "color": color,
                "fields": [
                    {"name": "Time", "value": timestamp, "inline": True},
                    {"name": "Status", "value": state, "inline": True}
                ]
            }
            if reason:
                embed_data["fields"].append({"name": "Reason", "value": reason, "inline": False})
            
            self.send_discord(f"{emoji} **Alarm {state}**", embed_data)
        
        # Pushover notification
        if self.config["pushover"]["enabled"]:
            priority = 1 if state == "ON" else 0
            message = f"Security alarm {state} at {timestamp}"
            if reason:
                message += f" - {reason}"
            self.send_pushover(message, priority=priority)

class DataLogger:
    def __init__(self):
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # CSV file for structured data
        self.csv_file = os.path.join(self.log_dir, f"smartcam_log_{datetime.now().strftime('%Y%m%d')}.csv")
        self.init_csv()
        
        # JSON file for session data
        self.session_file = os.path.join(self.log_dir, f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        self.session_data = {
            "start_time": datetime.now().isoformat(),
            "detections": [],
            "motion_events": [],
            "alarm_events": []
        }
        
        # Statistics
        self.stats = {
            "total_frames": 0,
            "motion_frames": 0,
            "face_detections": 0,
            "unknown_detections": 0,
            "known_detections": 0,
            "alarm_triggers": 0
        }
    
    def init_csv(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'event_type', 'label', 'confidence', 'motion_score', 'alarm_state'])
    
    def log_event(self, event_type, label="none", confidence=0, motion_score=0, alarm_state=False):
        timestamp = datetime.now().isoformat()
        
        # Convert numpy types to Python types for JSON serialization
        motion_score = int(motion_score) if motion_score else 0
        confidence = float(confidence) if confidence else 0.0
        
        # Log to CSV
        with open(self.csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, event_type, label, confidence, motion_score, alarm_state])
        
        # Log to session data
        event_data = {
            "timestamp": timestamp,
            "event_type": event_type,
            "label": label,
            "confidence": confidence,
            "motion_score": motion_score,
            "alarm_state": alarm_state
        }
        
        if event_type == "face_detection":
            self.session_data["detections"].append(event_data)
        elif event_type == "motion":
            self.session_data["motion_events"].append(event_data)
        elif event_type == "alarm":
            self.session_data["alarm_events"].append(event_data)
        
        # Update statistics
        self.update_stats(event_type, label)
    
    def update_stats(self, event_type, label):
        self.stats["total_frames"] += 1
        
        if event_type == "motion":
            self.stats["motion_frames"] += 1
        elif event_type == "face_detection":
            self.stats["face_detections"] += 1
            if label == "unknown":
                self.stats["unknown_detections"] += 1
            elif label != "none":
                self.stats["known_detections"] += 1
        elif event_type == "alarm" and label == "ON":
            self.stats["alarm_triggers"] += 1
    
    def save_session(self):
        self.session_data["end_time"] = datetime.now().isoformat()
        self.session_data["statistics"] = self.stats
        
        with open(self.session_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)
    
    def print_stats(self):
        print("\n=== SESSION STATISTICS ===")
        print(f"Total frames processed: {self.stats['total_frames']}")
        print(f"Frames with motion: {self.stats['motion_frames']}")
        print(f"Face detections: {self.stats['face_detections']}")
        print(f"Known person detections: {self.stats['known_detections']}")
        print(f"Unknown person detections: {self.stats['unknown_detections']}")
        print(f"Alarm triggers: {self.stats['alarm_triggers']}")
        if self.stats['total_frames'] > 0:
            print(f"Motion percentage: {(self.stats['motion_frames']/self.stats['total_frames']*100):.1f}%")

class Gate:
    def __init__(s): s.bg=None
    def score(s,gray):
        if s.bg is None: s.bg=gray.astype("float"); return 0
        cv2.accumulateWeighted(gray,s.bg,0.02)
        delta=cv2.absdiff(gray,cv2.convertScaleAbs(s.bg))
        _,mask=cv2.threshold(delta,25,255,cv2.THRESH_BINARY)
        return mask.sum()

gate=Gate()
logger=DataLogger()
notifier=NotificationManager(NOTIFICATION_CONFIG)

# Create snapshots directory for notification images
snapshots_dir = "snapshots"
if not os.path.exists(snapshots_dir):
    os.makedirs(snapshots_dir)

with serial.Serial(PORT, BAUD, timeout=1) as ser:
    time.sleep(2)
    ser.write(b"<ARM:1>\n"); ser.readline(); ser.readline()  # ACK + STATE
    on=False; miss=0
    print("SmartCam started - Press 'q' to quit")
    print("Data logging enabled - files will be saved in 'logs' directory")
    
    # Check which notification methods are enabled
    enabled_notifications = [k for k, v in NOTIFICATION_CONFIG.items() if v.get("enabled", False)]
    if enabled_notifications:
        print(f"Remote notifications enabled: {', '.join(enabled_notifications)}")
    else:
        print("Remote notifications disabled - edit NOTIFICATION_CONFIG to enable")
    
    try:
        while True:
            ok,frame=cap.read()
            if not ok: break
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            m=gate.score(gray)
            cv2.putText(frame,f"motion:{m}",(10,25),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

            label="none"
            confidence=0
            
            # Log motion events
            if m>6000:
                logger.log_event("motion", motion_score=m, alarm_state=on)
                
                faces=face.detectMultiScale(gray,1.2,5,minSize=(80,80))
                if len(faces):
                    x,y,w,h=max(faces,key=lambda r:r[2]*r[3])
                    roi=cv2.resize(gray[y:y+h,x:x+w],(200,200))
                    pred,conf=rec.predict(roi)
                    confidence=conf
                    label = labels[pred] if conf<70 else "unknown"
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    cv2.putText(frame,f"{label} {conf:.0f}",(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,0),2)
                    
                    # Log face detection
                    logger.log_event("face_detection", label=label, confidence=confidence, motion_score=m, alarm_state=on)
                    
                    # Save snapshot and send notification for unknown persons
                    if label == "unknown":
                        snapshot_path = os.path.join(snapshots_dir, f"unknown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                        cv2.imwrite(snapshot_path, frame)
                        notifier.notify_unknown_person(confidence, snapshot_path)

            if label=="unknown" and not on:
                ser.write(b"<ALARM:ON>\n"); ser.readline(); ser.readline(); on=True; miss=0
                logger.log_event("alarm", label="ON", motion_score=m, alarm_state=True)
                notifier.notify_alarm_state("ON", "Unknown person detected")
            elif on and (label!="unknown"):
                miss+=1
                if miss>30:
                    ser.write(b"<ALARM:OFF>\n"); ser.readline(); ser.readline(); on=False; miss=0
                    logger.log_event("alarm", label="OFF", motion_score=m, alarm_state=False)
                    notifier.notify_alarm_state("OFF", "No unknown persons detected")

            # Display stats on frame
            cv2.putText(frame,f"Detections: {logger.stats['face_detections']}",(10,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
            cv2.putText(frame,f"Unknown: {logger.stats['unknown_detections']}",(10,70),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)
            cv2.putText(frame,f"Alarms: {logger.stats['alarm_triggers']}",(10,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),1)
            
            cv2.imshow("SmartCam",frame)
            if cv2.waitKey(1)&0xFF==ord('q'): break
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        cap.release(); cv2.destroyAllWindows()
        ser.write(b"<ARM:0>\n"); ser.readline(); ser.readline()
        
        # Save session data and print statistics
        logger.save_session()
        logger.print_stats()
        print(f"Session data saved to: {logger.session_file}")
        print(f"CSV log saved to: {logger.csv_file}")