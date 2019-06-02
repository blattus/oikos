# oikios - the apartment hunter 🏹

# Background

I've been passively looking for an apartment in San Francisco for the past few months and decided to kick my search into high gear by automating it! This set of scripts:
* Automatically searches Craigslist for new apartment listings based on a specified price range and apartment size
* Uses the (Mapbox)[https://www.mapbox.com] API to generate a nice map based on the listing geodata
* Integrates with [Discord](https://discordapp.com/) to send notifications for apartment listings that meet specified criteria

I wrote about this project (link coming soon!) in case you'd like a deeper look.

Note: this requires Python 3.6+

# Setup and Configuration
* Clone this repo
* `pip install requirement.txt`
* Make a copy of `config_example.py` and rename it to `config.py`
* Edit `config.py` to include your Mapbox API key and Discord webhook URL
* Modify `settings.py` to update the settings for your search

# Deployment
When run once, `oikos.py` will search Craiglist for apartment listings and post the results to Discord based on your the settings specified in `settings.py`. In practice, you'll likely want to automate the script to run at a fixed interval. I did this by setting up a cron job to run hourly; you could alternatively run the main script in a while loop or similar. 

# TODO:
- [ ] [maybe] add some directions for hosting on Heroku or DigitalOcean
- [ ] document setting up the cron job