#!/bin/bash
service_name="$1"  # Get the Kubernetes service name from the first command-line argument
port=80  # Replace with the actual port number of your Flask service

# Check if service name is provided
if [ -z "$service_name" ]; then
    echo "Error: Kubernetes service name not provided."
    exit 1
fi

# Forward a local port to the Kubernetes service
kubectl port-forward service/$service_name $port:$port >/dev/null 2>&1 &

# Wait for port-forwarding to be ready
sleep 5

# Make HTTP request to the local forwarded port and capture response
response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$port)

# Check if response code indicates success or failure
if [ "${response}" == "200" ]; then
    echo "0"
    exit 0 # success
else
    echo "1"
    exit 1  # Exit with non-zero status to indicate failure
fi
