import boto3

class AWSSSMParameterReader:
    def __init__(self, region_name='us-west-2'):
        self.region_name = region_name
        self.ssm_client = boto3.client('ssm', region_name=self.region_name)

    def get_parameter(self, parameter_name):
        try:
            response = self.ssm_client.get_parameter(
                Name=parameter_name,
                WithDecryption=True
            )
            parameter_value = response['Parameter']['Value']
            return parameter_value
        except self.ssm_client.exceptions.ParameterNotFound:
            print(f"Parameter '{parameter_name}' not found.")
            return None
        except Exception as e:
            print(f"Error retrieving parameter '{parameter_name}': {e}")
            return None

# Usage example
reader = AWSSSMParameterReader()
parameter_name = '/myapp/database/password'

parameter_value = reader.get_parameter(parameter_name)
if parameter_value is not None:
    print(f"The value of '{parameter_name}' is: {parameter_value}")
