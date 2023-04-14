#!/bin/bash

# Define the port range
start_port=8081
end_port=8095

# Function to check if a variable is a number
is_number() {
  [[ $1 =~ ^[0-9]+$ ]]
}

# Iterate through the specified port range
for port in $(seq $start_port $end_port); do
  # Get the process ID using the current port
  pid=$(lsof -ti tcp:"$port")

  # Check if the PID is a number
  if is_number "$pid"; then
    # Kill the process and check if it was successful
    if kill -9 "$pid" &> /dev/null; then
      echo "Killed process with PID $pid on port $port."
    else
      echo "Error: Failed to kill process with PID $pid on port $port."
    fi
  else
    echo "No process found using port $port."
  fi
done
