"""
IS597 Final Project
Judy(Chu-Ting) Chan
Cindy(Ting-Yin) Yang
"""
import random
from pitch_count_sim import generate_team
from double_elimination import Tournament as DoubleEliminationTournament

# Constant variables for pitcher
ERA_MIN = 0.0
ERA_MAX = 108.0
IP_MIN = 0.1
IP_MAX = 9.2
K_MIN = 0
K_MAX = 13
WHIP_MIN = 0.21
WHIP_MAX = 12.0
AVG_MIN = 0.067
AVG_MAX = 0.8

# Constant variables for batter
AVG_B_MIN = 0.067
AVG_B_MAX = 0.8
OPS_MIN = 0
OPS_MAX = 1.507
RBI_MIN = 0
RBI_MAX = 13
BB_MIN = 0
BB_MAX = 10
SO_MIN = 0
SO_MAX = 13
SB_MIN = 0
SB_MAX = 3


def get_score(country_name):
    """Returns the total score for a given country's team based on their pitchers and batters' performances.

    :param country_name:The name of the country for which to calculate the total score.
    :return: The score of the given country's team.
    """
    team = generate_team(country_name, 3, 9)

    # Calculate pitcher's performance
    pitch_performance = []
    for pitcher in team.pitchers:
        normalized_ERA = 1 - pitcher.ERA / (ERA_MAX - ERA_MIN)
        normalized_WHIP = 1 - pitcher.WHIP / (WHIP_MAX - WHIP_MIN)
        normalized_BAA = 1 - pitcher.AVG / (AVG_MAX - AVG_MIN)
        normalized_IP = pitcher.IP / (IP_MAX - IP_MIN)
        normalized_K = pitcher.SO / (K_MAX - K_MIN)
        performance = (0.3 * normalized_ERA) + \
                      (0.25 * normalized_WHIP) + \
                      (0.15 * normalized_BAA) + \
                      (0.1 * normalized_IP) + \
                      (0.2 * normalized_K)
        pitch_performance.append(performance)
    pitch_score = sum(pitch_performance) / 3

    # Calculate hitter's performance
    hit_performance = []
    for batter in team.batters:
        normalized_SO = 1 - batter.SO / (SO_MAX - SO_MIN)
        normalized_AVG_B = batter.AVG / (AVG_B_MAX - AVG_B_MIN)
        normalized_OPS = batter.OPS / (OPS_MAX - OPS_MIN)
        normalized_RBI = batter.RBI / (RBI_MAX - RBI_MIN)
        normalized_BB = batter.BB / (BB_MAX - BB_MIN)
        normalized_SB = batter.SB / (SB_MAX - SB_MIN)
        performance = (0.25 * normalized_AVG_B) + \
                      (0.30 * normalized_OPS) + \
                      (0.15 * normalized_RBI) + \
                      (0.1 * normalized_BB) + \
                      (0.1 * normalized_SO) + \
                      (0.1 * normalized_SB)
        hit_performance.append(performance)
    hit_score = sum(hit_performance) / 9

    total_score = 7.5 * pitch_score + 2.5 * hit_score
    return total_score


def generate_pools(countries, num_pools=None):
    """Generates pools of countries of 4 countries each, given a list of countries.

    :param countries: A list of country names.
    :param num_pools: Number of pools.
    :return: A list of country pools.
    """
    if len(countries) < 4:
        raise ValueError("Number of countries should be at least 4")

    if num_pools is None:
        num_pools = len(countries) // 4

    if len(countries) < num_pools * 4:
        raise ValueError("Number of countries is wrong")

    pools = []
    selected_countries = set()
    for i in range(num_pools):
        available_countries = list(set(countries) - selected_countries)
        pool = random.sample(available_countries, k=4)
        pools.append(pool)
        selected_countries.update(pool)

    return pools


def get_defensive_rate(team):
    """Returns a defensive rate for a given team.

    :param team: The team to get the defensive rate for.
    :return: The defensive rate for the team.
    """
    team_runs_allowed = random.randint(0, 81)
    team_defensive_outs = 27

    return team_runs_allowed / team_defensive_outs


