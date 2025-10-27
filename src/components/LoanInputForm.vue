<template>
  <div class="input-form">
    <h1>Amortization Calculator</h1>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="principal">Loan Amount ($)</label>
        <input
          id="principal"
          v-model.number="loanData.principal"
          type="number"
          step="0.01"
          placeholder="e.g., 200000"
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
          placeholder="e.g., 5.5"
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

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <button type="submit" class="calculate-btn">Calculate</button>

      <button v-if="showReset" type="button" class="reset-btn" @click="handleReset">
        Reset
      </button>
    </form>
  </div>
</template>

<script>
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
        years: null
      },
      errorMessage: ''
    };
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
        years: null
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
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
  font-size: 1.8rem;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #34495e;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #3498db;
}

.calculate-btn,
.reset-btn {
  width: 100%;
  padding: 15px;
  font-size: 18px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.calculate-btn {
  background-color: #3498db;
  color: white;
}

.calculate-btn:hover {
  background-color: #2980b9;
}

.reset-btn {
  background-color: #95a5a6;
  color: white;
}

.reset-btn:hover {
  background-color: #7f8c8d;
}

.error-message {
  background-color: #e74c3c;
  color: white;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 15px;
  text-align: center;
}

@media (max-width: 600px) {
  .input-form {
    padding: 15px;
  }

  h1 {
    font-size: 1.5rem;
  }
}
</style>
