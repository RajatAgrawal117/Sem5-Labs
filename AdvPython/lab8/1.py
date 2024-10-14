import os
import pandas as pd

base_dir = 'D:\\SEM-5\\ADVANCE_PYTHON_LAB\\prac 6'
stores = [f's{i}' for i in range(1, 6)]

def generate_report(store):
    store_dir = os.path.join(base_dir, store)
    all_data = []
    
    for i in range(1, 13):
        file_path = os.path.join(store_dir, f'{str(i).zfill(2)}.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            
            if 'product_name' in df.columns and 'no_units_sold' in df.columns:
                if (df['no_units_sold'] < 0).any():
                    print(f"Error: Negative values found in {file_path}. These rows will be excluded.")
                    df = df[df['no_units_sold'] >= 0]
                
                if not df.empty:
                    all_data.append(df)
                else:
                    print(f"No valid data left in {file_path} after filtering out negative values.")
            else:
                print(f"Error: Columns not as expected in {file_path}")
    
    if all_data:
        all_data_df = pd.concat(all_data)
        total_sales = all_data_df.groupby('product_name')['no_units_sold'].sum().reset_index()
        total_sales = total_sales.sort_values(by='no_units_sold', ascending=False)
        overall_total_sales = total_sales['no_units_sold'].sum()
        top_5_products = total_sales.head(5)
        
        top_5_summary = "\n".join([
            f"{row['product_name']} - {row['no_units_sold']} units"
            for i, row in top_5_products.iterrows()
        ])
        
        report = pd.DataFrame({
            'Total Sales': [overall_total_sales],
            'Top 5 Best Selling Products': [top_5_summary]
        })
        
        report_file_path = os.path.join(store_dir, f'{store}_report.csv')
        report.to_csv(report_file_path, index=False)
        
        print(f'Report generated for {store} and saved at {report_file_path}')
    else:
        print(f"No valid data found for {store}")

for store in stores:
    generate_report(store)
