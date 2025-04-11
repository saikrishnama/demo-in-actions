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
TOTAL_FILES=$(wc -l < "$OBJECTS_FILE")

echo "Starting S3 Restore Process for $TOTAL_FILES files..."
echo "----------------------------------------" | tee -a "$LOG_FILE"

# Loop through each line in the file (each S3 object key)
while IFS= read -r OBJECT_KEY; do
    if [[ -n "$OBJECT_KEY" ]]; then
        ((FILE_NUMBER++))  # Increment file counter
        echo "[$FILE_NUMBER/$TOTAL_FILES] Checking: $OBJECT_KEY" | tee -a "$LOG_FILE"

        # Get object metadata to check restore status
        RESTORE_STATUS=$(aws s3api head-object --bucket "$BUCKET_NAME" --key "$OBJECT_KEY" --query "Restore" --output text 2>/dev/null)

        if [[ "$RESTORE_STATUS" == "None" || "$RESTORE_STATUS" == "null" ]]; then
            echo "🔹 Not restored. Submitting restore request..." | tee -a "$LOG_FILE"
            
            # Submit restore request
            aws s3api restore-object --bucket "$BUCKET_NAME" --key "$OBJECT_KEY" \
                --restore-request "{\"Days\": $RESTORE_DAYS, \"GlacierJobParameters\": {\"Tier\": \"$RESTORE_TIER\"}}" \
                >> "$LOG_FILE" 2>&1

            if [[ $? -eq 0 ]]; then
                echo "✔ Restore request submitted for: $OBJECT_KEY" | tee -a "$LOG_FILE"
            else
                echo "❌ Failed to restore: $OBJECT_KEY" | tee -a "$LOG_FILE"
            fi

        elif [[ "$RESTORE_STATUS" == *"ongoing-request=true"* ]]; then
            echo "⏳ Already being restored. Skipping..." | tee -a "$LOG_FILE"

        else
            echo "✅ Already restored. Skipping..." | tee -a "$LOG_FILE"
        fi

        # Optional delay to avoid hitting API rate limits
        # sleep 1
    fi
done < "$OBJECTS_FILE"

echo "All necessary restore requests submitted." | tee -a "$LOG_FILE"
