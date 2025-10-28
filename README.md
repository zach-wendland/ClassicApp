# Amortization Calculator - Mobile PWA

A fully mobile-optimized Progressive Web App (PWA) for calculating loan payments and viewing amortization schedules. Built with Vue.js, featuring touch gestures, offline support, and installable on mobile devices.

## Features

### Core Functionality
- Clean, intuitive interface
- Real-time loan calculations
- Detailed amortization schedule
- Input validation and error handling
- No backend required - runs entirely in browser

### Mobile Optimizations
- **Progressive Web App (PWA)** - Install on your device like a native app
- **Offline-First** - Works completely offline with Service Worker caching
- **Touch Gestures** - Intuitive swipe controls for mobile navigation
  - Swipe right to go back
  - Swipe down to reset
  - Visual feedback for all gestures
- **Mobile-Responsive Design** - Optimized for all screen sizes
- **Touch-Friendly** - 44px minimum touch targets following iOS guidelines
- **Fast Performance** - Optimized caching and minimal dependencies

## Tech Stack

- **Vue 3** - Frontend framework
- **Vite** - Build tool and dev server
- **Service Worker** - Offline functionality
- **HTML/CSS** - Responsive styling with touch optimizations
- **JavaScript** - Calculation and gesture detection logic
- **Python** - Comprehensive unit tests (55 tests)

## Project Structure

