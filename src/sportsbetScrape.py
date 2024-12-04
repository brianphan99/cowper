from scraper import get_html
import re

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

# gets sportsbet matches and returns object of odds and dates
def parseSportsbet(url ='https://www.sportsbet.com.au/betting/soccer'):
    html = get_html(url)

    # find the container for all the matches (separated into days (divs))
    daysContainer = html.find('div', {'data-automation-id': 'class-featured-events-container'})
    days = daysContainer.findChildren(recursive=False)

    matches = []

    for day in days:
        matchDay = {}

        dayDate = day.findChildren(recursive=False)[0].get_text(strip=True)
        matchDay['date'] = dayDate
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