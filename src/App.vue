<template>
  <div id="app">
    <div class="app-shell">
      <header class="hero">
        <div class="hero-copy">
          <p class="eyebrow">Mortgage planning toolkit</p>
          <h1>Numbers-forward amortization modeling</h1>
          <p class="intro">
            Model monthly payments, taxes, and payoff timelines with plain-language outputs.
            We added live market rates so your assumptions stay grounded in reality.
          </p>
          <ul class="hero-list">
            <li>Run what-if scenarios faster than a spreadsheet.</li>
            <li>See total interest, tax adjustments, and principle paydown.</li>
            <li>Share a readable schedule with clients or teammates.</li>
          </ul>
        </div>
        <MortgageRatesPanel
          :rates="mortgageRates"
          :loading="ratesLoading"
          :error="ratesError"
          @refresh="loadMortgageRates"
        />
      </header>

      <section class="panel-card form-wrapper">
        <LoanInputForm
          ref="inputForm"
          :show-reset="showResults"
          @calculate="handleCalculate"
          @reset="handleReset"
        />
      </section>

      <section v-if="showResults" class="results-section">
        <div class="panel-card">
          <LoanSummary :loan-info="loanInfo" :results="results" />
        </div>
        <div class="panel-card table-panel">
          <AmortizationTable :schedule="schedule" />
        </div>
      </section>

      <footer v-else class="panel-card empty-state">
        <h3>Need a monthly payment fast?</h3>
        <p>
          Plug in your loan details and we will build the amortization table, blended tax impact,
          and payoff overview in one pass. No purple gradients, just numbers you can trust.
        </p>
      </footer>
    </div>
  </div>
</template>

<script>
import LoanInputForm from './components/LoanInputForm.vue';
import LoanSummary from './components/LoanSummary.vue';
import AmortizationTable from './components/AmortizationTable.vue';
import MortgageRatesPanel from './components/MortgageRatesPanel.vue';
import { computeLoanDetails } from './utils/loanProcessor.js';
import { validateInputs } from './utils/calculator.js';
import { getMortgageRates } from './services/mortgageRateService.js';

export default {
  name: 'App',
  components: {
    LoanInputForm,
    LoanSummary,
    AmortizationTable,
    MortgageRatesPanel
  },
  data() {
    return {
      showResults: false,
      loanInfo: null,
      results: null,
      schedule: [],
      mortgageRates: [],
      ratesLoading: false,
      ratesError: ''
    };
  },
  created() {
    this.loadMortgageRates();
  },
  methods: {
    async handleCalculate(loanData) {
      const { principal, annualRate, years } = loanData;

      const validation = validateInputs(principal, annualRate, years);
      if (!validation.isValid) {
        this.$refs.inputForm.setError(validation.error);
        return;
      }

      const { loanInfo, results, schedule } = await computeLoanDetails(loanData);
      this.loanInfo = loanInfo;
      this.results = results;
      this.schedule = schedule;
      this.showResults = true;

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
    },
    async loadMortgageRates() {
      this.ratesLoading = true;
      this.ratesError = '';
      try {
        this.mortgageRates = await getMortgageRates();
      } catch (error) {
        this.ratesError = error?.message || 'Unable to load mortgage rates.';
      } finally {
        this.ratesLoading = false;
      }
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
  background: #f4f5fb;
  color: #0f172a;
  min-height: 100vh;
  padding: 32px 20px 60px;
}

#app {
  width: 100%;
}

.app-shell {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.hero {
  background: #ffffff;
  border-radius: 32px;
  padding: 32px;
  border: 1px solid #f1f2f6;
  box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 32px;
  align-items: center;
}

.hero-copy {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.eyebrow {
  font-size: 0.8rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #475467;
}

h1 {
  font-size: 2.5rem;
  line-height: 1.2;
  color: #0f172a;
}

.intro {
  color: #475467;
  max-width: 520px;
}

.hero-list {
  margin-left: 18px;
  color: #1d2939;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.panel-card {
  background: #ffffff;
  border-radius: 28px;
  border: 1px solid #eceff5;
  padding: 32px;
  box-shadow: 0 25px 35px rgba(15, 23, 42, 0.06);
}

.form-wrapper {
  padding: 0;
}

.results-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
  animation: fadeIn 0.5s ease;
}

.table-panel {
  padding: 24px;
}

.empty-state {
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.empty-state h3 {
  font-size: 1.5rem;
}

.empty-state p {
  color: #475467;
  line-height: 1.6;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  body {
    padding: 20px 12px 40px;
  }

  .hero {
    padding: 24px;
  }

  .panel-card {
    padding: 24px;
  }

  h1 {
    font-size: 2rem;
  }
}
</style>
