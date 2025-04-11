#!/bin/bash

# Set your S3 bucket name
BUCKET_NAME="your-bucket-name"

# Set the file containing object names (one per line)
OBJECTS_FILE="s3_objects.txt"

# Set the restore days and retrieval tier
RESTORE_DAYS=7
RESTORE_TIER="Expedited"  # Change to "Standard" or "Bulk" if needed

# Log file for tracking
LOG_FILE="restore_log.txt"

# Check if the objects file exists
if [[ ! -f "$OBJECTS_FILE" ]]; then
    echo "Error: File $OBJECTS_FILE not found!"
    exit 1
fi

# Initialize file counter
FILE_NUMBER=0

# Total number of files for reference
TOTAL_FILES=$(wc -l < "$OBJECTS_FILE")

echo "Starting S3 Restore Process for $TOTAL_FILES files..."
echo "----------------------------------------" | tee -a "$LOG_FILE"

# Loop through each line in the file (each S3 object key)
while IFS= read -r OBJECT_KEY; do
    if [[ -n "$OBJECT_KEY" ]]; then
        ((FILE_NUMBER++))  # Increment file counter
        echo "[$FILE_NUMBER/$TOTAL_FILES] Restoring: $OBJECT_KEY" | tee -a "$LOG_FILE"
        
        # AWS S3 Restore Command
        aws s3api restore-object --bucket "$BUCKET_NAME" --key "$OBJECT_KEY" \
            --restore-request "{\"Days\": $RESTORE_DAYS, \"GlacierJobParameters\": {\"Tier\": \"$RESTORE_TIER\"}}" \
            >> "$LOG_FILE" 2>&1

        # Check if the command was successful
        if [[ $? -eq 0 ]]; then
            echo "✔ Successfully submitted restore request for: $OBJECT_KEY" | tee -a "$LOG_FILE"
        else
            echo "❌ Failed to restore: $OBJECT_KEY" | tee -a "$LOG_FILE"
        fi

        # Optional delay to avoid hitting API rate limits (uncomment if needed)
        # sleep 1
    fi
done < "$OBJECTS_FILE"

echo "All restore requests submitted." | tee -a "$LOG_FILE"
