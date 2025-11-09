<template>
  <div class="loan-summary">
    <h2>Loan Summary</h2>

    <div class="summary-grid">
      <div class="summary-card highlight">
        <div class="label">Monthly Payment</div>
        <div class="value">${{ formatCurrency(results.monthlyPayment) }}</div>
      </div>

      <div class="summary-card">
        <div class="label">Loan Amount</div>
        <div class="value">${{ formatCurrency(loanInfo.principal) }}</div>
      </div>

      <div v-if="loanInfo.includeSalesTax" class="summary-card">
        <div class="label">Financed Amount (incl. Sales Tax)</div>
        <div class="value">${{ formatCurrency(loanInfo.financedPrincipal) }}</div>
      </div>

      <div class="summary-card">
        <div class="label">Interest Rate</div>
        <div class="value">{{ loanInfo.annualRate }}%</div>
      </div>

      <div class="summary-card">
        <div class="label">Loan Term</div>
        <div class="value">{{ loanInfo.years }} years</div>
      </div>

      <div v-if="loanInfo.includeSalesTax && loanInfo.stateCode" class="summary-card">
        <div class="label">Sales Tax Rate ({{ loanInfo.stateCode }})</div>
        <div class="value">{{ (loanInfo.taxRate * 100).toFixed(2) }}%</div>
      </div>

      <div v-if="loanInfo.includeSalesTax" class="summary-card">
        <div class="label">Sales Tax Amount</div>
        <div class="value">${{ formatCurrency(loanInfo.taxAmount) }}</div>
      </div>

      <div class="summary-card">
        <div class="label">Total Paid</div>
        <div class="value">${{ formatCurrency(results.totalPaid) }}</div>
      </div>

      <div class="summary-card">
        <div class="label">Total Interest</div>
        <div class="value">${{ formatCurrency(results.totalInterest) }}</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoanSummary',
  props: {
    loanInfo: {
      type: Object,
      required: true
    },
    results: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatCurrency(value) {
      return value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }
  }
};
</script>

<style scoped>
.loan-summary {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

h2 {
  text-align: left;
  color: #0f172a;
  font-size: 1.8rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
}

.summary-card {
  border-radius: 20px;
  border: 1px solid #e4e7ec;
  padding: 20px;
  background: #f9fafb;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 140px;
}

.summary-card.highlight {
  grid-column: span 2;
  background: #111827;
  color: white;
  border-color: #111827;
}

.label {
  font-size: 0.85rem;
  letter-spacing: 0.01em;
  text-transform: uppercase;
  color: #475467;
}

.summary-card.highlight .label {
  color: rgba(255, 255, 255, 0.7);
}

.value {
  font-size: 2rem;
  font-weight: 700;
  color: #0f172a;
}

.summary-card.highlight .value {
  color: white;
  font-size: 2.5rem;
}

@media (max-width: 768px) {
  h2 {
    font-size: 1.5rem;
  }

  .summary-card.highlight {
    grid-column: span 1;
  }

  .value {
    font-size: 1.5rem;
  }

  .summary-card.highlight .value {
    font-size: 2rem;
  }
}
</style>
