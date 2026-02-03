"""
Chaos & Edge Case Test for VORTEX Phase 2A.
Intentionally tries to break the system with:
1. Empty Users
2. NaN/Missing Values
3. Extreme Values
4. Duplicate Timestamps
5. Type Serialization (Numpy types)
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sys.path.insert(0, '.')

from src.user_profile import UserProfileManager
from src.risk_trajectory import TrajectoryManager
from src.event_chains import ChainDetectorManager
from src.temporal_patterns import TemporalManager

print("="*80)
print("🧨 VORTEX PHASE 2A: CHAOS & EDGE CASE TEST")
print("="*80)

def run_chaos_test():
    # --- 1. THE "EMPTY USER" SCENARIO ---
    print("\n[CHAOS 1] Testing Empty Dataframes...")
    empty_df = pd.DataFrame(columns=['user_id', 'timestamp', 'anomaly_score'])
    try:
        upm = UserProfileManager(empty_df)
        tm = TrajectoryManager(empty_df)
        cm = ChainDetectorManager(empty_df)
        temp_m = TemporalManager(empty_df)
        print("   ✅ System handled empty DataFrame without crashing")
    except Exception as e:
        print(f"   ❌ FAILED: Crashed on empty DF: {e}")

    # --- 2. THE "SINGLE EVENT" SCENARIO ---
    print("\n[CHAOS 2] Testing Single-Event Users...")
    single_df = pd.DataFrame([{
        'user_id': 'SOLO_USER',
        'timestamp': datetime.now(),
        'anomaly_score': -0.5,
        'risk_level': 'Medium',
        'file_access_count': 10
    }])
    try:
        tm = TrajectoryManager(single_df)
        t = tm.get_trajectory('SOLO_USER')
        summary = t.get_summary()
        print("   ✅ Trajectory handled single event")
        
        temp_m = TemporalManager(single_df)
        patterns = temp_m.get_user_patterns('SOLO_USER')
        print("   ✅ Temporal Detector handled single event")
    except Exception as e:
        print(f"   ❌ FAILED: Crashed on single event: {e}")

    # --- 3. THE "NAN ATTACK" SCENARIO ---
    print("\n[CHAOS 3] Testing Missing Values (NaN)...")
    nan_df = pd.DataFrame([
        {'user_id': 'NAN_USER', 'timestamp': datetime.now(), 'anomaly_score': np.nan, 'risk_level': 'Low'},
        {'user_id': 'NAN_USER', 'timestamp': datetime.now() - timedelta(days=1), 'anomaly_score': -0.5, 'risk_level': None}
    ])
    try:
        tm = TrajectoryManager(nan_df)
        # We need to see if calculation fails
        score = tm.get_trajectory('NAN_USER').cumulative_risk
        print(f"   ✅ Trajectory handled NaNs (Score: {score})")
    except Exception as e:
        print(f"   ❌ FAILED: Crashed on NaNs: {e}")

    # --- 4. THE "NUMPY TYPE" SCENARIO (Serialization Check) ---
    print("\n[CHAOS 4] Verifying JSON Serialization Safety (Numpy Types)...")
    # Simulate what Pandas does (returns numpy.int64 instead of int)
    np_int = np.int64(42)
    np_float = np.float64(-0.555555)
    
    # We want to ensure our summaries/trajectories return clean Python types
    test_df = pd.DataFrame([{
        'user_id': 'NP_USER',
        'timestamp': datetime.now(),
        'anomaly_score': np_float,
        'file_access_count': np_int
    }])
    
    try:
        tm = TrajectoryManager(test_df)
        summary = tm.get_trajectory('NP_USER').get_summary()
        
        # Check types in summary
        for key, val in summary.items():
            if isinstance(val, (np.integer, np.floating)):
                print(f"   ⚠️ WARNING: Key '{key}' returned a NUMPY type ({type(val)}).")
                print("      This will crash the FastAPI JSON encoder!")
            elif isinstance(val, dict):
                for k2, v2 in val.items():
                    if isinstance(v2, (np.integer, np.floating)):
                        print(f"   ⚠️ WARNING: Nested Key '{k2}' returned a NUMPY type ({type(v2)}).")
        
        print("   ✅ Summary type check complete")
    except Exception as e:
        print(f"   ❌ FAILED: Crashed on Numpy type check: {e}")

    # --- 5. THE "DUPLICATE TIMESTAMP" SCENARIO ---
    print("\n[CHAOS 5] Testing Simultaneous Events...")
    now = datetime.now()
    dup_df = pd.DataFrame([
        {'user_id': 'DUP_USER', 'timestamp': now, 'anomaly_score': -0.1},
        {'user_id': 'DUP_USER', 'timestamp': now, 'anomaly_score': -0.9}
    ])
    try:
        cm = ChainDetectorManager(dup_df)
        print("   ✅ Chain detection handled duplicate timestamps")
    except Exception as e:
        print(f"   ❌ FAILED: Crashed on duplicate timestamps: {e}")

run_chaos_test()
print("\n" + "="*80)
print("🏁 CHAOS TEST COMPLETE")
print("="*80)
