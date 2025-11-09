import { describe, it, expect } from 'vitest';
import {
  calculateMonthlyPayment,
  calculateTotalPaid,
  calculateTotalInterest,
  generateAmortizationSchedule,
  validateInputs
} from '../../src/utils/calculator.js';

describe('calculateMonthlyPayment', () => {
  it('computes payment for standard loan', () => {
    const payment = calculateMonthlyPayment(200000, 5, 30);
    expect(payment).toBeCloseTo(1073.64, 2);
  });

  it('handles zero interest', () => {
    const payment = calculateMonthlyPayment(120000, 0, 10);
    expect(payment).toBeCloseTo(1000, 5);
  });

  it('handles short term loans', () => {
    const payment = calculateMonthlyPayment(10000, 6, 2);
    expect(payment).toBeCloseTo(443.21, 2);
  });

  it('handles high interest', () => {
    const payment = calculateMonthlyPayment(50000, 15, 5);
    expect(payment).toBeCloseTo(1189.5, 2);
  });

  it('handles large loan', () => {
    const payment = calculateMonthlyPayment(1000000, 4, 30);
    expect(payment).toBeCloseTo(4774.15, 2);
  });
});

describe('calculateTotalPaid', () => {
  it('multiplies monthly payment by term', () => {
    const total = calculateTotalPaid(1073.64, 30);
    expect(total).toBeCloseTo(386510.4, 2);
  });

  it('handles short term', () => {
    expect(calculateTotalPaid(500, 5)).toBe(30000);
  });
});

describe('calculateTotalInterest', () => {
  it('subtracts principal from total paid', () => {
    const interest = calculateTotalInterest(386510.4, 200000);
    expect(interest).toBeCloseTo(186510.4, 2);
  });

  it('returns zero when total equals principal', () => {
    expect(calculateTotalInterest(100000, 100000)).toBe(0);
  });
});

describe('generateAmortizationSchedule', () => {
  it('creates expected number of payments', () => {
    const monthlyPayment = calculateMonthlyPayment(100000, 5, 10);
    const schedule = generateAmortizationSchedule(100000, 5, 10, monthlyPayment);
    expect(schedule).toHaveLength(120);
  });

  it('ensures principal + interest equals payment', () => {
    const monthlyPayment = calculateMonthlyPayment(150000, 5.5, 20);
    const schedule = generateAmortizationSchedule(150000, 5.5, 20, monthlyPayment);
    schedule.forEach((payment) => {
      const total = payment.principalPayment + payment.interestPayment;
      expect(total).toBeCloseTo(payment.paymentAmount, 2);
    });
  });

  it('reduces balance to zero by last payment', () => {
    const monthlyPayment = calculateMonthlyPayment(100000, 6, 15);
    const schedule = generateAmortizationSchedule(100000, 6, 15, monthlyPayment);
    expect(schedule.at(-1).remainingBalance).toBeCloseTo(0, 2);
  });
});

describe('validateInputs', () => {
  it('accepts valid inputs', () => {
    expect(validateInputs(200000, 5, 30)).toEqual({ isValid: true, error: null });
  });

  it('rejects invalid cases', () => {
    expect(validateInputs(0, 5, 30).isValid).toBe(false);
    expect(validateInputs(200000, -1, 30).isValid).toBe(false);
    expect(validateInputs(200000, 5, 0).isValid).toBe(false);
    expect(validateInputs(200000000, 5, 30).isValid).toBe(false);
    expect(validateInputs(200000, 150, 30).isValid).toBe(false);
    expect(validateInputs(200000, 5, 60).isValid).toBe(false);
  });
});
