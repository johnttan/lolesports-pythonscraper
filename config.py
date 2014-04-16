"""
Configuration file

retrieveurl + urlmatchnumber is the url that a HTTP GET request is sent to.
Lolesports redirects that URL to the match page.
This URL was chosen over the match page URL because it has a consistent naming structure.

Change the dev settings to enable test runs and/or logging.
Make sure to include correct port.
"""
from configdeployurl import deployurl as deployurl

configuration = {
    'dev': {
        'log': True,
        'scraper': False,
        'database': True,
        'databasescoring': True,
        'playerdatabase': True
    },
    'url': 'mongodb://localhost:27017/test',
    'deployurl': deployurl,
    'port': 27809,
    'database': 'test',
    'deploydatabase':'fantasydraft',
    'retrieveurl': 'http://na.lolesports.com/tourney/match/',
    'urlmatchnumbers': {
        'na': list(range(1669, 1798)),
        'eu': list(range(1800, 1900))
    },
    'gamematchnumbers': {
        'na': list(range(1856, 1956)),
        'eu': list(range(1987, 2500))
    }
}