"""
IS597 Final Project
Judy(Chu-Ting) Chan
Cindy(Ting-Yin) Yang
"""
import random
from simulation import generate_team, pitching_score, hitting_score
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


# def tiebreaker(pool, pool_idx, team_i, team_j, standings):
#     pool_name = f'pool_{chr(65+pool_idx)}'
#     pool_scores = [standings[pool_name][team] for team in pool]
#     print("pool score: ", pool_scores)
#     if pool_scores.count(pool_scores[0]) == 3:
#         team_i_defensive_rate = get_defensive_rate(team_i)
#         team_j_defensive_rate = get_defensive_rate(team_j)
#
#         print("-------------------------------------------")
#         print(team_i, team_i_defensive_rate, team_j, team_j_defensive_rate)
#
#         if team_i_defensive_rate < team_j_defensive_rate:
#             standings[pool_name][team_i] += 1
#         else:
#             standings[pool_name][team_j] += 1
#     return


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
        # TODO: Tiebreaker?
        return "It's a tie!"

def double_elimination_game(pools):

    standings = {country: 0 for pool in pools for country in pool}

    # play the first round matches
    winners = []
    losers = []
    for pool in pools:
        # print("pool:", pool)
        pool_winners = []
        pool_losers = []
        # shuffle the pool before playing matches
        # TODO: define how to pick the two countries
        random.shuffle(pool)
        matches = [(pool[i], pool[i + 1]) for i in range(0, 3, 2)]
        # print("matches:", matches)
        for match in matches:
            # TODO: define the winning formula based on the datasets
            winner = random.choice(match)
            # get the other country in the match as loser
            loser = match[0] if winner == match[1] else match[1]
            pool_winners.append(winner)
            pool_losers.append(loser)
            standings[winner] += 1
        # print("pool_winners: ", pool_winners)
        # print("pool_losers: ", pool_losers, "\n")
        winners.extend(pool_winners)
        losers.extend(pool_losers)

    print("winners: ", winners)
    print("losers: ", losers)

    # play the second round matches


    # winners_bracket = winners
    # losers_bracket = losers
    # print("winners_bracket: ", winners_bracket)
    # print("losers_bracket: ", losers_bracket)
    # wb_matches = [(winners_bracket[i], winners_bracket[j]) for i in range(4) for j in range(i + 1, 4)]
    # lb_matches = [(losers_bracket[i], losers_bracket[j]) for i in range(4) for j in range(i + 1, 4)]
    # print("wb_matches: ", wb_matches)
    # print("lb_matches: ", lb_matches)
    # for match in wb_matches:
    #     # TODO: define the winning formula based on the datasets
    #     winner = random.choice(match)

    return standings


def round_robin_simulation(num_sims):
    accumulated_results = []
    for sim in range(num_sims):
        print("------------------------------------------------------------------------------------------------\n")
        print(f"Running simulation {sim + 1} of {num_sims}...")
        pools = generate_pools(countries, None)
        standings, top_teams = round_robin_game(pools)
        accumulated_results.append((standings, top_teams))

        champion = final_game(accumulated_results[-1][1])
        print(f'{champion} wins the 2023 WBC!')
    return accumulated_results




if __name__ == "__main__":
    countries = ["AUS", "CUB", "ITA", "JPN", "MEX", "PUR", "USA", "VEN"]
    # pools = generate_pools(countries, None)
    # print(pools)

    results = round_robin_simulation(10)


    # db = double_elimination_game(pools)

