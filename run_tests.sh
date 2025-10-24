#!/bin/bash
cd "$(dirname "$0")"
python -m unittest discover -s PyCode -p "test_*.py"

