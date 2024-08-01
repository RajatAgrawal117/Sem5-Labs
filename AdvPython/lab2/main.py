import os
import csv
from statistics import mean

# Directories and file paths
reviews_directory = "lab2/reviews"
csv_file_path = "lab2/reviews_data.csv"
summary_file_path = "lab2/summary.txt"

# Prepare to write to CSV
with open(csv_file_path, "w", newline='') as csvfile:
    fieldnames = ["Customer ID", "Product ID", "Review Date", "Review Rating", "Review Text"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    total_reviews = 0
    valid_reviews_count = 0
    invalid_reviews_count = 0
    product_ratings = {}

    # Process each text file in the directory
    for filename in os.listdir(reviews_directory):
        if filename.endswith(".txt"):
            with open(os.path.join(reviews_directory, filename), "r") as file:
                content = file.read()
                lines = content.strip().split("\n")
                
                if len(lines) < 5:
                    invalid_reviews_count += 1
                    continue
                
                try:
                    customer_id = lines[0].split(": ")[1].strip()
                    product_id = lines[1].split(": ")[1].strip()
                    review_date = lines[2].split(": ")[1].strip()
                    review_rating = int(lines[3].split(": ")[1].strip())
                    review_text = lines[4].split(": ")[1].strip()

                    # Validate extracted data
                    if (len(customer_id) == 6 and len(product_id) == 10 and
                        1 <= review_rating <= 5 and len(review_date) == 10 and review_text):
                        writer.writerow({
                            "Customer ID": customer_id,
                            "Product ID": product_id,
                            "Review Date": review_date,
                            "Review Rating": review_rating,
                            "Review Text": review_text
                        })
                        total_reviews += 1
                        valid_reviews_count += 1

                        if product_id not in product_ratings:
                            product_ratings[product_id] = []
                        product_ratings[product_id].append(review_rating)
                    else:
                        invalid_reviews_count += 1
                except (IndexError, ValueError):
                    invalid_reviews_count += 1

# Analyze the CSV data and produce a summary
average_ratings = {pid: mean(ratings) for pid, ratings in product_ratings.items()}

# Get top 3 products
top_products = sorted(average_ratings.items(), key=lambda item: item[1], reverse=True)[:3]

# Write summary to a new file
with open(summary_file_path, "w") as summary:
    summary.write(f"Total number of reviews processed: {total_reviews}\n")
    summary.write(f"Total number of valid reviews: {valid_reviews_count}\n")
    summary.write(f"Total number of invalid reviews: {invalid_reviews_count}\n")
    summary.write("Top 3 products with the highest average ratings:\n")
    for product_id, avg_rating in top_products:
        summary.write(f"Product ID: {product_id}, Average Rating: {avg_rating:.2f}\n")
