# ABS Auto Loan Dashboard

## General information

This is a dashboard for visualization of auto loan data previously scraped from the SEC website (see project [ABS-EE Web Scraper](https://github.com/glebkorolkov/absscraper)). The dashboard is interactive and uses [Plotly Dash](https://plot.ly/products/dash/) as its engine. My objective was to create an EDA tool for auto loan data contained in ABS-EE filings which in its raw form is just a collection of many large xml files.

## Data

Dataset contains data on several hundred thousand auto loans provided by several car manufacturers to their customers in USA. Data was obtained through web scraping of ABS-EE filings from the SEC web site. Since November 2016 auto loan companies that issue asset-backed securities are obliged to file detailed loan-level data on their loan portfolios to the SEC on a monthly basis.

Database dump for the project is available here: https://s3.amazonaws.com/abseeexhibitstorage/autoloan/autoloans.sql.

## Dashboard

I used Plotly Dash as my dashboard engine because it is:
1. Interactive
2. Comes with many ready-to-use components (charts, controls, etc.)
3. Looks great
4. Provides fine-grained control over the look and feel of the dashboard
5. Free and open-source

The dashboard is a web app built on Flask and React. it uses MySQL database as a data source. At startup it loads data for a single auto loan portfolio (trust) and displays it. It then loads additional data when the user changes their trust selection. Data is cached in the filesystem to speed up display of previously loaded datasets.

## Installation

To deploy the dashboard locally follow these steps:
1. Set up a local MySQL server 
2. Create database 'assets' and import the provided database dump into it
3. Change database credentials in `config.py` if required
4. Clone dashboard code to any location
5. Navigate to the folder containing `requirements.txt` file
6. Create python virtual environment by running `python -m venv venv` or `python3 -m venv venv` (depending on the system) and then activate it: `source venv/bin/activate`
7. Install dependencies: `pip install -r requirements.txt`
8. Navigate to folder containing `dashboard.py` and run `python dashboard.py run`
9. Use this url in your browser to view the dashboard: `http://127.0.0.1:8050/`

Deployment on a remore server is a bit more complicated because you will need to set up a production web server (such as nginx or apache) as well as an application server (e.g. gunicorn or uwsgi).

A working example of the dashboard is available here: http://ec2-34-237-140-39.compute-1.amazonaws.com:8050/.

## Usage

Data is displayed separately for each ABS issuer (trust). Every issue has its own trust and loan portfolio created for it. As a result there are several separate loan portfolios for each car financing company. User can select car manufacturer and one of its trusts at the top of the page. Be patient! Datasets are quite large and loading each new one takes a bit of time.

There are several types of charts available: scatter plot, histogram, heat map, geographical map, and line graph. For each chart you can select what data you want to be displayed on chart axes. For example, you might want to check out if there is any relationship between interest rates and borrowers' credit scores or income-to-payment ratios. Or see if loan amount depends on a car model. In which US states do borrowers have higher credit score on average? Did it affect their interest rates?