def round_robin_game(pools):
    """The function simulates a round-robin tournament where each team in a pool plays every other team in the
    same pool. The winner is determined by comparing the scores obtained by each team in each match. In case
    of a tie, a random winner is chosen. The function recursively calls itself if there are more than two
    top teams that advance to the next round.

    :param pools: A list of lists, where each sublist contains the countries in a pool
    :return: A tuple containing the standings and the list of top teams that advance to the next round.
             The `standings` is a dictionary of dictionaries, where each inner dictionary contains the wins
             for each country in a pool (e.g. {'pool_A': {'USA': 2, 'Canada': 1, 'Mexico': 0}}).
             The list of top teams is a list of country names (e.g. ['USA', 'Canada']).
    """

    # Initialize the standings dictionary with zeroes for each country in each pool
    num_pools = len(pools)
    standings = {}
    for j in range(num_pools):
        pool_name = f'pool_{chr(65 + j)}'
        standings[pool_name] = {country: 0 for country in pools[j]}

    # Play each match and update the standings
    for pool_idx, pool in enumerate(pools):
        for i in range(len(pool)):
            for j in range(i + 1, len(pool)):
                if i != j:
                    team_i_score = get_score(pool[i])
                    team_j_score = get_score(pool[j])

                    if team_i_score > team_j_score:
                        standings[f'pool_{chr(65 + pool_idx)}'][pool[i]] += 1
                    elif team_j_score > team_i_score:
                        standings[f'pool_{chr(65 + pool_idx)}'][pool[j]] += 1
                    # when the two teams have the same scores
                    else:
                        winner = random.choice([pool[i], pool[j]])
                        standings[f'pool_{chr(65 + pool_idx)}'][winner] += 1

    # Find the teams with the highest number of wins
    top_teams = []
    for pool in standings.keys():
        wins = [(team, wins) for team, wins in standings[pool].items() if wins > 0]
        # Deal with the tiebreaker situation
        sorted_wins = sorted(wins, key=lambda x: (-x[1], -get_defensive_rate(x[0])))
        top_teams.extend([team for team, wins in sorted_wins[:2]])

    # If there are more than two top teams, recursively call the function with a new pool
    if len(top_teams) > 2:
        print("First round: ")
        print(standings)
        print("Countries get into the second round: ", top_teams)
        new_pool = generate_pools(top_teams, num_pools=1)
        new_standings, new_top_teams = round_robin_game(new_pool)
        return new_standings, new_top_teams
    else:
        print("\nSecond round: ")
        print(standings)
        print("Countries get into the final round: ", top_teams)
        return standings, top_teams



def final_game(top_2_teams: list):
    """Determines the winner of the final game between the top 2 teams.

    :param top_2_teams: A list containing the names of the top 2 teams.
    :return: The name of the winning team or "It's a tie!" if the scores are equal.
    """
    team1_score = get_score(top_2_teams[0])
    team2_score = get_score(top_2_teams[1])

    if team1_score > team2_score:
        return top_2_teams[0]
    elif team2_score > team1_score:
        return top_2_teams[1]
    else:
        return "It's a tie!"


# double elimination
def printMatches(matches):
    """Prints the active matches in the given list of matches.

    :param matches: A list of matches.
    """
    print("Active Matches:")
    for match in matches:
        if match.is_ready_to_start():
            print("\t{} vs {}".format(*[p.get_competitor()
                                        for p in match.get_participants()]))


def add_win(det, competitor):
    """Adds a win for the given competitor in the given double elimination tournament.The function first finds the
        active match for the given competitor and then adds a win for the competitor in that match.

    :param det: A double elimination tournament object.
    :param competitor: The competitor to add a win for.
    """
    det.add_win(det.get_active_matches_for_competitor(competitor)[0], competitor)


def checkActiveMatches(det, competitorPairs):
    """Checks if the given list of competitor pairs matches the active matches in the given double elimination tournament.

    :param det: A double elimination tournament object.
    :param competitorPairs: A list of competitor pairs.
    """

    # Gets the active matches in the tournament
    matches = det.get_active_matches()

    # Compares the number of active matches with the number of competitor pairs
    if len(competitorPairs) != len(matches):
        printMatches(matches)
        print(competitorPairs)
        raise Exception("Invalid number of competitors: {} vs {}".format(
            len(matches), len(competitorPairs)))

    # Checks if each competitor pair matches an active match
    for match in matches:
        inMatches = False
        for competitorPair in competitorPairs:
            participants = match.get_participants()

            # If the competitor pair matches the active match
            if competitorPair[0] == participants[0].get_competitor():
                if competitorPair[1] == participants[1].get_competitor():
                    inMatches = True
            elif competitorPair[0] == participants[1].get_competitor():
                if competitorPair[1] == participants[0].get_competitor():
                    inMatches = True

        # If no match was found for a competitor pair, raises an exception
        if not inMatches:
            printMatches(matches)
            print(competitorPairs)
            raise Exception("Wrong matches")


def round_robin_simulation():
    """This function simulates a round-robin tournament, where each country in the list of countries plays against each other.
    It generates pools, plays round-robin games, selects the top teams, and runs the final game between them to determine
    the winner of the tournament. It returns the semi-final and final results.

    :return:
    semi_final (list): A list of countries that reached the semi-final.
    final (list): A list of the top two countries that reached the final.
    """

    # Initialize an empty list to accumulate the results of each round-robin game
    accumulated_results = []

    # Generate pools, play round-robin games, and select the top teams
    pools = generate_pools(countries, None)
    standings, top_teams = round_robin_game(pools)
    accumulated_results.append((standings, top_teams))

    # Determine the champion by running the final game between the top teams
    semi_final = list(accumulated_results[0][0]['pool_A'].keys())
    final = list(accumulated_results[-1][1])
    champion = final_game(accumulated_results[-1][1])
    print(f'{champion} wins the 2023 WBC!')

    return semi_final, final


