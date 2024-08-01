# import os
# import csv
# from statistics import mean

# def extract_review_info(file_content):
#     lines = file_content.strip().split("\n")
#     if len(lines) < 5:
#         return None  
    
#     try:
#         customer_id = lines[0].split(": ")[1].strip()
#         product_id = lines[1].split(": ")[1].strip()
#         review_date = lines[2].split(": ")[1].strip()
#         review_rating = int(lines[3].split(": ")[1].strip())
#         review_text = lines[4].split(": ")[1].strip()

        
#         if (len(customer_id) == 6 and len(product_id) == 10 and
#             1 <= review_rating <= 5 and len(review_date) == 10 and review_text):
#             return customer_id, product_id, review_date, review_rating, review_text
#     except (IndexError, ValueError):
#         pass  

#     return None

# def save_to_csv(directory, output_csv):
#     with open(output_csv, "w", newline='') as csvfile:
#         fieldnames = ["Customer ID", "Product ID", "Review Date", "Review Rating", "Review Text"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         writer.writeheader()
#         for filename in os.listdir(directory):
#             if filename.endswith(".txt"):
#                 with open(os.path.join(directory, filename), "r") as file:
#                     content = file.read()
#                     review_info = extract_review_info(content)
#                     if review_info:
#                         writer.writerow({
#                             "Customer ID": review_info[0],
#                             "Product ID": review_info[1],
#                             "Review Date": review_info[2],
#                             "Review Rating": review_info[3],
#                             "Review Text": review_info[4]
#                         })

# def analyze_reviews(csv_file, summary_file):
#     product_ratings = {}
#     total_reviews = 0
#     valid_reviews_count = 0
#     invalid_reviews_count = 0

#     with open(csv_file, "r") as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             total_reviews += 1
#             try:
#                 product_id = row["Product ID"]
#                 review_rating = int(row["Review Rating"])
#                 if product_id and review_rating:
#                     if product_id not in product_ratings:
#                         product_ratings[product_id] = []
#                     product_ratings[product_id].append(review_rating)
#                     valid_reviews_count += 1
#                 else:
#                     invalid_reviews_count += 1
#             except (ValueError, KeyError):
#                 invalid_reviews_count += 1


#     average_ratings = {pid: mean(ratings) for pid, ratings in product_ratings.items()}

#     # Get top 3 products
#     top_products = sorted(average_ratings.items(), key=lambda item: item[1], reverse=True)[:3]

#     # Write summary to a new file
#     with open(summary_file, "w") as summary:
#         summary.write(f"Total number of reviews processed: {total_reviews}\n")
#         summary.write(f"Total number of valid reviews: {valid_reviews_count}\n")
#         summary.write(f"Total number of invalid reviews: {invalid_reviews_count}\n")
#         summary.write("Top 3 products with the highest average ratings:\n")
#         for product_id, avg_rating in top_products:
#             summary.write(f"Product ID: {product_id}, Average Rating: {avg_rating:.2f}\n")

# # Specify the directory containing the review text files and output files
# reviews_directory = "lab2/reviews"
# csv_file_path = "lab2/reviews_data.csv"
# summary_file_path = "lab2/summary.txt"

# # Extract data from text files and save to CSV
# save_to_csv(reviews_directory, csv_file_path)

# # Analyze the CSV data and produce a summary
# analyze_reviews(csv_file_path, summary_file_path)