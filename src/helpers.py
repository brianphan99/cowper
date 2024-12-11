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

# reads csv data and returns data in matches array
def readCsv(fileName):
    with open(f'./src/matchData/{fileName}.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # read the header if present
        header = next(reader)

        matches = []

        # loop through the rows
        for row in reader:
            match = {'datetime': row[0], 'odds': row[1:]}
            matches.append(match)

        return matches

def readFromCsv(fileName):
    """
    Reads data from a CSV file located in the 'src/matchData' directory.

    Args:
        fileName (str): The name of the CSV file to read, without the '.csv' extension.

    Returns:
        list: A list of rows, where each row is represented as a list of strings.
    """
    data = []   
    with open(f'./src/matchData/{fileName}.csv', mode="r") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
          data.append(row)
        return data

def formatTime(time):
    return datetime.fromisoformat(time).astimezone(timezone.utc).isoformat()
