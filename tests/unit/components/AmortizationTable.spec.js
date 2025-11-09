import { mount } from '@vue/test-utils';
import { describe, it, expect } from 'vitest';
import AmortizationTable from '../../../src/components/AmortizationTable.vue';

const sampleSchedule = [
  {
    paymentNumber: 1,
    paymentAmount: 1000,
    principalPayment: 300,
    interestPayment: 700,
    remainingBalance: 99900
  },
  {
    paymentNumber: 2,
    paymentAmount: 1000,
    principalPayment: 302,
    interestPayment: 698,
    remainingBalance: 99598
  }
];

describe('AmortizationTable', () => {
  it('renders rows for each payment in the schedule', () => {
    const wrapper = mount(AmortizationTable, {
      props: {
        schedule: sampleSchedule
      }
    });

    const rows = wrapper.findAll('tbody tr');
    expect(rows).toHaveLength(sampleSchedule.length);
    expect(rows[0].text()).toContain('$1,000.00');
    expect(rows[0].text()).toContain('$300.00');
    expect(rows[0].text()).toContain('$700.00');
  });

  it('displays summary info with payment count', () => {
    const wrapper = mount(AmortizationTable, {
      props: {
        schedule: sampleSchedule
      }
    });

    expect(wrapper.find('.table-info').text()).toContain('Showing all 2 payments');
  });
});

