# Twitter Bot - Advanced Search
A Python bot that uses Twitter's advanced search to filter and scrape results.

## Category
Web scraping/automation/data collection

## Purpose
Collect data from Twitter using the Advanced Search Option.

## User needs
Helping out the team's performance analyst collect data to let Committee teams know how much MPs have interacted with a Committee's Twitter account. The bot uses Twitter's advanced search formula to look for MPs tweets that mention the name of a Committee twitter account in a specific time span. Once the results are available on the page, the bot scrapes the results, filters out duplicates and writes them to a .csv file, ready for analysis.

## Data collected
- Mentions i.e. an MP sending out a tweet that includes a Committee's twitter handle

## File structure
Main file `tweet-advanced-search.py` that imports the following module
```
tweet-advanced-search.py
|_return_stats.py
```

## Dependencies
Built with Python 3.6.4 and the following modules
- [selenium](https://selenium-python.readthedocs.io/index.html)
- time
- re
- csv

## Developed by
Kostas Koutoupis ([@kkoutoup](https://github.com/kkoutoup)) for the Web and Publications Unit (WPU) of the Chambers and Committee Office (CCT), House of Commons

