#!/usr/bin/env python
"""
📊 توليد تقارير تجريبية للاختبار
"""

import os
import sys
from datetime import datetime, timedelta

# إضافة المسار
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


def generate_sample_daily():
    """توليد تقرير يومي تجريبي"""
    from reports.daily.generate_daily_report import DailyReport
    
    report = DailyReport()
    report.generate_report()
    print("✅ تم توليد تقرير يومي")


def generate_sample_weekly():
    """توليد تقرير أسبوعي تجريبي"""
    from reports.weekly.generate_weekly_report import WeeklyReport
    
    report = WeeklyReport()
    report.generate_report()
    print("✅ تم توليد تقرير أسبوعي")


def generate_sample_monthly():
    """توليد تقرير شهري تجريبي"""
    from reports.monthly.generate_monthly_report import MonthlyReport
    
    report = MonthlyReport()
    report.generate_report()
    print("✅ تم توليد تقرير شهري")


def generate_sample_alert():
    """توليد تنبيه تجريبي"""
    from reports.alerts.alert_manager import AlertLogger
    
    logger = AlertLogger()
    logger.log_alert(
        level="INFO",
        message="تقرير تجريبي - اختبار نظام التقارير",
        rhi=0.82
    )
    print("✅ تم تسجيل تنبيه تجريبي")


def main():
    """توليد جميع التقارير التجريبية"""
    print("=" * 60)
    print("📊 توليد تقارير تجريبية")
    print("=" * 60)
    
    generate_sample_daily()
    generate_sample_weekly()
    generate_sample_monthly()
    generate_sample_alert()
    
    print("\n" + "=" * 60)
    print("✅ تم توليد جميع التقارير التجريبية")
    print("=" * 60)


if __name__ == "__main__":
    main()
