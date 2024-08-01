import csv
import matplotlib.pyplot as plt

x = []
y = []

with open('./lab1/example.csv', 'r') as xyz:
    reader = csv.reader(xyz)
    next(reader)  
    for row in reader:
        x.append(row[0])
        y.append(float(row[1]))  

plt.bar(x, y)

plt.xlabel('Year')
plt.ylabel('Sales')
plt.title('Bar Graph')

plt.show()

