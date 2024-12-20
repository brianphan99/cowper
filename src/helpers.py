import csv
from datetime import datetime, timezone, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from matchData.Constants import API_KEY
import requests
from arb import totalP, parseOdds

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

def send_email(recipient_email, subject, body):
    try:
        # sender
        sender_email = "arbitrage.cowper@gmail.com"
        sender_password = "hllp zksz wvbi twwc"

        # Set up the email content
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # Attach the email body
        message.attach(MIMEText(body, "plain"))

        # Connect to the Gmail SMTP server
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
            server.login(sender_email, sender_password)  # Log in to your email account
            server.send_message(message)  # Send the email

        print("Email sent successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
def getSports():
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #
    # First get a list of in-season sports
    #   The sport 'key' from the response can be used to get odds in the next request
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    sports_response = requests.get(
        'https://api.the-odds-api.com/v4/sports', 
        params={
            'api_key': API_KEY
        }
    )


    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

    else:
        sports = []
        for sport in sports_response.json():
            if sport["group"] == "Soccer":
                sports.append(sport["key"])
        return sports
        with open('./src/matchData/sports.json', 'w') as f:
          json.dump(sports_response.json(), f)

def getOdds(sport):
        
    # An api key is emailed to you when you sign up to a plan
    # Get a free API key at https://api.the-odds-api.com/

    SPORT = sport # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

    REGIONS = 'au' # uk | us | eu | au. Multiple can be specified if comma delimited

    MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited

    ODDS_FORMAT = 'decimal' # decimal | american

    DATE_FORMAT = 'iso' # iso | unix

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #
    # Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
    # This will deduct from the usage quota
    # The usage quota cost = [number of markets specified] x [number of regions specified]
    # For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )

    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        odds_json = odds_response.json()
        print('Number of events:', len(odds_json))

        with open('./src/matchData/data.json', 'r') as file:
            data = json.load(file)

        data.append(odds_json)

        with open('./src/matchData/data.json', 'w') as f:
          json.dump(data, f)

        # Check the usage quota
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])

# sports = getSports()
# with open('./src/matchData/data.json', 'w') as f:
#   json.dump([], f)
# for sport in sports: 
#   getOdds(sport)
  

with open('./src/matchData/data.json', 'r') as file:
    data = json.load(file)  # Load JSON data into a Python object

    for league in data:
        for match in league:
            win_team = match["home_team"]
            lose_team = match["away_team"]

            max_win_odds = 0
            max_draw_odds = 0
            max_lose_odds = 0
            for bookmaker in match["bookmakers"]:
              max_win_odds = max(bookmaker["markets"][0]["outcomes"][0]["price"] , max_win_odds)
              max_lose_odds = max(bookmaker["markets"][0]["outcomes"][1]["price"] , max_lose_odds)
              max_draw_odds = max(bookmaker["markets"][0]["outcomes"][2]["price"] , max_draw_odds)

            if totalP([max_win_odds, max_draw_odds, max_lose_odds]) < 1:
              print(win_team + " vs " + lose_team)
              print(max_win_odds, max_lose_odds, max_draw_odds)
              print