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
def parseSportsbet(url ='https://www.sportsbet.com.au/betting/soccer'):
    html = get_html(url, 1)

    # find the container for all the matches (separated into days (divs))
    daysContainer = html.find('div', {'data-automation-id': 'class-featured-events-container'})
    days = daysContainer.findChildren(recursive=False)

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

    return(matches)

matches = parseSportsbet()

# Open a file for writing \
with open('./src/matchData/sportsbetMatches.csv', 'w', newline='') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    # Write header row 
    csvwriter.writerow(['Date', 'Time', 'Team1', 'Odds1', 'Outcome', 'Draw Odds', 'Team2', 'Odds2'])

    # Write data rows
    for match_day in matches: 
        for match in match_day["matches"]: 
            if len(match["odds"]) != 6: continue
            row = [match_day["date"], match["time"], match["odds"][0], match["odds"][1], 'Draw', match["odds"][3], match["odds"][4], match["odds"][5]]
            csvwriter.writerow(row)