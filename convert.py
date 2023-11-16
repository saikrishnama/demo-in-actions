def convert_names(names):
    result = []

    for name in names:
        result.append({
            "Name": name,
            "RoleName": "Default"
        })

    return result

if __name__ == "__main__":
    input_names = ["AA-Group1", "AA-GROUP2", "AA-GROUP3"]

    converted_data = convert_names(input_names)

    print("Converted data:")
    print(json.dumps(converted_data, indent=2))
