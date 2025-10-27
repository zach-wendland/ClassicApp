# Amortization Calculator

A simple, mobile-friendly amortization calculator built with Vue.js. Calculate your monthly loan payments and view a complete amortization schedule showing how your payments are split between principal and interest over time.

## Features

- Clean, intuitive interface
- Mobile-responsive design
- Real-time loan calculations
- Detailed amortization schedule
- No backend required - runs entirely in browser
- Input validation and error handling

## Tech Stack

- **Vue 3** - Frontend framework
- **Vite** - Build tool and dev server
- **HTML/CSS** - Responsive styling
- **JavaScript** - Calculation logic
- **Python** - Unit tests

## Project Structure

```
ClassicApp/
├── src/
│   ├── App.vue                      # Main app component
│   ├── main.js                      # Vue entry point
│   ├── components/
│   │   ├── LoanInputForm.vue        # Input form component
│   │   ├── LoanSummary.vue          # Results summary component
│   │   └── AmortizationTable.vue    # Payment schedule table
│   └── utils/
│       └── calculator.js            # Calculation functions
├── tests/
│   ├── calculator.py                # Python implementation
│   └── test_calculator.py           # Unit tests
├── index.html                       # HTML entry point
├── vite.config.js                   # Vite configuration
└── package.json                     # Dependencies
```

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Python 3 (for running tests)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ClassicApp
```

2. Install dependencies:
```bash
npm install
```

### Running the Application

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### Building for Production

Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Running Tests

The project includes comprehensive Python unit tests for all calculation functions.

Run the tests:
```bash
cd tests
python test_calculator.py
```

Run tests with verbose output:
```bash
cd tests
python test_calculator.py -v
```

## How to Use

1. Enter your loan details:
   - **Loan Amount**: The total amount you're borrowing
   - **Interest Rate**: Annual interest rate (as a percentage)
   - **Loan Term**: Number of years to repay the loan

2. Click **Calculate** to see:
   - Your monthly payment amount
   - Total amount paid over the life of the loan
   - Total interest paid
   - Complete amortization schedule

3. Click **Reset** to calculate a different loan

## Calculation Formulas

**Monthly Payment:**
```
M = P × [r(1 + r)^n] / [(1 + r)^n - 1]
```
Where:
- M = Monthly payment
- P = Principal (loan amount)
- r = Monthly interest rate (annual rate / 12 / 100)
- n = Number of payments (years × 12)

**Total Paid:**
```
Total = Monthly Payment × Number of Payments
```

**Total Interest:**
```
Interest = Total Paid - Principal
```

## Mobile Support

The app is fully responsive and works great on:
- Desktop browsers
- Tablets
- Mobile phones
- Can be saved to home screen for app-like experience

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
