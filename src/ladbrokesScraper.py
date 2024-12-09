from scraper import get_html
import csv

# scrapes ladbrokes, writes to csv and returns array of matches 
def scrapeLadbrokes(sport, region = 8):
	url = None

	if sport == 'soccer':
		regions = ['uk-ireland', 'australia', 'spain', 'germany', 'france', 'italy', 'americas', 'asia', 'rest-of-europe', 'rest-of-the-world', 'uefa', 'international']
		url = f'https://www.ladbrokes.com.au/sports/soccer/{regions[region]}'

	html = get_html(url, 1)

	matches = []

	# all date groups
	dateGrs = html.find_all('div', class_='competition-events__date-group')

	for dateGr in dateGrs:
		matchEls = dateGr.find_all('div', class_='sport-event-card')

		for match in matchEls:
			datetime = match.find('time').get('datetime')

			odds = match.get_text('|', strip=True).split('|')[-7:-1]

			matches.append({'datetime': datetime, 'odds': odds})

	writeToCsv(matches, sport, regions[region])

	return matches

def writeToCsv(data, sport, region):
	header = ['datetime', 'team1', 'odds1', 'draw', 'oddsdraw', 'team2', 'odds2']
	with open(f'./src/matchData/ladbrokes{sport}{region}.csv', mode='w', newline='') as file: 
		writer = csv.writer(file)
		
		writer.writerow(header)

		for match in data:
			row = [match['datetime']] + match['odds']
			writer.writerow(row)

scrapeLadbrokes('soccer')