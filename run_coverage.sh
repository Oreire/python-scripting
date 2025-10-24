#!/bin/bash
echo "Running tests with coverage..."
coverage run -m unittest discover -s PyCode -p "test_*.py"
coverage report -m

echo "Generating HTML coverage report..."
coverage html -d coverage_report
echo "HTML report generated in coverage_report/index.html"


