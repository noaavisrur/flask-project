#!/bin/bash
service_name="$1"  # Get the Kubernetes service name from the first command-line argument

# Check if service name is provided
if [ -z "$service_name" ]; then
    echo "Error: Kubernetes service name not provided."
    exit 1
fi

# Replace 'WINDOWS_MACHINE_IP' with the actual IP address of the Windows machine running Rancher Desktop
windows_machine_ip="172.21.8.216"

# Get the ClusterIP of the Kubernetes service
cluster_ip=$(kubectl --kubeconfig=/var/lib/jenkins/.kube/config get service $service_name -o=jsonpath='{.spec.clusterIP}')

# Check if the ClusterIP is empty (service might not be running or configured properly)
if [ -z "$cluster_ip" ]; then
    echo "Error: The service '$service_name' is not running or does not have a valid ClusterIP."
    exit 1
fi

# Get the dynamically assigned LoadBalancer port using JSONPath
port=$(kubectl --kubeconfig=/var/lib/jenkins/.kube/config get service $service_name -o=jsonpath='{.spec.ports[?(@.port==80)].nodePort}')

# Check if the service has a port assigned
if [ -z "$port" ]; then
    echo "Error: The service '$service_name' does not have a port assigned."
    exit 1
fi

# Make HTTP request to the Kubernetes service using the Windows machine's IP and the dynamically assigned LoadBalancer port (ClusterIP:Port)
echo $windows_machine_ip:$port
response=$(curl -s -o /dev/null -w "%{http_code}" http://$windows_machine_ip:$port)

# Check if response code indicates success or failure
if [ "${response}" == "200" ]; then
    echo "0"
    exit 0 # success
else
    echo "1"
    exit 1  # Exit with non-zero status to indicate failure
fi
