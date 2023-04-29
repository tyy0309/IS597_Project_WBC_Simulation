"""
IS597 Final Project
Judy(Chu-Ting) Chan
Cindy(Ting-Yin) Yang
"""
from dataclasses import dataclass
import random
import numpy as np
from typing import List, Tuple
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import csv
import matplotlib.pyplot as plt


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

def generate_pitcher_games_records(pitchers: List[Pitcher], sim_times):
    # Sort pitchers by performance
    pitchers.sort(key=lambda x: (x.ERA, x.WHIP, x.AVG, -x.IP, -x.SO))

    for pitcher in pitchers:
        pitcher.random_ERA = np.random.normal(pitcher.ERA, 0.2, sim_times)
        pitcher.random_WHIP = np.random.normal(pitcher.WHIP, 0.05, sim_times)
        pitcher.random_BAA = np.random.normal(pitcher.AVG, 0.01, sim_times)

        pitcher.random_ERA = np.clip(pitcher.random_ERA, 0, None)
        pitcher.random_WHIP = np.clip(pitcher.random_WHIP, 0, None)
        pitcher.random_BAA = np.clip(pitcher.random_BAA, 0, 1)

    country = pitchers[0].country
    with open(f'random_generated/pitcher_records_{country}.csv', mode='w', newline='') as output_file:
        fieldnames = ['player', 'team', 'Random_ERA', 'Random_WHIP', 'Random_BAA']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        writer.writeheader()
        for pitcher in pitchers:
            for i in range(sim_times):
                writer.writerow({
                    'player': pitcher.player,
                    'team': pitcher.country,
                    'Random_ERA': pitcher.random_ERA[i],
                    'Random_WHIP': pitcher.random_WHIP[i],
                    'Random_BAA': pitcher.random_BAA[i],
                })

def record_to_dict(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        next(reader)
        data = {}
        for row in reader:
            player = row[0]
            if player not in data:
                data[player] = []
            data[player].append(row[1:])

    return data


def pitching_score(country: str, pitch_count: int, sim_index):

    p1 = random.randint(45, pitch_count - 45)  # 先發投手用球數
    p3 = random.randint(5, 15)  # 後援投手用球數
    p2 = random.randint(5, pitch_count - p1 - p3)  # 中繼投手用球數

    pitch_for_each = [p1, p2, p3]
    # 100%?
    pitch_count_percentage = [count / (p1+p2+p3) for count in pitch_for_each]
    pitcher_data = record_to_dict(f'random_generated/pitcher_records_{country}.csv')
    weighted_performance = []
    # {player: [[aus,0.3,0.2,0.1],[aus, ..]]}
    for percentage, player in zip(pitch_count_percentage, pitcher_data.keys()):
        normalized_ERA = 1 - float(pitcher_data[player][sim_index][1]) / (ERA_MAX - ERA_MIN)
        normalized_WHIP = 1 - float(pitcher_data[player][sim_index][2]) / (WHIP_MAX - WHIP_MIN)
        normalized_BAA = 1 - float(pitcher_data[player][sim_index][3]) / (AVG_MAX - AVG_MIN)

        performance = (0.4 * normalized_ERA) + \
                      (0.35 * normalized_WHIP) + \
                      (0.25 * normalized_BAA)

        weighted_performance.append(percentage * performance)

    final_score = sum(weighted_performance) / 3
    return p1, round(p1 / pitch_count, 2), final_score


def generate_batter_games_records(batters: List[Batter], sim_times):

    for batter in batters:
        batter.random_BA = np.random.normal(batter.AVG, 0.02, sim_times)
        batter.random_OPS = np.random.normal(batter.OPS, 0.03, sim_times)

        batter.random_BA = np.clip(batter.random_BA, 0, 1)
        batter.random_OPS = np.clip(batter.random_OPS, 0, 1.5)

    country = batters[0].country
    with open(f'random_generated/batter_records_{country}.csv', mode='w', newline='') as output_file:
        fieldnames = ['player', 'team', 'Random_BA', 'Random_OPS']
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)

        writer.writeheader()
        for batter in batters:
            for i in range(sim_times):
                writer.writerow({
                    'player': batter.player,
                    'team': batter.country,
                    'Random_BA': batter.random_BA[i],
                    'Random_OPS': batter.random_OPS[i]
                })

def hitting_score(country, sim_index) -> float:

    batter_data = record_to_dict(f'random_generated/batter_records_{country}.csv')
    all_performance = []

    for player in batter_data.keys():
        normalized_BA = float(batter_data[player][sim_index][1]) / (AVG_B_MAX - AVG_B_MIN)
        normalized_OPS = float(batter_data[player][sim_index][2]) / (OPS_MAX - OPS_MIN)

        # Calculate the performance for each pitcher
        performance = (0.5 * normalized_BA) + \
                      (0.5 * normalized_OPS)

        # Add the weighted performance score for the current pitcher to the list
        all_performance.append(performance)

    # Let final score between 0～1
    return sum(all_performance) / 9


