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

trusts = {
    'Toyota': [
        {'cik': '1694919', 'name': 'Toyota Auto Receivables 2017 A Owner Trust'},
        {'cik': '1704304', 'name': 'Toyota Auto Receivables 2017 B Owner Trust'},
        {'cik': '1709987', 'name': 'Toyota Auto Receivables 2017 C Owner Trust'},
        {'cik': '1718100', 'name': 'Toyota Auto Receivables 2017 D Owner Trust'},
        {'cik': '1725585', 'name': 'Toyota Auto Receivables 2018 A Owner Trust'},
        {'cik': '1736712', 'name': 'Toyota Auto Receivables 2018 B Owner Trust'},
        {'cik': '1745763', 'name': 'Toyota Auto Receivables 2018 C Owner Trust'},
    ]
}

trusts_flat = []
for t in trusts:
    trusts_flat += trusts[t]

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

colorscales = dict(
    green=['#4CAF50', '#68BA6B', '#83C586', '#9FD0A1', '#BADBBB', '#D6E6D6', '#F1F1F1']
)

font_family = 'Work Sans, Open Sans, Helvetica, sans-serif'

numeric_types = ['float16', 'float32', 'float64',
                 'uint8', 'uint16', 'uint32', 'uint64',
                 'int8', 'int16', 'int32', 'int64']

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

countable_metrics = ['Total count']

# {Name: Field}
delinquency_metrics = {'Non-performing Percentage': '30 Days Delinquency Date',
                       'Repossessed Percentage': 'Repossession Date'}

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

Data on portfolio of auto loans underlying asset-backed notes issued by _{}_.

#### Sources

Data source: [EDGAR]  
Github repository: [TBD]

#### Author

Gleb Korolkov  
gleb[dot]korolkov[at]gmail[dot]com
'''