#!/usr/bin/env python
"""
📊 CORAL-CORE Monthly Report Generator
Generates monthly report in TXT format (English only)
"""

import os
import sys
from datetime import datetime, timedelta
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class MonthlyReport:
    """Monthly report generator"""
    
    def __init__(self, station_id="RAS_MOHAMMED_01"):
        self.station_id = station_id
        self.today = datetime.now()
        self.month = self.today.strftime("%Y-%m")
        self.report_file = f"reports/monthly/report_{self.month}.txt"
    
    def collect_monthly_data(self):
        """Collect monthly data from daily reports"""
        daily_reports = glob.glob(f"reports/daily/report_*.txt")
        daily_reports.sort()
        
        # Filter reports for this month
        monthly_reports = [r for r in daily_reports if self.month in r]
        
        monthly_data = {
            'rhi_values': [],
            'daily_alerts': [],
            'days_with_data': len(monthly_reports),
            'dates': []
        }
        
        for report_file in monthly_reports:
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract date
                    import re
                    date_match = re.search(r'Date: (\d{4}-\d{2}-\d{2})', content)
                    if date_match:
                        monthly_data['dates'].append(date_match.group(1))
                    
                    # Extract RHI
                    rhi_match = re.search(r'RHI: ([\d.]+)', content)
                    if rhi_match:
                        monthly_data['rhi_values'].append(float(rhi_match.group(1)))
                    
                    # Count alerts
                    alert_count = content.count('[WARNING]') + content.count('[CRITICAL]')
                    monthly_data['daily_alerts'].append(alert_count)
            except:
                pass
        
        return monthly_data
    
    def generate_report(self):
        """Generate monthly report"""
        data = self.collect_monthly_data()
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("📊 CORAL-CORE MONTHLY REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"📅 Month: {self.month}\n")
            f.write(f"📍 Station: {self.station_id}\n\n")
            
            f.write("-" * 60 + "\n")
            f.write("📈 MONTHLY SUMMARY\n")
            f.write("-" * 60 + "\n")
            f.write(f"Days with data: {data['days_with_data']}\n")
            
            if data['rhi_values']:
                avg_rhi = sum(data['rhi_values']) / len(data['rhi_values'])
                min_rhi = min(data['rhi_values'])
                max_rhi = max(data['rhi_values'])
                total_alerts = sum(data['daily_alerts'])
                
                f.write(f"Average RHI: {avg_rhi:.3f}\n")
                f.write(f"Minimum RHI: {min_rhi:.3f}\n")
                f.write(f"Maximum RHI: {max_rhi:.3f}\n")
                f.write(f"Total alerts: {total_alerts}\n\n")
                
                # Monthly statistics
                f.write(f"Days with alerts: {len([a for a in data['daily_alerts'] if a > 0])}\n")
                f.write(f"Average alerts per day: {total_alerts/len(data['daily_alerts']):.1f}\n\n")
                
                # Trend analysis
                if len(data['rhi_values']) > 7:
                    first_week = sum(data['rhi_values'][:7]) / 7
                    last_week = sum(data['rhi_values'][-7:]) / 7
                    
                    trend = last_week - first_week
                    if trend > 0.05:
                        f.write("Monthly trend: 📈 IMPROVING\n")
                    elif trend < -0.05:
                        f.write("Monthly trend: 📉 DECLINING\n")
                    else:
                        f.write("Monthly trend: ➡️ STABLE\n")
                    
                    f.write(f"Change: {trend:+.3f}\n\n")
                
                # Monthly classification
                if avg_rhi >= 0.8:
                    f.write("Monthly classification: 🟢 HEALTHY\n")
                    f.write("Recommendation: Continue regular monitoring\n")
                elif avg_rhi >= 0.5:
                    f.write("Monthly classification: 🟡 STRESSED\n")
                    f.write("Recommendation: Increase monitoring frequency\n")
                else:
                    f.write("Monthly classification: 🔴 CRITICAL\n")
                    f.write("Recommendation: IMMEDIATE INTERVENTION REQUIRED\n")
                
            else:
                f.write("Insufficient data for this month\n\n")
            
            f.write("\n" + "-" * 60 + "\n")
            f.write("📊 DAILY BREAKDOWN\n")
            f.write("-" * 60 + "\n")
            
            for i, (date, rhi, alerts) in enumerate(zip(
                data['dates'], 
                data['rhi_values'], 
                data['daily_alerts']
            )):
                f.write(f"{date}: RHI={rhi:.3f}, Alerts={alerts}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("✅ END OF MONTHLY REPORT\n")
            f.write("=" * 60 + "\n")
        
        print(f"✅ Monthly report created: {self.report_file}")
        return self.report_file


def main():
    report = MonthlyReport()
    report.generate_report()


if __name__ == "__main__":
    main()
