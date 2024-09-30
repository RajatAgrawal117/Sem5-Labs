# Swapping two numbers without using a third variable
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))

# Using arithmetic operators
a = a + b
b = a - b
a = a - b

print("After swapping:")
print("First number:", a)
print("Second number:", b)
