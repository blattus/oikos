import sqlite3
from logger import log

conn = sqlite3.connect('listings.db')
conn.set_trace_callback(log.info) # log the database connections
db = conn.cursor()

# create the table if it doesn't exist
db.execute('''
	CREATE TABLE IF NOT EXISTS listings(craigslist_id text, craigslist_url text, posted_on text, description text, 
		price int, neighborhood text, num_bedrooms text, sqft text, latitude real, longitude real, map_image text, notified int)
	''')

def insert_record(listing):
	'''
	inserts a single record into the database based on provided listing data
	'''

	# https://stackoverflow.com/questions/14108162/python-sqlite3-insert-into-table-valuedictionary-goes-here/16698310
	columns = ', '.join(listing.keys())
	placeholders = ':'+', :'.join(listing.keys())
	query = 'INSERT INTO listings (%s) VALUES (%s)' % (columns, placeholders)
	print(query)

	db.execute(query, listing)
	conn.commit()

def get_record(craigslist_id):
	'''
	retrieves data based on the provided ID
	'''

	db.execute('SELECT craigslist_id FROM listings WHERE craigslist_id = ?', (craigslist_id, ))
	data = db.fetchall()
	if len(data) == 0:
		return 0
	else:
		return data

def mark_as_notified(craigslist_id):
	'''
	mark a single listing as notified
	'''

	db.execute('UPDATE listings SET notified = 1 WHERE craigslist_id = ?', (craigslist_id, ))
	conn.commit()

