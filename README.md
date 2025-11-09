# Amortization Calculator

A simple, mobile-friendly amortization calculator built with Vue.js. Calculate your monthly loan payments and view a complete amortization schedule showing how your payments are split between principal and interest over time.

## Features

- Clean, card-based UI with high-contrast typography
- Mobile-responsive design
- Real-time loan calculations
- Detailed amortization schedule
- Live mortgage rate snapshot powered by FRED (with safe fallback)
- Input validation and error handling
- Optional state sales tax inclusion (API-ready with static fallback)

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

### Sales Tax (Optional)

You can optionally include state sales tax in the financed amount:

- Use the UI checkbox and select a state.
- By default, the app uses a static fallback for base state tax rates (no local taxes).
- To enable a provider (e.g., TaxJar), set environment variables and rebuild.

Environment variables (create a `.env` file):

```
VITE_TAX_API_PROVIDER=taxjar
VITE_TAXJAR_API_KEY=your_api_key_here
```

Notes:
- Provider usage is best-effort in this sample and may require adapting endpoints per provider docs.
- If the API fails or is not configured, the static fallback is used.

### Live Mortgage Rates (Optional)

To surface current 30-year, 15-year, and 5/1 ARM mortgage averages inside the hero panel, supply a FRED API key:

```
VITE_FRED_API_KEY=your_fred_api_key
```

Without a key the app falls back to baked-in sample data so the UI still renders.

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

Run the JavaScript unit tests (Vitest):
```bash
npm test
```

Python parity tests remain available:
```bash
cd tests
python test_calculator.py
```

## How to Use

1. Enter your loan details:
   - **Loan Amount**: The total amount you're borrowing
   - **Interest Rate**: Annual interest rate (as a percentage)
   - **Loan Term**: Number of years to repay the loan
   - (Optional) **State + Include Sales Tax**: Adds base state sales tax to the financed amount

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
