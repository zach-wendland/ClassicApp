import { describe, it, expect } from 'vitest';
import { computeLoanDetails, normalizeTaxRate } from '../../src/utils/loanProcessor.js';

describe('normalizeTaxRate', () => {
  it('handles decimal input', () => {
    expect(normalizeTaxRate(0.07)).toBe(0.07);
  });

  it('converts percentage input', () => {
    expect(normalizeTaxRate(7)).toBeCloseTo(0.07, 4);
  });

  it('guards against invalid values', () => {
    expect(normalizeTaxRate(null)).toBe(0);
    expect(normalizeTaxRate(-1)).toBe(0);
  });
});

describe('computeLoanDetails', () => {
  const baseLoan = {
    principal: 200000,
    annualRate: 5,
    years: 30,
    stateCode: '',
    includeSalesTax: false
  };

  it('returns expected structure without tax', async () => {
    const result = await computeLoanDetails(baseLoan, () => Promise.resolve({ rate: 0 }));
    expect(result.loanInfo.financedPrincipal).toBeCloseTo(200000, 2);
    expect(result.results.monthlyPayment).toBeCloseTo(1073.64, 2);
    expect(result.schedule).toHaveLength(360);
  });

  it('adds tax when requested', async () => {
    const result = await computeLoanDetails(
      { ...baseLoan, includeSalesTax: true, stateCode: 'WA' },
      () => Promise.resolve({ rate: 0.065 })
    );

    expect(result.loanInfo.taxAmount).toBeCloseTo(13000, 2);
    expect(result.loanInfo.financedPrincipal).toBeCloseTo(213000, 2);
    expect(result.results.monthlyPayment).toBeGreaterThan(1073.64);
  });

  it('normalizes percent-based provider rates', async () => {
    const result = await computeLoanDetails(
      { ...baseLoan, includeSalesTax: true, stateCode: 'TX' },
      () => Promise.resolve({ rate: 6.25 })
    );

    expect(result.loanInfo.taxRate).toBeCloseTo(0.0625, 4);
  });

  it('falls back when tax lookup fails', async () => {
    const failingLookup = () => Promise.reject(new Error('fail'));
    const result = await computeLoanDetails(
      { ...baseLoan, includeSalesTax: true, stateCode: 'CA' },
      failingLookup
    );

    expect(result.loanInfo.taxAmount).toBe(0);
    expect(result.loanInfo.financedPrincipal).toBe(baseLoan.principal);
  });
});
