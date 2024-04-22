import requests
from datetime import datetime

# Set your Databricks API endpoint and token
api_endpoint = "https://<YOUR-DATABRICKS-WORKSPACE-URL>/api/2.0/jobs/list"
api_token = "<YOUR-DATABRICKS-API-TOKEN>"

# Define the start and end time for the period you want to query
start_time = datetime(2024, 1, 15, 22, 0).isoformat()
end_time = datetime(2024, 1, 16, 2, 0).isoformat()

# Make the API request to get a list of all jobs
response = requests.get(api_endpoint, headers={"Authorization": "Bearer " + api_token})

# Check if the request was successful
if response.status_code == 200:
    jobs = response.json().get("jobs", [])

    # Filter jobs based on start time and end time
    filtered_jobs = [job for job in jobs if start_time <= job["created_time"] <= end_time]

    # Exclude jobs with policies
    filtered_jobs_without_policies = [job for job in filtered_jobs if not job.get("job_settings", {}).get("max_concurrent_runs")]

    # Print the list of jobs
    for job in filtered_jobs_without_policies:
        print(job)
else:
    print("Failed to retrieve jobs:", response.text)
