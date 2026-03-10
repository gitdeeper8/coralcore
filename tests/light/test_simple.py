"""
🧪 CORAL-CORE Light Tests for Termux
Simple tests without heavy dependencies
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Test importing core modules"""
    try:
        from coralcore.parameters.calcification import calcification_rate
        print("✅ calcification_rate imported")
        
        from coralcore.rhi.composite import ReefHealthIndex
        print("✅ ReefHealthIndex imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_calcification():
    """Test calcification calculation"""
    from coralcore.parameters.calcification import calcification_rate
    
    # Test with valid inputs
    rate = calcification_rate(
        omega_a=3.4,
        phi_ps=0.65,
        temperature=28.0,
        t_thr=31.5,
        species='acropora_millepora'
    )
    
    print(f"✅ Calcification rate: {rate:.3f}")
    assert rate > 0, "Rate should be positive"
    assert rate < 3, "Rate should be reasonable"
    
    # Test with stressed conditions
    rate2 = calcification_rate(
        omega_a=2.2,
        phi_ps=0.35,
        temperature=30.0,
        t_thr=31.0
    )
    
    print(f"✅ Stressed rate: {rate2:.3f}")
    assert rate2 < rate, "Stressed rate should be lower"
    
    return True

def test_rhi():
    """Test RHI calculation"""
    from coralcore.rhi.composite import ReefHealthIndex
    
    rhi_calc = ReefHealthIndex()
    
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
    
    rhi = rhi_calc.compute(params, return_full=True)
    
    print(f"✅ RHI: {rhi.rhi:.3f}")
    print(f"✅ Status: {rhi.status}")
    
    assert 0 <= rhi.rhi <= 1, "RHI should be between 0 and 1"
    
    return True

def test_alert():
    """Test alert system"""
    from coralcore.rhi.alert import AlertManager
    
    manager = AlertManager('TEST001')
    
    params = {'phi_ps': 0.2}
    alerts = manager.check_alerts(rhi=0.45, parameters=params)
    
    print(f"✅ Alerts triggered: {len(alerts)}")
    
    if alerts:
        print(f"✅ First alert: {alerts[0].level.value}")
    
    return True

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 CORAL-CORE Light Test Suite for Termux")
    print("=" * 60)
    
    tests = [
        ("Import modules", test_imports),
        ("Calcification", test_calcification),
        ("RHI", test_rhi),
        ("Alert system", test_alert),
    ]
    
    passed = 0
    for name, test_func in tests:
        print(f"\n📋 Testing {name}...")
        try:
            if test_func():
                print(f"  ✅ {name} passed")
                passed += 1
            else:
                print(f"  ❌ {name} failed")
        except Exception as e:
            print(f"  ❌ {name} error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Results: {passed}/{len(tests)} tests passed")
    print("=" * 60)
    
    return passed == len(tests)

if __name__ == "__main__":
    run_all_tests()
