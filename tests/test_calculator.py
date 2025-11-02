"""
Unit tests for amortization calculator functions
"""

import unittest
from calculator import (
    calculate_monthly_payment,
    calculate_total_paid,
    calculate_total_interest,
    generate_amortization_schedule,
    validate_inputs
)


class TestCalculateMonthlyPayment(unittest.TestCase):
    """Test cases for calculate_monthly_payment function"""

    def test_standard_loan(self):
        """Test with standard loan parameters"""
        # $200,000 loan at 5% for 30 years
        payment = calculate_monthly_payment(200000, 5, 30)
        self.assertAlmostEqual(payment, 1073.64, places=2)

    def test_zero_interest(self):
        """Test with 0% interest rate"""
        payment = calculate_monthly_payment(120000, 0, 10)
        expected = 120000 / (10 * 12)
        self.assertAlmostEqual(payment, expected, places=2)

    def test_short_term_loan(self):
        """Test with short-term loan"""
        # $10,000 loan at 6% for 2 years
        payment = calculate_monthly_payment(10000, 6, 2)
        self.assertAlmostEqual(payment, 443.21, places=2)

    def test_high_interest_rate(self):
        """Test with high interest rate"""
        # $50,000 loan at 15% for 5 years
        payment = calculate_monthly_payment(50000, 15, 5)
        self.assertAlmostEqual(payment, 1189.50, places=2)

    def test_large_loan(self):
        """Test with large loan amount"""
        # $1,000,000 loan at 4% for 30 years
        payment = calculate_monthly_payment(1000000, 4, 30)
        self.assertAlmostEqual(payment, 4774.15, places=2)


class TestCalculateTotalPaid(unittest.TestCase):
    """Test cases for calculate_total_paid function"""

    def test_standard_calculation(self):
        """Test total paid calculation"""
        monthly_payment = 1073.64
        years = 30
        total = calculate_total_paid(monthly_payment, years)
        expected = 1073.64 * 30 * 12
        self.assertAlmostEqual(total, expected, places=2)

    def test_short_term(self):
        """Test with short term"""
        monthly_payment = 500
        years = 5
        total = calculate_total_paid(monthly_payment, years)
        self.assertEqual(total, 30000)


class TestCalculateTotalInterest(unittest.TestCase):
    """Test cases for calculate_total_interest function"""

    def test_interest_calculation(self):
        """Test total interest calculation"""
        total_paid = 386510.40
        principal = 200000
        interest = calculate_total_interest(total_paid, principal)
        self.assertAlmostEqual(interest, 186510.40, places=2)

    def test_zero_interest(self):
        """Test with zero interest scenario"""
        principal = 100000
        total_paid = principal
        interest = calculate_total_interest(total_paid, principal)
        self.assertEqual(interest, 0)


class TestGenerateAmortizationSchedule(unittest.TestCase):
    """Test cases for generate_amortization_schedule function"""

    def test_schedule_length(self):
        """Test that schedule has correct number of payments"""
        principal = 100000
        annual_rate = 5
        years = 10
        monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
        schedule = generate_amortization_schedule(principal, annual_rate, years, monthly_payment)

        self.assertEqual(len(schedule), 120)  # 10 years * 12 months

    def test_first_payment(self):
        """Test first payment details"""
        principal = 200000
        annual_rate = 5
        years = 30
        monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
        schedule = generate_amortization_schedule(principal, annual_rate, years, monthly_payment)

        first_payment = schedule[0]
        self.assertEqual(first_payment['paymentNumber'], 1)
        self.assertAlmostEqual(first_payment['paymentAmount'], monthly_payment, places=2)
        # First payment should have higher interest than principal
        self.assertGreater(first_payment['interestPayment'], first_payment['principalPayment'])

    def test_last_payment(self):
        """Test last payment has zero balance"""
        principal = 100000
        annual_rate = 6
        years = 15
        monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
        schedule = generate_amortization_schedule(principal, annual_rate, years, monthly_payment)

        last_payment = schedule[-1]
        self.assertEqual(last_payment['paymentNumber'], 180)  # 15 years * 12
        self.assertAlmostEqual(last_payment['remainingBalance'], 0, places=2)

    def test_balance_decreases(self):
        """Test that balance decreases with each payment"""
        principal = 50000
        annual_rate = 4
        years = 5
        monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
        schedule = generate_amortization_schedule(principal, annual_rate, years, monthly_payment)

        for i in range(len(schedule) - 1):
            self.assertGreater(
                schedule[i]['remainingBalance'],
                schedule[i + 1]['remainingBalance']
            )

    def test_payment_breakdown(self):
        """Test that payment = principal + interest for each payment"""
        principal = 150000
        annual_rate = 5.5
        years = 20
        monthly_payment = calculate_monthly_payment(principal, annual_rate, years)
        schedule = generate_amortization_schedule(principal, annual_rate, years, monthly_payment)

        for payment in schedule:
            total = payment['principalPayment'] + payment['interestPayment']
            self.assertAlmostEqual(total, payment['paymentAmount'], places=2)


