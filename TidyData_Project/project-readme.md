# Federal R&D Spending Analysis - Tidy Data Project

## Project Overview

This project demonstrates data transformation and analysis techniques by applying tidy data principles to federal Research & Development (R&D) spending data from 1976 to 2017. By transforming a complex, wide-format dataset into a clean, tidy format, we enable straightforward analysis and visualization of spending trends across different federal departments and over time.

## Data Analysis Highlights

The analysis reveals several important patterns in federal R&D spending:

1. **Department Dominance**: The Department of Defense (DOD) consistently receives the largest portion of federal R&D funding, followed by Health & Human Services (HHS) and the National Institutes of Health (NIH).

2. **Historical Decline**: R&D spending as a percentage of GDP has declined dramatically from nearly 5% in 1976 to less than 1% by 2017, with the sharpest drops occurring in the late 1970s and 1980s.

3. **Funding Fluctuations**: While the DOD saw significant increases during the Reagan administration (1980s) and post-9/11 period (early 2000s), there's a notable decline after 2010, potentially reflecting budget sequestration.

4. **Healthcare Investment**: HHS and NIH show steady growth in R&D funding since the 1990s, reflecting increasing national emphasis on biomedical research.

## Understanding Tidy Data

Tidy data is a standardized way of structuring datasets to facilitate analysis, following these key principles:

1. **Each variable forms a column**: Every measured attribute gets its own column.
2. **Each observation forms a row**: Each data point is in its own row.
3. **Each type of observational unit forms a table**: Related observations are grouped together.

In our original dataset, these principles were violated by:
- Using column names to store two variables (year and GDP)
- Spreading observations (years) across columns instead of rows

Our transformation process addressed these issues to create a properly structured dataset.

## Requirements

To run this project, you need:

- Python 3.6+
- pandas
- numpy
- matplotlib
- seaborn

Install dependencies with:
```bash
pip install pandas numpy matplotlib seaborn
```

## Project Structure

```
.
├── fed_rd_year&gdp.csv       # Original raw data
├── tidy-data-project.py      # Main Python script
├── README.md                 # This file
└── TidyData_Project/         # Output directory
    ├── tidy_federal_rd_data.csv     # Cleaned data in tidy format
    ├── spending_over_time.png       # Visualization of dept spending
    └── spending_percent_gdp.png     # Visualization of GDP percentage
```

## Data Description

### Original Dataset
- **File**: `fed_rd_year&gdp.csv`
- **Structure**: 14 rows (departments) × 43 columns (dept name + 42 year-GDP combinations)
- **Issues**: Years in column headers combined with GDP values (e.g., '1976_gdp1790000000000.0')

### Tidy Dataset
- **File**: `tidy_federal_rd_data.csv`
- **Structure**: 588 rows × 5 columns
- **Variables**:
  - `department`: Federal department name
  - `year`: Year of observation (1976-2017)
  - `gdp`: Gross Domestic Product for that year
  - `spending`: R&D spending amount
  - `spending_pct_gdp`: Spending as percentage of GDP

## Data Transformation Process

The script performs these key transformations:

1. **Melting**: Converting from wide to long format using `pd.melt()`
   - Transforms year columns into rows
   - Creates a temporary 'year_gdp' column containing the original column names

2. **Splitting**: Separating combined variables with `str.split()`
   - Splits 'year_gdp' (e.g., '1976_gdp1790000000000.0') into:
     - 'year' (e.g., '1976')
     - 'gdp_info' (e.g., '1790000000000.0')

3. **Type Conversion & Cleaning**:
   - Converting years to integers
   - Converting GDP values to floats
   - Dropping temporary columns
   - Calculating spending as percentage of GDP

4. **Aggregation & Analysis**:
   - Creating decade-based groupings
   - Calculating growth rates across time periods
   - Building pivot tables for comparative analysis

## Visualizations

### 1. R&D Spending Over Time by Top 5 Departments
![R&D Spending Over Time by Top 5 Departments](TidyData_Project/spending_over_time.png)

This visualization shows:
- DOD's dominant position in R&D funding
- The major increase in defense R&D during the Reagan administration
- A second surge in DOD funding post-9/11
- Steady growth in health-related R&D (HHS/NIH) since the 1990s
- Relative stability in NASA and DOE funding

### 2. Total Federal R&D Spending as Percentage of GDP
![Total Federal R&D Spending as Percentage of GDP](TidyData_Project/spending_percent_gdp.png)

This visualization reveals:
- Dramatic decline in R&D investment relative to GDP since the 1970s
- Brief stabilization in the mid-1980s
- Another plateau in the early 2000s
- Continued decline to historic lows in recent years

## Running the Analysis

To run the analysis in VS Code:

1. Ensure all requirements are installed
2. Save the script as `tidy-data-project.py`
3. Place the data file `fed_rd_year&gdp.csv` in the same directory
4. Create a folder named `TidyData_Project` for outputs
5. Execute the script in VS Code:
   - Right-click in the editor and select "Run Python File in Terminal"
   - Or use the Play button in the top-right corner

## Error Handling

The script includes robust error handling for:
- Missing data files
- Empty CSV files
- Path resolution issues
- Data type conversion problems

## References

- Wickham, H. (2014). "Tidy Data." Journal of Statistical Software, 59(10), 1-23. [Link](https://www.jstatsoft.org/article/view/v059i10)
- Pandas Documentation: [pandas.melt](https://pandas.pydata.org/docs/reference/api/pandas.melt.html)
- Federal R&D Budget Historical Analysis: [AAAS Historical Trends](https://www.aaas.org/programs/r-d-budget-and-policy/historical-trends-federal-rd)
