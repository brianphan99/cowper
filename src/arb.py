# arb functions
# note: rounding to 2 decimal places is done where money is used

# main arb function
def arb(inv, odds1, odds2):
    if (checkArb(odds1, odds2)):
        print('Arb found!')

        impP = totalP(odds1, odds2)
        print(f'Total Implied Probability: {impP}')

        bestOdds = maxOdds(odds1, odds2)
        stakes = calcStakes(inv, bestOdds, impP)
        print(f'Stake Distribution (${inv} investment): {stakes}')

        aReturns = calcReturns(stakes, bestOdds)
        print(f'Returns: {aReturns}')




# calculates implied probabilities
def calcImpP(odds):
    p = []
    for i in range(len(odds)):
        p.append(1 / odds[i])

    return p

# calculates best (max) odds given two sets
def maxOdds(odds1, odds2):
    oddsMax = []
    for i in range(len(odds1)):
        oddsMax.append(max(odds1[i], odds2[i]))

    return oddsMax

# calculates total best (minimum) implied probabilities given 2 sets of odds
def totalP(odds1, odds2):
    # get best odds
    bestOdds = maxOdds(odds1, odds2)

    # calculate implied probabilities
    impP = []
    for i in range(len(bestOdds)):
        impP.append(1 / bestOdds[i])

    # get sum
    sumP = sum(impP)

    return sumP


# checks whether an opportunity is available
def checkArb(odds1, odds2):
    # check whether sum of probabilities is less than 100%
    return totalP(odds1, odds2) < 1

# calculates stake distribution
def calcStakes(investment, odds, pTotal):
    stakes = []

    for i in range(len(odds)):
        stakes.append(round(investment * (1/odds[i]) / pTotal, 2))

    return stakes

# calculates possible profits
def calcReturns(stakes, odds):
    profits = []

    for i in range(len(odds)):
        profits.append(round(stakes[i] * odds[i],2))
    
    return profits