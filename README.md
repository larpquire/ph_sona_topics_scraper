## ph_sona_topics_scraper
This scraper extracts topic/content data of the different Philippine SONA speeches from the [Philippine Presidential Museum website](http://malacanang.gov.ph/sona-content-charts-and-word-clouds/). The webpage to be scraped is quite javascript-heavy and most of the key information are generated dynamically, so selenium is used along with PhantomJS to get the job done (although, scrapy with splash is also widely recommended, I can't seem to install splash without using docker).

## Requirements
1. Selenium (`pip install selenium`)
2. PhantomJS (from http://phantomjs.org/download.html)

## Running the scraper
cd to the directory containing the file sona_topics_scraper and then run:
```
$ python sona_topics_scraper.py
```
It's going to take a few minutes for the scraping to finish. This is due to the tons of `time.sleep()` calls included in the script, so you might want to comment them out. (Hey, I don't want to make it look like I'm launching a DDoS attack or something.).

Anyway, once finished, a file `output_data.json` should magically appear in the directory.

## Output data
Each item in the JSON file is a Python `dict` with the following keys and values:
* `author`: Name of the president.
* `title`: Title of the SONA speech.
* `delivered`: Date when the speech was delivered.
* `topics`: `dict` containing the topics as keys and their corresponding proportion to the content as values.

## Contributing
Please feel free to comment or suggest improvements.
