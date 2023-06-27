#!/bin/bash
port=5000  # Replace with the actual port number of your Flask server

# Make HTTP request to Flask server and capture response
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port)

# Print response
echo "HTTP response code: ${response}"

# Check if response code indicates success or failure
if [ "${response}" == "200" ]; then
    echo "Flask directory test passed!"
else
    echo "Flask directory test failed!"
    exit 1  # Exit with non-zero status to indicate failure
fi
