/**
 * Professional Loan Calculator Engine
 * Advanced features: extra payments, bi-weekly, PMI, taxes, insurance
 */

/**
 * Calculate monthly mortgage payment (principal + interest only)
 */
export function calculateMonthlyPayment(principal, annualRate, years) {
  if (!Number.isFinite(principal) || !Number.isFinite(annualRate) || !Number.isFinite(years)) {
    throw new Error('Invalid input: All parameters must be finite numbers');
  }

  const monthlyRate = annualRate / 100 / 12;
  const numberOfPayments = years * 12;

  if (annualRate === 0) {
    return principal / numberOfPayments;
  }

  return principal *
    (monthlyRate * Math.pow(1 + monthlyRate, numberOfPayments)) /
    (Math.pow(1 + monthlyRate, numberOfPayments) - 1);
}

/**
 * Calculate total monthly payment including all costs
 */
export function calculateTotalMonthlyPayment(params) {
  const {
    principal,
    annualRate,
    years,
    propertyTax = 0,
    homeInsurance = 0,
    pmi = 0,
    hoaFees = 0,
  } = params;

  const principalAndInterest = calculateMonthlyPayment(principal, annualRate, years);

  return {
    principalAndInterest,
    propertyTax: propertyTax / 12,
    homeInsurance: homeInsurance / 12,
    pmi,
    hoaFees,
    total: principalAndInterest + (propertyTax / 12) + (homeInsurance / 12) + pmi + hoaFees
  };
}

/**
 * Calculate PMI (typically 0.5% - 1% of loan amount annually if down payment < 20%)
 */
export function calculatePMI(homePrice, downPayment, pmiRate = 0.5) {
  const loanAmount = homePrice - downPayment;
  const ltv = (loanAmount / homePrice) * 100;

  if (ltv <= 80) {
    return 0; // No PMI needed
  }

  return (loanAmount * (pmiRate / 100)) / 12; // Monthly PMI
}

/**
 * Generate advanced amortization schedule with extra payments
 */
export function generateAdvancedSchedule(params) {
  const {
    principal,
    annualRate,
    years,
    extraPayment = 0,
    extraPaymentFrequency = 'monthly', // 'monthly', 'yearly', 'once'
    extraPaymentStartMonth = 1,
  } = params;

  const monthlyRate = annualRate / 100 / 12;
  const basePayment = calculateMonthlyPayment(principal, annualRate, years);
  let balance = principal;
  const schedule = [];
  let month = 1;
  let totalInterest = 0;
  let totalPrincipal = 0;

  while (balance > 0) {
    const interestPayment = balance * monthlyRate;
    let principalPayment = basePayment - interestPayment;

    // Add extra payment
    let currentExtraPayment = 0;
    if (month >= extraPaymentStartMonth) {
      if (extraPaymentFrequency === 'monthly') {
        currentExtraPayment = extraPayment;
      } else if (extraPaymentFrequency === 'yearly' && (month - extraPaymentStartMonth) % 12 === 0) {
        currentExtraPayment = extraPayment;
      } else if (extraPaymentFrequency === 'once' && month === extraPaymentStartMonth) {
        currentExtraPayment = extraPayment;
      }
    }

    principalPayment += currentExtraPayment;

    // Don't overpay
    if (principalPayment > balance) {
      principalPayment = balance;
      currentExtraPayment = principalPayment - (basePayment - interestPayment);
    }

    balance -= principalPayment;
    totalInterest += interestPayment;
    totalPrincipal += principalPayment;

    schedule.push({
      month,
      payment: interestPayment + principalPayment,
      principalPayment,
      interestPayment,
      extraPayment: currentExtraPayment,
      balance: Math.max(0, balance),
      cumulativeInterest: totalInterest,
      cumulativePrincipal: totalPrincipal,
    });

    month++;

    // Safety check
    if (month > years * 12 * 2) break;
  }

  return {
    schedule,
    totalMonths: schedule.length,
    totalInterest,
    totalPrincipal,
    totalPaid: totalInterest + totalPrincipal,
    monthsSaved: (years * 12) - schedule.length,
    interestSaved: (basePayment * years * 12) - principal - totalInterest,
  };
}

/**
 * Calculate bi-weekly payment plan
 */
export function calculateBiWeeklyPlan(principal, annualRate, years) {
  const monthlyPayment = calculateMonthlyPayment(principal, annualRate, years);
  const biWeeklyPayment = monthlyPayment / 2;

  // Bi-weekly means 26 payments per year (not 24)
  const biWeeklyRate = annualRate / 100 / 26;
  let balance = principal;
  let totalInterest = 0;
  let paymentNumber = 0;

  while (balance > 0 && paymentNumber < years * 26 * 2) {
    const interestPayment = balance * biWeeklyRate;
    let principalPayment = biWeeklyPayment - interestPayment;

    if (principalPayment > balance) {
      principalPayment = balance;
    }

    balance -= principalPayment;
    totalInterest += interestPayment;
    paymentNumber++;
  }

  return {
    biWeeklyPayment,
    totalPayments: paymentNumber,
    yearsToPayoff: paymentNumber / 26,
    totalInterest,
    totalPaid: principal + totalInterest,
    comparedToMonthly: {
      monthlyPayment,
      monthlyTotalInterest: (monthlyPayment * years * 12) - principal,
      interestSaved: ((monthlyPayment * years * 12) - principal) - totalInterest,
      timeSaved: years - (paymentNumber / 26),
    }
  };
}

