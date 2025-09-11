# Import libraries
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

#  Load dataset
df = pd.read_csv("Superstore.csv", encoding='latin1')   # ensure file is in same folder

# Data Cleaning
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])
df.drop_duplicates(inplace=True)

# Feature Engineering
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Month-Year'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()

# INTERACTIVE VISUALIZATIONS
# 1) Monthly Sales Trend
monthly_sales = df.groupby('Month-Year')['Sales'].sum().reset_index()
fig = px.line(monthly_sales, x="Month-Year", y="Sales",
              title="Monthly Sales Trend")
fig.show()

# 2) Sales by Category
cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
fig = px.bar(cat_sales, x="Category", y="Sales",
             title="Total Sales by Category", text="Sales")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.show()

# 3) Top 10 Sub-Categories by Sales
subcat_sales = (
    df.groupby('Sub-Category')['Sales']
    .sum()
    .reset_index()
    .sort_values('Sales', ascending=False)
    .head(10)
)
fig = px.bar(subcat_sales, x="Sales", y="Sub-Category", orientation="h",
             title="Top 10 Sub-Categories by Sales", text="Sales")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.show()

# 4) Region-wise Sales & Profit
region_perf = df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
fig = px.bar(region_perf, x="Region", y="Sales", title="Sales by Region", text="Sales")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.show()

fig = px.bar(region_perf, x="Region", y="Profit", title="Profit by Region", text="Profit")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.show()

# 5) Top 10 Customers by Sales
top_customers = (
    df.groupby('Customer Name')['Sales']
    .sum()
    .reset_index()
    .sort_values('Sales', ascending=False)
    .head(10)
)
fig = px.bar(top_customers, x="Sales", y="Customer Name", orientation="h",
             title="Top 10 Customers by Sales", text="Sales")
fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.show()

# 6) Discount vs Profit Relationship
fig = px.scatter(df, x="Discount", y="Profit", color="Category",
                 size="Sales", hover_data=["Sub-Category"],
                 title="Discount vs Profit by Category")
fig.show()

# 7) Correlation Heatmap
corr = df[['Sales','Profit','Discount','Quantity']].corr()
fig = ff.create_annotated_heatmap(
    z=corr.values,
    x=list(corr.columns),
    y=list(corr.index),
    annotation_text=corr.round(2).values,
    colorscale='Viridis',
    showscale=True
)
fig.update_layout(title="Correlation Heatmap")
fig.show()

# CUSTOMER BEHAVIOR ANALYSIS
cust_stats = df.groupby('Customer ID').agg(
    total_sales=('Sales', 'sum'),
    total_profit=('Profit', 'sum'),
    orders=('Order ID', 'nunique')
).reset_index()
cust_stats['avg_order_value'] = cust_stats['total_sales'] / cust_stats['orders']

print("\n📊 Customer Stats Summary:\n", cust_stats.describe())

# Save outputs
monthly_sales.to_csv("monthly_sales.csv", index=False)
cat_sales.to_csv("category_sales.csv", index=False)
cust_stats.to_csv("customer_stats.csv", index=False)

print("\n✅ Analysis Complete! All interactive charts displayed in browser.")

