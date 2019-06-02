import config
from craigslist import CraigslistHousing
import database
from logger import log
from mapbox import Static
import requests
import settings

def get_map(latitude,longitude):
	service = Static(access_token=config.MAPBOX_ACCESS_TOKEN)

	point_on_map = {
		'type' : 'Feature',
		'properties' : {'name' : 'point'},
		'geometry' : {
			'type' : 'Point',
			'coordinates' : [longitude, latitude]
		}
	}

	response = service.image('mapbox.streets', retina=True, features=point_on_map, lon=longitude, lat=latitude, z=15)
	
	return response.url

def send_notification(listing):
	log.info('Sending notification for listing ID {}'.format(listing['craigslist_id']))

	# set the color of the notification based on where it falls in my target price range
	# TODO: move these to config.py?
	if listing['price'] <= settings.green_max:
		color = 2664261  # green
	elif listing['price'] > settings.green_max and listing['price'] <= settings.yellow_max:
		color = 16761095 # yellow
	elif listing['price'] > settings.yellow_max:
		color = 14431557 # red

	notification_data = {
		"embeds" : [{
			"title" : f"**${listing['price']}** | {listing['description']}",
			"url" : f"{listing['craigslist_url']}",
			"fields" : [
				{
					"name" : "Bedrooms",
					"value" : f"{listing['num_bedrooms']}",
					"inline" : True
				},
				{
					"name" : f"Square Feet",
					"value" : f"{listing['sqft']}",
					"inline" : True
				}
			],
			"thumbnail" : {
				"url" : listing['map_image']
			},
			"footer" : {
				"text" : f"posted {listing['posted_on']} | {listing['neighborhood']}",
				"icon_url" : "https://i.imgur.com/r8jnedb.png"
			},
			"color" : color
		}]
	}

	r = requests.post(config.DISCORD_WEBHOOK_URL, json=notification_data)

def main():
	# get the data from Craigslist
	housing = CraigslistHousing(site='sfbay', area='sfc', category='apa',
								filters={'posted_today' : True, 'min_price': settings.min_price, 
								'max_price': settings.max_price, 'min_bedrooms': settings.min_bedrooms})

	log.info('Retrieving listings')
	for result in housing.get_results(sort_by='newest', geotagged=True):
		# result = {'id': '6902060582', 'repost_of': None, 'name': 'Spacious one bedroom apartment near USF& GG PK', 'url': 'https://sfbay.craigslist.org/sfc/apa/d/san-francisco-spacious-one-bedroom/6902060582.html', 'datetime': '2019-05-31 21:44', 'price': '$2950', 'where': 'inner richmond', 'has_image': True, 'has_map': True, 'geotag': (37.775905, -122.458591), 'bedrooms': '1', 'area': None}

		# create a `listing` dict with the fields I care about and process the result
		listing = {}
		listing['craigslist_id'] = result['id']
		listing['craigslist_url'] = result['url']
		listing['posted_on'] = result['datetime']
		listing['description'] = result['name']
		listing['price'] = int(result['price'][1:])	# price always has a leading '$' so we need to strip the leading character
		listing['neighborhood'] = str.lower(result['where']) if result['where'] else '' # sometimes this is null
		listing['num_bedrooms'] = result['bedrooms']
		listing['sqft'] = result['area']
		listing['latitude'] = result['geotag'][0]
		listing['longitude'] = result['geotag'][1]

		# get the map image from Mapbox
		listing['map_image'] = get_map(listing['latitude'],listing['longitude'])

		# decide if we want to notify about this listing
		# https://stackoverflow.com/questions/2783969/compare-string-with-all-values-in-array
		if any(x in listing['neighborhood'] for x in settings.neighborhood_blacklist):
			notify = False
		else:
			notify = True
		
		# check if the listing is a duplicate
		if database.get_record(listing['craigslist_id']):
			log.info('Found duplicate record with ID {}, skipping'.format(listing['craigslist_id']))
			continue	# if duplicate we assume we've procsessed this listing so just skip it
		# otherwise we should save the listing and notify if applicable
		else:
			log.info('{} looks like a new listing, processing'.format('craigslist_id'))
			database.insert_record(listing)
			if notify is True:
				send_notification(listing)
				database.mark_as_notified(listing['craigslist_id'])

if __name__ == '__main__':
	main()


