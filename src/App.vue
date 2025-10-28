<template>
  <div id="app" ref="appContainer">
    <!-- Gesture Hint Overlay -->
    <transition name="fade">
      <div v-if="showGestureHint" class="gesture-hint">
        <div class="hint-icon">{{ gestureHintIcon }}</div>
        <div class="hint-text">{{ gestureHintText }}</div>
      </div>
    </transition>

    <LoanInputForm
      ref="inputForm"
      :show-reset="showResults"
      @calculate="handleCalculate"
      @reset="handleReset"
    />

    <div v-if="showResults" class="results-section" ref="resultsSection">
      <div class="gesture-indicator">
        <p>Swipe right to go back • Swipe down to reset</p>
      </div>
      <LoanSummary :loan-info="loanInfo" :results="results" />
      <AmortizationTable :schedule="schedule" />
    </div>

    <footer v-if="!showResults">
      <p>Enter your loan details above to calculate your amortization schedule</p>
      <p class="gesture-tip">Tip: Swipe down anywhere to reset</p>
    </footer>
  </div>
</template>

<script>
import { onMounted, onBeforeUnmount } from 'vue';
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
import { useGestures } from './utils/gestures.js';

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
      schedule: [],
      showGestureHint: false,
      gestureHintText: '',
      gestureHintIcon: '',
      gestureDetector: null
    };
  },
  mounted() {
    this.initializeGestures();
  },
  beforeUnmount() {
    this.cleanupGestures();
  },
  methods: {
    initializeGestures() {
      const { setupGestures } = useGestures();

      const callbacks = {
        onSwipeRight: () => {
          if (this.showResults) {
            this.showGestureHintMessage('←', 'Going back...');
            setTimeout(() => {
              this.handleReset();
            }, 300);
          }
        },
        onSwipeDown: () => {
          this.showGestureHintMessage('↓', 'Resetting...');
          setTimeout(() => {
            this.handleReset();
          }, 300);
        },
        onSwipeLeft: () => {
          if (this.showResults) {
            this.showGestureHintMessage('→', 'Scroll the table');
          }
        },
        onSwipeUp: () => {
          this.showGestureHintMessage('↑', 'Scrolling up...');
        }
      };

      const options = {
        minSwipeDistance: 60,
        maxSwipeTime: 500,
        swipeAngleTolerance: 35
      };

      this.gestureDetector = setupGestures(
        this.$refs.appContainer,
        callbacks,
        options
      );
    },
    cleanupGestures() {
      if (this.gestureDetector) {
        this.gestureDetector.destroy();
      }
    },
    showGestureHintMessage(icon, text) {
      this.gestureHintIcon = icon;
      this.gestureHintText = text;
      this.showGestureHint = true;

      setTimeout(() => {
        this.showGestureHint = false;
      }, 1500);
    },
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

      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
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
  touch-action: pan-y;
  -webkit-user-select: none;
  user-select: none;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}

/* Gesture Hint Overlay */
.gesture-hint {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.85);
  color: white;
  padding: 25px 40px;
  border-radius: 20px;
  text-align: center;
  z-index: 9999;
  pointer-events: none;
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.hint-icon {
  font-size: 3rem;
  margin-bottom: 10px;
  animation: pulse 0.6s ease-in-out infinite alternate;
}

.hint-text {
  font-size: 1.1rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}

@keyframes pulse {
  from {
    transform: scale(1);
    opacity: 0.8;
  }
  to {
    transform: scale(1.1);
    opacity: 1;
  }
}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Gesture Indicator */
.gesture-indicator {
  text-align: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  margin-bottom: 20px;
  backdrop-filter: blur(5px);
}

.gesture-indicator p {
  color: white;
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.9;
  font-weight: 500;
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

footer p {
  margin: 8px 0;
}

.gesture-tip {
  font-size: 0.85rem;
  opacity: 0.75;
  font-style: italic;
}

/* Touch-friendly improvements */
button,
input,
a {
  -webkit-tap-highlight-color: rgba(255, 255, 255, 0.2);
  touch-action: manipulation;
}

/* Improve button touch targets */
button {
  min-height: 44px;
  min-width: 44px;
}

@media (max-width: 600px) {
  body {
    padding: 10px;
  }

  .results-section {
    margin-top: 20px;
  }

  .gesture-hint {
    padding: 20px 35px;
  }

  .hint-icon {
    font-size: 2.5rem;
  }

  .hint-text {
    font-size: 1rem;
  }

  .gesture-indicator p {
    font-size: 0.8rem;
  }
}

@media (hover: none) and (pointer: coarse) {
  /* Show gesture indicators only on touch devices */
  .gesture-indicator {
    display: block;
  }
}

@media (hover: hover) and (pointer: fine) {
  /* Hide gesture indicators on desktop */
  .gesture-indicator {
    display: none;
  }

  .gesture-tip {
    display: none;
  }
}
</style>
