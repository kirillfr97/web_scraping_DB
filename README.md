# Web Scraping with MongoDB

This is a Python project that allows you to collect information (links and article titles) from various news websites, such as Bloomberg, CNBC, etc. The collected information is then stored in a MongoDB database, and notifications are sent to a designated Slack channel using the Slack API.

## Project Structure

The project has the following structure:

- `config/`: Contains helper and configuration files.
  - `helpers.py`: Contains methods to retrieve specific values from environment variables.
  - `settings.py`: Contains names of the environment variables used in the project.

- `scrapers/`: Contains scraper classes for extracting links from websites.
  - `base_scraper.py`: Defines the base class `BaseScraper` with core methods.
  - `base_link_scraper.py`: Defines the `BaseLinkScraper` class, which inherits from `BaseScraper`. It provides methods to extract links from websites and implements crawling logic.
  - `bloomberg.py`: Defines the main `BloombergScraper` class, which inherits from `BaseLinkScraper`. It specifically targets the `https://www.bloomberg.com`.
  - ...

- `utils/`: Contains utility files.
  - `mongo.py`: Contains the `MongoDataBase` class, which handles connection and interaction with the MongoDB database.
  - `slack.py`: Defines the message_to_slack method for sending messages to Slack.

- `scrape.py`: The main script from which the project is executed.


## Dependencies

The project relies on the following dependencies:

- Python 3.7 or higher
- MongoDB
- Required Python packages (can be installed using pip):
  - `pandas`
  - `beautifulsoup4`
  - `pymongo`
  - `slack_sdk`

## Getting Started

To get started with the web_scraping_DB, follow these steps:

1. Clone the repository: `git clone https://github.com/kirillfr97/web_scraping_DB.git`
2. Install the required Python libraries: `pip install -r requirements.txt`
3. Set up your MongoDB database and obtain the connection details.
4. Configure the necessary environment variables in the `settings.py` file within the `config` directory:
   - `MONGO_URL`: MongoDB cluster URL
   - `MONGO_DATABASE_NAME`: Name of the MongoDB database
   - `SLACK_BOT_TOKEN`: Slack bot token
   - `SLACK_CHANNEL`: Name of the Slack channel to receive messages
   - `TIME_INTERVAL`: Time interval in minutes for receiving updates
5. Run the `scrape.py` script to start collecting information from the specified websites and storing it in the MongoDB database.

## Usage

You can use the web_scraping_DB for scraping and collecting information from various news websites. The `scrape.py` script serves as the entry point for the project and can be customized to suit your specific requirements. 

## License

web_scraping_DB is licensed under the MIT License. Feel free to modify and distribute the project as per the terms of the license.

