from argparse import ArgumentParser

from utils.mongo import MongoData, MongoDataBase
from scrapers.implicit_scraper import ImplicitLinkScraper

# Create an argument parser
parser = ArgumentParser()

# Add an optional argument to specify the name of the web-page in the setup file
parser.add_argument('-w', '--webpage', help='Unnecessary argument: name of web-page in setup file')

# Parse the command-line arguments
args = parser.parse_args()

# Establish a connection to the MongoDB cluster
cluster = MongoDataBase()

# Get file with info
file = cluster.setup_file

# Retrieve information base on the command-line argument
test_info = file.get(args.webpage) if args.webpage in file \
    else list(file.values())[-1]  # or use the last value from the file

# Creating scraper with test information
scraper = ImplicitLinkScraper(**test_info)

# Scrape the web-page
page_data = scraper.start()

# Check if there is data in the page_data DataFrame
if not page_data.empty:
    print(page_data[MongoData.Title].values)
else:
    print('Nothing to show!')
