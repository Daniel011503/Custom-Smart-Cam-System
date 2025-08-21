# analyze_logs.py - Data Analysis Tool for SmartCam Logs
import json, csv, os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict, Counter

class LogAnalyzer:
    def __init__(self, logs_dir="logs"):
        self.logs_dir = logs_dir
        self.sessions = []
        self.csv_data = []
        
    def load_data(self):
        """Load all session JSON files and CSV data"""
        if not os.path.exists(self.logs_dir):
            print(f"Logs directory '{self.logs_dir}' not found!")
            return
            
        # Load JSON session files
        for file in os.listdir(self.logs_dir):
            if file.startswith("session_") and file.endswith(".json"):
                with open(os.path.join(self.logs_dir, file), 'r') as f:
                    self.sessions.append(json.load(f))
        
        # Load CSV files
        for file in os.listdir(self.logs_dir):
            if file.startswith("smartcam_log_") and file.endswith(".csv"):
                with open(os.path.join(self.logs_dir, file), 'r') as f:
                    reader = csv.DictReader(f)
                    self.csv_data.extend(list(reader))
                    
        print(f"Loaded {len(self.sessions)} sessions and {len(self.csv_data)} CSV records")
    
    def analyze_detections(self):
        """Analyze face detection patterns"""
        print("\n=== DETECTION ANALYSIS ===")
        
        total_detections = 0
        known_detections = 0
        unknown_detections = 0
        detection_by_hour = defaultdict(int)
        confidence_scores = []
        
        for record in self.csv_data:
            if record['event_type'] == 'face_detection':
                total_detections += 1
                hour = datetime.fromisoformat(record['timestamp']).hour
                detection_by_hour[hour] += 1
                
                if record['label'] == 'unknown':
                    unknown_detections += 1
                elif record['label'] != 'none':
                    known_detections += 1
                    
                if float(record['confidence']) > 0:
                    confidence_scores.append(float(record['confidence']))
        
        print(f"Total face detections: {total_detections}")
        print(f"Known person detections: {known_detections}")
        print(f"Unknown person detections: {unknown_detections}")
        
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            print(f"Average confidence score: {avg_confidence:.1f}")
        
        # Peak activity hours
        if detection_by_hour:
            peak_hour = max(detection_by_hour, key=detection_by_hour.get)
            print(f"Peak activity hour: {peak_hour}:00 ({detection_by_hour[peak_hour]} detections)")
            
        return detection_by_hour, confidence_scores
    
    def analyze_motion(self):
        """Analyze motion patterns"""
        print("\n=== MOTION ANALYSIS ===")
        
        motion_events = [r for r in self.csv_data if r['event_type'] == 'motion']
        motion_scores = [float(r['motion_score']) for r in motion_events if float(r['motion_score']) > 0]
        
        if motion_scores:
            avg_motion = sum(motion_scores) / len(motion_scores)
            max_motion = max(motion_scores)
            min_motion = min(motion_scores)
            
            print(f"Total motion events: {len(motion_events)}")
            print(f"Average motion score: {avg_motion:.1f}")
            print(f"Max motion score: {max_motion:.1f}")
            print(f"Min motion score: {min_motion:.1f}")
            
        return motion_scores
    
    def analyze_alarms(self):
        """Analyze alarm patterns"""
        print("\n=== ALARM ANALYSIS ===")
        
        alarm_events = [r for r in self.csv_data if r['event_type'] == 'alarm']
        alarm_on_events = [r for r in alarm_events if r['label'] == 'ON']
        alarm_off_events = [r for r in alarm_events if r['label'] == 'OFF']
        
        print(f"Total alarm activations: {len(alarm_on_events)}")
        print(f"Total alarm deactivations: {len(alarm_off_events)}")
        
        # Calculate alarm durations
        durations = []
        on_times = [datetime.fromisoformat(r['timestamp']) for r in alarm_on_events]
        off_times = [datetime.fromisoformat(r['timestamp']) for r in alarm_off_events]
        
        for i, on_time in enumerate(on_times):
            # Find corresponding off time
            for off_time in off_times:
                if off_time > on_time:
                    duration = (off_time - on_time).total_seconds()
                    durations.append(duration)
                    break
        
        if durations:
            avg_duration = sum(durations) / len(durations)
            print(f"Average alarm duration: {avg_duration:.1f} seconds")
            
        return alarm_on_events, durations
    
    def create_visualizations(self):
        """Create visualization charts"""
        try:
            detection_by_hour, confidence_scores = self.analyze_detections()
            motion_scores = self.analyze_motion()
            alarm_events, durations = self.analyze_alarms()
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # 1. Detections by hour
            if detection_by_hour:
                hours = list(range(24))
                counts = [detection_by_hour.get(h, 0) for h in hours]
                ax1.bar(hours, counts, color='skyblue')
                ax1.set_title('Face Detections by Hour')
                ax1.set_xlabel('Hour of Day')
                ax1.set_ylabel('Number of Detections')
                ax1.set_xticks(range(0, 24, 2))
            
            # 2. Confidence score distribution
            if confidence_scores:
                ax2.hist(confidence_scores, bins=20, color='lightgreen', alpha=0.7)
                ax2.set_title('Confidence Score Distribution')
                ax2.set_xlabel('Confidence Score')
                ax2.set_ylabel('Frequency')
                ax2.axvline(x=70, color='red', linestyle='--', label='Threshold (70)')
                ax2.legend()
            
            # 3. Motion scores over time
            if motion_scores:
                ax3.plot(motion_scores, color='orange', alpha=0.7)
                ax3.set_title('Motion Scores Over Time')
                ax3.set_xlabel('Event Number')
                ax3.set_ylabel('Motion Score')
                ax3.axhline(y=6000, color='red', linestyle='--', label='Motion Threshold')
                ax3.legend()
            
            # 4. Alarm duration distribution
            if durations:
                ax4.hist(durations, bins=15, color='salmon', alpha=0.7)
                ax4.set_title('Alarm Duration Distribution')
                ax4.set_xlabel('Duration (seconds)')
                ax4.set_ylabel('Frequency')
            
            plt.tight_layout()
            plt.savefig(os.path.join(self.logs_dir, 'analysis_charts.png'), dpi=300, bbox_inches='tight')
            print(f"\nVisualization saved to: {os.path.join(self.logs_dir, 'analysis_charts.png')}")
            plt.show()
            
        except ImportError:
            print("\nNote: Install matplotlib for visualizations: pip install matplotlib")
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        report_file = os.path.join(self.logs_dir, f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(report_file, 'w') as f:
            f.write("SMARTCAM DATA ANALYSIS REPORT\n")
            f.write("="*50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Session summary
            f.write(f"SESSIONS ANALYZED: {len(self.sessions)}\n")
            f.write(f"CSV RECORDS: {len(self.csv_data)}\n\n")
            
            # Detection stats
            detections = [r for r in self.csv_data if r['event_type'] == 'face_detection']
            f.write(f"TOTAL FACE DETECTIONS: {len(detections)}\n")
            
            known = len([r for r in detections if r['label'] not in ['unknown', 'none']])
            unknown = len([r for r in detections if r['label'] == 'unknown'])
            f.write(f"KNOWN PERSONS: {known}\n")
            f.write(f"UNKNOWN PERSONS: {unknown}\n\n")
            
            # Motion stats
            motion = [r for r in self.csv_data if r['event_type'] == 'motion']
            f.write(f"MOTION EVENTS: {len(motion)}\n\n")
            
            # Alarm stats
            alarms = [r for r in self.csv_data if r['event_type'] == 'alarm' and r['label'] == 'ON']
            f.write(f"ALARM ACTIVATIONS: {len(alarms)}\n")
            
        print(f"Analysis report saved to: {report_file}")

def main():
    analyzer = LogAnalyzer()
    analyzer.load_data()
    
    if not analyzer.csv_data and not analyzer.sessions:
        print("No log data found! Run SmartCam to generate logs first.")
        return
    
    analyzer.analyze_detections()
    analyzer.analyze_motion() 
    analyzer.analyze_alarms()
    analyzer.create_visualizations()
    analyzer.generate_report()

if __name__ == "__main__":
    main()
