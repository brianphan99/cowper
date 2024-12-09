from scraper import get_html
import re
import csv
from datetime import datetime

# gets sportsbet matches and returns object of odds and dates
def parseSportsbet(sport):
    url = None
    if sport == 'soccer':
        url = 'https://www.sportsbet.com.au/betting/soccer'
    elif sport == 'tennis':
        url = 'https://www.sportsbet.com.au/betting/tennis'

    html = get_html(url, 1)

    # find the container for all the matches (separated into days (divs))
    daysContainer = None
    days = None
    if sport == 'soccer':
        daysContainer = html.find('div', {'data-automation-id': 'class-featured-events-container'})
        days = daysContainer.findChildren(recursive=False)
    elif sport == 'tennis':
        daysContainer = html.find('ul', class_=re.compile(r'.*upcomingEventsListDesktop.*'))
        days = daysContainer.findChildren(recursive=False)
        days.pop(0)

    matches = []

    for day in days:
        # get individual matches
        match_elements = day.find_all('li', class_=re.compile(r'.*cardOuterItem.*'))

        for match_element in match_elements:
            match = {}
            # get time of match
            time = match_element.find('time').get('datetime')
            match['datetime'] = time

            # get odds
            odds_element = match_element.find('div', class_=re.compile(r'.*outcomeCardItems.*'))
            odds = odds_element.get_text('|', strip=True).split('|')
            match['odds'] = odds

            matches.append(match)
        

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


parseSportsbet('soccer')