from helpers import readFromCsv
import re
from arb import arb, checkArb

def normalize_name(name):
    """
    Normalize a team name by converting to lowercase and removing non-alphanumeric characters.

    Args:
        name (str): The team name to normalize.

    Returns:
        str: The normalized team name.
    """
    # Convert to lowercase and keep only alphanumeric + spaces
    return re.sub(r'[^a-zA-Z0-9 ]', '', name).lower().strip()

def jaccard_similarity(s1, s2):
    """
    Calculate the Jaccard similarity between two strings based on word tokens.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        float: The Jaccard similarity score (0 to 1).
    """
    # Split strings into sets of words
    set1, set2 = set(s1.split()), set(s2.split())
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union else 0.0

def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance (edit distance) between two strings.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The Levenshtein distance between the strings.
    """
    len1, len2 = len(s1), len(s2)
    # Initialize DP table
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    # Fill DP table
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Deletion
                dp[i][j - 1] + 1,      # Insertion
                dp[i - 1][j - 1] + cost  # Substitution
            )
    return dp[len1][len2]

def similarity_score(name1, name2):
    """
    Calculate a combined similarity score between two team names using Jaccard and Levenshtein methods.

    Args:
        name1 (str): The first team name.
        name2 (str): The second team name.

    Returns:
        float: A similarity score between 0 and 1.
    """
    # Normalize names
    name1, name2 = normalize_name(name1), normalize_name(name2)

    # Token similarity
    token_similarity = jaccard_similarity(name1, name2)

    # Character similarity
    levenshtein_dist = levenshtein_distance(name1, name2)
    max_len = max(len(name1), len(name2))
    char_similarity = (max_len - levenshtein_dist) / max_len if max_len > 0 else 1.0

    # Combine with weights
    return 0.8 * token_similarity + 0.2 * char_similarity

def matching(sitesData):
    """
    Match and compare team data from multiple betting sites.

    Args:
        sitesData (list): A list of lists, where each sublist contains match data from one site.

    Returns:
        dict: A dictionary with matched teams and their corresponding odds.
        
    """
    data = dict()

    # Compare matches from the first site with other sites
    for index in range(1, len(sitesData)):

        # Iterate through matches in the first site
        for match_1 in sitesData[0]:
            best_score = 0
            # Create match identifier
            match = match_1[1] + " vs " + match_1[5]  
            if match not in data:
                # Initialize data with odds from the first site
                data[match] = [[float(match_1[i]) for i in range(2, len(match_1), 2)]]

            # Compare with matches from the other sites
            for match_2 in sitesData[index]:

                # Check if matches occur at the same time
                if match_1[0] == match_2[0]:
                    # Calculate similarity score for team names
                    score = max(
                        similarity_score(match_1[1], match_2[1]),
                        similarity_score(match_1[1], match_2[5]),
                        similarity_score(match_1[5], match_2[1]),
                        similarity_score(match_1[5], match_2[5])
                    )
                    if score > best_score:
                        best_score = score
                        # Determine the best match for team names
                        if similarity_score(match_1[1], match_2[1]) > similarity_score(match_1[1], match_2[5]):
                            if index == len(data[match]) - 1:
                                data[match][-1] = [float(match_2[i]) for i in range(2, len(match_2), 2)]
                            else:
                                data[match].append([float(match_2[i]) for i in range(2, len(match_2), 2)])
                        else:
                            if index == len(data[match]) - 1:
                                data[match][-1] = [float(match_2[i]) for i in range(len(match_2) - 1, 1, -2)]
                            else:
                                data[match].append([float(match_2[i]) for i in range(len(match_2) - 1, 1, -2)])

            # Remove matches with low similarity score
            if best_score < 0.5:
                del data[match]

    return data

# Read data from CSV files and perform matching
data = matching([readFromCsv('sportsbet_soccer'), readFromCsv('ladbrokes_soccer')])

print('\n')
print(f'Found {len(data)} matches\n')
print('Looking for arbs...\n')

# Perform arbitrage calculations on the matched data
for match in data:
    print(match)
    arb(100, data[match])