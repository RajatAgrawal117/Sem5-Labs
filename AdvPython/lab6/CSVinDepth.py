import pandas as pd
import os
# Define the directories
directories = ['April', 'July', 'June']
# initialize an empty list to store all the dataframes
all_dataframes = []

# loop through each directory
for directory in directories:
    # loop through each CSV file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            # read the CSV file into a pandas dataframe
            df = pd.read_csv(os.path.join(directory, filename))
            # append the dataframe to the list
            all_dataframes.append(df)

# concatenate all the dataframes into a single dataframe
single_dataframe = pd.concat(all_dataframes)
single_dataframe = single_dataframe.dropna() #skip null values of productID adn StoreID

print(single_dataframe)

# Calculate total sales for each Product_ID
total_sales_by_product = single_dataframe.groupby('ProductID')['Quantity'].sum().reset_index()

print(total_sales_by_product)