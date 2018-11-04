# Database configuration file

# Defaults
defaults = {
    'autoloans_table': 'autoloans_flat',
    'filings_table': 'filings'
}

# Credentials for database with asset data
db_config = {
    'type': 'mysql',
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': '3306',
    'name': 'assets'
}
