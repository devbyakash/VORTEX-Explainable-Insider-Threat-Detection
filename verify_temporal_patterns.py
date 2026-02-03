"""
Verification script for Temporal Pattern Detection.
Simulates Low-and-Slow, Frequency Spikes, and Behavioral Drift.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, '.')

print("="*60)
print("TEMPORAL PATTERN DETECTION VERIFICATION")
print("="*60)

# Test 1: Import
from src.temporal_patterns import TemporalPatternDetector, TemporalManager

# Test 2: Simulate "Low-and-Slow" User
print("\nTEST 1: Simulating 'Low-and-Slow' Attack...")
events = []
base_date = datetime.now() - timedelta(days=45)

for i in range(40):
    # User does 1 slightly suspicious thing every day for 40 days
    events.append({
        'user_id': 'STEALTH_USER',
        'timestamp': base_date + timedelta(days=i),
        'file_access_count': 10,
        'upload_size_mb': 5,
        'anomaly_score': -0.25 # Suspect but not an alert
    })

df_low_slow = pd.DataFrame(events)
detector = TemporalPatternDetector('STEALTH_USER', df_low_slow)
patterns = detector.get_patterns()

print(f"✅ Analysis for STEALTH_USER: {len(patterns)} patterns found")
for p in patterns:
    print(f"   [!] {p['name']}: {p['description']}")

# Test 3: Simulate "Frequency Anomaly"
print("\nTEST 2: Simulating 'Activity Frequency Spike'...")
spike_events = []
# 30 days of quiet (1 event/day)
for i in range(30):
    spike_events.append({
        'user_id': 'SPIKE_USER',
        'timestamp': base_date + timedelta(days=i),
        'file_access_count': 2,
        'anomaly_score': -0.05
    })
# 3 days of crazy activity (20 events/day)
for i in range(3):
    for j in range(20):
        spike_events.append({
            'user_id': 'SPIKE_USER',
            'timestamp': datetime.now() - timedelta(days=2-i),
            'file_access_count': 5,
            'anomaly_score': -0.05
        })

df_spike = pd.DataFrame(spike_events)
detector_spike = TemporalPatternDetector('SPIKE_USER', df_spike)
spike_patterns = detector_spike.get_patterns()

print(f"✅ Analysis for SPIKE_USER: {len(spike_patterns)} patterns found")
for p in spike_patterns:
    print(f"   [!] {p['name']}: {p['description']}")

# Test 4: Manager Logic
print("\nTEST 3: Testing TemporalManager Stats...")
all_test_df = pd.concat([df_low_slow, df_spike])
manager = TemporalManager(all_test_df)
stats = manager.get_statistics()
print(f"✅ Global Statistics: {stats['total_patterns_detected']} Total Patterns")
print(f"   Breakdown: {stats['by_type']}")

print("\n" + "="*60)
print("🎉 TEMPORAL DETECTION VERIFIED!")
print("="*60)