def double_elimination(stat):
    """This function simulates a double-elimination tournament. It receives a dictionary of country statistics as input,
        plays matches between countries, and eliminates countries until there is only one left, which is the champion of the
        tournament.

    :param stat: A dictionary of country statistics.
    :return:
    semi_unique (list): A list of countries that reached the semi-final.
    accumulated_winners (list): A list of the top two countries that reached the final.
    """

    # Create a DoubleEliminationTournament object using the keys of the stat dictionary
    det = DoubleEliminationTournament(stat.keys())

    # For each country in the stat dictionary, calculate the score using the get_score function
    for country in stat.keys():
        stat[country] = get_score(country)

    # Play matches between countries and eliminate countries until there is only one left, which is the champion of the
    # tournament
    matches = det.get_active_matches()
    accumulated_winners = []
    print("\n 14 Matches:")

    while len(matches) > 0:
        for match in matches:
            left, right = match.get_participants()[0].get_competitor(), match.get_participants()[1].get_competitor()
            if stat[left] > stat[right]:
                winner = left
            elif stat[left] < stat[right]:
                winner = right
            else:
                print("It's tie!")
            det.add_win(match, winner)
            print(match)
            accumulated_winners.append(winner)

        matches = det.get_active_matches()

    # Determine the semi-final and final results
    unique_elements = list(set(accumulated_winners))
    last_indices = [len(accumulated_winners) - 1 - accumulated_winners[::-1].index(element) for element in
                    unique_elements]
    semi_unique = [x for _, x in
                   sorted(zip(last_indices, unique_elements), key=lambda pair: pair[0], reverse=True)[:4]]

    print("\nSemi Final: ", semi_unique)
    print("Final: ", accumulated_winners[-2:])
    print(f'{accumulated_winners[-1:][0]} wins the 2023 WBC!')

    return semi_unique, accumulated_winners[-2:]


if __name__ == "__main__":
    countries = ["AUS", "CUB", "ITA", "JPN", "MEX", "PUR", "USA", "VEN"]

    num_sims = int(input("Enter the count of simulation: "))

    semi_rrf = {team: 0 for team in countries}  # semi-finals in round-robin format
    final_rrf = {team: 0 for team in countries}   # finals in round-robin format
    semi_def = {team: 0 for team in countries}   # semi-finals in double elimination format
    final_def = {team: 0 for team in countries}   # finals in double elimination format

    for sim in range(num_sims):
        # Simulate the round-robin format and update team performance dictionaries
        print("\n------------------------------------------------------------------------------------------------")
        print("------------------------------------------------------------------------------------------------")
        print(f"Running simulation {sim + 1} of {num_sims}...")
        print(f"\n -----Round Robin Format-----")
        semi_list_r, final_list_r = round_robin_simulation()

        for team in semi_list_r:
            semi_rrf[team] += 1

        for team in final_list_r:
            final_rrf[team] += 1

        # Simulate the double elimination format and update team performance dictionaries
        print(f"\n -----Double Elimination Format-----")
        random.shuffle(countries)
        stat = {}
        for team in countries:
            stat[team] = 0
        semi_list_d, final_list_d = double_elimination(stat)

        for team in semi_list_d:
            semi_def[team] += 1

        for team in final_list_d:
            final_def[team] += 1

    # print a summary of the tournament results
    print('\n\n------------------------------------------------------------------------------------------------')
    print("\nSummary Statistics")
    print("Simulation times:", num_sims)

    # print the team performance in the round-robin format
    print("\n -----Round Robin Format-----")
    print(f'{"Country":<10}{"#Semi":>8}{"Semi-Final Prob.":>20}{"#Final":>10}{"Final Prob.":>18}')
    semi_probs_rrf = [semi_rrf[k] / num_sims for k in semi_rrf.keys()]
    final_probs_rrf = [final_rrf[k] / num_sims for k in final_rrf.keys()]

    for i in range(len(semi_rrf)):
        k = list(semi_rrf.keys())[i]
        print(f"{k:<10}{semi_rrf[k]:>8}{semi_probs_rrf[i]:>15,.2f}{final_rrf[k]:>15}{final_probs_rrf[i]:>15,.2f}")

    # print the team performance in the double-elimination format
    print("\n -----Double Elimination Format-----")
    print(f'{"Country":<10}{"#Semi":>8}{"Semi-Final Prob.":>20}{"#Final":>10}{"Final Prob.":>18}')
    semi_probs_def = [semi_def[k] / num_sims for k in semi_def.keys()]
    final_probs_def = [final_def[k] / num_sims for k in final_def.keys()]

    for i in range(len(semi_def)):
        k = list(semi_def.keys())[i]
        print(f"{k:<10}{semi_def[k]:>8}{semi_probs_def[i]:>15,.2f}{final_def[k]:>15}{final_probs_def[i]:>15,.2f}")