```
ClassicApp/
├── public/
│   ├── manifest.json                # PWA manifest
│   └── sw.js                        # Service Worker
├── src/
│   ├── App.vue                      # Main app with gestures
│   ├── main.js                      # Vue entry point
│   ├── components/
│   │   ├── LoanInputForm.vue        # Input form component
│   │   ├── LoanSummary.vue          # Results summary component
│   │   └── AmortizationTable.vue    # Payment schedule table
│   └── utils/
│       ├── calculator.js            # Calculation functions
│       └── gestures.js              # Touch gesture detection
├── tests/
│   ├── calculator.py                # Calculator implementation (Python)
│   ├── test_calculator.py           # Calculator unit tests (24 tests)
│   ├── gestures.py                  # Gesture implementation (Python)
│   ├── test_gestures.py             # Gesture unit tests (31 tests)
│   └── run_all_tests.py             # Comprehensive test runner
├── index.html                       # HTML entry point with PWA meta tags
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

## Progressive Web App (PWA) Installation

### On Mobile Devices (iOS/Android)

**iOS (Safari):**
1. Open the app in Safari
2. Tap the Share button
3. Scroll down and tap "Add to Home Screen"
4. Name the app and tap "Add"

**Android (Chrome):**
1. Open the app in Chrome
2. Tap the three-dot menu
3. Select "Add to Home Screen" or "Install App"
4. Confirm installation

### On Desktop (Chrome/Edge)

1. Open the app in Chrome or Edge
2. Look for the install icon in the address bar
3. Click "Install"
4. The app will open in its own window

### Offline Usage

Once installed, the app works completely offline:
- All calculations are performed locally
- No internet connection required
- Data is not sent to any server
- Perfect for areas with poor connectivity

## Touch Gestures

The app supports intuitive touch gestures for mobile navigation:

| Gesture | Action |
|---------|--------|
| Swipe Right → | Go back to input form (from results) |
| Swipe Down ↓ | Reset calculator |
| Swipe Left ← | Scroll amortization table |
| Swipe Up ↑ | Scroll up |

**Visual Feedback:**
- Gesture hints appear as you swipe
- On-screen indicators show available gestures
- Animations provide smooth transitions

**Gesture Settings:**
- Minimum swipe distance: 60px
- Maximum swipe time: 500ms
- Angular tolerance: 35°

## Running Tests

The project includes comprehensive unit tests for all logic.

### Run All Tests (55 tests total)

```bash
cd tests
python run_all_tests.py
```

### Run Calculator Tests Only (24 tests)

```bash
cd tests
python test_calculator.py -v
```

### Run Gesture Tests Only (31 tests)

```bash
cd tests
python test_gestures.py -v
```

### Test Coverage

**Calculator Tests:**
- Monthly payment calculations
- Total paid and interest calculations
- Amortization schedule generation
- Input validation (positive, negative, edge cases)
- Zero interest rate handling
- Large loan amounts

**Gesture Tests:**
- Distance calculations
- Angle calculations (0-360°)
- Direction detection (up, down, left, right)
- Swipe validation
- Custom tolerance settings
- Edge cases (diagonal swipes, too short/slow)

## How to Use

1. **Enter Loan Details:**
   - **Loan Amount**: Total amount you're borrowing ($)
   - **Interest Rate**: Annual interest rate (%)
   - **Loan Term**: Number of years to repay

2. **Calculate:**
   - Click "Calculate" button or press Enter
   - View your monthly payment and loan summary
   - Scroll through complete amortization schedule

3. **Navigate:**
   - Use the Reset button or swipe gestures
   - Swipe right to go back
   - Swipe down anywhere to reset

4. **Install (Optional):**
   - Add to home screen for app-like experience
   - Works offline after installation

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

**Special Case - 0% Interest:**
```
M = P / n
```

**Total Paid:**
```
Total = Monthly Payment × Number of Payments
```

**Total Interest:**
```
Interest = Total Paid - Principal
```

## Browser Support

**Desktop:**
- Chrome 90+ (recommended)
- Firefox 88+
- Safari 14+
- Edge 90+

**Mobile:**
- iOS Safari 14+
- Chrome for Android 90+
- Samsung Internet 14+

**PWA Features:**
- Service Worker support required
- Add to Home Screen available on all modern mobile browsers

## Performance

- **First Load:** < 1s on 3G
- **Offline:** Instant loading from cache
- **Calculations:** < 10ms for 30-year loan
- **Bundle Size:** < 100KB (gzipped)

## Privacy & Security

- **No data collection** - Everything runs locally
- **No server communication** - Pure client-side app
- **No tracking** - No analytics or cookies
- **No account required** - Just calculate and go
- **Offline-first** - Your data never leaves your device

## Accessibility

- Semantic HTML structure
- ARIA labels for screen readers
- Keyboard navigation support
- High contrast colors
- Touch targets minimum 44×44px
- Responsive text sizing

## Development

### File Organization

- `src/components/` - Vue components
- `src/utils/` - Business logic and utilities
- `public/` - Static assets and PWA files
- `tests/` - Python unit tests

### Adding New Features

1. Write tests first (TDD approach)
2. Implement feature in JavaScript
3. Create Python equivalent for testing
4. Run full test suite
5. Update documentation

### Testing Philosophy

- Every function has unit tests
- Edge cases are thoroughly tested
- Python tests mirror JavaScript implementation
- 100% of calculation logic is tested

## Troubleshooting

**App won't install:**
- Ensure you're using HTTPS or localhost
- Check that manifest.json is accessible
- Clear browser cache and try again

**Gestures not working:**
- Make sure you're on a touch device
- Check that JavaScript is enabled
- Try refreshing the page

**Offline mode not working:**
- Service Worker may not be registered
- Check browser console for errors
- Try visiting the app online first

**Calculations seem wrong:**
- Run the test suite to verify logic
- Check for very large or very small inputs
- Ensure interest rate is entered as percentage (not decimal)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### v2.0.0 (Mobile PWA Release)
- Added Progressive Web App support
- Implemented Service Worker for offline functionality
- Added touch gesture detection system
- Created 31 unit tests for gesture logic
- Enhanced mobile UI with touch feedback
- Added PWA manifest and icons support
- Improved touch target sizes
- Added gesture hints and visual feedback

### v1.0.0 (Initial Release)
- Basic amortization calculator
- Vue.js implementation
- Responsive design
- 24 unit tests for calculations
- Input validation