class TestValidateInputs(unittest.TestCase):
    """Test cases for validate_inputs function"""

    def test_valid_inputs(self):
        """Test with valid inputs"""
        result = validate_inputs(200000, 5, 30)
        self.assertTrue(result['isValid'])
        self.assertIsNone(result['error'])

    def test_zero_principal(self):
        """Test with zero principal"""
        result = validate_inputs(0, 5, 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan amount must be greater than 0')

    def test_negative_principal(self):
        """Test with negative principal"""
        result = validate_inputs(-10000, 5, 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan amount must be greater than 0')

    def test_negative_rate(self):
        """Test with negative interest rate"""
        result = validate_inputs(200000, -1, 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Interest rate must be 0 or greater')

    def test_zero_years(self):
        """Test with zero years"""
        result = validate_inputs(200000, 5, 0)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan term must be greater than 0')

    def test_negative_years(self):
        """Test with negative years"""
        result = validate_inputs(200000, 5, -10)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan term must be greater than 0')

    def test_excessive_principal(self):
        """Test with excessively large principal"""
        result = validate_inputs(200000000, 5, 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan amount seems too large')

    def test_excessive_rate(self):
        """Test with excessively high interest rate"""
        result = validate_inputs(200000, 150, 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Interest rate seems too high')

    def test_excessive_years(self):
        """Test with excessively long term"""
        result = validate_inputs(200000, 5, 100)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan term seems too long')

    def test_zero_interest_valid(self):
        """Test that 0% interest is valid"""
        result = validate_inputs(100000, 0, 10)
        self.assertTrue(result['isValid'])
        self.assertIsNone(result['error'])


class TestSecurityVulnerabilities(unittest.TestCase):
    """Security regression tests for discovered vulnerabilities"""

    def test_infinity_principal_rejected(self):
        """Regression test: Infinity principal must be rejected"""
        result = validate_inputs(float('inf'), 5, 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan amount must be a valid number')

    def test_infinity_rate_rejected(self):
        """Regression test: Infinity rate must be rejected"""
        result = validate_inputs(200000, float('inf'), 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Interest rate must be a valid number')

    def test_infinity_years_rejected(self):
        """Regression test: Infinity years must be rejected"""
        result = validate_inputs(200000, 5, float('inf'))
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan term must be a valid number')

    def test_nan_principal_rejected(self):
        """Regression test: NaN principal must be rejected"""
        result = validate_inputs(float('nan'), 5, 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan amount must be a valid number')

    def test_nan_rate_rejected(self):
        """Regression test: NaN rate must be rejected"""
        result = validate_inputs(200000, float('nan'), 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Interest rate must be a valid number')

    def test_nan_years_rejected(self):
        """Regression test: NaN years must be rejected"""
        result = validate_inputs(200000, 5, float('nan'))
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan term must be a valid number')

    def test_calculation_rejects_infinity(self):
        """Regression test: Calculation functions reject Infinity"""
        with self.assertRaises(ValueError):
            calculate_monthly_payment(float('inf'), 5, 30)

    def test_calculation_rejects_nan(self):
        """Regression test: Calculation functions reject NaN"""
        with self.assertRaises(ValueError):
            calculate_monthly_payment(float('nan'), 5, 30)

    def test_negative_infinity_rejected(self):
        """Test that negative infinity is also rejected"""
        result = validate_inputs(float('-inf'), 5, 30)
        self.assertFalse(result['isValid'])
        self.assertEqual(result['error'], 'Loan amount must be a valid number')


if __name__ == '__main__':
    unittest.main()
