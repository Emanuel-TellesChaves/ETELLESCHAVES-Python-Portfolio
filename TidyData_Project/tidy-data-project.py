#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Federal R&D Spending - Tidy Data Project

## Project Description
This script applies tidy data principles to analyze federal R&D spending from 1976-2017.
It transforms a wide-format dataset into a tidy format, enabling clear analysis of spending
patterns across different departments and over time.

## Tidy Data Principles Applied:
1. Each variable forms a column
2. Each observation forms a row
3. Each type of observational unit forms a table
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setting plot style
plt.style.use('seaborn-v0_8-whitegrid')  # Clean, professional style for visualizations
sns.set_palette("viridis")  # Using viridis for color-blind friendly visualization

"""
## Data Loading
The original dataset has years as columns with GDP information embedded in column names.
This violates tidy data principles as multiple variables (year and GDP) are stored in column headers.
"""
# 1. loading the data
# ---------------------
try:
    # Getting the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct absolute path to the data file
    file_path = os.path.join(script_dir, 'fed_rd_year&gdp.csv')
    
    # I'm adding this temporarily for debugging purposes
    print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"Looking for file at: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    # Verifying file exists before attempting to read 
    #this is optional, I'm just adding it in case I need it for another project too
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

"""
## Data Transformation Process
To achieve a tidy dataset, we need to:
1. Convert from wide to long format (melting)
2. Separate the combined variables in column names
3. Create proper data types and calculate derived metrics
"""

# 2. Data Cleaning and Transformation to Tidy Format
# --------------------------------------------

"""
### Step 1: Melting the Dataframe
Converting from wide to long format addresses the tidy data principle that each observation
should be in its own row. This transforms our year columns into rows.
"""
print("\n--- Step 1: Melting the dataframe ---")
melted_df = pd.melt(df, id_vars=['department'], 
                   var_name='year_gdp', 
                   value_name='spending')
print(f"Melted dataframe shape: {melted_df.shape}")
print(melted_df.head())

"""
### Step 2: Splitting Combined Variables
The column names contain both year and GDP information (e.g., '1976_gdp1790000000000.0').
We need to separate these into distinct variables to follow the principle that each variable
forms a column.
"""
print("\n--- Step 2: Splitting year_gdp column ---")
melted_df[['year', 'gdp_info']] = melted_df['year_gdp'].str.split('_gdp', expand=True)

# Convert year to integer
melted_df['year'] = melted_df['year'].astype(int)

# Convert GDP string to float with proper handling of scientific notation
melted_df['gdp'] = pd.to_numeric(melted_df['gdp_info'], errors='coerce')

print(melted_df.head())

"""
### Step 3: Finalizing the Tidy Dataset
Now we can create the final tidy dataset by:
1. Removing intermediate columns we no longer need
2. Calculating derived metrics (spending as % of GDP)
3. Reordering columns for clarity
"""
print("\n--- Step 3: Finalizing tidy dataset ---")
# Drop intermediate columns
tidy_df = melted_df.drop(['year_gdp', 'gdp_info'], axis=1)

# Calculate spending as percentage of GDP
# This derived metric allows us to understand R&D investment relative to economic output
tidy_df['spending_pct_gdp'] = (tidy_df['spending'] / tidy_df['gdp']) * 100

# Reordering columns for clarity
tidy_df = tidy_df[['department', 'year', 'gdp', 'spending', 'spending_pct_gdp']]

print("Final tidy dataset:")
print(tidy_df.head())

# Save tidy dataset to current directory instead of nested TidyData_Project subdirectory
tidy_df.to_csv('tidy_federal_rd_data.csv', index=False)

"""
## Data Visualization
With our data now in tidy format, we can easily create insightful visualizations.
These visualizations reveal patterns that would be difficult to see in the original format.
"""

