<template>
  <section class="rates-panel">
    <div class="panel-header">
      <div>
        <p class="eyebrow">Market snapshot</p>
        <h3>Live mortgage rates</h3>
      </div>
      <button class="refresh-btn" type="button" :disabled="loading" @click="$emit('refresh')">
        <span v-if="loading">Refreshing...</span>
        <span v-else>Refresh</span>
      </button>
    </div>

    <div v-if="loading" class="panel-state">
      Pulling the latest data...
    </div>

    <div v-else-if="error" class="panel-state error">
      {{ error }}
    </div>

    <ul v-else class="rate-list">
      <li v-for="rate in rates" :key="rate.term" class="rate-item">
        <div class="rate-meta">
          <p class="term">{{ rate.term }}</p>
          <p class="timestamp" v-if="rate.asOf && rate.asOf !== 'Sample data'">
            Updated {{ formatDate(rate.asOf) }}
          </p>
        </div>
        <p class="rate-value">
          {{ formatRate(rate.rate) }}%
        </p>
      </li>
    </ul>

    <p class="panel-foot">
      Source: {{ (rates[0] && rates[0].source) || 'Sample data' }}
    </p>
  </section>
</template>

<script>
export default {
  name: 'MortgageRatesPanel',
  props: {
    rates: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: ''
    }
  },
  methods: {
    formatRate(value) {
      if (typeof value !== 'number' || Number.isNaN(value)) {
        return '--';
      }
      return value.toFixed(2);
    },
    formatDate(dateString) {
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString(undefined, {
          month: 'short',
          day: 'numeric',
          year: 'numeric'
        });
      } catch (error) {
        return dateString;
      }
    }
  }
};
</script>

<style scoped>
.rates-panel {
  background: #ffffff;
  border-radius: 18px;
  border: 1px solid #e4e7ec;
  padding: 24px;
  box-shadow: 0 15px 45px rgba(15, 23, 42, 0.08);
  min-width: 280px;
}

.panel-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.eyebrow {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #475467;
  margin-bottom: 4px;
}

h3 {
  font-size: 1.25rem;
  color: #0f172a;
  margin: 0;
}

.refresh-btn {
  border: 1px solid #d0d5dd;
  background: #f8fafc;
  color: #0f172a;
  padding: 8px 14px;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-btn:not(:disabled):hover {
  background: #0f172a;
  color: #ffffff;
}

.panel-state {
  background: #f8fafc;
  border-radius: 12px;
  padding: 16px;
  color: #475467;
  font-size: 0.9rem;
  margin: 8px 0;
}

.panel-state.error {
  color: #b42318;
  background: #fef3f2;
  border: 1px solid #fecdca;
}

.rate-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0;
  padding: 0;
}

.rate-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: 12px;
  border-bottom: 1px dashed #e4e7ec;
}

.rate-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.rate-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.term {
  font-size: 1rem;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
}

.timestamp {
  font-size: 0.8rem;
  color: #667085;
  margin: 0;
}

.rate-value {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: #0f172a;
}

.panel-foot {
  font-size: 0.75rem;
  color: #98a2b3;
  margin-top: 16px;
}

@media (max-width: 640px) {
  .rates-panel {
    padding: 20px;
  }

  .panel-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .rate-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
}
</style>
