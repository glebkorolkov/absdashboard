# Definitions for chart axes, etc.

# Scatter plot axes
msp_axes = [
    # 'First Filing Date',
    'Origination Date',
    'Loan Amount ($)',
    'Interest Rate (%)',
    # 'Subvention Type',
    'Original Loan Term (months)',
    # 'Grace Period (months)',
    'Vehicle Model',
    # 'New/Used State',
    'Vehicle Model Year',
    # 'Vehicle Type',
    'Vehicle Value ($)',
    'Credit Score',
    # 'Income Verification Level',
    # 'Employment Verification Level',
    # 'Co-obligor',
    'Payment-to-Income Percentage',
    # 'Underwriting Indicator',
    # 'Geographic Location',
    # 'Zero Balance Reason',
    # 'Zero Balance Date',
    # '30 Days Delinquency Date',
    # '90 Days Delinquency Date',
    # 'Repossession Date'
    ]

# Histogram axes
hg_axes = [
    # 'First Filing Date',
    'Origination Date',
    'Loan Amount ($)',
    'Interest Rate (%)',
    'Subvention Type',
    'Original Loan Term (months)',
    'Grace Period (months)',
    'Vehicle Model',
    'New/Used State',
    'Vehicle Model Year',
    'Vehicle Type',
    'Vehicle Value ($)',
    'Credit Score',
    'Income Verification Level',
    'Employment Verification Level',
    'Co-obligor',
    'Payment-to-Income Percentage',
    # 'Underwriting Indicator',
    'Geographic Location',
    # 'Zero Balance Reason',
    # 'Zero Balance Date',
    # '30 Days Delinquency Date',
    # '90 Days Delinquency Date',
    # 'Repossession Date'
]

# Heatmap x and y axes
hm_axes = [
    # 'First Filing Date',
    'Origination Date',
    'Loan Amount ($)',
    'Interest Rate (%)',
    'Subvention Type',
    'Original Loan Term (months)',
    'Grace Period (months)',
    'Vehicle Model',
    'New/Used State',
    'Vehicle Model Year',
    'Vehicle Type',
    'Vehicle Value ($)',
    'Credit Score',
    'Income Verification Level',
    'Employment Verification Level',
    'Co-obligor',
    'Payment-to-Income Percentage',
    # 'Underwriting Indicator',
    'Geographic Location',
    # 'Zero Balance Reason',
    # 'Zero Balance Date',
    # '30 Days Delinquency Date',
    # '90 Days Delinquency Date',
    # 'Repossession Date'
]

# Heatmap z axis
hm_zaxis = [
    'Total count',
    'Non-performing Percentage',
    'Repossessed Percentage',
    # 'First Filing Date',
    # 'Origination Date',
    'Loan Amount ($)',
    'Interest Rate (%)',
    # 'Subvention Type',
    'Original Loan Term (months)',
    # 'Grace Period (months)',
    # 'Vehicle Model',
    # 'New/Used State',
    'Vehicle Model Year',
    # 'Vehicle Type',
    'Vehicle Value ($)',
    'Credit Score',
    # 'Income Verification Level',
    # 'Employment Verification Level',
    # 'Co-obligor',
    'Payment-to-Income Percentage',
    # 'Underwriting Indicator',
    # 'Geographic Location',
    # 'Zero Balance Reason',
    # 'Zero Balance Date',
    # '30 Days Delinquency Date',
    # '90 Days Delinquency Date',
    # 'Repossession Date'
]

# Indicators for display on map
map_metrics = [
    # 'First Filing Date',
    # 'Origination Date',
    'Total count',
    'Non-performing Percentage',
    'Repossessed Percentage',
    'Loan Amount ($) - Avg.',
    'Interest Rate (%) - Avg.',
    # 'Subvention Type',
    'Original Loan Term (months) - Avg.',
    # 'Grace Period (months)',
    # 'Vehicle Model',
    # 'New/Used State',
    # 'Vehicle Model Year',
    # 'Vehicle Type',
    'Vehicle Value ($) - Avg.',
    'Credit Score - Avg.',
    # 'Income Verification Level',
    # 'Employment Verification Level',
    # 'Co-obligor',
    'Payment-to-Income Percentage - Avg.',
    # 'Underwriting Indicator',
    # 'Geographic Location',
    # 'Zero Balance Reason',
    # 'Zero Balance Date',
    # '30 Days Delinquency Date',
    # '90 Days Delinquency Date',
    # 'Repossession Date'
]

# Color definitions
colors = dict(
    green='#4CAF50',
    teal='#009688',
    orange='#ff9800',
    deep_orange='#ff5722',
    amber='#ffc107',
    pink='#e91e63',
    red='#f44336',
    light_grey='#f1f1f1'
)

# Colorscale
colorscales = dict(
    green=['#4CAF50', '#68BA6B', '#83C586', '#9FD0A1', '#BADBBB', '#D6E6D6', '#F1F1F1']
)

# Fonts
font_family = 'Work Sans, Open Sans, Helvetica, sans-serif'

# List of pandas numeric types potentially used
numeric_types = ['float16', 'float32', 'float64',
                 'uint8', 'uint16', 'uint32', 'uint64',
                 'int8', 'int16', 'int32', 'int64']

# Field types
percentage_fields = [
    'Interest Rate (%)',
    'Payment-to-Income Percentage',
    'Non-performing Percentage',
    'Repossessed Percentage',
]

dollar_fields = [
    'Loan Amount ($)',
    'Vehicle Value ($)',
    'Total value'
]

date_fields = [
    'First Filing Date',
    'Origination Date',
    'Zero Balance Date',
    '30 Days Delinquency Date',
    '90 Days Delinquency Date',
    'Repossession Date'
]

categorical_fields = ['Geographic Location', 'Vehicle Model']


# Countable and delinquency fields
countable_metrics = ['Total count']

# {Name: Field}
delinquency_metrics = {'Non-performing Percentage': '30 Days Delinquency Date',
                       'Repossessed Percentage': 'Repossession Date'}

# Text templates
loading_string = "## Loading..."

about_text = '''
#### About

This is a visualization tool for auto loan data from ABS-EE filings. ABS-EE forms are filed to the SEC by issuers 
of asset-backed securities. Each loan is described with approx. 60 data points relating to its terms, 
borrower's credit, vehicle, and activity on the loan. Form are filed on a monthly basis enabling investors and general 
public to track performance of loan portfolios over time. 

This dashboard was designed to make it easier to make sense of auto loan data in ABS-EE filings by utilizing visual 
tools such as histograms, maps, heatmaps and charts.

#### Dataset

Data on portfolio of _{:,}_ auto loans underlying asset-backed notes issued by _{}_.

#### Sources

Data source: [SEC EDGAR](https://searchwww.sec.gov/EDGARFSClient/jsp/EDGAR_MainAccess.jsp?search_text=*&sort=Date&formType=FormABSEE&isAdv=true&stemming=true&numResults=10&querySic=6189&fromDate=11/01/2016&toDate=10/10/2018&numResults=10)  
Scraper on Github: [https://github.com/glebkorolkov/absscraper](https://github.com/glebkorolkov/absscraper)  
Dashboard on Github: [https://github.com/glebkorolkov/absdashboard](https://github.com/glebkorolkov/absdashboard)

#### Author

Gleb Korolkov
'''