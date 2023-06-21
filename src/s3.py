import boto3

class S3Client:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3')

    def write_data(self, key, data):
        try:
            obj = self.s3.Object(self.bucket_name, key)
            obj.put(Body=data)
            print(f"Data written successfully to {self.bucket_name}/{key}")
        except Exception as e:
            print(f"Error writing data to S3: {str(e)}")

    def read_data(self, key):
        try:
            obj = self.s3.Object(self.bucket_name, key)
            response = obj.get()
            data = response['Body'].read().decode('utf-8')
            print(f"Data read successfully from {self.bucket_name}/{key}")
            return data
        except Exception as e:
            print(f"Error reading data from S3: {str(e)}")
            return None

# Usage example
bucket_name = 'your_bucket_name'
s3_client = S3Client(bucket_name)

# Write data to S3
data_key = 'example.txt'
data_content = 'Hello, S3!'
s3_client.write_data(data_key, data_content)

# Read data from S3
read_data = s3_client.read_data(data_key)
print(read_data)

#######

import boto3

class S3Client:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def write_data(self, key, data):
        try:
            self.s3.put_object(Body=data, Bucket=self.bucket_name, Key=key)
            print(f"Data written successfully to {self.bucket_name}/{key}")
        except Exception as e:
            print(f"Error writing data to S3: {str(e)}")

    def read_data(self, key):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            data = response['Body'].read().decode('utf-8')
            print(f"Data read successfully from {self.bucket_name}/{key}")
            return data
        except Exception as e:
            print(f"Error reading data from S3: {str(e)}")
            return None

# Usage example
bucket_name = 'your_bucket_name'
s3_client = S3Client(bucket_name)

# Write data to S3
data_key = 'example.txt'
data_content = 'Hello, S3!'
s3_client.write_data(data_key, data_content)

# Read data from S3
read_data = s3_client.read_data(data_key)
print(read_data)
#########
import pandas as pd
import boto3
from io import StringIO

class S3Client:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3')

    def write_dataframe_to_s3(self, key, dataframe):
        try:
            csv_buffer = StringIO()
            dataframe.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()
            self.s3.put_object(Body=csv_data, Bucket=self.bucket_name, Key=key)
            print(f"DataFrame written successfully to {self.bucket_name}/{key}")
        except Exception as e:
            print(f"Error writing DataFrame to S3: {str(e)}")

    def read_dataframe_from_s3(self, key):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            csv_data = response['Body'].read().decode('utf-8')
            dataframe = pd.read_csv(StringIO(csv_data))
            print(f"DataFrame read successfully from {self.bucket_name}/{key}")
            return dataframe
        except Exception as e:
            print(f"Error reading DataFrame from S3: {str(e)}")
            return None

# Usage example
bucket_name = 'your_bucket_name'
s3_client = S3Client(bucket_name)

# Sample DataFrame
data = {'Name': ['John', 'Jane', 'Adam', 'Emily'],
        'Age': [28, 32, 45, 27],
        'City': ['New York', 'Seattle', 'San Francisco', 'Boston']}
df = pd.DataFrame(data)

# Write DataFrame to S3
data_key = 'data.csv'
s3_client.write_dataframe_to_s3(data_key, df)

# Read DataFrame from S3
read_df = s3_client.read_dataframe_from_s3(data_key)
print(read_df)
