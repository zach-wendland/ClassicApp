"""
Red Team Penetration Testing Script
Tests calculator with malicious/extreme inputs
"""

import sys
sys.path.insert(0, '/home/user/ClassicApp/tests')

from calculator import (
    calculate_monthly_payment,
    calculate_total_paid,
    calculate_total_interest,
    generate_amortization_schedule,
    validate_inputs
)

print("=" * 70)
print("RED TEAM PENETRATION TEST - AMORTIZATION CALCULATOR")
print("=" * 70)
print()

vulnerabilities = []

# Test 1: Infinity values
print("TEST 1: Infinity Attack")
print("-" * 70)
try:
    result = calculate_monthly_payment(float('inf'), 5, 30)
    print(f"❌ VULNERABILITY: Accepts Infinity as input, result: {result}")
    vulnerabilities.append("Accepts Infinity values - causes invalid calculations")
except Exception as e:
    print(f"✓ Handled: {e}")

try:
    validation = validate_inputs(float('inf'), 5, 30)
    if validation['isValid']:
        print(f"❌ VULNERABILITY: Validation accepts Infinity!")
        vulnerabilities.append("Validation does not reject Infinity")
    else:
        print(f"✓ Validation rejects Infinity: {validation['error']}")
except Exception as e:
    print(f"✓ Exception raised: {e}")
print()

# Test 2: NaN values
print("TEST 2: NaN Attack")
print("-" * 70)
try:
    result = calculate_monthly_payment(float('nan'), 5, 30)
    print(f"❌ VULNERABILITY: Accepts NaN as input, result: {result}")
    vulnerabilities.append("Accepts NaN values - causes invalid calculations")
except Exception as e:
    print(f"✓ Handled: {e}")

try:
    validation = validate_inputs(float('nan'), 5, 30)
    if validation['isValid']:
        print(f"❌ VULNERABILITY: Validation accepts NaN!")
        vulnerabilities.append("Validation does not reject NaN")
except Exception as e:
    print(f"✓ Exception raised: {e}")
print()

# Test 3: Extremely large numbers (near MAX_SAFE_INTEGER)
print("TEST 3: Integer Overflow Attack")
print("-" * 70)
max_safe = 9007199254740991  # JavaScript MAX_SAFE_INTEGER
try:
    result = calculate_monthly_payment(max_safe, 5, 30)
    print(f"Result for MAX_SAFE_INTEGER: {result}")
    if result > max_safe * 2:
        print(f"❌ VULNERABILITY: Calculation overflow detected")
        vulnerabilities.append("Integer overflow in calculations")
    else:
        print(f"✓ Calculation within reasonable bounds")
except Exception as e:
    print(f"Exception: {e}")
print()

# Test 4: Negative interest rate (edge case)
print("TEST 4: Negative Interest Rate")
print("-" * 70)
validation = validate_inputs(200000, -5, 30)
if validation['isValid']:
    print(f"❌ VULNERABILITY: Accepts negative interest rate")
    vulnerabilities.append("Accepts negative interest rates")
else:
    print(f"✓ Rejects negative rate: {validation['error']}")
print()

# Test 5: Zero principal
print("TEST 5: Zero Principal")
print("-" * 70)
validation = validate_inputs(0, 5, 30)
if validation['isValid']:
    print(f"❌ VULNERABILITY: Accepts zero principal")
    vulnerabilities.append("Accepts zero principal")
else:
    print(f"✓ Rejects zero principal: {validation['error']}")
print()

# Test 6: Extremely long loan term
print("TEST 6: Extreme Loan Term (1000 years)")
print("-" * 70)
try:
    validation = validate_inputs(100000, 5, 1000)
    if validation['isValid']:
        payment = calculate_monthly_payment(100000, 5, 1000)
        schedule = generate_amortization_schedule(100000, 5, 1000, payment)
        print(f"❌ VULNERABILITY: Generates {len(schedule)} payment schedule (12000 payments)")
        print(f"   This could cause browser crash/memory issues")
        vulnerabilities.append("No limit on schedule size - DoS risk")
    else:
        print(f"✓ Rejects extreme term: {validation['error']}")
except Exception as e:
    print(f"Exception: {e}")
print()

# Test 7: Very small numbers (precision issues)
print("TEST 7: Floating Point Precision")
print("-" * 70)
principal = 0.01
rate = 0.01
years = 1
try:
    payment = calculate_monthly_payment(principal, rate, years)
    print(f"Payment for $0.01 loan: ${payment}")
    if payment == 0:
        print(f"❌ VULNERABILITY: Underflow to zero")
        vulnerabilities.append("Floating point underflow")
    else:
        print(f"✓ Handles small numbers")
except Exception as e:
    print(f"Exception: {e}")
print()

# Test 8: Extremely high interest rate
print("TEST 8: Extreme Interest Rate (1000%)")
print("-" * 70)
validation = validate_inputs(100000, 1000, 30)
if validation['isValid']:
    try:
        payment = calculate_monthly_payment(100000, 1000, 30)
        print(f"❌ VULNERABILITY: Accepts 1000% interest, payment: ${payment:,.2f}")
        vulnerabilities.append("No reasonable upper limit on interest rate")
    except Exception as e:
        print(f"Calculation exception: {e}")
else:
    print(f"✓ Rejects extreme rate: {validation['error']}")
print()

# Test 9: Rounding errors accumulation
print("TEST 9: Rounding Error Accumulation")
print("-" * 70)
principal = 100000
rate = 5.5555555
years = 30
payment = calculate_monthly_payment(principal, rate, years)
schedule = generate_amortization_schedule(principal, rate, years, payment)
final_balance = schedule[-1]['remainingBalance']
if final_balance > 1.0:
    print(f"❌ VULNERABILITY: Final balance is ${final_balance:.2f}, should be $0.00")
    vulnerabilities.append("Rounding errors accumulate in amortization")
else:
    print(f"✓ Final balance within tolerance: ${final_balance:.10f}")
print()

# Test 10: Decimal injection in years
print("TEST 10: Decimal Years (should be integer)")
print("-" * 70)
validation = validate_inputs(100000, 5, 30.5)
payment = calculate_monthly_payment(100000, 5, 30.5)
months = 30.5 * 12
print(f"30.5 years = {months} months (366 payments)")
print(f"✓ Note: App accepts decimal years - may be intentional")
print()

# SUMMARY
print("=" * 70)
print("VULNERABILITY SUMMARY")
print("=" * 70)
if vulnerabilities:
    print(f"Found {len(vulnerabilities)} vulnerabilities:\n")
    for i, vuln in enumerate(vulnerabilities, 1):
        print(f"{i}. {vuln}")
else:
    print("✓ No critical vulnerabilities found")
print()
