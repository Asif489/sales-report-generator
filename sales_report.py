import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =========================
# LOAD DATA
# =========================
file_path = "sales_data_sample.csv"
df = pd.read_csv(file_path, encoding="latin1")

# Convert date
df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])

# =========================
# DATA CLEANING
# =========================
df.dropna(subset=['SALES'], inplace=True)
df['YEAR'] = df['ORDERDATE'].dt.year
df['MONTH'] = df['ORDERDATE'].dt.month

# =========================
# CREATE REPORT FOLDER
# =========================
if not os.path.exists("reports"):
    os.makedirs("reports")

# =========================
# KPI CALCULATIONS
# =========================
total_sales = df['SALES'].sum()
total_orders = df['ORDERNUMBER'].nunique()
total_customers = df['CUSTOMERNAME'].nunique()

print("===== SALES SUMMARY =====")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Customers: {total_customers}")

# =========================
# SALES BY YEAR
# =========================
sales_by_year = df.groupby('YEAR')['SALES'].sum()

plt.figure()
sales_by_year.plot(kind='bar')
plt.title("Sales by Year")
plt.ylabel("Revenue")
plt.savefig("reports/sales_by_year.png")

# =========================
# SALES BY COUNTRY
# =========================
sales_by_country = df.groupby('COUNTRY')['SALES'].sum().sort_values(ascending=False)

plt.figure(figsize=(10,6))
sales_by_country.head(10).plot(kind='bar')
plt.title("Top 10 Countries by Sales")
plt.savefig("reports/sales_by_country.png")

# =========================
# TOP PRODUCTS
# =========================
top_products = df.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False)

plt.figure()
top_products.plot(kind='bar')
plt.title("Sales by Product Line")
plt.savefig("reports/product_sales.png")

# =========================
# MONTHLY SALES TREND
# =========================
monthly_sales = df.groupby(['YEAR', 'MONTH'])['SALES'].sum()

plt.figure(figsize=(12,6))
monthly_sales.plot()
plt.title("Monthly Sales Trend")
plt.savefig("reports/monthly_trend.png")

# =========================
# TOP CUSTOMERS
# =========================
top_customers = df.groupby('CUSTOMERNAME')['SALES'].sum().sort_values(ascending=False).head(10)

plt.figure()
top_customers.plot(kind='bar')
plt.title("Top 10 Customers")
plt.savefig("reports/top_customers.png")

# =========================
# EXPORT SUMMARY TO EXCEL
# =========================
report_file = "reports/sales_report.xlsx"

with pd.ExcelWriter(report_file) as writer:
    sales_by_year.to_excel(writer, sheet_name="Yearly Sales")
    sales_by_country.to_excel(writer, sheet_name="Country Sales")
    top_products.to_excel(writer, sheet_name="Product Sales")
    top_customers.to_excel(writer, sheet_name="Top Customers")

print("\n✅ Report Generated Successfully!")
print(f"📁 Check 'reports/' folder")