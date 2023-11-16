import json

def remove_duplicates(input_data):
    try:
        # Remove duplicates based on all key-value pairs
        unique_data = [dict(t) for t in {tuple(record.items()) for record in input_data}]

        return unique_data

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    sample_data = [
        {
            "Name": "AA-ADMIN1",
            "RoleName": "Default"
        },
        {
            "Name": "AA-ADMIN1",
            "RoleName": "Default"
        },
        {
            "Name": "AA-ADMIN1",
            "RoleName": "Default"
        },
        {
            "Name": "AA-ADMIN2",
            "RoleName": "Default"
        }
    ]

    cleaned_data = remove_duplicates(sample_data)

    if cleaned_data:
        print("Original data:")
        print(json.dumps(sample_data, indent=2))
        print("\nCleaned data:")
        print(json.dumps(cleaned_data, indent=2))
    else:
        print("Failed to remove duplicates.")
