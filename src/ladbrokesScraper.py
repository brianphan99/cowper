from scraper import get_html
from helpers import writeToCsv, formatTime

# scrapes ladbrokes, writes to csv and returns array of matches 
def scrapeLadbrokes(sport, region = 0):
	url = None

	if sport == 'soccer':
		regions = ['uefa', 'uk-ireland', 'australia', 'spain', 'germany', 'france', 'italy', 'americas', 'asia', 'rest-of-europe', 'rest-of-the-world', 'uefa', 'international']
		url = f'https://www.ladbrokes.com.au/sports/soccer/{regions[region]}'

	html = get_html(url, 'div.competition-events__date-group')

	matches = []

	# all date groups
	dateGrs = html.find_all('div', class_='competition-events__date-group')

	for dateGr in dateGrs:
		matchEls = dateGr.find_all('div', class_='sport-event-card')

		for match in matchEls:
			time = formatTime(match.find('time').get('datetime'))

			odds = match.get_text('|', strip=True).split('|')[-7:-1]
			if (len(odds) != 6): continue

			matches.append({'datetime': time, 'odds': odds})

	writeToCsv(matches, sport, f'ladbrokes_{sport}_{region}')

	return matches