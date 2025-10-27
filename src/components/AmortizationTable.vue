<template>
  <div class="amortization-table">
    <h2>Payment Schedule</h2>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Payment</th>
            <th>Principal</th>
            <th>Interest</th>
            <th>Balance</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="payment in schedule" :key="payment.paymentNumber">
            <td>{{ payment.paymentNumber }}</td>
            <td>${{ formatCurrency(payment.paymentAmount) }}</td>
            <td>${{ formatCurrency(payment.principalPayment) }}</td>
            <td>${{ formatCurrency(payment.interestPayment) }}</td>
            <td>${{ formatCurrency(payment.remainingBalance) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="table-info">
      Showing all {{ schedule.length }} payments
    </div>
  </div>
</template>

<script>
export default {
  name: 'AmortizationTable',
  props: {
    schedule: {
      type: Array,
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
.amortization-table {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 20px;
  font-size: 1.6rem;
}

.table-container {
  overflow-x: auto;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

thead {
  background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
  color: white;
}

th {
  padding: 15px 10px;
  text-align: right;
  font-weight: 600;
  position: sticky;
  top: 0;
  background: #2c3e50;
}

th:first-child {
  text-align: center;
}

td {
  padding: 12px 10px;
  text-align: right;
  border-bottom: 1px solid #ecf0f1;
}

td:first-child {
  text-align: center;
  font-weight: 600;
  color: #7f8c8d;
}

tbody tr:hover {
  background-color: #f8f9fa;
}

tbody tr:last-child {
  background-color: #e8f5e9;
  font-weight: 600;
}

.table-info {
  text-align: center;
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-top: 10px;
}

@media (max-width: 600px) {
  .amortization-table {
    padding: 15px 10px;
  }

  h2 {
    font-size: 1.4rem;
  }

  th,
  td {
    padding: 10px 5px;
    font-size: 0.85rem;
  }

  th:first-child,
  td:first-child {
    padding: 10px 8px;
  }
}
</style>
