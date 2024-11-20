import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from PyPDF2 import PdfMerger

# Constants
INPUT_CSV = "orders.csv"
OUTPUT_FOLDER = "invoices"
MERGED_PDF = "all_invoices.pdf"

# Step 1: Load Order Data
def load_order_data():
    try:
        orders = pd.read_csv(INPUT_CSV)
        return orders
    except FileNotFoundError:
        print(f"Error: {INPUT_CSV} file not found.")
        return pd.DataFrame()

# Step 2: Calculate Total Amount and Create PDFs
def create_invoice(order):
    # Extract order details
    order_id = order["Order ID"]
    customer_name = order["Customer Name"]
    product_name = order["Product Name"]
    quantity = int(order["Quantity"])
    unit_price = float(order["Unit Price"])
    total_amount = quantity * unit_price
    date_of_purchase = datetime.now().strftime("%Y-%m-%d")
    
    # PDF file path
    pdf_file_path = os.path.join(OUTPUT_FOLDER, f"{order_id}.pdf")
    
    # Create PDF invoice
    c = canvas.Canvas(pdf_file_path, pagesize=A4)
    c.drawString(100, 750, f"Invoice Number: {order_id}")
    c.drawString(100, 730, f"Date of Purchase: {date_of_purchase}")
    c.drawString(100, 710, f"Customer Name: {customer_name}")
    c.drawString(100, 690, f"Product Name: {product_name}")
    c.drawString(100, 670, f"Quantity: {quantity}")
    c.drawString(100, 650, f"Unit Price: ${unit_price:.2f}")
    c.drawString(100, 630, f"Total Amount: ${total_amount:.2f}")
    c.save()
    
    print(f"Invoice created for Order ID {order_id}")
    return pdf_file_path

# Step 3: Generate Invoices for All Orders
def generate_invoices():
    orders = load_order_data()
    if orders.empty:
        return []

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    pdf_paths = []
    for _, order in orders.iterrows():
        pdf_path = create_invoice(order)
        pdf_paths.append(pdf_path)
    
    return pdf_paths

# Step 4: Merge PDFs into a Single PDF
def merge_pdfs(pdf_paths):
    merger = PdfMerger()
    for pdf_path in pdf_paths:
        merger.append(pdf_path)
    
    merger.write(MERGED_PDF)
    merger.close()
    print(f"All invoices merged into {MERGED_PDF}")

# Main Program
def main():
    pdf_paths = generate_invoices()
    if pdf_paths:
        merge_pdfs(pdf_paths)
    else:
        print("No invoices to merge.")

if __name__ == "__main__":
    main()
