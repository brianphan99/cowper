from scraper import get_html
import re
from helpers import writeToCsv, formatTime

# scrapes sportsbet, writes to csv and returns array of matches 
def scrapeSportsbet(sport):
    url = f'https://www.sportsbet.com.au/betting/{sport}'

    html = get_html(url, 'div[data-automation-id=class-featured-events-container]')
    print(f'Scraping Sportsbet {sport}')

    # find the container for all the matches (separated into days (divs))
    daysContainer = html.find('div', {'data-automation-id': 'class-featured-events-container'})
    days = daysContainer.findChildren(recursive=False)

    matches = []

    for day in days:
        # get individual matches
        match_elements = day.find_all('li', class_=re.compile(r'.*cardOuterItem.*'))

        for match_element in match_elements:
            if (not match_element.find('time')): continue
            # get time of match
            time = formatTime(match_element.find('time').get('datetime'))

            # get odds
            odds_element = match_element.find('div', class_=re.compile(r'.*outcomeCardItems.*'))
            odds = odds_element.get_text('|', strip=True).split('|')

            matches.append({'datetime': time, 'odds': odds})
    
    writeToCsv(matches, sport, f'sportsbet_{sport}')

    return matches

