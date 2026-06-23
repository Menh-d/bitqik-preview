#!/bin/bash
echo "----------------------------------------"
echo "  Starting bitqik Home Web Page Server  "
echo "----------------------------------------"
echo "To view the website, open your browser and go to:"
echo "👉 http://localhost:8000"
echo "----------------------------------------"
echo "Press Ctrl+C to stop the server."
python3 -m http.server 8000
