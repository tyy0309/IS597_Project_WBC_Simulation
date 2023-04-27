"""
IS597 Final Project
Judy(Chu-Ting) Chan
Cindy(Ting-Yin) Yang
"""
import random
import pandas as pd
from typing import List
from dataclasses import dataclass

@dataclass
class Player:
    player: str
    country: str

@dataclass
class Pitcher(Player):
    W: int
    L: int
    ERA: float
    G: int
    GS: int
    CG: int
    SHO: int
    SV: int
    SVO: int
    IP: float
    H: int
    R: int
    ER: int
    HR: int
    HB: int
    BB: int
    SO: int
    WHIP: float
    AVG: float

@dataclass
class Batter(Player):
    G: int
    AB: int
    R: int
    H: int
    two_B: int
    three_B: int
    HR: int
    RBI: int
    BB: int
    SO: int
    SB: int
    CS: int
    AVG: float
    OBP: float
    SLG: float
    OPS: float

@dataclass
class Team:
    pitchers: List[Pitcher]
    batters: List[Batter]

def generate_players(player_type, country, num_of_players):
    if player_type not in ['Pitchers', 'Batters']:
        raise ValueError("Invalid player type. Choose either 'Pitcher' or 'Batter'.")

    if num_of_players < 1:
        raise ValueError("Number of players must be at least 1.")

    data_file = f"data/{player_type.lower()}.csv"
    players_data = pd.read_csv(data_file)
    players = players_data[players_data['team'] == country]

    if len(players) < num_of_players:
        raise ValueError(f"Not enough {player_type.lower()}s from {country}")

    random_players = players.sample(num_of_players)
    players_list = []

    sorted_players = sorted(random_players.iterrows(), key=lambda x: x[1][-1])

    for _, player in sorted_players:
        players_list.append(list(player))

    return players_list


def generate_team(country, num_pitchers, num_batters):
    pitchers_list = generate_players('Pitchers', country, num_pitchers)
    batters_list = generate_players('Batters', country, num_batters)

    pitchers = [Pitcher(*pitcher_data) for pitcher_data in pitchers_list]
    batters = [Batter(*batter_data) for batter_data in batters_list]

    return Team(pitchers, batters)


def generate_pools(countries, num_pools=None):
    if len(countries) < 4:
        raise ValueError("Number of countries should be at least 4")

    if num_pools is None:
        num_pools = len(countries) // 4

    if len(countries) < num_pools*4:
        raise ValueError("Number of countries is wrong")

    pools = []
    for i in range(num_pools):
        pool = random.sample(countries, k=4)
        pools.append(pool)

    # standings = {'pool_A': {country: 0 for country in pools[0]},
    #              'pool_B': {country: 0 for country in pools[1]}}
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

                    # TODO: generate runs_allowed and defensive_outs, should be combined with get_defensive_rate()
                    team_i_runs_allowed = random.randint(0, 81)
                    team_i_defensive_outs = 27
                    team_j_runs_allowed = random.randint(0, 81)
                    team_j_defensive_outs = 27
                    team_i_defensive_rate = team_i_runs_allowed / team_i_defensive_outs
                    team_j_defensive_rate = team_j_runs_allowed / team_j_defensive_outs

                    if team_i_score > team_j_score:
                        # print("---------")
                        # print(pool[j], standings[f'pool_{chr(65+pool_idx)}'])
                        standings[f'pool_{chr(65+pool_idx)}'][pool[i]] += 1
                    elif team_j_score > team_i_score:
                        # print("----------")
                        # print(pool[j], standings[f'pool_{chr(65+pool_idx)}'])
                        standings[f'pool_{chr(65+pool_idx)}'][pool[j]] += 1

                    # TODO: Pool tiebreakers
                    else:
                        if team_i_defensive_rate > team_j_defensive_rate:
                            standings[f'pool_{chr(65+pool_idx)}'][pool[i]] += 1
                        else:
                            standings[f'pool_{chr(65+pool_idx)}'][pool[j]] += 1

    # Find the teams with the highest number of wins
    top_teams = []
    for pool in standings.keys():
        wins = [(team, wins) for team, wins in standings[pool].items() if wins > 0]
        sorted_wins = sorted(wins, key=lambda x: (-x[1], -get_defensive_rate(x[0])))
        top_teams.extend([team for team, wins in sorted_wins[:2]])

    if len(top_teams) > 2:
        print("First round: ")
        print(standings)
        print("Countries get into the second round: ", top_teams)
        new_standings, new_top_teams = generate_pools(top_teams, num_pools=1)
        return new_standings, new_top_teams
    else:
        print("\nSecond round: ")
        print(standings)
        print("Countries get into the final round: ", top_teams)
        return standings, top_teams


def get_defensive_rate(team):
    team_runs_allowed = random.randint(0, 81)
    team_defensive_outs = 27
    return team_runs_allowed / team_defensive_outs






if __name__ == "__main__":
    countries = ["AUS", "CUB", "ITA", "JPN", "MEX", "PUR", "USA", "VEN"]

    # while True:
    #     print("Please choose two countries to match up:")
    #     print(" ".join([f"{i + 1}. {country}" for i, country in enumerate(countries)]))
    #     countryA = countries[int(input("Enter the number of country A: ")) - 1]
    #     countryB = countries[int(input("Enter the number of country B: ")) - 1]
    #     if countryA == countryB:
    #         print("Error: You can't choose the same country!")
    #     else:
    #         break
    #
    # num_iterations = int(input("Enter the count of simulation: "))

    team1 = generate_pools(countries)
