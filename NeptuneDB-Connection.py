import sys
import json
import datetime
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import ReadOnlyCredentials
from types import SimpleNamespace
import boto3

# Configuration
protocol = 'https'

# Default values
default_host = "your-neptune-endpoint"
default_port = 8182
default_method = "GET"
default_query_type = "status"
default_query = ""

# Use EC2 instance profile for AWS credentials
session = boto3.Session()
credentials = session.get_credentials().get_frozen_credentials()
region = session.region_name

def validate_input(method, query_type):
    if method not in ["GET", "POST"]:
        print('Method must be "GET" or "POST", but is "' + method + '".')
        sys.exit()
    if method == "GET" and query_type == "sparqlupdate":
        print('SPARQL UPDATE is not supported in GET mode. Please choose POST.')
        sys.exit()

def get_canonical_uri_and_payload(query_type, query, method):
    if query_type == 'sparql':
        canonical_uri = '/sparql/'
        payload = {'query': query}
    elif query_type == 'sparqlupdate':
        canonical_uri = '/sparql/'
        payload = {'update': query}
    elif query_type == 'gremlin':
        canonical_uri = '/gremlin/'
        payload = {'gremlin': query}
        if method == 'POST':
            payload = json.dumps(payload)
    elif query_type == 'openCypher':
        canonical_uri = '/openCypher/'
        payload = {'query': query}
    elif query_type == "loader":
        canonical_uri = "/loader/"
        payload = query
    elif query_type == "status":
        canonical_uri = "/status/"
        payload = {}
    else:
        print('Query type should be from ["gremlin", "sparql", "sparqlupdate", "loader", "status"] but is "' + query_type + '".')
        sys.exit()
    return canonical_uri, payload

def make_signed_request(host, method, query_type, query):
    service = 'neptune-db'
    endpoint = f"{protocol}://{host}:{default_port}"
    
    print(f"\n+++++ USER INPUT +++++\nhost = {host}\nmethod = {method}\nquery_type = {query_type}\nquery = {query}")

    # Validate input
    validate_input(method, query_type)

    # Get canonical URI and payload
    canonical_uri, payload = get_canonical_uri_and_payload(query_type, query, method)

    # Assign payload to data or params
    data = payload if method == 'POST' else None
    params = payload if method == 'GET' else None

    # Create request URL
    request_url = endpoint + canonical_uri

    # Create and sign request
    creds = SimpleNamespace(
        access_key=credentials.access_key,
        secret_key=credentials.secret_key,
        token=credentials.token,
        region=region,
    )
    request = AWSRequest(method=method, url=request_url, data=data, params=params)
    SigV4Auth(creds, service, region).add_auth(request)

    # Send the request
    if method == 'GET':
        print('++++ BEGIN GET REQUEST +++++')
        print(f'Request URL = {request_url}')
        response = requests.get(request_url, headers=request.headers, verify=False, params=params)
    elif method == 'POST':
        print('\n+++++ BEGIN POST REQUEST +++++')
        print(f'Request URL = {request_url}')
        response = requests.post(request_url, headers=request.headers, verify=False, data=data)
    else:
        print('Request method is neither "GET" nor "POST", something is wrong here.')
        sys.exit()

    print('\n+++++ RESPONSE +++++')
    print(f'Response code: {response.status_code}\n')
    print(response.text)
    response.close()
    return response.text

def main():
    # Replace these default values as needed
    host = default_host
    method = default_method
    query_type = default_query_type
    query = default_query

    make_signed_request(host, method, query_type, query)

if __name__ == "__main__":
    main()
