# Web Scraping with MongoDB

This is a Python project that allows you to collect information (article links, titles and content) from various news websites, such as Bloomberg, CNBC, etc. The collected information is then stored in a MongoDB database, and notifications are sent to a designated Slack channel using the Slack API and to a specified Pusher Channel via Pusher API.

## Project Structure

The project has the following structure:

- `config/`: Contains helper and configuration files.
  - `helpers.py`: Contains method to retrieve values from environment variables.
  - `settings.py`: Contains names of the environment variables used in the project.

- `scrapers/`: Contains scraper classes for extracting links from websites.
  - `base_scraper.py`: Defines the base class `BaseScraper` with core methods.
  - `base_link_scraper.py`: Defines the `BaseLinkScraper` class, which inherits from `BaseScraper`. It provides methods to extract links from websites and implements crawling logic.
  - `implicit_scraper.py`: Defines the main `ImplicitLinkScraper` class, which inherits from `BaseLinkScraper`. It provides tools for scraping different websites, information about which is stored in external sources (setup file). 

- `utils/`: Contains utility files.
  - `mongo.py`: Contains the `MongoDataBase` class, which handles connection and interaction with the MongoDB database.
  - `slack.py`: Defines methods to send messages to specified Slack channel.
  - `webpages.py`: Provides methods to extract information about websites to be scraped.
  - `unfurl.py`: Provides methods to extract metadata from websites.
  - `server.py`: Defines methods to send events to specified Pusher channel.
  - `response.py`: Provides methods to send GET request with custom headers.

- `scrape.py`: The main script from which the project is executed.

- `scrape_test.py`: A script used for testing, which accepts an optional argument `-w (--webpage)` to specify the website to be tested (as recorded in the database).

## Dependencies

The project relies on the following dependencies:

- Python 3.7 or higher,
- MongoDB,
- Required Python packages (can be installed using pip):
  - `pandas`
  - `lxml`
  - `pymongo`
  - `pusher`
  - `slack_sdk`

## Getting Started

To get started follow these steps:

1. Clone the repository: `git clone https://github.com/bettertarder/web_scraping.git`
2. Install the required Python libraries: `pip install -r requirements.txt`
3. Set up your MongoDB database and obtain the connection details.
4. Configure the necessary environment variables described in the `config/settings.py` file such as:
   - `MONGO_URL`: MongoDB cluster URL,
   - `MONGO_DATABASE_NAME`: Name of the MongoDB database,
   - `MONGO_COLLECTION`: Name of the MongoDB collection, where all documents are stored,
   - `MONGO_SETUP`: Name of the MongoDB collection, where special **Source Files** is stored, which holds necessary information for scraping, 
   - `MONGO_TTL_VALUE`: The TTL value used in [TTL index](https://www.mongodb.com/docs/manual/core/index-ttl/) to automatically remove documents from a collection after a certain amount of time,
   - `SLACK_BOT_TOKEN`: Used to interact with the Slack platform via Slack API, 
   - `SLACK_CHANNEL`: Name of the Slack channel to send messages,
   - `SLACK_REPORT_CHANNEL`: Name of the Slack channel to send report messages,
   - `PUSHER_APP_ID`: Represents the Pusher application ID, which is a unique identifier for Pusher application,
   - `PUSHER_APP_KEY`: Represents the Pusher API key, which is a secret key that authorizes access to Pusher application,
   - `PUSHER_APP_SECRET`: Represents the Pusher API secret, which is used to sign authentication requests and validate that they come from trusted server,
   - `PUSHER_APP_CLUSTER`: Specifies the Pusher cluster that application is located in,
   - `TIME_INTERVAL`: Latency in minutes before next scraping.
5. Create and add to MongoDB **Source Files**, which stores information about scraping webpages.
6. Run the `scrape.py` script to start collecting information from the specified websites, storing it in the MongoDB database and sending updates to Slack.

## Example of a **Source File**

<pre>
{
    "name": "ExampleName",
    "enable: true,
    "target_url": "https://www.example.com",
    "crawl_urls": [
        "https://www.example.com/page1",
        "https://www.example.com/page2"
    ],
    "sections":[
        ["//node_page1/node_A"],
        [
            "//node_page2a/node_B",
            "//node_page2b/node_C",
        ]
    ],
    "sponsored": "html_class_sponsored",
    "filter": "(?:/filter1/|/filter2/)\\S*"
}
</pre>

- `name`: The name of the website, 
- `enable`: if `false`, disable this website for scraping, 
- `target_url`: The URL that is the target for crawling, 
- `crawl_urls`: An array of URLs that will be crawled as part of the `target_url`,
- `sections`: An array of arrays of XPaths representing sections/elements of interest within the crawled pages. 
- `sponsored`: **(Unnecessary)** An HTML class name representing a specific element of sponsor content. By default, `sponsored` value is empty and no article will be skipped.
- `filter`: **(Unnecessary)** A regular expression pattern used to filter URLs during crawling. The pattern `'(?:/filter1/|/filter2/)\S*'` will match URLs that contain either `'/filter1/'` or `'/filter2/'` followed by any non-whitespace characters.  By default, `filter` value is `'https\S*'`. 


## XPath

XPath uses path expressions to select nodes in an XML document. The node is selected by following a path or steps. The most useful path expressions are listed below:

| Expression | Description                                                                                           |
|------------|-------------------------------------------------------------------------------------------------------|
| _nodename_ | Selects all nodes with the name "_nodename_"                                                          |
| /          | Selects from the root node                                                                            |
| //         | Selects nodes in the document from the current node that match the selection no matter where they are |
| .          | Selects the current node                                                                              |
| ..         | Selects the parent of the current node                                                                |
| @          | Selects attributes                                                                                    |

More information is [here](https://monilnigdi.medium.com/xpath-for-locating-elements-in-details-809e5a902a51).


## Usage

You can use this project for scraping and collecting information from various news websites. The `scrape.py` script serves as the entry point for the project and can be customized to suit your specific requirements. Additionally, the `scrape_test.py` script allows you to test and verify the logic on a particular website.
