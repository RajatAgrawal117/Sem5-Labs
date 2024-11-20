# import kagglehub

# # Download latest version
# path = kagglehub.dataset_download("puneetbhaya/online-retail")

# print("Path to dataset files:", path)
# i = 0
# j = 10
# if(j>=i):
#     print("hello")
    
# q1 = 5
# q2 = 4
# q3 = 10

# total = (q1 + q2 + q3)/3
# print("Total:", total)

# import matplotlib as plt

# plt.plot()

stock = 6
borrowed_books = 3

# Book availability check
while borrowed_books < stock:
    print("Volume available.")
    borrowed_books = borrowed_books+ 1
    print("Available volumes:", stock - borrowed_books)

print("No more volumes available.")