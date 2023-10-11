# whs-calculation
calculate a golf player index according to the world handicap system

# how it will work 
the script will look in a defaul folder (/data/scorecards/) for excel files of scorecards. 
the scorecards can be filled manually_ or scraped directly from golfshot.
If manually: use the _scorecard.xlsx template in the templates folder
add the files in data/scorecards/{your_name}/{your_scorecard.xlsx}
note: the {your_name} folder and YOUR_NAME row entry in the excel file should match

If scraping (the easiest): 
scraping is done with chromedriver, so chrome and corresponding chromedriver should be 
available.
simply edit the webdriver variable with the path to your chromedriver in scrape_scorecards.py



# options
usage: 
```
main.py [-h] [-n NUMBER] [-u USERNAME] [-r] [-p PLAYER] [-i PROFILE_ID]
```

options:
  * *-h ->  show this help message and exit*
  * *-u ->  Username for GolfShot account*
  * *-p ->  player name, used for parsing scorecards (should match with player name in scorecard folder)*
  * *-r ->  refresh scorecards - the golfshot data will be scraped*
  * *-n ->  if refresh: number of scorecards to import (Default = 1 i.e. the last round)*
  * *-i ->  if refresh & another user's data is to be screened: the profile id to be screened*