"""
### Visualization 1: R&D Spending Over Time by Top Departments
This time-series visualization helps us understand:
- Which departments receive the most R&D funding
- How spending patterns have changed over time
- Major historical shifts in R&D priorities
"""
# 3. Visualizations
# ----------------

print("\n--- Creating Visualization 1: Spending Over Time by Top Departments ---")

# Identify top 5 departments by total spending
# Focusing on top departments makes the visualization clearer and more meaningful
top_depts = tidy_df.groupby('department')['spending'].sum().nlargest(5).index

# Define a distinct color palette
# Using distinct colors improves differentiation between departments
distinct_colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']

plt.figure(figsize=(14, 8))

# Plot data for each top department with distinct colors
for dept, color in zip(top_depts, distinct_colors):
    dept_data = tidy_df[tidy_df['department'] == dept]
    plt.plot(dept_data['year'], dept_data['spending'] / 1e9, 
             marker='o', 
             linewidth=2, 
             label=dept,
             color=color)

# Add labels and legend
plt.title('R&D Spending Over Time by Top 5 Departments', fontsize=16)
plt.xlabel('Year', fontsize=14)
plt.ylabel('Spending (Billions USD)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True)
plt.xticks(tidy_df['year'].unique()[::5])  # Display every 5th year for readability
plt.tight_layout()
plt.savefig('spending_over_time.png', dpi=300)
plt.show()

"""
### Visualization 2: R&D Spending as Percentage of GDP
This visualization provides important context by showing:
- How R&D investment has changed relative to the size of the economy
- Long-term trends in national R&D prioritization
- Historical periods of increased or decreased investment
"""
print("\n--- Creating Visualization 2: R&D Spending as % of GDP ---")

# Calculating total spending as percentage of GDP for each year
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
plt.xticks(tidy_df['year'].unique()[::5])  # Display every 5th year for readability
plt.tight_layout()
plt.savefig('spending_percent_gdp.png', dpi=300)
plt.show()

"""
## Additional Analyses
With data in tidy format, we can easily perform additional analyses that provide
insights into spending patterns across time periods and departments.
"""

"""
### Analysis 1: Pivot Table of Average Spending by Department and Decade
This aggregation helps identify:
- How department funding has shifted across decades
- Which departments have seen the most significant changes
- Long-term patterns in R&D priorities
"""
# 4. Pivot Table Analysis
# --------------------------
print("\n--- Creating Pivot Table: Average Spending by Department and Decade ---")

# Create a decade column
# Grouping by decade provides a more manageable time scale for historical comparison
tidy_df['decade'] = (tidy_df['year'] // 10) * 10

# Creating pivot table with average spending by department and decade
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

"""
### Analysis 2: Department Growth Rate Analysis
This analysis reveals:
- Which departments have seen the fastest R&D funding growth
- Departments with declining funding
- Potential shifts in national research priorities
"""
# 5. Additional Analysis: Department Spending Growth Rates
# -----------------------------------------------
print("\n--- Department Spending Growth Analysis ---")

# Calculate the compound annual growth rate (CAGR) for each department
# CAGR is a better metric than simple percentage change as it accounts for the time period
# First, get the first and last year for each department
growth_df = tidy_df.groupby(['department', 'year'])['spending'].sum().reset_index()

# Create a pivot table with years as columns and departments as rows
growth_pivot = growth_df.pivot(index='department', columns='year', values='spending')

# Calculating overall growth rate (from first to last available year)
first_year = growth_pivot.columns.min()
last_year = growth_pivot.columns.max()
years_diff = last_year - first_year

growth_pivot['growth_rate'] = ((growth_pivot[last_year] / growth_pivot[first_year]) ** (1 / years_diff) - 1) * 100

# And finally sort by growth rate
top_growth = growth_pivot['growth_rate'].sort_values(ascending=False)

print("Top departments by spending growth rate (1976-2017):")
print(top_growth.head(10))

print("\nBottom departments by spending growth rate (1976-2017):")
print(top_growth.tail(5))
