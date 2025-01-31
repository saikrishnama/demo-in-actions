import requests
import pandas as pd
from datetime import datetime, timedelta
# pip install pandas openpyxl

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

# Get the list of users
response = requests.get(USERS_ENDPOINT, headers=headers)

if response.status_code == 200:
    users = response.json().get('Resources', [])
    
    # Current date
    today = datetime.utcnow()
    
    # List to store user details
    user_data = []
    
    for user in users:
        last_login = user.get('lastLogin')
        email = user.get('emails', [{}])[0].get('value', 'N/A')  # Extract email
        
        if last_login:
            last_login_date = datetime.strptime(last_login, '%Y-%m-%dT%H:%M:%S.%fZ')
            last_login_str = last_login_date.strftime('%Y-%m-%d')
        else:
            last_login_str = "Never Logged In"
        
        user_data.append({
            'Username': user.get('userName'),
            'Email ID': email,
            'Last Login': last_login_str
        })
    
    # Create a DataFrame
    df = pd.DataFrame(user_data, columns=['Username', 'Email ID', 'Last Login'])
    
    # Save to Excel file
    excel_filename = 'databricks_users.xlsx'
    df.to_excel(excel_filename, index=False)
    
    print(f"User data has been saved to {excel_filename}")

else:
    print(f"Failed to fetch users. Status code: {response.status_code}, Response: {response.text}")
