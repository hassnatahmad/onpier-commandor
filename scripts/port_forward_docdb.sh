#!/bin/bash

pod_name="docdb-connector"
pod_port=8081
forward_port=8081

# File to store PIDs of background processes
pid_file="port_forward_pids.txt"

# Curl command
curl_command() {
  echo "Enabling change streams for database 'prisma-core-business_file-expose-db' and collection 'FileMetadata' on port $1"
  curl -X 'POST' "http://localhost:$1/db/command" \
    -H 'accept: application/json' \
    -H 'Authorization: Basic b25waWVyOm9ucGllcg==' \
    -H 'Content-Type: application/json' \
    -d '{"modifyChangeStreams": 1,"database": "prisma-core-business_file-expose-db","collection": "FileMetadata","enable": true}'
}

if [ "$1" == "start" ]; then
  # Clear the PID file
  # shellcheck disable=SC2188
  >"$pid_file"

  # Get all contexts from kubeconfig
  contexts=$(kubectl config get-contexts -o name)

  # Iterate through contexts
  for context in $contexts; do
    # Set the current context
    kubectl config use-context "$context" >/dev/null 2>&1

    # Get the namespace and pod for the docdb-connector
    namespace_pod=$(kubectl get pods --selector=app="$pod_name" -o custom-columns=:metadata.namespace,:metadata.name --no-headers | head -n 1)

    if [ -n "$namespace_pod" ]; then
      # Extract namespace and pod name
      namespace=$(echo "$namespace_pod" | awk '{print $1}')
      pod=$(echo "$namespace_pod" | awk '{print $2}')

      # Start kubectl port-forward in the background
      kubectl port-forward --namespace="$namespace" --context="$context" "$pod" "$forward_port":"$pod_port" >/dev/null 2>&1 &

      # Save the PID of the background process
      echo $! >> "$pid_file"

      # Run the curl command and print the response
      response=$(curl_command "$forward_port")
      echo "$response"

      # Increment forward_port for the next context
      forward_port=$((forward_port + 1))
    fi
  done

  echo "Port-forwarding started. To stop, run the script with the 'stop' argument."

elif [ "$1" == "stop" ]; then
  if [ -f "$pid_file" ]; then
    # Read PIDs from the file and kill the processes
    while read -r pid; do
      kill "$pid"
    done <"$pid_file"

    # Remove the PID file
    rm "$pid_file"
  else
    echo "No port-forwarding processes found."
  fi

else
  echo "Usage: $0 start|stop"
fi
