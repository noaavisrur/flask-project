#!/bin/bash
service_name="$1"  # Get the Kubernetes service name from the first command-line argument

# Check if service name is provided
if [ -z "$service_name" ]; then
    echo "Error: Kubernetes service name not provided."
    exit 1
fi

# Replace 'WINDOWS_MACHINE_IP' with the actual IP address of the Windows machine running Rancher Desktop
windows_machine_ip="WINDOWS_MACHINE_IP"

# Ensure that kubectl is configured to use the local cluster on Rancher Desktop
kubectl --kubeconfig=/path/to/your/kubeconfig.yaml config use-context "rancher-desktop"

# Get the host port mapped to the Kubernetes service's target port
port=$(kubectl --kubeconfig=/path/to/your/kubeconfig.yaml get service $service_name -o=jsonpath='{.spec.ports[0].nodePort}')

# Check if the service has been exposed with a nodePort
if [ -z "$port" ]; then
    echo "Error: The service '$service_name' does not have a nodePort assigned."
    exit 1
fi

# Make HTTP request to the Kubernetes service using the Windows machine's IP and the mapped port
response=$(curl -s -o /dev/null -w "%{http_code}" http://$windows_machine_ip:$port)

# Check if response code indicates success or failure
if [ "${response}" == "200" ]; then
    echo "0"
    exit 0 # success
else
    echo "1"
    exit 1  # Exit with non-zero status to indicate failure
fi
