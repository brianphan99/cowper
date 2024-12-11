from scraper import get_html
import csv
from datetime import datetime, timezone

# scrapes ladbrokes, writes to csv and returns array of matches 
def scrapeLadbrokes(sport, region = 0):
	url = None

	if sport == 'soccer':
		regions = ['uefa', 'uk-ireland', 'australia', 'spain', 'germany', 'france', 'italy', 'americas', 'asia', 'rest-of-europe', 'rest-of-the-world', 'uefa', 'international']
		url = f'https://www.ladbrokes.com.au/sports/soccer/{regions[region]}'

	html = get_html(url)

	matches = []

	# all date groups
	dateGrs = html.find_all('div', class_='competition-events__date-group')

	for dateGr in dateGrs:
		matchEls = dateGr.find_all('div', class_='sport-event-card')

		for match in matchEls:
			time = match.find('time').get('datetime')
			time = datetime.fromisoformat(time).astimezone(timezone.utc).isoformat()

			odds = match.get_text('|', strip=True).split('|')[-7:-1]
			if (len(odds) != 6): continue

			matches.append({'datetime': time, 'odds': odds})

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