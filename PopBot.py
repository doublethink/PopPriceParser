import PopParser
import RootParser
import csv
import datetime

domain = 'poppriceguide.com'

rootParser = RootParser.RootParser(domain, "/guide/PopVinyl/1/")
rootLinks = rootParser.parse_target()

results = []
for link in rootLinks:

    parser = PopParser.Parser(link[1], domain, link[0])
    results.append(parser.parse_target())

date = datetime.datetime.now()
filename = 'Results/pop_prices_{0}{1}{2}.csv'.format(date.day, date.month, date.year)
date = date.isoformat()

with open(filename, 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='*', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Category', 'Number', 'Name', 'Value', 'Is Variant', 'URL', 'Date'])
    for pops in results:
        for pop in pops:
            spamwriter.writerow([pop.category, pop.number, pop.name, pop.value, pop.is_variant, pop.url, date])
