import requests
import json

# Databricks workspace URL and token
DATABRICKS_INSTANCE = "https://<databricks-instance>.cloud.databricks.com"
TOKEN = "<your-access-token>"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Group name to add users to
GROUP_NAME = "dumpusers"

def get_all_users():
    """Retrieve all users in the Databricks workspace."""
    url = f"{DATABRICKS_INSTANCE}/api/2.0/preview/scim/v2/Users"
    users = []
    next_page = url

    while next_page:
        response = requests.get(next_page, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch users: {response.text}")

        data = response.json()
        users.extend(data.get("Resources", []))
        next_page = data.get("next", {}).get("href")

    return users

def add_user_to_group(user_id):
    """Add a user to the specified group."""
    url = f"{DATABRICKS_INSTANCE}/api/2.0/preview/scim/v2/Groups"

    # Get the group details to retrieve its ID
    response = requests.get(url, headers=HEADERS, params={"filter": f"displayName eq '{GROUP_NAME}'"})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch group details: {response.text}")

    groups = response.json().get("Resources", [])
    if not groups:
        raise Exception(f"Group '{GROUP_NAME}' does not exist.")

    group_id = groups[0]["id"]

    # Add the user to the group
    patch_url = f"{url}/{group_id}"
    payload = {
        "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
        "Operations": [
            {
                "op": "add",
                "path": "members",
                "value": [
                    {"value": user_id}
                ]
            }
        ]
    }

    response = requests.patch(patch_url, headers=HEADERS, data=json.dumps(payload))
    if response.status_code != 204:
        raise Exception(f"Failed to add user {user_id} to group: {response.text}")

def main():
    try:
        users = get_all_users()
        print(f"Retrieved {len(users)} users from the workspace.")

        for user in users:
            user_id = user["id"]
            user_email = user.get("emails", [{}])[0].get("value", "Unknown")
            print(f"Adding user {user_email} to group '{GROUP_NAME}'...")
            add_user_to_group(user_id)

        print("All users have been added to the group successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
