import boto3
import json

# Initialize SQS client
sqs = boto3.client('sqs', region_name='your_region_name', aws_access_key_id='your_access_key_id', aws_secret_access_key='your_secret_access_key')

# Define the SQS queue URL
queue_url = 'your_queue_url'

# Receive messages from the queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=['All'],
    MaxNumberOfMessages=10,  # Specify the maximum number of messages to receive
    WaitTimeSeconds=20  # Specify the wait time (in seconds) for new messages
)

# Process received messages
messages = response.get('Messages', [])
for message in messages:
    # Extract the message body
    body = message['Body']

    # Process the message
    try:
        msg = json.loads(body)
        operation_type = msg.get('operatiom_type')
        data = msg.get('data', {})

        if operation_type == 'NOMINATED':
            print('Table nominated')
            # Add your logic for table nominated here

        elif operation_type == 'EXCEMPTED':
            table_name = data.get('table_name')
            if table_name == 'BDA':
                print('Table excepted')
                # Add your logic for table excepted here

        else:
            print('Invalid operation type')

    except json.JSONDecodeError:
        print('Failed to decode message body as JSON')

    # Delete the message from the queue
    receipt_handle = message['ReceiptHandle']
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
