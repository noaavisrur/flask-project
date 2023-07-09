#!/bin/bash
ip_address="$1"  # Get IP address from the first command-line argument
port=5000  # Replace with the actual port number of your Flask server

# Check if IP address is provided
if [ -z "$ip_address" ]; then
    echo "Error: IP address not provided."
    exit 1
fi

# Make HTTP request to Flask server and capture response
response=$(curl -s -o /dev/null -w "%{http_code}" http://$ip_address:$port)

# Check if response code indicates success or failure
if [ "${response}" == "200" ]; then
    echo "0"
    exit 0 # success
else
    echo "1"
    exit 1  # Exit with non-zero status to indicate failure
fi
