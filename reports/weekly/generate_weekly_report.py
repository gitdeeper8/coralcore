#!/usr/bin/env python
"""
📊 CORAL-CORE Weekly Report Generator
Generates weekly report in TXT format (English only)
"""

import os
import sys
from datetime import datetime, timedelta
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class WeeklyReport:
    """Weekly report generator"""
    
    def __init__(self, station_id="RAS_MOHAMMED_01"):
        self.station_id = station_id
        self.today = datetime.now()
        self.week_start = (self.today - timedelta(days=self.today.weekday())).strftime("%Y-%m-%d")
        self.week_end = self.today.strftime("%Y-%m-%d")
        self.report_file = f"reports/weekly/report_week_{self.week_start}_to_{self.week_end}.txt"
    
    def collect_weekly_data(self):
        """Collect weekly data from daily reports"""
        daily_reports = glob.glob(f"reports/daily/report_*.txt")
        daily_reports.sort(reverse=True)
        daily_reports = daily_reports[:7]  # Last 7 days
        
        weekly_data = {
            'rhi_values': [],
            'alert_counts': 0,
            'days_with_data': len(daily_reports),
            'daily_status': []
        }
        
        for report_file in daily_reports:
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract RHI
                    import re
                    rhi_match = re.search(r'RHI: ([\d.]+)', content)
                    if rhi_match:
                        rhi = float(rhi_match.group(1))
                        weekly_data['rhi_values'].append(rhi)
                    
                    # Extract status
                    status_match = re.search(r'Status: (\w+)', content)
                    if status_match:
                        weekly_data['daily_status'].append(status_match.group(1))
                    
                    # Count alerts
                    alert_count = content.count('[WARNING]') + content.count('[CRITICAL]')
                    weekly_data['alert_counts'] += alert_count
            except:
                pass
        
        return weekly_data
    
    def generate_report(self):
        """Generate weekly report"""
        data = self.collect_weekly_data()
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("📊 CORAL-CORE WEEKLY REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"📅 Period: {self.week_start} to {self.week_end}\n")
            f.write(f"📍 Station: {self.station_id}\n\n")
            
            f.write("-" * 60 + "\n")
            f.write("📈 WEEKLY SUMMARY\n")
            f.write("-" * 60 + "\n")
            f.write(f"Days with data: {data['days_with_data']}/7\n")
            
            if data['rhi_values']:
                avg_rhi = sum(data['rhi_values']) / len(data['rhi_values'])
                min_rhi = min(data['rhi_values'])
                max_rhi = max(data['rhi_values'])
                
                f.write(f"Average RHI: {avg_rhi:.3f}\n")
                f.write(f"Minimum RHI: {min_rhi:.3f}\n")
                f.write(f"Maximum RHI: {max_rhi:.3f}\n")
                f.write(f"Total alerts: {data['alert_counts']}\n\n")
                
                # Status assessment
                if avg_rhi >= 0.8:
                    f.write("Overall status: 🟢 HEALTHY\n")
                elif avg_rhi >= 0.5:
                    f.write("Overall status: 🟡 STRESSED\n")
                else:
                    f.write("Overall status: 🔴 CRITICAL\n")
                
                # Trend analysis
                if len(data['rhi_values']) >= 2:
                    first = data['rhi_values'][0]
                    last = data['rhi_values'][-1]
                    change = last - first
                    
                    if change > 0.05:
                        f.write(f"Trend: 📈 IMPROVING (+{change:.3f})\n")
                    elif change < -0.05:
                        f.write(f"Trend: 📉 DECLINING ({change:.3f})\n")
                    else:
                        f.write("Trend: ➡️ STABLE\n")
            else:
                f.write("Insufficient data\n\n")
            
            f.write("\n" + "-" * 60 + "\n")
            f.write("📊 DAILY RHI VALUES\n")
            f.write("-" * 60 + "\n")
            
            for i, rhi in enumerate(data['rhi_values'][::-1]):
                day = (self.today - timedelta(days=i)).strftime("%Y-%m-%d")
                status = data['daily_status'][i] if i < len(data['daily_status']) else "UNKNOWN"
                f.write(f"{day}: {rhi:.3f} ({status})\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("✅ END OF WEEKLY REPORT\n")
            f.write("=" * 60 + "\n")
        
        print(f"✅ Weekly report created: {self.report_file}")
        return self.report_file


def main():
    report = WeeklyReport()
    report.generate_report()


if __name__ == "__main__":
    main()
