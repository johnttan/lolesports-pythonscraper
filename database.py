import json
import pymongo
from pprint import pprint
from pymongo import MongoClient
from config import configuration as cfg
from playerinfo import playerinfo
from scraper import retrieveandprocessGame as retrieve


"""
This module commits data retrieved
by scraper.py to the MongoDB database specified in config.py.

Can be imported into a scheduling module.
Import retrievelatest(region) to retrieve the latest games.
Specify argument region as string, i.e. retrievelatest('na')
"""

"""
Retrieve(matchnumber). Returns matchdoc dict.
"""

client = MongoClient(cfg['deployurl'])
db = client[cfg['deploydatabase']]
cUsers = db.Users
cPlayers = db.Players
cGames = db.Games
cRetrievedURLs = db.RetrievedURLs
cGames.create_index("gameID", unique=True)

"""
Checks if there is document for storing retrieved URLs. If not, one is made.
"""
if cRetrievedURLs.count() == 0:
    retrievedURLs = {
        'na':[],
        'eu':[]
    }
    cRetrievedURLs.insert(retrievedURLs)

"""
Resets the RetrievedURLs collection in MongoDB. Hardcoded regions.
"""
def resetretrievedurls():
    cRetrievedURLs.update({}, {"$set":
                                    {
                                        "na": [],
                                        "nanext": cfg['urlmatchnumbers']['na'][0],
                                        "eu": [],
                                        "eunext": cfg['urlmatchnumbers']['eu'][0]
                                    }
                                })
"""
Updates the RetrievedURLs document to reflect the games that have been retrieved,
and what the next game is (region + next)
"""
def updatelatestgame(urlmatchnumber, region):
    retrievedURLs = cRetrievedURLs.find_one()
    cRetrievedURLs.update({}, {"$addToSet":
                                    {
                                        region: urlmatchnumber
                                    }
                                })
    cRetrievedURLs.update({}, {"$set":
                                    {
                                        region + 'next': urlmatchnumber
                                    }
                                })

"""
Retrieves and stores latest games in a region, commits data to database.
"""
def retrievelatest(region):
    try:
        while True:
            url =  {
            region: cRetrievedURLs.find_one()[region + 'next']
            }
            try:
                #This is where the game is stored in database.
                #Throws DuplicateKeyError if game already exists
                cGames.insert(retrieve(url[region]))
            except pymongo.errors.DuplicateKeyError:
                print(str(url[region]) + ' already retrieved.')
            updatelatestgame(url[region] + 1, region)
            
    except KeyError:
        print('No more games ' + region)
        pass

"""
Calls functions to retrieve and store all NA and EU games
Note: Resets RetrievedURLs to empty arrays and the first game of each region.
"""

def retrieveallgames():
    resetretrievedurls()
    retrievelatest('na')
    retrievelatest('eu')


def retrievelatestna():
    retrievelatest('na')
def retrievelatesteu():
    retrievelatest('eu')


exports = {
    'retrievelatest': retrievelatest,
    'resetretrieved': resetretrievedurls
}
