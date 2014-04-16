lolesportspythonscraper
=======================

Scrapes lolesports.com for match and player data. 

scraper.py contains function for scraping data from lolesports.com based on the URL match number (e.g. the number at end of http://na.lolesports.com/tourney/match/2183)

database.py commits the data to a MongoDB database as specified in config.py

playerinfo.py contains dictionary with player information (teams/roles).
