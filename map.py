import config
from mapbox import Static

service = Static(access_token=config.MAPBOX_ACCESS_TOKEN)

# point_on_map = {
# 	'type' : 'Feature',
# 	'properties' : {'name' : 'point'},
# 	'geometry' : {
# 		'type' : 'Point',
# 		'coordinates' : [-122.4583, 37.7756]
# 	}
# }

# response = service.image('mapbox.streets', retina=True, features=point_on_map, lon=-122.4583, lat=37.7756, z=15)
# print(response.url)


point_on_map = {
	'type' : 'Feature',
	'properties' : {'name' : 'point'},
	'geometry' : {
		'type' : 'Point',
		'coordinates' : [-122.4267, 37.7689]
	}
}

response = service.image('mapbox.streets', retina=True, features=point_on_map, lon=-122.4267, lat=37.7689, z=12)
print(response.url)