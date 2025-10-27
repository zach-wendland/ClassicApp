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

      <div class="summary-card">
        <div class="label">Interest Rate</div>
        <div class="value">{{ loanInfo.annualRate }}%</div>
      </div>

      <div class="summary-card">
        <div class="label">Loan Term</div>
        <div class="value">{{ loanInfo.years }} years</div>
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
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 25px;
  font-size: 1.6rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.summary-card {
  background: white;
  border: 2px solid #ecf0f1;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  transition: transform 0.2s, box-shadow 0.2s;
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.summary-card.highlight {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  border: none;
  grid-column: span 2;
}

.label {
  font-size: 0.9rem;
  margin-bottom: 8px;
  opacity: 0.8;
  font-weight: 500;
}

.summary-card.highlight .label {
  opacity: 0.95;
}

.value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2c3e50;
}

.summary-card.highlight .value {
  font-size: 2.5rem;
  color: white;
}

@media (max-width: 600px) {
  .loan-summary {
    padding: 15px;
  }

  h2 {
    font-size: 1.4rem;
  }

  .summary-grid {
    grid-template-columns: 1fr;
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