/**
 * Compare two loan scenarios
 */
export function compareLoanScenarios(loan1, loan2) {
  const schedule1 = generateAdvancedSchedule(loan1);
  const schedule2 = generateAdvancedSchedule(loan2);

  return {
    loan1: {
      ...loan1,
      ...schedule1,
      monthlyPayment: calculateMonthlyPayment(loan1.principal, loan1.annualRate, loan1.years),
    },
    loan2: {
      ...loan2,
      ...schedule2,
      monthlyPayment: calculateMonthlyPayment(loan2.principal, loan2.annualRate, loan2.years),
    },
    comparison: {
      paymentDifference: Math.abs(
        calculateMonthlyPayment(loan1.principal, loan1.annualRate, loan1.years) -
        calculateMonthlyPayment(loan2.principal, loan2.annualRate, loan2.years)
      ),
      interestDifference: Math.abs(schedule1.totalInterest - schedule2.totalInterest),
      timeDifference: Math.abs(schedule1.totalMonths - schedule2.totalMonths),
      totalCostDifference: Math.abs(schedule1.totalPaid - schedule2.totalPaid),
    }
  };
}

/**
 * Calculate refinance savings
 */
export function calculateRefinanceSavings(currentLoan, newLoan, closingCosts = 0) {
  const currentSchedule = generateAdvancedSchedule(currentLoan);
  const newSchedule = generateAdvancedSchedule(newLoan);

  const currentRemainingCost = currentSchedule.totalPaid - (currentSchedule.schedule[currentLoan.monthsPaid || 0]?.cumulativePrincipal || 0);
  const newTotalCost = newSchedule.totalPaid + closingCosts;

  return {
    currentMonthlyPayment: calculateMonthlyPayment(currentLoan.principal, currentLoan.annualRate, currentLoan.years),
    newMonthlyPayment: calculateMonthlyPayment(newLoan.principal, newLoan.annualRate, newLoan.years),
    monthlySavings: calculateMonthlyPayment(currentLoan.principal, currentLoan.annualRate, currentLoan.years) -
                    calculateMonthlyPayment(newLoan.principal, newLoan.annualRate, newLoan.years),
    totalSavings: currentRemainingCost - newTotalCost,
    breakEvenMonths: closingCosts / (calculateMonthlyPayment(currentLoan.principal, currentLoan.annualRate, currentLoan.years) -
                                     calculateMonthlyPayment(newLoan.principal, newLoan.annualRate, newLoan.years)),
    worthRefinancing: (currentRemainingCost - newTotalCost) > 0,
  };
}

/**
 * Validate all inputs
 */
export function validateAdvancedInputs(params) {
  const {
    principal,
    annualRate,
    years,
    propertyTax = 0,
    homeInsurance = 0,
    pmi = 0,
    extraPayment = 0,
  } = params;

  // Check for invalid numeric values
  if (!Number.isFinite(principal)) {
    return { isValid: false, error: 'Loan amount must be a valid number' };
  }

  if (!Number.isFinite(annualRate)) {
    return { isValid: false, error: 'Interest rate must be a valid number' };
  }

  if (!Number.isFinite(years)) {
    return { isValid: false, error: 'Loan term must be a valid number' };
  }

  // Check for positive values
  if (principal <= 0) {
    return { isValid: false, error: 'Loan amount must be greater than 0' };
  }

  if (annualRate < 0) {
    return { isValid: false, error: 'Interest rate must be 0 or greater' };
  }

  if (years <= 0) {
    return { isValid: false, error: 'Loan term must be greater than 0' };
  }

  // Check for reasonable upper limits
  if (principal > 100000000) {
    return { isValid: false, error: 'Loan amount seems too large' };
  }

  if (annualRate > 100) {
    return { isValid: false, error: 'Interest rate seems too high' };
  }

  if (years > 50) {
    return { isValid: false, error: 'Loan term seems too long' };
  }

  // Validate optional fields
  if (propertyTax < 0 || homeInsurance < 0 || pmi < 0 || extraPayment < 0) {
    return { isValid: false, error: 'Additional costs must be 0 or greater' };
  }

  return { isValid: true, error: null };
}

/**
 * Format currency
 */
export function formatCurrency(value, decimals = 2) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

/**
 * Format percentage
 */
export function formatPercent(value, decimals = 2) {
  return `${value.toFixed(decimals)}%`;
}
