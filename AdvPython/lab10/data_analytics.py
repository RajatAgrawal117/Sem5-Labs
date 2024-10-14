import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("online_retail.csv", encoding="ISO-8859-1")

# 2. Data Cleaning
# Drop rows with missing CustomerID
df = df.dropna(subset=["CustomerID"])

# Convert InvoiceDate to datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Create TotalAmountSpent (Quantity * UnitPrice)
df["TotalAmountSpent"] = df["Quantity"] * df["UnitPrice"]

# Group by CustomerID to create the required features for segmentation
customer_df = df.groupby("CustomerID").agg({
    "TotalAmountSpent": "sum",
    "InvoiceDate": "max",
    "Quantity": "sum"
}).reset_index()

# Calculate Average Purchase Value, but handle cases where Quantity is zero to avoid division by zero
customer_df["AveragePurchaseValue"] = np.where(customer_df["Quantity"] > 0,
                                               customer_df["TotalAmountSpent"] /
                                               customer_df["Quantity"],
                                               0)

# Convert InvoiceDate to the number of days since last purchase
current_date = pd.to_datetime("today")
customer_df["DaysSinceLastPurchase"] = (
    current_date - customer_df["InvoiceDate"]).dt.days

# Handle missing values by imputing the mean (you can also use median if preferred)
customer_df["AveragePurchaseValue"].fillna(
    customer_df["AveragePurchaseValue"].mean(), inplace=True)

# Replace any infinite values that might have occurred
customer_df.replace([np.inf, -np.inf], np.nan, inplace=True)
customer_df.dropna(subset=["AveragePurchaseValue"], inplace=True)

# 3. Descriptive Statistics
# Calculating basic statistics
mean_spent = customer_df["TotalAmountSpent"].mean()
median_spent = customer_df["TotalAmountSpent"].median()
std_spent = customer_df["TotalAmountSpent"].std()

mean_items = customer_df["Quantity"].mean()
median_items = customer_df["Quantity"].median()
std_items = customer_df["Quantity"].std()

# Save the statistics to a file
with open("customer_segmentation_summary.txt", "w") as f:
    f.write(f"Mean Total Amount Spent: {mean_spent}\n")
    f.write(f"Median Total Amount Spent: {median_spent}\n")
    f.write(f"Standard Deviation of Total Amount Spent: {std_spent}\n\n")
    f.write(f"Mean Total Items Purchased: {mean_items}\n")
    f.write(f"Median Total Items Purchased: {median_items}\n")
    f.write(f"Standard Deviation of Total Items Purchased: {std_items}\n\n")

# 4. Customer Segmentation using K-means Clustering
# Select relevant features for clustering
X = customer_df[["TotalAmountSpent", "Quantity",
                 "DaysSinceLastPurchase", "AveragePurchaseValue"]]

# Apply K-means clustering
kmeans = KMeans(n_clusters=5, random_state=35)
customer_df["Segment"] = kmeans.fit_predict(X)

# 5. Visualization
# Scatter plot of TotalAmountSpent vs Quantity colored by segment
plt.figure(figsize=(20, 12))
sns.scatterplot(x="TotalAmountSpent", y="Quantity",
                hue="Segment", data=customer_df, palette="Set2")
plt.title("Customer Segmentation based on Total Amount Spent and Quantity")

# Save the plot as an image
plt.savefig("customer_segmentation_plot.png")

# 6. Customer Insights
segment_summary = customer_df.groupby("Segment").agg({
    "TotalAmountSpent": ["mean", "median"],
    "Quantity": ["mean", "median"],
    "DaysSinceLastPurchase": ["mean", "median"],
    "AveragePurchaseValue": ["mean", "median"]
})

# Save segment insights to the text file
with open("customer_segmentation_summary.txt", "a") as f:
    f.write("Segment Insights:\n")
    f.write(segment_summary.to_string())
