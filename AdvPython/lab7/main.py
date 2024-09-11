import json
import os


def validate_entry(entry):
    required_fields = ['country', 'date',
                       'confirmed_cases', 'deaths', 'recovered']
    for field in required_fields:
        if field not in entry:
            return False
    if not isinstance(entry['date'], str) or not entry['date']:
        return False
    for key in ['confirmed_cases', 'deaths', 'recovered']:
        if not all(sub_key in entry[key] for sub_key in ['total', 'new']):
            return False
    return True


folder_path = ''
file_names = ['Germany.json', 'Russia.json', 'Ukraine.json',
              'Italy.json', 'USA.json', 'Japan.json', 'Europe.json', 'England.json']
combined_data = []

for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            valid_data = []
            for entry in data:
                if validate_entry(entry):
                    valid_data.append(entry)
                else:
                    print(
                        f"Error: Missing or invalid data in file {file_name} entry: {entry}")
            combined_data.extend(valid_data)
            print(f"Successfully loaded and validated data from {file_path}")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")

countries = set(item['country'] for item in combined_data)
print("Available countries:")
for country in sorted(countries):
    print(f"- {country}")

selected_country = input("Enter the country you want to view data for: ")
filtered_data = [
    item for item in combined_data if item['country'] == selected_country]

output_file_path = os.path.join(folder_path, 'output.txt')
with open(output_file_path, 'w') as output_file:
    if filtered_data:
        output_file.write(f"Data for {selected_country}:\n\n")
        for record in filtered_data:
            output_file.write(f"Date: {record['date']}\n")
            output_file.write(
                f"Confirmed Cases: {record['confirmed_cases']['total']} (New: {record['confirmed_cases']['new']})\n")
            output_file.write(
                f"Deaths: {record['deaths']['total']} (New: {record['deaths']['new']})\n")
            output_file.write(
                f"Recovered: {record['recovered']['total']} (New: {record['recovered']['new']})\n")
            output_file.write("-" * 40 + "\n")
        output_file.write(
            f"\nData for {selected_country} written to {output_file_path}.\n")
    else:
        output_file.write(f"Data for {selected_country} not found.\n")
        print(f"No data available for {selected_country}.")

country_case_totals = {}
for item in combined_data:
    country = item['country']
    total_cases = item['confirmed_cases']['total']
    if country not in country_case_totals:
        country_case_totals[country] = total_cases
    else:
        country_case_totals[country] = max(
            country_case_totals[country], total_cases)

sorted_countries = sorted(country_case_totals.items(),
                          key=lambda x: x[1], reverse=True)
top_5_highest = sorted_countries[:5]
top_5_lowest = sorted_countries[-5:]

with open(output_file_path, 'a') as output_file:
    output_file.write("\nTop 5 countries with the highest number of cases:\n")
    for country, cases in top_5_highest:
        output_file.write(f"{country}: {cases} cases\n")

    output_file.write("\nTop 5 countries with the lowest number of cases:\n")
    for country, cases in top_5_lowest:
        output_file.write(f"{country}: {cases} cases\n")

print(f"Top 5 highest and lowest cases data written to {output_file_path}.")


with open(output_file_path, 'r') as output_file:
    print("\n" + output_file.read())
