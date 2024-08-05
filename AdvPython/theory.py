import json

data = {
    "name": "John",
    "age": 30,
    "city": "New York"
    
}
file_path = "data.json"
with open(file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)
    print("Data has been written to", file_path)
