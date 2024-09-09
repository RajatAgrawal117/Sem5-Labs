import pandas as pd
import os

directories = ['AdvPython/lab6/April', 'AdvPython/lab6/July', 'AdvPython/lab6/June','AdvPython/lab6/March']
all_dataframes = []

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            df = pd.read_csv(os.path.join(directory, filename))
            all_dataframes.append(df)

single_dataframe = pd.concat(all_dataframes)
single_dataframe = single_dataframe.dropna()

print(single_dataframe)

total_sales_by_product = single_dataframe.groupby('ProductID')['Quantity'].sum().reset_index()

print(total_sales_by_product)

product_names = pd.read_csv('AdvPython/lab6/product_names.csv')

total_sales_by_product = pd.merge(total_sales_by_product, product_names, on='ProductID')

single_dataframe['MonthYear'] = pd.to_datetime(single_dataframe['Date']).dt.to_period('M')
unique_months = single_dataframe['MonthYear'].nunique()

total_sales_by_product['AverageQuantityPerMonth'] = total_sales_by_product['Quantity'] / unique_months

top_5_products = total_sales_by_product.sort_values(by='Quantity', ascending=False).head(5)

print("Top 5 Best-Selling Products:")
print(top_5_products[['ProductID', 'ProductName', 'Quantity', 'AverageQuantityPerMonth']])

total_sales_by_product[['ProductID', 'ProductName', 'Quantity', 'AverageQuantityPerMonth']].to_csv('sales_summary.csv', index=False)

print("Sales summary has been saved to 'sales_summary.csv'")
