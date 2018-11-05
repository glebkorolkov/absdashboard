from sqlalchemy import create_engine
import numpy as np
import pandas as pd
from config import db_config
from definitions import *


class Helper(object):
    """
    Helper class.
    """

    @staticmethod
    def get_db_engine(user, password, host, port, database):
        """
        Create database engine.
        :param user: db username
        :param password: db password
        :param host: db host/ip address
        :param port: db port (should be 3306 in most cases)
        :param database: db name
        :return: sqlalchemy engine object
        """
        return create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

    @staticmethod
    def get_trust_list():
        # Create database engine
        engine = Helper.get_db_engine(
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['name']
        )
        query = "SELECT DISTINCT trustCik, trustName FROM assets.filings " \
                "WHERE trustCik IN " \
                "   (SELECT DISTINCT trustCik FROM assets.autoloans_flat) " \
                "ORDER BY trustName, trustCik;"
        trust_table = pd.read_sql(query, engine)

        def extract_name(trust_name):
            """
            Extract manufacturer's name from trust name.
            :param trust_name: string
            :return: string
            """
            delimiters = [
                'Vehicle Owner',
                'Credit Auto Owner',
                'Financial Consumer',
                'Auto Receivables',
                'Auto Loan',
                'Auto Owner'
            ]

            name = trust_name
            for delimiter in delimiters:
                if delimiter in trust_name:
                    name = trust_name.split(delimiter)[0].strip()
                    break
            return name

        trust_table['trustCik'] = trust_table['trustCik'].astype(str)
        trust_table['manufacturer'] = trust_table['trustName'].apply(extract_name)
        manufacturers = sorted(trust_table['manufacturer'].unique())
        trusts = {}
        for manufacturer in manufacturers:
            m_trusts = trust_table[trust_table['manufacturer'] == manufacturer][['trustCik', 'trustName']]\
                    .rename(columns={'trustCik': 'cik', 'trustName': 'name'})\
                    .to_dict('index').values()
            m_trusts = list(m_trusts)
            trusts[manufacturer] = m_trusts

        return trusts

    @staticmethod
    def load_autoloans_by_cik(ciks):
        """
        Load data from database for a list of ciks (trust identifiers).
        :param ciks: list of cik strings
        :return: pandas dataframe
        """

        # Create database engine
        engine = Helper.get_db_engine(
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['name']
        )
        # Fields to be extracted from database
        extractable_fields = [
            'dateFirstFiling',
            'originationDate',
            'originalLoanAmount',
            'originalInterestRatePercentage',
            'subvented',
            'originalLoanTerm',
            'gracePeriodNumber',
            'vehicleModelName',
            'vehicleNewUsedCode',
            'vehicleModelYear',
            'vehicleTypeCode',
            'vehicleValueAmount',
            'obligorCreditScore',
            'obligorIncomeVerificationLevelCode',
            'obligorEmploymentVerificationCode',
            'coObligorIndicator',
            'paymentToIncomePercentage',
            'underwritingIndicator',
            'obligorGeographicLocation',
            'zeroBalanceCode',
            'zeroBalanceEffectiveDate',
            'delinquency30Days',
            'delinquency90Days',
            'repossessedDate'
        ]
        # Build query
        query = f"SELECT {', '.join(extractable_fields)} FROM assets.autoloans_flat \
                 WHERE trustCik IN ({', '.join(ciks)});"
        # Get data (takes a while)
        data = pd.read_sql(query, engine,
                           parse_dates=[
                               'dateFirstFiling',
                               'originationDate',
                               'zeroBalanceEffectiveDate',
                               'delinquency30Days',
                               'delinquency90Days',
                               'repossessedDate'
                           ]
                           )

        # Define code mappings
        vehicle_new_used_map = {'1': 'New', '2': 'Used'}
        vehicle_type_map = {
            '1': 'Car',
            '2': 'Truck',
            '3': 'SUV',
            '4': 'Motorcycle',
            '98': 'Other',
            '99': 'Unknown'
        }
        income_verification_map = {
            '1': 'Not Stated',
            '2': 'Not Verified',
            '3': 'Lvl 3 Verified',
            '4': 'Lvl 4 Verified',
            '5': 'Lvl 5 Verified'
        }
        employment_verification_map = {
            '1': 'Not Stated',
            '2': 'Not Verified',
            '3': 'Lvl 3 Verified'
        }
        zero_balance_map = {
            '1': 'Terminated',
            '2': 'Repurchased or Replaced',
            '3': 'Charged-off',
            '4': 'Servicing Transfer',
            '99': 'Unavailable'
        }
        # yes_no_map = {'0': 'No', '1': 'Yes'}
        subvented_map = {
            '0': 'No',
            '1': 'Rate',
            '2': 'Principal',
            '1|2': 'Both'
        }

        # Convert some fields to categorical type
        data[[
            'subvented',
            'vehicleNewUsedCode',
            'vehicleModelName',
            'vehicleTypeCode',
            'obligorIncomeVerificationLevelCode',
            'obligorEmploymentVerificationCode',
            'coObligorIndicator',
            'obligorGeographicLocation',
            'zeroBalanceCode'
        ]] = data[[
            'subvented',
            'vehicleNewUsedCode',
            'vehicleModelName',
            'vehicleTypeCode',
            'obligorIncomeVerificationLevelCode',
            'obligorEmploymentVerificationCode',
            'coObligorIndicator',
            'obligorGeographicLocation',
            'zeroBalanceCode'
        ]].astype('category')

        # Clean fields
        data.obligorCreditScore = \
            data.obligorCreditScore.apply(lambda x: np.nan if x.lower() in ["no score", "none", "0", 0] else x)
        data.obligorGeographicLocation = data.obligorGeographicLocation.apply(lambda x: x.strip())

        # Rename categories
        data.subvented = data.subvented.cat.rename_categories(subvented_map)
        data.vehicleNewUsedCode = data.vehicleNewUsedCode.cat.rename_categories(vehicle_new_used_map)
        data.vehicleTypeCode = data.vehicleTypeCode.cat.rename_categories(vehicle_type_map)
        data.obligorIncomeVerificationLevelCode = data.obligorIncomeVerificationLevelCode\
            .cat.rename_categories(income_verification_map)
        data.obligorEmploymentVerificationCode = data.obligorEmploymentVerificationCode\
            .cat.rename_categories(employment_verification_map)
        data.coObligorIndicator = data.coObligorIndicator.map(lambda x: 'Yes' if x == 1 else 'No')
        data.zeroBalanceCode = data.zeroBalanceCode.cat.rename_categories(zero_balance_map)

        # Change type for non-categorical columns
        data.paymentToIncomePercentage = data.paymentToIncomePercentage.astype('float16')
        data.originalInterestRatePercentage = data.originalInterestRatePercentage.astype('float16')
        data.vehicleModelYear = data.vehicleModelYear.astype('uint16')
        data.originalLoanTerm = data.originalLoanTerm.astype('uint16')
        data.originalLoanAmount = data.originalLoanAmount.astype('float32')
        data.vehicleValueAmount = data.vehicleValueAmount.astype('float32')
        data.obligorCreditScore = data.obligorCreditScore.astype('float16')

        # Cap values at 1.0 for paymentToIncomePercentage
        data.paymentToIncomePercentage = data.paymentToIncomePercentage.map(lambda x: min(x, 1))

        # Rename columns
        data.rename({
            'dateFirstFiling': 'First Filing Date',
            'originationDate': 'Origination Date',
            'originalLoanAmount': 'Loan Amount ($)',
            'originalInterestRatePercentage': 'Interest Rate (%)',
            'subvented': 'Subvention Type',
            'originalLoanTerm': 'Original Loan Term (months)',
            'gracePeriodNumber': 'Grace Period (months)',
            'vehicleModelName': 'Vehicle Model',
            'vehicleNewUsedCode': 'New/Used State',
            'vehicleModelYear': 'Vehicle Model Year',
            'vehicleTypeCode': 'Vehicle Type',
            'vehicleValueAmount': 'Vehicle Value ($)',
            'obligorCreditScore': 'Credit Score',
            'obligorIncomeVerificationLevelCode': 'Income Verification Level',
            'obligorEmploymentVerificationCode': 'Employment Verification Level',
            'coObligorIndicator': 'Co-obligor',
            'paymentToIncomePercentage': 'Payment-to-Income Percentage',
            'underwritingIndicator': 'Underwriting Indicator',
            'obligorGeographicLocation': 'Geographic Location',
            'zeroBalanceCode': 'Zero Balance Reason',
            'zeroBalanceEffectiveDate': 'Zero Balance Date',
            'delinquency30Days': '30 Days Delinquency Date',
            'delinquency90Days': '90 Days Delinquency Date',
            'repossessedDate': 'Repossession Date'
        }, axis=1, inplace=True)

        # Add features
        data['Loan-To-Value (%)'] = data['Loan Amount ($)'] / data['Vehicle Value ($)']

        print(f"Loaded dataset of {len(data)} items. "
              f"Memory usage: {round(data.memory_usage().sum()/(1024*1024), 2)} Mb")
        return data

    @staticmethod
    def get_format(fieldname, precision=0, style='plotly'):
        """
        Get format string.
        :param fieldname: string
        :param precision: no of decimal places
        :param style: either 'plotly' or 'python'
        :return: format string in js/plotly or python format
        """
        frmts = ["d", "{}"]
        if fieldname in percentage_fields:
            frmts = [f'.{precision}%', '{' + f':.{precision}%' + '}']
        elif fieldname in dollar_fields:
            frmts = ['$s', '${' + f':,.{precision}f' + '}']
        elif fieldname in date_fields:
            frmts = ["", ""]

        return frmts[0] if style == 'plotly' else frmts[1]

    @staticmethod
    def get_months(min_date, max_date):
        """
        Compute end-of-month dates between two dates passed as arguments.
        :param min_date: python datetime object
        :param max_date: python datetime object
        :return: list of pandas timestamp objects
        """
        mdates = (pd.date_range(min_date, max_date, freq='M', closed='left').strftime("%Y-%m-%d").tolist())
        # if max_date.strftime("%Y-%m-%d") not in mdates:
        #     mdates.append(max_date.strftime("%Y-%m-%d"))
        # if min_date.strftime("%Y-%m-%d") not in mdates:
        #     mdates.insert(0, min_date.strftime("%Y-%m-%d"))

        return mdates
