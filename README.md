# whs-calculation
calculate a golf player index according to the world handicap system

# how it will work 
the script will look in a defaul folder (/data/scorecards/) for excel files of scorecards. 
the scorecards can be filled manually or scraped directly from golfshot



# options
usage: 
```
main.py [-h] [-n NUMBER] [-u USERNAME] [-r] [-p PLAYER] [-i PROFILE_ID]
```

options:
  * -h, --help            show this help message and exit
  * -n NUMBER, --number NUMBER
                        number of scorecards to import (Default = 1 i.e. the last round)
  * -u USERNAME, --username USERNAME
                        Username for GolfShot account
  * -r, --refresh         Refresh local copy of the disposable domains file.
  * -p PLAYER, --player PLAYER
                        player name, used for parsing scorecards (should match with player name in scorecard folder)
  * -i PROFILE_ID, --profile_id PROFILE_ID
                        the profile id to be screened, if not the data of the user has to be scraped




