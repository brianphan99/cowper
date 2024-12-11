from scraper import get_html
import re
import csv
from datetime import datetime, timezone

# scrapes sportsbet, writes to csv and returns array of matches 
def scrapeSportsbet(sport):
    url = f'https://www.sportsbet.com.au/betting/{sport}'

    html = get_html(url)

    # find the container for all the matches (separated into days (divs))
    daysContainer = html.find('div', {'data-automation-id': 'class-featured-events-container'})
    days = daysContainer.findChildren(recursive=False)

    matches = []

    for day in days:
        # get individual matches
        match_elements = day.find_all('li', class_=re.compile(r'.*cardOuterItem.*'))

        for match_element in match_elements:
            # get time of match
            time = match_element.find('time').get('datetime')
            time = datetime.fromisoformat(time).astimezone(timezone.utc).isoformat()

            # get odds
            odds_element = match_element.find('div', class_=re.compile(r'.*outcomeCardItems.*'))
            odds = odds_element.get_text('|', strip=True).split('|')

            matches.append({'datetime': time, 'odds': odds})
        
    writeToCsv(matches, sport)

    return matches

# writes match data to csv file
def writeToCsv(data, sport):
    with open(f'./src/matchData/sportsbet{sport}.csv', 'w', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile)

        # Write header row 
        soccerHeaders = ['datetime', 'team1', 'odds1', 'draw', 'oddsdraw', 'team2', 'odds2']
        tennisHeaders = ['datetime', 'player1', 'odds1', 'player2', 'odds2']
        
        header = soccerHeaders if sport == 'soccer' else tennisHeaders
        csvwriter.writerow(header)

        # Write data rows
        for match in data: 
            if len(match["odds"]) != (len(header) - 1): continue
            row = [match["datetime"]] + match['odds']
            csvwriter.writerow(row)