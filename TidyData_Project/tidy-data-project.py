# Federal R&D Spending - Tidy Data Project

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set plot style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")

# 1. Data Loading
# ---------------
try:
    # Get the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct absolute path to the data file
    file_path = os.path.join(script_dir, 'fed_rd_year&gdp.csv')
    
    # Add this temporarily for debugging
    print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"Looking for file at: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    # Verify file exists before attempting to read
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at: {file_path}")
    
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Display dataset information
    print(f"Original dataset shape: {df.shape}")
    print("\nFirst 5 rows of the original dataset:")
    print(df.head())

except FileNotFoundError as e:
    print(f"Error: {str(e)}")
    print("Please ensure the data file is in the correct location.")
    exit(1)
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
    exit(1)
except Exception as e:
    print(f"Unexpected error loading data: {str(e)}")
    exit(1)

# 2. Data Cleaning and Transformation to Tidy Format
# -------------------------------------------------

# Step 1: Melt the dataframe to convert from wide to long format
# This transforms columns (years) into rows
print("\n--- Step 1: Melting the dataframe ---")
melted_df = pd.melt(df, id_vars=['department'], 
                   var_name='year_gdp', 
                   value_name='spending')
print(f"Melted dataframe shape: {melted_df.shape}")
print(melted_df.head())

# Step 2: Split the year_gdp column into separate year and gdp columns
# The format is like '1976_gdp1790000000000.0'
print("\n--- Step 2: Splitting year_gdp column ---")
melted_df[['year', 'gdp_info']] = melted_df['year_gdp'].str.split('_gdp', expand=True)

# Convert year to integer
melted_df['year'] = melted_df['year'].astype(int)

# Convert GDP string to float with proper handling of scientific notation
melted_df['gdp'] = pd.to_numeric(melted_df['gdp_info'], errors='coerce')

print(melted_df.head())

# Step 3: Create the final tidy dataset
print("\n--- Step 3: Finalizing tidy dataset ---")
# Drop intermediate columns
tidy_df = melted_df.drop(['year_gdp', 'gdp_info'], axis=1)

# Calculate spending as percentage of GDP
tidy_df['spending_pct_gdp'] = (tidy_df['spending'] / tidy_df['gdp']) * 100

# Reorder columns for clarity
tidy_df = tidy_df[['department', 'year', 'gdp', 'spending', 'spending_pct_gdp']]

print("Final tidy dataset:")
print(tidy_df.head())

# Save the tidy dataset
tidy_df.to_csv(os.path.join('TidyData_Project', 'tidy_federal_rd_data.csv'), index=False)

# 3. Visualizations
# ----------------

# Visualization 1: R&D Spending Over Time by Top Departments
print("\n--- Creating Visualization 1: Spending Over Time by Top Departments ---")

# Identify top 5 departments by total spending
top_depts = tidy_df.groupby('department')['spending'].sum().nlargest(5).index

plt.figure(figsize=(14, 8))

# Plot data for each top department
for dept in top_depts:
    dept_data = tidy_df[tidy_df['department'] == dept]
    plt.plot(dept_data['year'], dept_data['spending'] / 1e9, marker='o', linewidth=2, label=dept)

# Add labels and legend
plt.title('R&D Spending Over Time by Top 5 Departments', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Spending (Billions USD)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.xticks(tidy_df['year'].unique()[::5])  # Display every 5th year
plt.tight_layout()
plt.savefig(os.path.join('TidyData_Project', 'spending_over_time.png'), dpi=300)
plt.show()

# Visualization 2: Total R&D Spending as Percentage of GDP Over Time
print("\n--- Creating Visualization 2: R&D Spending as % of GDP ---")

# Calculate total spending as percentage of GDP for each year
annual_data = tidy_df.groupby('year').agg({
    'spending': 'sum',
    'gdp': 'first'  # GDP is the same for all departments in a given year
})
annual_data['spending_pct_gdp'] = (annual_data['spending'] / annual_data['gdp']) * 100

plt.figure(figsize=(14, 8))
plt.plot(annual_data.index, annual_data['spending_pct_gdp'], 
         marker='o', linewidth=3, color='purple')

plt.title('Total Federal R&D Spending as Percentage of GDP', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Percentage of GDP', fontsize=14)
plt.grid(True)
plt.xticks(tidy_df['year'].unique()[::5])  # Display every 5th year
plt.tight_layout()
plt.savefig(os.path.join('TidyData_Project', 'spending_percent_gdp.png'), dpi=300)
plt.show()

# 4. Pivot Table Analysis
# ----------------------
print("\n--- Creating Pivot Table: Average Spending by Department and Decade ---")

# Create a decade column
tidy_df['decade'] = (tidy_df['year'] // 10) * 10

# Create pivot table with average spending by department and decade
pivot_table = pd.pivot_table(
    tidy_df,
    values='spending',
    index='department',
    columns='decade',
    aggfunc='mean'
)

# Format the pivot table to show values in millions
pivot_table_millions = pivot_table / 1e6

print("Average R&D Spending by Department and Decade (in Millions USD):")
print(pivot_table_millions)

# 5. Additional Analysis: Department Spending Growth Rates
# -------------------------------------------------------
print("\n--- Department Spending Growth Analysis ---")

# Calculate the compound annual growth rate (CAGR) for each department
# First, get the first and last year for each department
growth_df = tidy_df.groupby(['department', 'year'])['spending'].sum().reset_index()

# Create a pivot table with years as columns and departments as rows
growth_pivot = growth_df.pivot(index='department', columns='year', values='spending')

# Calculate overall growth rate (from first to last available year)
first_year = growth_pivot.columns.min()
last_year = growth_pivot.columns.max()
years_diff = last_year - first_year

growth_pivot['growth_rate'] = ((growth_pivot[last_year] / growth_pivot[first_year]) ** (1 / years_diff) - 1) * 100

# Sort by growth rate
top_growth = growth_pivot['growth_rate'].sort_values(ascending=False)

print("Top departments by spending growth rate (1976-2017):")
print(top_growth.head(10))

print("\nBottom departments by spending growth rate (1976-2017):")
print(top_growth.tail(5))
