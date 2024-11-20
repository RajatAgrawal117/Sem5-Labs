import csv

def calculate_average_marks(input_file, output_file):
    with open(input_file, mode='r') as infile:
        reader = csv.DictReader(infile)
        student_averages = []
        print(reader.fieldnames)
        print(reader.line_num)  
        print(reader.dialect)
        print(reader.reader)
        print(reader.restkey)
        for row in reader:
            student_name = row['student_name']
            total_marks = 0
            num_subjects = 0
            
            for i in range(1, 6):
                total_marks += int(row[f'subject{i}'])
                num_subjects += 1
            
            average_marks = total_marks / num_subjects
            
            # Store the result
            student_averages.append({
                'student_name': student_name,
                'average_marks': average_marks
            })

    with open(output_file, mode='w', newline='') as outfile:
        fieldnames = ['student_name', 'average_marks']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(student_averages)

# Define input and output file names
input_csv = "data/student.csv"
output_csv = 'average.csv'

# Calculate average marks and write to the output CSV file
calculate_average_marks(input_csv, output_csv)

print("Average marks have been calculated and written to", output_csv)
