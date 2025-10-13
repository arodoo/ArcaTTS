#!/bin/bash

echo "Installing Grammar Module dependencies..."

# Activate venv if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    source venv/Scripts/activate
fi

# Install language-tool-python
pip install language-tool-python

echo ""
echo "✓ Grammar module dependencies installed!"
echo ""
echo "Quick Test:"
echo "  python -m modules.grammar.test_grammar"
echo ""
echo "Check Kafka file:"
echo "  python -m modules.grammar.cli check boocks/franz-kafka.txt"
echo ""
echo "Correct Kafka file:"
echo "  python -m modules.grammar.cli correct boocks/franz-kafka.txt"
