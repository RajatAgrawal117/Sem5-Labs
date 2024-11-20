import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("online_retail.csv", encoding="ISO-8859-1")
df = df.dropna(subset=["CustomerID"])
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["TotalAmountSpent"] = df["Quantity"] * df["UnitPrice"]

customer_df = df.groupby("CustomerID").agg({
    "TotalAmountSpent": "sum",
    "InvoiceDate": "max",
    "Quantity": "sum"
}).reset_index()

customer_df["AveragePurchaseValue"] = np.where(customer_df["Quantity"] > 0,
                                               customer_df["TotalAmountSpent"] / customer_df["Quantity"],
                                               0)

current_date = pd.to_datetime("today")
customer_df["DaysSinceLastPurchase"] = (current_date - customer_df["InvoiceDate"]).dt.days
customer_df["AveragePurchaseValue"].fillna(customer_df["AveragePurchaseValue"].mean(), inplace=True)
customer_df.replace([np.inf, -np.inf], np.nan, inplace=True)
customer_df.dropna(subset=["AveragePurchaseValue"], inplace=True)

mean_spent = customer_df["TotalAmountSpent"].mean()
median_spent = customer_df["TotalAmountSpent"].median()
std_spent = customer_df["TotalAmountSpent"].std()

mean_items = customer_df["Quantity"].mean()
median_items = customer_df["Quantity"].median()
std_items = customer_df["Quantity"].std()

with open("customer_segmentation_summary.txt", "w") as f:
    f.write(f"Mean Total Amount Spent: {mean_spent}\n")
    f.write(f"Median Total Amount Spent: {median_spent}\n")
    f.write(f"Standard Deviation of Total Amount Spent: {std_spent}\n\n")
    f.write(f"Mean Total Items Purchased: {mean_items}\n")
    f.write(f"Median Total Items Purchased: {median_items}\n")
    f.write(f"Standard Deviation of Total Items Purchased: {std_items}\n\n")

X = customer_df[["TotalAmountSpent", "Quantity", "DaysSinceLastPurchase", "AveragePurchaseValue"]]
kmeans = KMeans(n_clusters=5, random_state=42)
customer_df["Segment"] = kmeans.fit_predict(X)

customer_df["Segment"] = customer_df["Segment"].map({
    0: "High Spenders",
    1: "Frequent Shoppers",
    2: "Inactive Customers",
    3: "Occasional Spenders",
    4: "Low Spenders"
})

plt.figure(figsize=(10, 8))
sns.scatterplot(x="TotalAmountSpent", y="Quantity", hue="Segment", data=customer_df, palette="Set2")
plt.title("Customer Segmentation based on Total Amount Spent and Quantity")
plt.savefig("customer_segmentation_plot_5_clusters.png")

segment_summary = customer_df.groupby("Segment").agg({
    "TotalAmountSpent": ["mean", "median"],
    "Quantity": ["mean", "median"],
    "DaysSinceLastPurchase": ["mean", "median"],
    "AveragePurchaseValue": ["mean", "median"]
})

with open("customer_segmentation_summary.txt", "a") as f:
    f.write("\nSegment Insights (5 Clusters):\n")
    f.write(segment_summary.to_string())
