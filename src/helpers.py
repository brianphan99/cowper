import csv
from datetime import datetime, timezone

# headers for all sports
SOCCER_HEADERS = ['datetime', 'team1', 'odds1', 'draw', 'oddsdraw', 'team2', 'odds2']
TENNIS_HEADERS = ['datetime', 'player1', 'odds1', 'player2', 'odds2']

# writes match data to csv file
def writeToCsv(data, sport, fileName):
    with open(f'./src/matchData/{fileName}.csv', 'w', newline='') as csvfile: 
        csvwriter = csv.writer(csvfile)

        # get the header based on the sport
        header = None
        match sport:
            case 'soccer':
                header = SOCCER_HEADERS
            case 'tennis':
                header = TENNIS_HEADERS

        # write the header row
        csvwriter.writerow(header)

        # Write data rows
        for match in data: 
            if len(match["odds"]) != (len(header) - 1): continue
            row = [match["datetime"]] + match['odds']
            csvwriter.writerow(row)

def formatTime(time):
    return datetime.fromisoformat(time).astimezone(timezone.utc).isoformat()