def calculate_total_score(team1: Team, team2: Team, pitch_count: int, sim_index):
    p1_cnt, p1_cnt_pct, team1_pitching_score = pitching_score(team1.pitchers[0].country, pitch_count, sim_index)
    team1_hitting_score = hitting_score(team1.batters[0].country, sim_index)
    team1_total_score = (0.7 * team1_pitching_score) + (0.3 * team1_hitting_score)

    p2_cnt, p2_cnt_pct, team2_pitching_score = pitching_score(team2.pitchers[0].country, pitch_count, sim_index)
    team2_hitting_score = hitting_score(team2.batters[0].country, sim_index)
    team2_total_score = (0.7 * team2_pitching_score) + (0.3 * team2_hitting_score)
    print('\n\nTEAM1', team1_pitching_score, team1_hitting_score)
    print('TEAM2', team2_pitching_score, team2_hitting_score)
    return team1_total_score, team2_total_score, p1_cnt, p2_cnt


def monte_carlo_simulation(team1: Team, team2: Team, num_iterations: int) -> tuple[int, int, float, float]:
    team1_wins = 0
    team2_wins = 0
    team1_more_pitches_when_winning = 0
    team2_more_pitches_when_winning = 0

    print(f'\n{"sim":<10}{"t1-Country":<15}{"t1-p1_cnt":<15}{"t1-p1_cnt_%":<15}{"t1-result":<15}{"|":<5}{"t2-Country":<15}{"t2-p1_cnt":<15}{"t2-p1_cnt_%":<15}{"t2-result":<15}')

    for i in range(num_iterations):
        # random.seed()  # Reset the random seed for each iteration
        pitch_count = random.randint(120, 200)

        team1_total_score, team2_total_score, p1_cnt, p2_cnt = calculate_total_score(team1, team2, pitch_count, i)
        p1_cnt_pct = p1_cnt / pitch_count
        p2_cnt_pct = p2_cnt / pitch_count

        if team1_total_score > team2_total_score:
            team1_wins += 1
            result = 'win'
            if p1_cnt > p2_cnt:
                team1_more_pitches_when_winning += 1
        else:
            team2_wins += 1
            result = 'lose'
            if p2_cnt > p1_cnt:
                team2_more_pitches_when_winning += 1

        print(
            f'{(i + 1):<10}{team1.pitchers[0].country:<15}{p1_cnt:<15}{round(p1_cnt_pct, 2):<15}{result:<15}{"|":<5}{team2.pitchers[0].country:<15}{p2_cnt:<15}{round(p2_cnt_pct, 2):<15}{"win" if result == "lose" else "lose":<15}')

    team1_win_rate = team1_wins / num_iterations
    team2_win_rate = team2_wins / num_iterations

    # Calculate conditional probabilities
    p_A_given_B = team1_more_pitches_when_winning / team1_wins
    p_C_given_D = team2_more_pitches_when_winning / team2_wins

    print("\nSummary Statistics")
    print("simulation times:", num_iterations)
    print(f'{"Team 1":<20}{" ":<10}{" ":<10}{" ":<15}{"Team 2":<20}')
    print(f'{"P(A|B)":<10}{"win_times":<15}{"lose_times":<15}{"win_rate=P(B)":<15}{"P(C|D)":<10}{"win_times":<15}{"lose_times":<15}{"win_rate=P(D)":<15}')
    print(f'{round(p_A_given_B, 2):<10}{team1_wins:<15}{team2_wins:<15}{round(team1_win_rate, 2):<15}{round(p_C_given_D, 2):<10}{team2_wins:<15}{team1_wins:<15}{round(team2_win_rate, 2):<15}')

    return team1_wins, team2_wins, team1_win_rate, team2_win_rate


# Creating a plot to validate monte_carlo_simulation function
def create_plot(team1, team2, p1_cnt_pct_list, team1_results, team2_results):
    plt.scatter(p1_cnt_pct_list, team1_results, label=f'{team1.pitchers[0].country} results')
    plt.scatter(p1_cnt_pct_list, team2_results, label=f'{team2.pitchers[0].country} results')
    plt.xlabel('Pitcher 1st Pitch Strike Percentage')
    plt.ylabel('Team score')
    plt.legend()
    plt.show()





if __name__ == "__main__":

    countries = ["AUS", "CUB", "ITA", "JPN", "MEX", "PUR", "USA", "VEN"]

    while True:
        print("Please choose two countries to match up:")
        print(" ".join([f"{i + 1}. {country}" for i, country in enumerate(countries)]))
        countryA = countries[int(input("Enter the number of country A: ")) - 1]
        countryB = countries[int(input("Enter the number of country B: ")) - 1]
        if countryA == countryB:
            print("Error: You can't choose the same country!")
        else:
            break

    num_iterations = int(input("Enter the count of simulation: "))

    team1 = generate_team(countryA, 3, 9)
    team2 = generate_team(countryB, 3, 9)

    generate_pitcher_games_records(team1.pitchers, num_iterations)
    generate_batter_games_records(team1.batters, num_iterations)

    generate_pitcher_games_records(team2.pitchers, num_iterations)
    generate_batter_games_records(team2.batters, num_iterations)

    # print(calculate_total_score(team1, team2, 300, 1))
    # print(team1.pitchers)
    # print(team1.batters)
    # print(pitching_score(team1.pitchers, 300))
    # print(hitting_score(team1.batters))
    team1_wins, team2_wins, team1_win_rate, team2_win_rate = monte_carlo_simulation(team1, team2, num_iterations)
    # create_plot(team1, team2, p1_cnt_pct_list, team1_results, team2_results)
