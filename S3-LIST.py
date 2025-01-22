#!/bin/bash

# Output file
output_file="buckets_with_lifecycle.txt"

# Clear the output file
> $output_file

# Get a list of all bucket names
buckets=$(aws s3api list-buckets --query "Buckets[].Name" --output text)

# Check each bucket for lifecycle configuration
for bucket in $buckets; do
    echo "Checking bucket: $bucket"
    lifecycle=$(aws s3api get-bucket-lifecycle-configuration --bucket $bucket 2>/dev/null)
    if [ $? -eq 0 ]; then
        echo "Bucket with lifecycle rules: $bucket"
        echo $bucket >> $output_file
    fi
done

echo "Buckets with lifecycle rules written to $output_file"
