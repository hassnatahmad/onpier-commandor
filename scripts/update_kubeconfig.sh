#!/bin/bash

# Get all AWS profiles using the AWS CLI
profiles=$(aws configure list-profiles)

# get first profile
# shellcheck disable=SC2046
aws sso login --profile $(echo "$profiles" | cut -d' ' -f1)
# Loop through each profile
for profile in $profiles; do
    echo "Working on profile: $profile"

    # Get EKS clusters in the current profile
    clusters=$(aws eks list-clusters --profile "$profile" --region eu-central-1 --output text --query 'clusters[]')

    # Check if there are any clusters in the profile
    if [ -z "$clusters" ]; then
        echo "No clusters found for profile: $profile"
    else
        # Loop through each EKS cluster in the profile
        for cluster in $clusters; do
            echo "Updating kubeconfig for cluster: $cluster"

            # Update the .kubeconfig file for the current cluster and profile
            aws eks update-kubeconfig --profile "$profile" --region eu-central-1 --name "$cluster"
        done
    fi
done

# Print the final kubeconfig
echo "Updated .kube/config:"
# cat ~/.kube/config