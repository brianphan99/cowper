# arb functions
#
# note: rounding to 2 decimal places is done where money is used
#
# odds = array of array of odds for each site
# e.g.: [<sportsbet>[1.0, 2.3, 3.4], <ladbrokes>[3.2, 2.1, 4.4], ...]


# main arb function
def arb(inv, odds):
    if (checkArb(odds)):
        print('\nArb found!')

        bestOdds = maxOdds(odds)
        print(f'Best Odds\n {bestOdds}')

        impP = totalP(parseOdds(bestOdds))
        print(f'Total Implied Probability\n {impP}')

        stakes = calcStakes(inv, parseOdds(bestOdds), impP)
        print(f'Stake Distribution (${inv} investment)\n {stakes}')

        aReturns = calcReturns(stakes, parseOdds(bestOdds))
        print(f'Returns\n {aReturns}')

        return True
    else:
        return False

# calculates implied probabilities
def calcImpP(odds):
    p = []
    for i in range(len(odds)):
        p.append(1 / odds[i])

    return p

# calculates best (max) odds given n sites
def maxOdds(odds):
    oddsMax = []
    for i in range(len(odds[0])):
        # array of odds for a given outcome across all sites
        outcomeOdds = [o[i] for o in odds]

        maxOdd = max(outcomeOdds)
        oddsMax.append({'site': outcomeOdds.index(maxOdd), 'odds': maxOdd})

    return oddsMax

# parses maxOdds array of objects into array of odds
def parseOdds(odds):
    return [o['odds'] for o in odds]

# calculates total best (minimum) implied probabilities given best odds
def totalP(bestOdds):
    # calculate implied probabilities
    impP = []
    for i in range(len(bestOdds)):
        impP.append(1 / bestOdds[i])

    # get sum
    sumP = sum(impP)

    return sumP


# checks whether an opportunity is available
def checkArb(odds):
    bestOdds = maxOdds(odds)
    # check whether sum of probabilities is less than 100%
    return totalP(parseOdds(bestOdds)) < 1

# calculates stake distribution
def calcStakes(investment, odds, pTotal):
    stakes = []

    for i in range(len(odds)):
        stakes.append(round(investment * (1/odds[i]) / pTotal, 2))

    return stakes

# calculates possible profits
# returns array of profits
def calcReturns(stakes, odds):
    profits = []

    for i in range(len(odds)):
        profits.append(round(stakes[i] * odds[i],2))
    
    return profits