import pandas as pd

# File paths
file_names = ["lab2alt/data1.csv", "lab2alt/data2.csv", "lab2alt/data3.csv", "lab2alt/data4.csv", "lab2alt/data5.csv"]

# Initialize counters
total_reviews = 0
valid_reviews_count = 0
invalid_reviews_count = 0

# List to store valid DataFrames
valid_dataframes = []

for file_name in file_names:
    df = pd.read_csv(file_name)
    
    # Debug: Print the column names
    print(f"Columns in {file_name}: {df.columns.tolist()}")

    # Perform validation checks directly in DataFrame
    valid_reviews = df[
        (df['Customer ID'].str.len() == 6) &
        (df['Product ID'].str.len() == 10) &
        (df['Review Rating'].astype(int).between(1, 5)) &
        (df['Review Date'].str.len() == 10) &
        (df['Review Text'].notna())
    ]
    
    # Count valid and invalid reviews
    total_reviews += len(df)
    valid_reviews_count += len(valid_reviews)
    invalid_reviews_count += len(df) - len(valid_reviews)  # Invalid reviews are the remainder

    # Append valid reviews to list
    valid_dataframes.append(valid_reviews)

# Combine all valid DataFrames into one
combined_df = pd.concat(valid_dataframes, ignore_index=True)

# Group by Product ID and calculate the average rating
average_ratings = combined_df.groupby('Product ID')['Review Rating'].mean()

# Identify top 3 products with the highest average ratings
top_products = average_ratings.nlargest(3)

# Write the summary to a text file
with open("summary.txt", "w") as summary_file:
    summary_file.write(f"Total number of reviews processed: {total_reviews}\n")
    summary_file.write(f"Total number of valid reviews: {valid_reviews_count}\n")
    summary_file.write(f"Total number of invalid reviews: {invalid_reviews_count}\n")
    summary_file.write("Top 3 products with the highest average ratings:\n")
    for product_id, avg_rating in top_products.items():
        summary_file.write(f"Product ID: {product_id}, Average Rating: {avg_rating:.2f}\n")

print("Summary file created: summary.txt")
