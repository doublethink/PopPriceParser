import PopParser
import RootParser
import csv
import datetime
import psycopg2
import logging

domain = 'poppriceguide.com'

rootParser = RootParser.RootParser(domain, "/guide/PopVinyl/1/")
rootLinks = rootParser.parse_target()

results = []
for link in rootLinks:

    parser = PopParser.Parser(link[1], domain, link[0])
    results.append(parser.parse_target())

date = datetime.datetime.now()
logging.basicConfig(filename='/home/stephen/scripts/PopPriceParser/Results/errors_log.log',level=logging.DEBUG)
date = date.isoformat()

connection = None

try:
	connection = psycopg2.connect(database='poppricedb', user='stephen')
	cursor = connection.cursor()
	for pops in results:
		for pop in pops:
			cursor.execute('INSERT INTO raw_daily_rates VALUES (\'{0}\', \'{1}\', \'{2}\', {3}, {4}, \'{5}\', \'{6}\');'.format(pop.category, pop.number, pop.name.replace("'",""), pop.value, pop.is_variant, pop.url, date))
	
	connection.commit()

except Exception as e:
	logging.debug("Error {0}".format(e))

finally:

	if connection:
		connection.close()
