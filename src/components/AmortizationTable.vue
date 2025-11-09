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
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

h2 {
  font-size: 1.5rem;
  color: #0f172a;
}

.table-container {
  overflow-x: auto;
  border-radius: 20px;
  border: 1px solid #eceef3;
  background: #ffffff;
  box-shadow: inset 0 1px 0 #f8fafc;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f8fafc;
  color: #0f172a;
}

th {
  padding: 16px 12px;
  text-align: right;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border-bottom: 1px solid #e4e7ec;
}

th:first-child {
  text-align: left;
}

td {
  padding: 14px 12px;
  text-align: right;
  border-bottom: 1px solid #f1f3f8;
  font-variant-numeric: tabular-nums;
}

td:first-child {
  text-align: left;
  font-weight: 600;
  color: #475467;
}

tbody tr:last-child td {
  border-bottom: none;
  background: #f0fdf4;
  color: #14532d;
}

tbody tr:hover td {
  background: #f9fafb;
}

.table-info {
  font-size: 0.85rem;
  color: #667085;
}

@media (max-width: 600px) {
  th,
  td {
    padding: 12px 8px;
    font-size: 0.85rem;
  }
}
</style>

