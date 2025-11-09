import {
  calculateMonthlyPayment,
  calculateTotalPaid,
  calculateTotalInterest,
  generateAmortizationSchedule
} from './calculator.js';
import { getStateSalesTax } from '../services/taxService.js';

export function normalizeTaxRate(rawRate) {
  const rateNum = Number(rawRate);
  if (!Number.isFinite(rateNum) || rateNum <= 0) {
    return 0;
  }
  // Providers might return decimal (0.065) or percent (6.5)
  return rateNum > 1 ? rateNum / 100 : rateNum;
}

export async function computeLoanDetails(loanData, taxLookup = getStateSalesTax) {
  const principal = Number(loanData.principal);
  const annualRate = Number(loanData.annualRate);
  const years = Number(loanData.years);
  const stateCode = loanData.stateCode || '';
  const includeSalesTax = !!loanData.includeSalesTax;

  let taxRate = 0;
  let taxAmount = 0;

  if (includeSalesTax && stateCode && typeof taxLookup === 'function') {
    try {
      const taxInfo = await taxLookup(stateCode);
      taxRate = normalizeTaxRate(taxInfo?.rate);
      taxAmount = principal * taxRate;
    } catch (error) {
      taxRate = 0;
      taxAmount = 0;
    }
  }

  const financedPrincipal = principal + taxAmount;
  const monthlyPayment = calculateMonthlyPayment(financedPrincipal, annualRate, years);
  const totalPaid = calculateTotalPaid(monthlyPayment, years);
  const totalInterest = calculateTotalInterest(totalPaid, financedPrincipal);
  const schedule = generateAmortizationSchedule(financedPrincipal, annualRate, years, monthlyPayment);

  return {
    loanInfo: {
      principal,
      financedPrincipal,
      annualRate,
      years,
      stateCode,
      includeSalesTax,
      taxRate,
      taxAmount
    },
    results: {
      monthlyPayment,
      totalPaid,
      totalInterest
    },
    schedule
  };
}

