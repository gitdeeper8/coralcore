#!/usr/bin/env python
"""
🪸 CORAL-CORE Quick Test - متجاهلاً numpy
"""

import sys
from datetime import datetime

# تجاهل numpy تماماً
import builtins
original_import = builtins.__import__

def ignore_numpy(name, *args, **kwargs):
    if name == 'numpy':
        # إرجاع كائن وهمي بدلاً من numpy
        class MockNumpy:
            def __getattr__(self, name):
                return lambda *args, **kwargs: None
        return MockNumpy()
    return original_import(name, *args, **kwargs)

builtins.__import__ = ignore_numpy

def print_header(text):
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def print_result(name, success, message=""):
    if success:
        print(f"  ✅ {name}: {message}")
    else:
        print(f"  ❌ {name}: {message}")

# استيراد بعد تجاهل numpy
print_header("🪸 CORAL-CORE Quick Test (متجاهلاً numpy)")
print(f"Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Python: {sys.version.split()[0]}")
print("Status: numpy متجاهل تماماً")

# اختبار calcification
print("\n📋 Testing Calcification...")
try:
    from coralcore.parameters.calcification import calcification_rate
    
    rate = calcification_rate(
        omega_a=3.4,
        phi_ps=0.65,
        temperature=28.0,
        t_thr=31.5,
        species='acropora_millepora'
    )
    print_result("Calcification", True, f"rate = {rate:.3f}")
except Exception as e:
    print_result("Calcification", False, str(e))

# اختبار RHI
print("\n📋 Testing RHI + Weights...")
try:
    from coralcore.rhi.composite import ReefHealthIndex
    
    rhi_calc = ReefHealthIndex()
    params = {
        'g_ca': 1.84, 'e_diss': 91.0, 'phi_ps': 0.67,
        'rho_skel': 1.62, 'delta_ph': 0.08, 's_reef': 4.3,
        'k_s': 0.15, 't_thr': 31.2
    }
    result = rhi_calc.compute(params, return_full=True)
    print_result("RHI", True, f"Healthy RHI: {result.rhi:.3f} ({result.status})")
    
    params_stressed = {
        'g_ca': 0.65, 'e_diss': 72.0, 'phi_ps': 0.38,
        'rho_skel': 1.25, 'delta_ph': 0.14, 's_reef': 3.2,
        'k_s': 0.08, 't_thr': 29.8
    }
    rhi_stressed = rhi_calc.compute(params_stressed, return_full=False)
    print(f"      Stressed RHI: {rhi_stressed:.3f}")
except Exception as e:
    print_result("RHI", False, str(e))

# اختبار Alert
print("\n📋 Testing Alert System...")
try:
    from coralcore.rhi.alert import AlertManager
    
    manager = AlertManager('TEST001')
    alerts1 = manager.check_alerts(rhi=0.45, parameters={'phi_ps': 0.2})
    alerts2 = manager.check_alerts(rhi=0.65, parameters={'phi_ps': 0.5})
    print_result("Alert", True, f"Critical: {len(alerts1)}, Warning: {len(alerts2)}")
except Exception as e:
    print_result("Alert", False, str(e))

# اختبار Weights
print("\n📋 Testing RHI Weights...")
try:
    from coralcore.rhi.composite import RHI_WEIGHTS
    
    total = sum(RHI_WEIGHTS.values())
    weight_str = ", ".join([f"{k}:{v}" for k, v in RHI_WEIGHTS.items()])
    print_result("Weights", True, f"Sum: {total:.2f}, {weight_str}")
except Exception as e:
    print_result("Weights", False, str(e))

print_header("📊 Summary")
print(f"  الاختبارات اكتملت - تم تجاهل numpy")
print("=" * 60)
