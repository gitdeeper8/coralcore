#!/usr/bin/env python
"""
اختبار نظيف - بدون أي تأثيرات سابقة
"""

import sys

# إضافة المجلد النظيف للمسار
sys.path.insert(0, '.')

print("=" * 60)
print("🧪 اختبار نظيف - CORAL-CORE بدون numpy")
print("=" * 60)

# استيراد مباشر من الملف النظيف
try:
    from coralcore_clean.parameters.calcification import calcification_rate, get_species_constant
    
    # اختبار 1
    rate1 = calcification_rate(omega_a=3.4, phi_ps=0.65, temperature=28.0, t_thr=31.5, species='acropora_millepora')
    print(f"✅ اختبار 1: rate = {rate1:.3f}")
    
    # اختبار 2
    rate2 = calcification_rate(omega_a=2.2, phi_ps=0.35, temperature=30.0, t_thr=31.0)
    print(f"✅ اختبار 2: rate = {rate2:.3f}")
    
    # اختبار 3 - ثابت النوع
    acro = get_species_constant('acropora_millepora')
    print(f"✅ اختبار 3: Acropora k = {acro['k']}")
    
    print("\n🎉 جميع اختبارات calcification نجحت!")
    
except Exception as e:
    print(f"❌ فشل: {e}")

print("\n" + "=" * 60)

# اختبار RHI من المجلد الأصلي
try:
    from coralcore.rhi.composite import ReefHealthIndex
    print("✅ RHI module imported successfully")
    
    rhi = ReefHealthIndex()
    params = {
        'g_ca': 1.84, 'e_diss': 91.0, 'phi_ps': 0.67,
        'rho_skel': 1.62, 'delta_ph': 0.08, 's_reef': 4.3,
        'k_s': 0.15, 't_thr': 31.2
    }
    result = rhi.compute(params, return_full=True)
    print(f"✅ RHI = {result.rhi:.3f} ({result.status})")
    
except Exception as e:
    print(f"❌ RHI فشل: {e}")

print("=" * 60)
