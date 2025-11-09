<template>
  <div class="input-form">
    <div class="form-header">
      <p class="eyebrow">Loan inputs</p>
      <h1>Amortization calculator</h1>
      <p class="subhead">Ground your payment assumptions with structured inputs and instant feedback.</p>
    </div>

    <form @submit.prevent="handleSubmit">
      <div class="form-grid">
        <div class="form-group">
          <label for="principal">Loan Amount ($)</label>
          <input
            id="principal"
            v-model.number="loanData.principal"
            type="number"
            step="0.01"
            placeholder="e.g., 425000"
            required
          />
        </div>

        <div class="form-group">
          <label for="rate">Interest Rate (%)</label>
          <input
            id="rate"
            v-model.number="loanData.annualRate"
            type="number"
            step="0.01"
            placeholder="e.g., 6.5"
            required
          />
        </div>

        <div class="form-group">
          <label for="years">Loan Term (Years)</label>
          <input
            id="years"
            v-model.number="loanData.years"
            type="number"
            step="1"
            placeholder="e.g., 30"
            required
          />
        </div>

        <div class="form-group">
          <label for="state">State</label>
          <select id="state" v-model="loanData.stateCode">
            <option value="">Select state</option>
            <option v-for="s in states" :key="s.code" :value="s.code">
              {{ s.code }} - {{ s.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="form-group checkbox-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="loanData.includeSalesTax" />
          Include state sales tax in loan
        </label>
        <small class="help-text">If checked, we apply the state average sales tax to your financed amount.</small>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <div class="actions">
        <button type="submit" class="calculate-btn">Run amortization</button>

        <button v-if="showReset" type="button" class="reset-btn" @click="handleReset">
          Reset
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { listStates } from '../services/taxService';
export default {
  name: 'LoanInputForm',
  props: {
    showReset: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      loanData: {
        principal: null,
        annualRate: null,
        years: null,
        stateCode: '',
        includeSalesTax: false
      },
      errorMessage: ''
    };
  },
  computed: {
    states() {
      return listStates();
    }
  },
  methods: {
    handleSubmit() {
      this.errorMessage = '';
      this.$emit('calculate', this.loanData);
    },
    handleReset() {
      this.loanData = {
        principal: null,
        annualRate: null,
        years: null,
        stateCode: '',
        includeSalesTax: false
      };
      this.errorMessage = '';
      this.$emit('reset');
    },
    setError(message) {
      this.errorMessage = message;
    }
  }
};
</script>

<style scoped>
.input-form {
  width: 100%;
  padding: 32px;
}

.form-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 24px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.75rem;
  color: #667085;
}

h1 {
  font-size: 2rem;
  color: #0f172a;
}

.subhead {
  color: #475467;
  max-width: 420px;
  font-size: 0.95rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  color: #0f172a;
  font-weight: 600;
  font-size: 0.95rem;
}

input,
select {
  width: 100%;
  padding: 14px 16px;
  font-size: 1rem;
  border: 1px solid #d0d5dd;
  border-radius: 14px;
  transition: border 0.2s ease, box-shadow 0.2s ease;
  background: #fcfdff;
}

input:focus,
select:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.checkbox-group {
  padding: 18px;
  border: 1px dashed #d0d5dd;
  border-radius: 18px;
  background: #f8fafc;
  gap: 12px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 12px;
  font-weight: 600;
  color: #0f172a;
}

.checkbox-label input {
  width: auto;
  accent-color: #111827;
}

.help-text {
  color: #475467;
  font-size: 0.85rem;
}

.error-message {
  border-radius: 16px;
  padding: 14px 18px;
  background: #fef3f2;
  color: #b42318;
  border: 1px solid #fecdca;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.calculate-btn,
.reset-btn {
  width: 100%;
  padding: 16px;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.calculate-btn {
  background: #111827;
  color: #ffffff;
  box-shadow: 0 12px 20px rgba(15, 23, 42, 0.2);
}

.calculate-btn:hover {
  transform: translateY(-1px);
}

.reset-btn {
  background: #f3f4f6;
  color: #0f172a;
}

@media (max-width: 640px) {
  .input-form {
    padding: 24px;
  }

  h1 {
    font-size: 1.6rem;
  }
}
</style>
