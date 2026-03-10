#!/usr/bin/env python
"""
🚨 CORAL-CORE Alert Logger
Logs alerts to text file (English only)
"""

import os
from datetime import datetime, timedelta


class AlertLogger:
    """Alert logger"""
    
    def __init__(self, log_file="reports/alerts/alert_log.txt"):
        self.log_file = log_file
    
    def log_alert(self, level, message, station="RAS_MOHAMMED_01", rhi=None):
        """Log new alert"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{timestamp}] {level}\n")
            f.write(f"📍 Station: {station}\n")
            f.write(f"📝 Message: {message}\n")
            if rhi is not None:
                f.write(f"📊 RHI: {rhi:.3f}\n")
            f.write("-" * 50 + "\n")
        
        print(f"✅ Alert logged: {level}")
    
    def get_recent_alerts(self, hours=24):
        """Get recent alerts"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = []
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            current_alert = []
            for line in lines:
                if line.startswith('['):
                    # Extract timestamp
                    time_str = line[1:20]
                    try:
                        alert_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                        if alert_time > cutoff:
                            current_alert = [line]
                        else:
                            current_alert = []
                    except:
                        pass
                elif current_alert is not None:
                    current_alert.append(line)
                    if line.startswith('-' * 50):
                        recent.append(''.join(current_alert))
                        current_alert = None
        except:
            pass
        
        return recent
    
    def get_alerts_by_level(self, level):
        """Get alerts filtered by level"""
        alerts = []
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by alert
            alert_blocks = content.split('-' * 50)
            
            for block in alert_blocks:
                if f'] {level}' in block:
                    alerts.append(block.strip())
        except:
            pass
        
        return alerts
    
    def clear_old_alerts(self, days=30):
        """Delete old alerts"""
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.strftime("%Y-%m-%d")
        
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            keep = True
            
            for line in lines:
                if line.startswith('['):
                    # Check alert date
                    time_str = line[1:20]
                    try:
                        alert_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                        keep = alert_time > cutoff
                    except:
                        keep = True
                
                if keep:
                    new_lines.append(line)
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            
            print(f"✅ Alerts older than {cutoff_str} cleared")
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main test function"""
    logger = AlertLogger()
    
    # Log test alert
    logger.log_alert(
        level="INFO",
        message="Alert system test",
        rhi=0.85
    )
    
    # Show recent alerts
    recent = logger.get_recent_alerts(hours=24)
    print(f"\nRecent alerts ({len(recent)}):")
    for alert in recent[-3:]:
        print(alert[:100] + "...")


if __name__ == "__main__":
    main()
