# Order Price Calculator

# Project Summary

A modular Python utility for calculating the final price of an order based on quantity, unit price, and tax percentage. Designed for reproducibility, testability, and CPD-ready validation, this project demonstrates full-stack testing awareness and secure-by-design CLI integration.

# Project Structure

python-scripting/
├── PyCode/
│   ├── __init__.py
│   ├── order_calculator.py         # Core logic and CLI wrapper
│   └── test_order_calculator.py    # Comprehensive test suite
├── run_tests.sh                    # Basic test runner
├── run_coverage.sh                 # Coverage runner with HTML output
├── coverage_report/                # HTML coverage output
├── requirements.txt                # Optional: dependencies
└── README.md                       # Project documentation



# Features

- Calculates subtotal, tax, and final price
- CLI wrapper for interactive use
- Full unit test coverage (100%)
- Handles edge cases and invalid inputs
- Mocked CLI input for testable interaction
- HTML coverage report generation

# Usage

Run interactively:
python PyCode/order_calculator.py


Example input:
Enter quantity: 2
Enter unit price (£): 50
Enter tax percentage (%): 10


Output:
----- Order Summary -----
Quantity: 2
Unit Price: £50.00
Subtotal: £100.00
Tax (10%): £10.00
Final Price: £110.00


🧪 Testing

Run all tests:
./run_tests.sh


Run with coverage:
./run_coverage.sh


View HTML report:
start coverage_report/index.html



✅ Coverage Summary


file:///C:/Publications/python-scripting/coverage_report/index.html



# Validation Highlights

- Input validation for None, non-numeric, and missing arguments
- Negative values and boundary conditions tested
- CLI input flow mocked for reproducibility
- main() entry point excluded from coverage (# pragma: no cover)


# License & Attribution

This project is authored by Ayomide Ajayi and must be properly attributed in all derivative works, educator resource packs, and institutional presentations.

“Every original authored work herein is the intellectual property of Ayomide Ajayi. Attribution is mandatory for citation, reuse, or integration.”


