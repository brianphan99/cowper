from scraper import get_html
import re
import csv
from datetime import datetime

"""
Return value:

matches = [
    {
    "date": "Thursday, 5 Dec",
    "matches": [
        {
        "time": "05:00",
        "odds": ["Bologna", "1.70", "Draw", "3.40", "AC Monza", "5.00"]
        },
        ...
    ]},
    ...
]
"""

def formatDate(dateStr):
    dateArr = dateStr.split(' ')
    dateArr.pop(0)

    dayStr = dateArr[0].zfill(2)
    monthStr = dateArr[1]
    yearStr = dateArr[2] if len(dateArr) > 2 else datetime.now().year

    monthNum = str(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'].index(monthStr) + 1).zfill(2)

    formattedDate = f"{dayStr}/{monthNum}/{yearStr}"

    return formattedDate

# gets sportsbet matches and returns object of odds and dates
def parseSportsbet(sport):
    url = 0
    if sport == 'soccer':
        url = 'https://www.sportsbet.com.au/betting/soccer'
    elif sport == 'tennis':
        url = 'https://www.sportsbet.com.au/betting/tennis'

    html = get_html(url, 1)

    # find the container for all the matches (separated into days (divs))
    daysContainer = 0
    days = 0
    if sport == 'soccer':
        daysContainer = html.find('div', {'data-automation-id': 'class-featured-events-container'})
        days = daysContainer.findChildren(recursive=False)
    elif sport == 'tennis':
        daysContainer = html.find('ul', class_=re.compile(r'.*upcomingEventsListDesktop.*'))
        days = daysContainer.findChildren(recursive=False)
        days.pop(0)

    matches = []

    for day in days:
        matchDay = {}

        dayDate = day.findChildren(recursive=False)[0].get_text(strip=True)
        matchDay['date'] = formatDate(dayDate)
        matchDay['matches'] = []

        # get individual matches
        match_elements = day.find_all('li', class_=re.compile(r'.*cardOuterItem.*'))
        for match_element in match_elements:
            match = {}
            # get time of match
            time = match_element.find('time').get_text(strip=True)
            match['time'] = time

            # get odds
            odds_element = match_element.find('div', class_=re.compile(r'.*outcomeCardItems.*'))
            odds = odds_element.get_text('|', strip=True).split('|')
            match['odds'] = odds

            matchDay['matches'].append(match)
        
        matches.append(matchDay)

    # Open a file for writing \
    with open(f'./src/matchData/sportsbet{sport}.csv', 'w', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile)

        # Write header row 
        soccerHeaders = ['Date', 'Time', 'Team1', 'Odds1', 'Draw', 'Draw Odds', 'Team2', 'Odds2']
        tennisHeaders = ['Date', 'Time', 'Player1', 'Odds1', 'Player2', 'Odds2']
        
        header = soccerHeaders if sport == 'soccer' else tennisHeaders
        csvwriter.writerow(header)

        # Write data rows
        for match_day in matches: 
            for match in match_day["matches"]: 
                if len(match["odds"]) != (len(header) - 2): continue
                row = [match_day["date"], match["time"]] + match['odds']
                csvwriter.writerow(row)

    return matches

matches = parseSportsbet('tennis')