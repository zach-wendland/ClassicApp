"""
Python implementation of amortization calculator functions
This mirrors the JavaScript implementation for testing purposes
"""

def calculate_monthly_payment(principal, annual_rate, years):
    """
    Calculate monthly payment for a loan

    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (as percentage, e.g., 5 for 5%)
        years: Loan term in years

    Returns:
        Monthly payment amount
    """
    import math

    # Defensive check for invalid inputs
    if not isinstance(principal, (int, float)) or math.isnan(principal) or math.isinf(principal):
        raise ValueError('Invalid input: principal must be a finite number')
    if not isinstance(annual_rate, (int, float)) or math.isnan(annual_rate) or math.isinf(annual_rate):
        raise ValueError('Invalid input: annual_rate must be a finite number')
    if not isinstance(years, (int, float)) or math.isnan(years) or math.isinf(years):
        raise ValueError('Invalid input: years must be a finite number')

    monthly_rate = annual_rate / 100 / 12
    number_of_payments = years * 12

    if annual_rate == 0:
        return principal / number_of_payments

    monthly_payment = principal * \
        (monthly_rate * pow(1 + monthly_rate, number_of_payments)) / \
        (pow(1 + monthly_rate, number_of_payments) - 1)

    return monthly_payment


def calculate_total_paid(monthly_payment, years):
    """
    Calculate total amount paid over life of loan

    Args:
        monthly_payment: Monthly payment amount
        years: Loan term in years

    Returns:
        Total amount paid
    """
    return monthly_payment * years * 12


def calculate_total_interest(total_paid, principal):
    """
    Calculate total interest paid over life of loan

    Args:
        total_paid: Total amount paid
        principal: Original loan amount

    Returns:
        Total interest paid
    """
    return total_paid - principal


def generate_amortization_schedule(principal, annual_rate, years, monthly_payment):
    """
    Generate complete amortization schedule

    Args:
        principal: Loan amount
        annual_rate: Annual interest rate (as percentage)
        years: Loan term in years
        monthly_payment: Monthly payment amount

    Returns:
        List of payment dictionaries
    """
    monthly_rate = annual_rate / 100 / 12
    number_of_payments = years * 12
    remaining_balance = principal
    schedule = []

    for i in range(1, number_of_payments + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment

        # Handle final payment rounding
        if i == number_of_payments:
            remaining_balance = 0

        schedule.append({
            'paymentNumber': i,
            'paymentAmount': monthly_payment,
            'principalPayment': principal_payment,
            'interestPayment': interest_payment,
            'remainingBalance': max(0, remaining_balance)
        })

    return schedule


def validate_inputs(principal, annual_rate, years):
    """
    Validate loan inputs

    Args:
        principal: Loan amount
        annual_rate: Annual interest rate
        years: Loan term in years

    Returns:
        Dictionary with isValid flag and error message
    """
    import math

    # Check for invalid numeric values (NaN, Infinity, etc.)
    if not isinstance(principal, (int, float)) or math.isnan(principal) or math.isinf(principal):
        return {'isValid': False, 'error': 'Loan amount must be a valid number'}

    if not isinstance(annual_rate, (int, float)) or math.isnan(annual_rate) or math.isinf(annual_rate):
        return {'isValid': False, 'error': 'Interest rate must be a valid number'}

    if not isinstance(years, (int, float)) or math.isnan(years) or math.isinf(years):
        return {'isValid': False, 'error': 'Loan term must be a valid number'}

    # Check for positive values
    if principal <= 0:
        return {'isValid': False, 'error': 'Loan amount must be greater than 0'}

    if annual_rate < 0:
        return {'isValid': False, 'error': 'Interest rate must be 0 or greater'}

    if years <= 0:
        return {'isValid': False, 'error': 'Loan term must be greater than 0'}

    # Check for reasonable upper limits
    if principal > 100000000:
        return {'isValid': False, 'error': 'Loan amount seems too large'}

    if annual_rate > 100:
        return {'isValid': False, 'error': 'Interest rate seems too high'}

    if years > 50:
        return {'isValid': False, 'error': 'Loan term seems too long'}

    return {'isValid': True, 'error': None}
