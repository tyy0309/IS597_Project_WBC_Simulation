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
    team = generate_team(country_name, 3, 9)

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
    team_runs_allowed = random.randint(0, 81)
    team_defensive_outs = 27

    return team_runs_allowed / team_defensive_outs


def round_robin_game(pools):
    num_pools = len(pools)
    standings = {}
    for j in range(num_pools):
        pool_name = f'pool_{chr(65 + j)}'
        standings[pool_name] = {country: 0 for country in pools[j]}

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
                        # TODO: define the winner by the team's performance
                        winner = random.choice([pool[i], pool[j]])
                        standings[f'pool_{chr(65 + pool_idx)}'][winner] += 1
                        # tiebreaker(pool, pool_idx, pool[i], pool[j], standings)
        # print(standings)

    # Find the teams with the highest number of wins
    top_teams = []
    for pool in standings.keys():
        wins = [(team, wins) for team, wins in standings[pool].items() if wins > 0]
        # Deal with the tiebreaker situation
        sorted_wins = sorted(wins, key=lambda x: (-x[1], -get_defensive_rate(x[0])))
        top_teams.extend([team for team, wins in sorted_wins[:2]])

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
    team1_score = get_score(top_2_teams[0])
    team2_score = get_score(top_2_teams[1])

    if team1_score > team2_score:
        return top_2_teams[0]
    elif team2_score > team1_score:
        return top_2_teams[1]
    else:
        return "It's a tie!"


## double elimination
def printMatches(matches):
    print("Active Matches:")
    for match in matches:
        if match.is_ready_to_start():
            print("\t{} vs {}".format(*[p.get_competitor()
                                        for p in match.get_participants()]))


def add_win(det, competitor):
    det.add_win(det.get_active_matches_for_competitor(competitor)[0], competitor)


def checkActiveMatches(det, competitorPairs):
    matches = det.get_active_matches()
    if len(competitorPairs) != len(matches):
        printMatches(matches)
        print(competitorPairs)
        raise Exception("Invalid number of competitors: {} vs {}".format(
            len(matches), len(competitorPairs)))
    for match in matches:
        inMatches = False
        for competitorPair in competitorPairs:
            participants = match.get_participants()
            if competitorPair[0] == participants[0].get_competitor():
                if competitorPair[1] == participants[1].get_competitor():
                    inMatches = True
            elif competitorPair[0] == participants[1].get_competitor():
                if competitorPair[1] == participants[0].get_competitor():
                    inMatches = True
        if not inMatches:
            printMatches(matches)
            print(competitorPairs)
            raise Exception("Wrong matches")


def round_robin_simulation():
    accumulated_results = []

    pools = generate_pools(countries, None)
    standings, top_teams = round_robin_game(pools)
    accumulated_results.append((standings, top_teams))

    semi_final = list(accumulated_results[0][0]['pool_A'].keys())
    final = list(accumulated_results[-1][1])

    champion = final_game(accumulated_results[-1][1])
    print(f'{champion} wins the 2023 WBC!')

    return semi_final, final

def double_elimination(stat):
    det = DoubleEliminationTournament(stat.keys())

    for country in stat.keys():
        stat[country] = get_score(country)

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

    # print(accumulated_winners)
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

    semi_rrf = {team: 0 for team in countries}
    final_rrf = {team: 0 for team in countries}
    semi_def = {team: 0 for team in countries}
    final_def = {team: 0 for team in countries}

    for sim in range(num_sims):
        print("\n------------------------------------------------------------------------------------------------")
        print("------------------------------------------------------------------------------------------------")
        print(f"Running simulation {sim + 1} of {num_sims}...")
        print(f"\n -----Round Robin Format-----")
        semi_list_r, final_list_r = round_robin_simulation()

        for team in semi_list_r:
            semi_rrf[team] += 1

        for team in final_list_r:
            final_rrf[team] += 1

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

    print('\n\n------------------------------------------------------------------------------------------------')
    print("\nSummary Statistics")
    print("Simulation times:", num_sims)
    print("\n -----Round Robin Format-----")
    print(f'{"Country":<10}{"#Semi":>8}{"Semi-Final Prob.":>20}{"#Final":>10}{"Final Prob.":>18}')
    semi_probs_rrf = [semi_rrf[k] / num_sims for k in semi_rrf.keys()]
    final_probs_rrf = [final_rrf[k] / num_sims for k in final_rrf.keys()]

    for i in range(len(semi_rrf)):
        k = list(semi_rrf.keys())[i]
        print(f"{k:<10}{semi_rrf[k]:>8}{semi_probs_rrf[i]:>15,.2f}{final_rrf[k]:>15}{final_probs_rrf[i]:>15,.2f}")

    print("\n -----Double Elimination Format-----")
    print(f'{"Country":<10}{"#Semi":>8}{"Semi-Final Prob.":>20}{"#Final":>10}{"Final Prob.":>18}')
    semi_probs_def = [semi_def[k] / num_sims for k in semi_def.keys()]
    final_probs_def = [final_def[k] / num_sims for k in final_def.keys()]

    for i in range(len(semi_def)):
        k = list(semi_def.keys())[i]
        print(f"{k:<10}{semi_def[k]:>8}{semi_probs_def[i]:>15,.2f}{final_def[k]:>15}{final_probs_def[i]:>15,.2f}")
