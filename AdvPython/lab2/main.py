import os
import csv


reviews_directory = "reviews"
csv_file_path = "lab2/reviews_data.csv"
summary_file_path = "summary.txt"


# Opening CSV file
with open(csv_file_path, "w", newline='') as csvfile:
    fieldnames = ["Customer ID", "Product ID",
                  "Review Date", "Review Rating", "Review Text"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    total_reviews = 0
    valid_reviews_count = 0
    invalid_reviews_count = 0
    product_ratings = {}

    for filename in os.listdir(reviews_directory):
        if filename.endswith(".txt"):
            with open(os.path.join(reviews_directory, filename), "r") as file:
                content = file.read()
                lines = content.strip().split("\n")
                print(content)
                print(lines)

                if len(lines) < 5:
                    invalid_reviews_count += 1
                    continue

                try:
                    customer_id = lines[0].split(": ")[1].strip()
                    product_id = lines[1].split(": ")[1].strip()
                    review_date = lines[2].split(": ")[1].strip()
                    review_rating = int(lines[3].split(": ")[1].strip())
                    review_text = lines[4].split(": ")[1].strip()

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

# Calculate average ratings for each product
average_ratings = {}
for pid in product_ratings:
    average_ratings[pid] = sum(product_ratings[pid]) / \
        len(product_ratings[pid])

# Get top 3 products by average rating
top_products = sorted(
    product_ratings, key=lambda pid: average_ratings[pid], reverse=True)[:3]

# Write summary to a new file
with open(summary_file_path, "w") as summary:
    summary.write(f"Total number of reviews processed: {total_reviews}\n")
    summary.write(f"Total number of valid reviews: {valid_reviews_count}\n")
    summary.write(
        f"Total number of invalid reviews: {invalid_reviews_count}\n")
    summary.write("Top 3 products with the highest average ratings:\n")
    for product_id in top_products:
        summary.write(
            f"Product ID: {product_id}, Average Rating: {average_ratings[product_id]:.2f}\n")
