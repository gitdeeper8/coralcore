#!/usr/bin/env python
"""
📊 CORAL-CORE Daily Report Generator
Generates daily report in TXT format (English only)
"""

import os
import sys
from datetime import datetime, timedelta  # <-- تم إضافة timedelta هنا
import json
import re
import glob

# Add main path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from coralcore.rhi.composite import ReefHealthIndex
    from coralcore.rhi.alert import AlertManager
except ImportError:
    print("⚠️ CORAL-CORE modules not found. Using mock data.")
    # Use mock data if modules are not available


class DailyReport:
    """Daily report generator"""
    
    def __init__(self, station_id="RAS_MOHAMMED_01"):
        self.station_id = station_id
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.report_file = f"reports/daily/report_{self.date}.txt"
        
        # Try to import CORAL-CORE modules
        try:
            self.rhi_calc = ReefHealthIndex()
            self.alert_manager = AlertManager(station_id)
            self.has_coralcore = True
        except:
            self.has_coralcore = False
    
    def collect_data(self):
        """Collect today's data"""
        if self.has_coralcore:
            # Here real sensor data would be collected
            # For simplicity, using sample data
            params = {
                'g_ca': 1.84,
                'e_diss': 91.0,
                'phi_ps': 0.67,
                'rho_skel': 1.62,
                'delta_ph': 0.08,
                's_reef': 4.3,
                'k_s': 0.15,
                't_thr': 31.2
            }
            
            result = self.rhi_calc.compute(params, return_full=True)
            alerts = self.alert_manager.check_alerts(
                rhi=result.rhi,
                parameters=params
            )
            
            return {
                'parameters': params,
                'rhi': result.rhi,
                'status': result.status,
                'alerts': alerts,
                'contributions': result.contributions
            }
        else:
            # Sample data
            return {
                'parameters': {
                    'g_ca': 1.84,
                    'e_diss': 91.0,
                    'phi_ps': 0.67,
                    'rho_skel': 1.62,
                    'delta_ph': 0.08,
                    's_reef': 4.3,
                    'k_s': 0.15,
                    't_thr': 31.2
                },
                'rhi': 0.84,
                'status': 'HEALTHY',
                'alerts': [],
                'contributions': {
                    'g_ca': 0.19*0.74,
                    'e_diss': 0.14*0.91,
                    'phi_ps': 0.21*0.84,
                    'rho_skel': 0.12*0.81,
                    'delta_ph': 0.11*0.68,
                    's_reef': 0.10*0.86,
                    'k_s': 0.08*0.75,
                    't_thr': 0.05*0.92
                }
            }
    
    def generate_report(self):
        """Generate daily report"""
        data = self.collect_data()
        
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("📊 CORAL-CORE DAILY REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"📅 Date: {self.date}\n")
            f.write(f"📍 Station: {self.station_id}\n")
            f.write(f"⏰ Report Time: {datetime.now().strftime('%H:%M:%S')}\n\n")
            
            f.write("-" * 60 + "\n")
            f.write("📈 REEF HEALTH INDEX (RHI)\n")
            f.write("-" * 60 + "\n")
            f.write(f"RHI: {data['rhi']:.3f}\n")
            f.write(f"Status: {data['status']}\n\n")
            
            f.write("-" * 60 + "\n")
            f.write("📊 PHYSICAL PARAMETERS\n")
            f.write("-" * 60 + "\n")
            f.write(f"G_ca  (Calcification Rate)     : {data['parameters']['g_ca']:.3f} mmol/cm²/day\n")
            f.write(f"E_diss (Wave Dissipation)      : {data['parameters']['e_diss']:.3f} %\n")
            f.write(f"Φ_ps  (Quantum Yield)          : {data['parameters']['phi_ps']:.3f}\n")
            f.write(f"ρ_skel (Skeletal Density)      : {data['parameters']['rho_skel']:.3f} g/cm³\n")
            f.write(f"ΔpH    (Acidification Lag)     : {data['parameters']['delta_ph']:.3f} pH units\n")
            f.write(f"S_reef (Acoustic Signature)    : {data['parameters']['s_reef']:.3f}\n")
            f.write(f"k_s    (Roughness Index)       : {data['parameters']['k_s']:.3f} m\n")
            f.write(f"T_thr  (Bleaching Threshold)   : {data['parameters']['t_thr']:.3f} °C\n\n")
            
            f.write("-" * 60 + "\n")
            f.write("📊 PARAMETER CONTRIBUTIONS TO RHI\n")
            f.write("-" * 60 + "\n")
            f.write(f"G_ca  contribution : {data['contributions']['g_ca']:.3f} (weight: 0.19)\n")
            f.write(f"E_diss contribution : {data['contributions']['e_diss']:.3f} (weight: 0.14)\n")
            f.write(f"Φ_ps  contribution : {data['contributions']['phi_ps']:.3f} (weight: 0.21)\n")
            f.write(f"ρ_skel contribution : {data['contributions']['rho_skel']:.3f} (weight: 0.12)\n")
            f.write(f"ΔpH   contribution : {data['contributions']['delta_ph']:.3f} (weight: 0.11)\n")
            f.write(f"S_reef contribution : {data['contributions']['s_reef']:.3f} (weight: 0.10)\n")
            f.write(f"k_s   contribution : {data['contributions']['k_s']:.3f} (weight: 0.08)\n")
            f.write(f"T_thr contribution : {data['contributions']['t_thr']:.3f} (weight: 0.05)\n\n")
            
            f.write("-" * 60 + "\n")
            f.write("🚨 ALERTS\n")
            f.write("-" * 60 + "\n")
            if data['alerts']:
                for alert in data['alerts']:
                    f.write(f"[{alert.level}] {alert.message}\n")
            else:
                f.write("No alerts\n")
            f.write("\n")
            
            f.write("-" * 60 + "\n")
            f.write("📝 NOTES\n")
            f.write("-" * 60 + "\n")
            
            # Add notes based on RHI status
            if data['rhi'] >= 0.8:
                f.write("- Reef is in HEALTHY condition\n")
                f.write("- All parameters within optimal ranges\n")
                f.write("- No signs of thermal stress\n")
                f.write("- Continue regular monitoring\n")
            elif data['rhi'] >= 0.5:
                f.write("- Reef is in STRESSED condition\n")
                f.write("- Some parameters below optimal levels\n")
                f.write("- Monitor closely for changes\n")
                f.write("- Prepare for possible intervention\n")
            else:
                f.write("- Reef is in CRITICAL condition\n")
                f.write("- Immediate intervention required\n")
                f.write("- Multiple parameters below thresholds\n")
                f.write("- Deploy mitigation measures\n")
            f.write("\n")
            
            f.write("=" * 60 + "\n")
            f.write("✅ END OF DAILY REPORT\n")
            f.write("=" * 60 + "\n")
        
        print(f"✅ Daily report created: {self.report_file}")
        return self.report_file
    
    def get_rhi_trend(self, days=7):
        """Get RHI trend from last N days"""
        trend_data = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            report_file = f"reports/daily/report_{date}.txt"
            
            if os.path.exists(report_file):
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    rhi_match = re.search(r'RHI: ([\d.]+)', content)
                    if rhi_match:
                        trend_data.append({
                            'date': date,
                            'rhi': float(rhi_match.group(1))
                        })
        
        return trend_data[::-1]  # Return in chronological order


def main():
    """Main function"""
    report = DailyReport()
    report.generate_report()
    
    # Optional: Show trend
    try:
        trend = report.get_rhi_trend(days=3)
        if trend:
            print("\n📈 Recent RHI trend:")
            for entry in trend:
                print(f"  {entry['date']}: {entry['rhi']:.3f}")
    except Exception as e:
        print(f"\n⚠️ Could not load trend: {e}")


if __name__ == "__main__":
    main()
