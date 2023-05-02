"""
IS597 Final Project
Judy(Chu-Ting) Chan
Cindy(Ting-Yin) Yang
"""
import random
import statistics as stats
from simulation import generate_team
import pandas as pd
from typing import List
from dataclasses import dataclass

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
    pitch_score = sum(pitch_performance)/3

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

    if len(countries) < num_pools*4:
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
        pool_name = f'pool_{chr(65+j)}'
        standings[pool_name] = {country: 0 for country in pools[j]}

    for pool_idx, pool in enumerate(pools):
        for i in range(len(pool)):
            for j in range(i+1, len(pool)):
                if i != j:
                    team_i_score = get_score(pool[i])
                    team_j_score = get_score(pool[j])

                    if team_i_score > team_j_score:
                        standings[f'pool_{chr(65+pool_idx)}'][pool[i]] += 1
                    elif team_j_score > team_i_score:
                        standings[f'pool_{chr(65+pool_idx)}'][pool[j]] += 1
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


# 1 vs 1 選出贏家輸家
def play_match(countries):
    # TODO: define the winning formula based on the datasets
    winner = random.choice(countries)
    # get the other country in the match as loser
    loser = countries[0] if winner == countries[1] else countries[1]
    return winner, loser


# 將國家放入winner, loser bracket內
def play_round(countries):
    # standings = {country: 0 for pool in pools for country in pool}
    winners = []
    losers = []
    random.shuffle(countries)
    for i in range(0, len(countries), 2):
        match = (countries[i], countries[i+1])
        print("match: ", match)
        winner, loser = play_match(match)
        winners.append(winner)
        losers.append(loser)

    return winners, losers


def update_standings(winners, losers, standings):
    for country in winners:
        standings[country]["wins"] += 1
    for country in losers:
        standings[country]["losses"] += 1


def print_round_results(round_name, winners, losers, standings):
    print(f"\n{round_name}")
    print("winners: ", winners)
    print("losers: ", losers)
    print("Standings after ", round_name, ": ")
    print(standings)


def double_elimination_game(pools):

    standings = {country: {"wins": 0, "losses": 0} for pool in pools for country in pool}

    # play the first round matches
    winners = []
    losers = []
    for pool in pools:
        # TODO: define how to pick the two countries
        random.shuffle(pool)
        pool_winners, pool_losers = play_round(pool)
        winners.extend(pool_winners)
        losers.extend(pool_losers)

    # update standings after first round
    update_standings(winners, losers, standings)
    print_round_results("First round", winners, losers, standings)

    # play the second round match
    second_round_winners, second_round_losers = play_round(winners)

    # update standings after second round
    update_standings(second_round_winners, second_round_losers, standings)
    print_round_results("Second round", second_round_winners, second_round_losers, standings)

    # play the losers bracket matches
    loser_round_winners, loser_round_losers = play_round(losers)


    # update standings after loser bracket round
    update_standings(loser_round_winners, loser_round_losers, standings)
    print_round_results("Loser round", loser_round_winners, loser_round_losers, standings)

    # play the next round matches
    # next_round_winners, _ = play_round(second_round_winners)
    # next_round_losers = []
    # for loser in loser_round_winners:
    #     loser_match = (loser, loser_round_losers.pop(0))
    #     winner, _ = play_match(loser_match)
    #     next_round_losers.append(winner)

    # update standings after next round
    # update_standings(next_round_winners, next_round_losers, standings)
    # print_round_results("Next round", next_round_winners, next_round_losers, standings)
    #
    # # eliminate countries with 2 losses
    # next_round_losers = [country for country in next_round_losers if standings[country]["losses"] < 2]

    return standings


def round_robin_simulation(num_sims):
    semi_stat = {"AUS": 0, "CUB": 0, "ITA": 0, "JPN": 0, "MEX": 0, "PUR": 0, "USA": 0, "VEN": 0}
    final_stat = {"AUS": 0, "CUB": 0, "ITA": 0, "JPN": 0, "MEX": 0, "PUR": 0, "USA": 0, "VEN": 0}

    for sim in range(num_sims):
        accumulated_results = []

        print("------------------------------------------------------------------------------------------------\n")
        print(f"Running simulation {sim + 1} of {num_sims}...")
        pools = generate_pools(countries, None)
        standings, top_teams = round_robin_game(pools)
        accumulated_results.append((standings, top_teams))

        semi_final = list(accumulated_results[0][0]['pool_A'].keys())
        for team in semi_final:
            semi_stat[team] += 1

        final = list(accumulated_results[-1][1])
        for team in final:
            final_stat[team] += 1

        champion = final_game(accumulated_results[-1][1])
        print(f'{champion} wins the 2023 WBC!')

    print('\n\n------------------------------------------------------------------------------------------------')
    print("\nSummary Statistics")
    print("simulation times:", num_sims)
    # print(semi_stat)
    # print(final_stat)

    semi_probs = [semi_stat[k] / num_sims for k in semi_stat.keys()]
    final_probs = [final_stat[k] / num_sims for k in final_stat.keys()]

    print(f'{"Country":<10}{"#Semi":>8}{"Semi-Final Prob.":>20}{"#Final":>10}{"Final Prob.":>18}')
    for i in range(len(semi_stat)):
        k = list(semi_stat.keys())[i]
        print(f"{k:<10}{semi_stat[k]:>8}{semi_probs[i]:>15,.2f}{final_stat[k]:>15}{final_probs[i]:>15,.2f}")
    # print(f'{"Total":<10}{str(num_sims * 4):>8}{"-":>15}{str(num_sims * 2):>15}{"-":>15}')

    return accumulated_results


if __name__ == "__main__":
    countries = ["AUS", "CUB", "ITA", "JPN", "MEX", "PUR", "USA", "VEN"]

    # pools = generate_pools(countries, None)

    # num_sims = int(input("Enter the count of simulation: "))
    # results = round_robin_simulation(num_sims)


    # double_elimination_game(pools)

