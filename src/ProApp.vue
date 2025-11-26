<template>
  <div id="pro-app" :class="{ 'dark': darkMode }" class="min-h-screen transition-colors duration-300">
    <!-- Header -->
    <header class="glass-card m-4 p-4 animate-slide-down">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <div>
            <h1 class="text-2xl font-bold text-gradient">Pro Loan Calculator</h1>
            <p class="text-sm text-slate-600 dark:text-slate-400">Professional Financial Analysis Suite</p>
          </div>
        </div>

        <!-- Dark Mode Toggle -->
        <button
          @click="toggleDarkMode"
          class="p-3 rounded-xl bg-slate-200 dark:bg-slate-700 hover:scale-110 transition-transform"
          :title="darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        >
          <svg v-if="!darkMode" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
          <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </button>
      </div>
    </header>

    <main class="max-w-7xl mx-auto p-4 space-y-6">
      <!-- Quick Stats -->
      <div v-if="calculated" class="grid grid-cols-1 md:grid-cols-4 gap-4 animate-slide-up">
        <div class="stat-card">
          <div class="text-sm text-slate-600 dark:text-slate-400 font-medium mb-1">Monthly Payment</div>
          <div class="text-3xl font-bold text-gradient">{{ formatCurrency(results.monthlyPayment) }}</div>
        </div>
        <div class="stat-card">
          <div class="text-sm text-slate-600 dark:text-slate-400 font-medium mb-1">Total Interest</div>
          <div class="text-2xl font-bold text-warning-600">{{ formatCurrency(schedule.totalInterest) }}</div>
        </div>
        <div class="stat-card">
          <div class="text-sm text-slate-600 dark:text-slate-400 font-medium mb-1">Total Paid</div>
          <div class="text-2xl font-bold text-slate-700 dark:text-slate-200">{{ formatCurrency(schedule.totalPaid) }}</div>
        </div>
        <div class="stat-card">
          <div class="text-sm text-slate-600 dark:text-slate-400 font-medium mb-1">Months to Payoff</div>
          <div class="text-2xl font-bold text-success-600">{{ schedule.totalMonths }}</div>
          <div class="text-xs text-slate-500">{{ (schedule.totalMonths / 12).toFixed(1) }} years</div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Input Form (Left Column) -->
        <div class="lg:col-span-1 space-y-4">
          <div class="glass-card p-6 animate-fade-in">
            <h2 class="text-xl font-bold mb-6 flex items-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
              Loan Details
            </h2>

            <!-- Loan Amount -->
            <div class="mb-6">
              <label class="block text-sm font-semibold mb-2">Loan Amount</label>
              <input
                v-model.number="loanData.principal"
                type="number"
                class="input-field"
                placeholder="300,000"
                @input="calculate"
              />
              <input
                v-model.number="loanData.principal"
                type="range"
                min="10000"
                max="2000000"
                step="10000"
                class="w-full mt-2"
                @input="calculate"
              />
              <div class="text-xs text-slate-500 mt-1">{{ formatCurrency(loanData.principal || 0) }}</div>
            </div>

            <!-- Interest Rate -->
            <div class="mb-6">
              <label class="block text-sm font-semibold mb-2">Interest Rate (%)</label>
              <input
                v-model.number="loanData.annualRate"
                type="number"
                step="0.01"
                class="input-field"
                placeholder="6.5"
                @input="calculate"
              />
              <input
                v-model.number="loanData.annualRate"
                type="range"
                min="0"
                max="20"
                step="0.1"
                class="w-full mt-2"
                @input="calculate"
              />
              <div class="text-xs text-slate-500 mt-1">{{ formatPercent(loanData.annualRate || 0) }}</div>
            </div>

            <!-- Loan Term -->
            <div class="mb-6">
              <label class="block text-sm font-semibold mb-2">Loan Term (Years)</label>
              <input
                v-model.number="loanData.years"
                type="number"
                class="input-field"
                placeholder="30"
                @input="calculate"
              />
              <input
                v-model.number="loanData.years"
                type="range"
                min="1"
                max="40"
                step="1"
                class="w-full mt-2"
                @input="calculate"
              />
              <div class="text-xs text-slate-500 mt-1">{{ loanData.years || 0 }} years</div>
            </div>

            <!-- Extra Payment -->
            <div class="mb-6">
              <label class="block text-sm font-semibold mb-2 flex items-center">
                <span class="mr-2">💰 Extra Monthly Payment</span>
                <span class="text-xs font-normal text-slate-500">(Optional)</span>
              </label>
              <input
                v-model.number="loanData.extraPayment"
                type="number"
                class="input-field"
                placeholder="0"
                @input="calculate"
              />
              <input
                v-model.number="loanData.extraPayment"
                type="range"
                min="0"
                max="5000"
                step="50"
                class="w-full mt-2"
                @input="calculate"
              />
              <div class="text-xs text-slate-500 mt-1">{{ formatCurrency(loanData.extraPayment || 0) }}</div>
            </div>

            <!-- Calculate Button -->
            <button @click="calculate" class="btn-primary w-full">
              <svg class="w-5 h-5 inline-block mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              Calculate Loan
            </button>

            <!-- Error Message -->
            <div v-if="error" class="mt-4 p-4 bg-red-100 dark:bg-red-900/30 border-2 border-red-400 dark:border-red-700 rounded-xl text-red-700 dark:text-red-300 animate-scale-in">
              {{ error }}
            </div>
          </div>
        </div>

        <!-- Results (Right Columns) -->
        <div v-if="calculated" class="lg:col-span-2 space-y-6 animate-fade-in">
          <!-- Savings Summary (if extra payment) -->
          <div v-if="loanData.extraPayment > 0" class="glass-card p-6 bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 border-2 border-green-200 dark:border-green-800">
            <h3 class="text-lg font-bold mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
              Extra Payment Impact
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="text-sm text-slate-600 dark:text-slate-400">Interest Saved</div>
                <div class="text-2xl font-bold text-green-600">{{ formatCurrency(schedule.interestSaved) }}</div>
              </div>
              <div>
                <div class="text-sm text-slate-600 dark:text-slate-400">Time Saved</div>
                <div class="text-2xl font-bold text-green-600">{{ schedule.monthsSaved }} months</div>
                <div class="text-xs text-slate-500">{{ (schedule.monthsSaved / 12).toFixed(1) }} years</div>
              </div>
            </div>
          </div>

          <!-- Payment Breakdown Table -->
          <div class="glass-card p-6">
            <h3 class="text-lg font-bold mb-4">📊 Payment Schedule (First Year)</h3>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead class="bg-slate-100 dark:bg-slate-800">
                  <tr>
                    <th class="px-4 py-2 text-left">Month</th>
                    <th class="px-4 py-2 text-right">Payment</th>
                    <th class="px-4 py-2 text-right">Principal</th>
                    <th class="px-4 py-2 text-right">Interest</th>
                    <th class="px-4 py-2 text-right">Balance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="payment in schedule.schedule.slice(0, 12)" :key="payment.month" class="border-b border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                    <td class="px-4 py-2">{{ payment.month }}</td>
                    <td class="px-4 py-2 text-right font-semibold">{{ formatCurrency(payment.payment) }}</td>
                    <td class="px-4 py-2 text-right text-green-600">{{ formatCurrency(payment.principalPayment) }}</td>
                    <td class="px-4 py-2 text-right text-orange-600">{{ formatCurrency(payment.interestPayment) }}</td>
                    <td class="px-4 py-2 text-right">{{ formatCurrency(payment.balance) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="mt-4 text-center">
              <button @click="showFullSchedule = !showFullSchedule" class="btn-secondary text-sm">
                {{ showFullSchedule ? 'Show Less' : 'Show Full Schedule' }}
              </button>
            </div>
          </div>

          <!-- Full Schedule (expandable) -->
          <div v-if="showFullSchedule" class="glass-card p-6 max-h-96 overflow-y-auto animate-slide-down">
            <h3 class="text-lg font-bold mb-4 sticky top-0 bg-white dark:bg-slate-800 pb-2">📋 Complete Payment Schedule</h3>
            <div class="space-y-1">
              <div v-for="payment in schedule.schedule" :key="payment.month" class="grid grid-cols-5 gap-2 text-xs p-2 hover:bg-slate-50 dark:hover:bg-slate-800/50 rounded">
                <div>Month {{ payment.month }}</div>
                <div class="text-right font-semibold">{{ formatCurrency(payment.payment) }}</div>
                <div class="text-right text-green-600">{{ formatCurrency(payment.principalPayment) }}</div>
                <div class="text-right text-orange-600">{{ formatCurrency(payment.interestPayment) }}</div>
                <div class="text-right">{{ formatCurrency(payment.balance) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="glass-card m-4 mt-8 p-4 text-center text-sm text-slate-600 dark:text-slate-400">
      <p>Professional Loan Calculator v3.0 • Built with Vue 3 + TailwindCSS • All calculations performed locally</p>
    </footer>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue';
import {
  calculateMonthlyPayment,
  generateAdvancedSchedule,
  validateAdvancedInputs,
  formatCurrency,
  formatPercent,
} from './utils/advancedCalculator';

export default {
  name: 'ProApp',
  setup() {
    const darkMode = ref(false);
    const calculated = ref(false);
    const showFullSchedule = ref(false);
    const error = ref('');

    const loanData = reactive({
      principal: 300000,
      annualRate: 6.5,
      years: 30,
      extraPayment: 0,
      extraPaymentFrequency: 'monthly',
      extraPaymentStartMonth: 1,
    });

    const results = ref({});
    const schedule = ref({});

    const toggleDarkMode = () => {
      darkMode.value = !darkMode.value;
      localStorage.setItem('darkMode', darkMode.value);
    };

    const calculate = () => {
      error.value = '';

      // Validate inputs
      const validation = validateAdvancedInputs(loanData);
      if (!validation.isValid) {
        error.value = validation.error;
        calculated.value = false;
        return;
      }

      try {
        // Calculate monthly payment
        const monthlyPayment = calculateMonthlyPayment(
          loanData.principal,
          loanData.annualRate,
          loanData.years
        );

        // Generate schedule with extra payments
        const scheduleData = generateAdvancedSchedule(loanData);

        results.value = {
          monthlyPayment,
        };

        schedule.value = scheduleData;
        calculated.value = true;
        showFullSchedule.value = false;
      } catch (err) {
        error.value = err.message;
        calculated.value = false;
      }
    };

    // Load dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
      darkMode.value = true;
    }

    // Initial calculation
    calculate();

    return {
      darkMode,
      calculated,
      showFullSchedule,
      error,
      loanData,
      results,
      schedule,
      toggleDarkMode,
      calculate,
      formatCurrency,
      formatPercent,
    };
  },
};
</script>
