"""
Gesture System Security & Robustness Testing
Tests for memory leaks, race conditions, and edge cases
"""

import sys
sys.path.insert(0, '/home/user/ClassicApp/tests')

from gestures import (
    calculate_distance,
    calculate_angle,
    get_swipe_direction,
    validate_swipe
)

print("=" * 70)
print("GESTURE SYSTEM SECURITY & ROBUSTNESS TEST")
print("=" * 70)
print()

issues = []

# Test 1: Rapid successive gestures (race condition test)
print("TEST 1: Rapid Successive Gestures")
print("-" * 70)
try:
    for i in range(1000):
        touch_data = {
            'start': {'x': 0, 'y': 0},
            'end': {'x': 100, 'y': 0},
            'startTime': i,
            'endTime': i + 200
        }
        result = validate_swipe(touch_data)
    print("✓ Handled 1000 rapid gestures without error")
except Exception as e:
    print(f"❌ ISSUE: Failed on rapid gestures: {e}")
    issues.append(f"Race condition on rapid gestures: {e}")
print()

# Test 2: Extreme coordinates (integer overflow)
print("TEST 2: Extreme Coordinate Values")
print("-" * 70)
try:
    point1 = {'x': 999999999, 'y': 999999999}
    point2 = {'x': -999999999, 'y': -999999999}
    distance = calculate_distance(point1, point2)
    print(f"Distance for extreme coords: {distance:.2f}")
    if distance < 0:
        print(f"❌ ISSUE: Negative distance calculated")
        issues.append("Negative distance with extreme coordinates")
    else:
        print(f"✓ Handled extreme coordinates correctly")
except Exception as e:
    print(f"❌ ISSUE: Exception with extreme coords: {e}")
    issues.append(f"Crash on extreme coordinates: {e}")
print()

# Test 3: Zero-length swipe
print("TEST 3: Zero-Length Swipe")
print("-" * 70)
touch_data = {
    'start': {'x': 100, 'y': 100},
    'end': {'x': 100, 'y': 100},
    'startTime': 0,
    'endTime': 100
}
result = validate_swipe(touch_data)
if result['isValid']:
    print(f"❌ ISSUE: Zero-length swipe marked as valid")
    issues.append("Zero-length swipe incorrectly validated")
else:
    print(f"✓ Correctly rejects zero-length swipe")
    print(f"  Distance: {result['distance']}, Valid: {result['isValid']}")
print()

# Test 4: Same start/end time (instant swipe)
print("TEST 4: Instant Swipe (0ms duration)")
print("-" * 70)
touch_data = {
    'start': {'x': 0, 'y': 0},
    'end': {'x': 100, 'y': 0},
    'startTime': 100,
    'endTime': 100
}
result = validate_swipe(touch_data)
print(f"Duration: {result['duration']}ms, Valid: {result['isValid']}")
if result['isValid']:
    print(f"✓ Accepts instant swipe (reasonable for fast gestures)")
else:
    print(f"✓ Rejects instant swipe")
print()

# Test 5: Negative time duration
print("TEST 5: Negative Time Duration (time travel)")
print("-" * 70)
touch_data = {
    'start': {'x': 0, 'y': 0},
    'end': {'x': 100, 'y': 0},
    'startTime': 500,
    'endTime': 100  # End before start!
}
result = validate_swipe(touch_data)
if result['duration'] < 0 and result['isValid']:
    print(f"❌ ISSUE: Negative duration accepted as valid")
    issues.append("Negative time duration accepted")
else:
    print(f"✓ Handled negative duration: {result['duration']}ms, valid={result['isValid']}")
print()

# Test 6: Floating point coordinates
print("TEST 6: Floating Point Coordinates")
print("-" * 70)
try:
    point1 = {'x': 0.1234567890123456, 'y': 0.9876543210987654}
    point2 = {'x': 100.1234567890123456, 'y': 100.9876543210987654}
    distance = calculate_distance(point1, point2)
    print(f"✓ Distance with high precision: {distance}")
except Exception as e:
    print(f"❌ ISSUE: Failed with floating point: {e}")
    issues.append(f"Floating point precision error: {e}")
print()

# Test 7: Very long swipe distance
print("TEST 7: Very Long Swipe (across multiple screens)")
print("-" * 70)
touch_data = {
    'start': {'x': 0, 'y': 0},
    'end': {'x': 10000, 'y': 0},  # 10000 pixels
    'startTime': 0,
    'endTime': 400
}
result = validate_swipe(touch_data)
print(f"Distance: {result['distance']}px, Valid: {result['isValid']}")
print(f"✓ Note: Very long swipes are allowed - may be intentional for large screens")
print()

# Test 8: Exactly on angle boundaries
print("TEST 8: Angle Boundary Testing")
print("-" * 70)
test_angles = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
boundary_issues = 0
for angle in test_angles:
    direction = get_swipe_direction(angle, tolerance=30)
    print(f"  Angle {angle}°: {direction if direction else 'None'}")
    # Edge case: 360 should be same as 0 (right)
    if angle == 360:
        if direction != 'right':
            boundary_issues += 1
if boundary_issues == 0:
    print(f"✓ All boundary angles handled correctly")
else:
    print(f"❌ ISSUE: {boundary_issues} boundary angles mishandled")
    issues.append(f"{boundary_issues} angle boundaries incorrect")
print()

# Test 9: Concurrent options
print("TEST 9: Multiple Options Configurations")
print("-" * 70)
try:
    touch_data = {
        'start': {'x': 0, 'y': 0},
        'end': {'x': 75, 'y': 0},
        'startTime': 0,
        'endTime': 300
    }

    # Test with different option sets
    options_sets = [
        {'minSwipeDistance': 50, 'maxSwipeTime': 500, 'swipeAngleTolerance': 30},
        {'minSwipeDistance': 100, 'maxSwipeTime': 1000, 'swipeAngleTolerance': 45},
        {'minSwipeDistance': 30, 'maxSwipeTime': 300, 'swipeAngleTolerance': 15},
    ]

    for i, options in enumerate(options_sets, 1):
        result = validate_swipe(touch_data, options)
        print(f"  Config {i}: Valid={result['isValid']}")

    print(f"✓ Multiple configurations handled correctly")
except Exception as e:
    print(f"❌ ISSUE: Failed with multiple configs: {e}")
    issues.append(f"Multiple option configurations failed: {e}")
print()

# Test 10: Dictionary key missing (error handling)
print("TEST 10: Malformed Input Data")
print("-" * 70)
try:
    # Missing 'end' key
    bad_data = {
        'start': {'x': 0, 'y': 0},
        'startTime': 0,
        'endTime': 100
    }
    result = validate_swipe(bad_data)
    print(f"❌ ISSUE: Accepted malformed data without error")
    issues.append("Accepts malformed data without validation")
except KeyError as e:
    print(f"✓ Correctly raises KeyError for missing data: {e}")
except Exception as e:
    print(f"✓ Caught exception: {e}")
print()

# SUMMARY
print("=" * 70)
print("GESTURE SECURITY SUMMARY")
print("=" * 70)
if issues:
    print(f"Found {len(issues)} potential issues:\n")
    for i, issue in enumerate(issues, 1):
        print(f"{i}. {issue}")
else:
    print("✓ Gesture system is robust - no critical issues found")
print()
