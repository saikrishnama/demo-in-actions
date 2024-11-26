import os
import json
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import InstanceMetadataProvider, InstanceMetadataFetcher
from types import SimpleNamespace
import requests

# Configuration
protocol = 'https'

# Default values
default_host = "your-neptune-endpoint.amazonaws.com:8182"
default_method = "GET"
default_query_type = "status"
default_query = ""

# Get credentials from the EC2 instance profile
def get_instance_profile_credentials():
    provider = InstanceMetadataProvider(fetcher=InstanceMetadataFetcher(timeout=1, num_attempts=2))
    creds = provider.load()
    if not creds:
        raise Exception("Could not retrieve credentials from the instance profile.")
    return SimpleNamespace(
        access_key=creds.access_key,
        secret_key=creds.secret_key,
        token=creds.token,
        region=os.getenv('AWS_REGION', 'us-east-1'),
    )

# Function to make signed requests
def make_signed_request(host, method, query_type, query):
    service = 'neptune-db'
    endpoint = protocol + '://' + host

    print()
    print('+++++ USER INPUT +++++')
    print(f'host = {host}')
    print(f'method = {method}')
    print(f'query_type = {query_type}')
    print(f'query = {query}')

    # Validate input
    if method not in ['GET', 'POST']:
        raise ValueError(f"Method must be 'GET' or 'POST', but is {method}.")

    # Canonical URI and Payload
    canonical_uri, payload = get_canonical_uri_and_payload(query_type, query, method)

    data = payload if method == 'POST' else None
    params = payload if method == 'GET' else None

    # Create Request URL
    request_url = endpoint + canonical_uri

    # Fetch credentials
    creds = get_instance_profile_credentials()

    # Create and sign request
    request = AWSRequest(method=method, url=request_url, data=data, params=params)
    SigV4Auth(creds, service, creds.region).add_auth(request)

    # Send Request
    r = None
    if method == 'GET':
        print(f'Request URL: {request_url}')
        r = requests.get(request_url, headers=request.headers, verify=False, params=params)
    elif method == 'POST':
        print(f'Request URL: {request_url}')
        r = requests.post(request_url, headers=request.headers, verify=False, data=data)
    
    if r:
        print()
        print('+++++ RESPONSE +++++')
        print(f'Response code: {r.status_code}')
        response = r.text
        r.close()
        print(response)
        return response

# Helper to get canonical URI and payload
def get_canonical_uri_and_payload(query_type, query, method):
    if query_type == 'sparql':
        return '/sparql/', {'query': query}
    elif query_type == 'sparqlupdate':
        return '/sparql/', {'update': query}
    elif query_type == 'gremlin':
        payload = {'gremlin': query}
        return '/gremlin/', json.dumps(payload) if method == 'POST' else payload
    elif query_type == 'openCypher':
        return '/openCypher/', {'query': query}
    elif query_type == "loader":
        return "/loader/", query
    elif query_type == "status":
        return "/status/", {}
    elif query_type == "gremlin/status":
        return "/gremlin/status/", {}
    elif query_type == "openCypher/status":
        return "/openCypher/status/", {}
    elif query_type == "sparql/status":
        return "/sparql/status/", {}
    else:
        raise ValueError(f'Invalid query_type: {query_type}')

# Main Execution
if __name__ == "__main__":
    # Defaults
    host = default_host
    method = default_method
    query_type = default_query_type
    query = default_query

    # Call Neptune
    try:
        make_signed_request(host, method, query_type, query)
    except Exception as e:
        print(f"Error: {str(e)}")
