from sportsbetScraper import scrapeSportsbet
from ladbrokesScraper import scrapeLadbrokes
from helpers import readFromCsv
from matching import matching
from arb import arb

if __name__ == "__main__":
  print("main")

scrapeSportsbet('soccer')
scrapeLadbrokes('soccer')