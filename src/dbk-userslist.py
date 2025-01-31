import requests
from datetime import datetime, timedelta

# Databricks workspace URL and personal access token
DATABRICKS_INSTANCE = 'https://<your-databricks-instance>'
TOKEN = '<your-personal-access-token>'

# API endpoint to list users
USERS_ENDPOINT = f'{DATABRICKS_INSTANCE}/api/2.0/preview/scim/v2/Users'

# Headers for the API request
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# List of exception users (usernames to exclude from the inactive list)
EXCEPTION_USERS = [
    'admin@example.com',  # Example admin account
    'service-account@example.com'  # Example service account
]

# Get the list of users
response = requests.get(USERS_ENDPOINT, headers=headers)

if response.status_code == 200:
    users = response.json().get('Resources', [])
    
    # Current date
    today = datetime.utcnow()
    
    # List to store users who haven't logged in for more than 90 days
    inactive_users = []
    
    for user in users:
        username = user.get('userName')
        
        # Skip exception users
        if username in EXCEPTION_USERS:
            continue
        
        last_login = user.get('lastLogin')
        if last_login:
            last_login_date = datetime.strptime(last_login, '%Y-%m-%dT%H:%M:%S.%fZ')
            if (today - last_login_date) > timedelta(days=90):
                inactive_users.append({
                    'userName': username,
                    'lastLogin': last_login
                })
    
    # Print the list of inactive users
    if inactive_users:
        print("Users who have not logged in for more than 90 days:")
        for user in inactive_users:
            print(f"Username: {user['userName']}, Last Login: {user['lastLogin']}")
    else:
        print("No users found who haven't logged in for more than 90 days.")
else:
    print(f"Failed to fetch users. Status code: {response.status_code}, Response: {response.text}")
