# americanas-scraper

This is a simple Scrapy crawler for alcoholic beverages on www.americanas.com.br

## Parameters examples

The spider will have three parameters as input on command line and they are:

query: what you're looking for
pages: number of pages to be crawled
abv: average alcohol by volume of the items you're crawling

## Running the script

To run the script you just need scrapy installed, then, for example, type:

scrapy crawl americanas -a query=beer -a pages=10 -a abv=0.05 -o beer-output.json

This will crawl 10 result pages for the query "beer", calculate alcohol per unit and then store all crawled items and their extracted properties to an output file named "beer-output.json".
