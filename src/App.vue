<template>
  <div id="app">
    <LoanInputForm
      ref="inputForm"
      :show-reset="showResults"
      @calculate="handleCalculate"
      @reset="handleReset"
    />

    <div v-if="showResults" class="results-section">
      <LoanSummary :loan-info="loanInfo" :results="results" />
      <AmortizationTable :schedule="schedule" />
    </div>

    <footer v-if="!showResults">
      <p>Enter your loan details above to calculate your amortization schedule</p>
    </footer>
  </div>
</template>

<script>
import LoanInputForm from './components/LoanInputForm.vue';
import LoanSummary from './components/LoanSummary.vue';
import AmortizationTable from './components/AmortizationTable.vue';
import {
  calculateMonthlyPayment,
  calculateTotalPaid,
  calculateTotalInterest,
  generateAmortizationSchedule,
  validateInputs
} from './utils/calculator.js';

export default {
  name: 'App',
  components: {
    LoanInputForm,
    LoanSummary,
    AmortizationTable
  },
  data() {
    return {
      showResults: false,
      loanInfo: null,
      results: null,
      schedule: []
    };
  },
  methods: {
    handleCalculate(loanData) {
      const { principal, annualRate, years } = loanData;

      // Validate inputs
      const validation = validateInputs(principal, annualRate, years);
      if (!validation.isValid) {
        this.$refs.inputForm.setError(validation.error);
        return;
      }

      // Calculate results
      const monthlyPayment = calculateMonthlyPayment(principal, annualRate, years);
      const totalPaid = calculateTotalPaid(monthlyPayment, years);
      const totalInterest = calculateTotalInterest(totalPaid, principal);
      const schedule = generateAmortizationSchedule(principal, annualRate, years, monthlyPayment);

      // Store results
      this.loanInfo = { principal, annualRate, years };
      this.results = {
        monthlyPayment,
        totalPaid,
        totalInterest
      };
      this.schedule = schedule;
      this.showResults = true;

      // Scroll to results
      this.$nextTick(() => {
        const resultsSection = document.querySelector('.results-section');
        if (resultsSection) {
          resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    },
    handleReset() {
      this.showResults = false;
      this.loanInfo = null;
      this.results = null;
      this.schedule = [];
    }
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
}

.results-section {
  margin-top: 30px;
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

footer {
  text-align: center;
  margin-top: 40px;
  color: white;
  opacity: 0.9;
  font-size: 0.95rem;
}

@media (max-width: 600px) {
  body {
    padding: 10px;
  }

  .results-section {
    margin-top: 20px;
  }
}
</style>
