import pandas as pd
import os

directories = ['AdvPython/lab6/April', 'AdvPython/lab6/July', 'AdvPython/lab6/June', 'AdvPython/lab6/March']
all_dataframes = []

for directory in directories:
    try:
        if not os.path.exists(directory):
            raise FileNotFoundError(f"Directory {directory} does not exist.")

        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
                try:
                    df = pd.read_csv(file_path)
                    if df.empty:
                        raise ValueError(f"Error: {filename} is empty.")
                    elif (df < 0).any().any():
                        raise ValueError(f"Error: {filename} contains zero or negative values.")
                    else:
                        all_dataframes.append(df)
                except pd.errors.EmptyDataError:
                    print(f"Error: {filename} is empty or corrupt.")
                except Exception as e:
                    print(f"Error reading {filename}: {e}")

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except Exception as e:
        print(f"Error accessing directory {directory}: {e}")

if not all_dataframes:
    raise ValueError("No valid CSV files found in the provided directories.")

single_dataframe = pd.concat(all_dataframes)
single_dataframe = single_dataframe.dropna()

required_columns = ['ProductID', 'Quantity', 'Date']
for column in required_columns:
    if column not in single_dataframe.columns:
        raise ValueError(f"Missing required column: {column}")

if (single_dataframe['Quantity'] < 0).any():
    raise ValueError("Negative quantities found in data.")

total_sales_by_product = single_dataframe.groupby('ProductID')['Quantity'].sum().reset_index()

if total_sales_by_product.empty:
    raise ValueError("No sales data found for any product.")

try:
    product_names = pd.read_csv('AdvPython/lab6/product_names.csv')
    if product_names.empty:
        raise ValueError("Product names CSV is empty.")
except FileNotFoundError:
    raise FileNotFoundError("Product names file not found.")
except pd.errors.EmptyDataError:
    raise ValueError("Product names CSV is empty or corrupt.")
except Exception as e:
    raise Exception(f"Error reading product names: {e}")

total_sales_by_product = pd.merge(total_sales_by_product, product_names, on='ProductID', how='left')

if 'Date' not in single_dataframe.columns:
    raise ValueError("'Date' column is missing.")

try:
    single_dataframe['MonthYear'] = pd.to_datetime(single_dataframe['Date']).dt.to_period('M')
except Exception as e:
    raise ValueError(f"Error parsing dates: {e}")

unique_months = single_dataframe['MonthYear'].nunique()

total_sales_by_product['AverageQuantityPerMonth'] = round(total_sales_by_product['Quantity'] / 3)

top_5_products = total_sales_by_product.sort_values(by='Quantity', ascending=False).head(5)

print("Top 5 Best-Selling Products:")
print(top_5_products[['ProductID', 'ProductName', 'Quantity', 'AverageQuantityPerMonth']])

try:
    total_sales_by_product[['ProductID', 'ProductName', 'Quantity', 'AverageQuantityPerMonth']].to_csv('AdvPython/lab6/sales_summary.csv', index=False)
    print("Sales summary has been saved to 'sales_summary.csv'")
except Exception as e:
    print(f"Error saving sales summary: {e}")
