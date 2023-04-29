"""
IS597 Final Project
Judy(Chu-Ting) Chan
Cindy(Ting-Yin) Yang
"""
import random
import pandas as pd
from typing import List
from dataclasses import dataclass


def get_random_score(team_stats):
    # TODO: Implement a function that generates a random score based on the team's performance statistics
    # For example, you could use a regression model that predicts the expected score based on factors such as batting average, pitching effectiveness, etc.
    return random.randint(0, 10)


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

    # print(pools)
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
                    # TODO: the score could be defined by the hitting score and pitching score in sim.py
                    team_i_score = random.randint(0, 10)
                    team_j_score = random.randint(0, 10)

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


def round_robin_simulation(pools, num_sims):
    accumulated_results = []
    for sim in range(num_sims):
        print("------------------------------------------------------------------------------------------------\n")
        print(f"Running simulation {sim + 1} of {num_sims}...")
        standings, top_teams = round_robin_game(pools)
        accumulated_results.append((standings, top_teams))
    return accumulated_results




if __name__ == "__main__":
    countries = ["AUS", "CUB", "ITA", "JPN", "MEX", "PUR", "USA", "VEN"]
    pools = generate_pools(countries, None)
    results = round_robin_simulation(pools, 100)

