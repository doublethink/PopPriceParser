import PopParser
import RootParser
import csv
import datetime
import psycopg2
import logging

domain = 'poppriceguide.com'
logging.basicConfig(filename='/home/stephen/logs/parser.log',level=logging.DEBUG)

rootParser = RootParser.RootParser(domain, "/guide/PopVinyl/1/")
rootLinks = rootParser.parse_target()

results = []
for link in rootLinks:

    parser = PopParser.Parser(link[1], domain, link[0])
    results.append(parser.parse_target())

date = datetime.datetime.now().isoformat()

connection = None

try:
	# Connect to internal Postgres server
    connection = psycopg2.connect(database='poppricedb', user='stephen')
    cursor = connection.cursor()
    # Set up todays summary
    cursor.execute('DROP TABLE IF EXISTS raw_single_day;')
    statement = """CREATE TABLE raw_single_day (
        category varchar(15),
        number varchar(15),
        name text,
        value money,
        is_variant boolean,
        url text,
        date text
    );"""
    cursor.execute(statement)
    # Insert results into daily table
    for pops in results:
        for pop in pops:
            cursor.execute('INSERT INTO raw_single_day VALUES (\'{0}\', \'{1}\', \'{2}\', {3}, {4}, \'{5}\', \'{6}\');'.format(pop.category, pop.number, pop.name.replace("'",""), pop.value, pop.is_variant, pop.url, date))

    # Insert the remaining into the summary page
    cursor.execute('INSERT INTO raw_daily_rates SELECT * FROM raw_single_day ;')
    connection.commit()

except Exception as e:
	logging.debug("Error {0}".format(e))

finally:

	if connection:
		connection.close()
