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
    # TODO: 先發投手要是最強的
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

    for _, player in random_players.iterrows():
        player_list = list(player)
        reordered_player = [player_list[0], player_list[1], player_list[2], player_list[-1], *player_list[3:-1]]
        players_list.append(reordered_player)

    return players_list


def generate_team(country, num_pitchers, num_batters):
    pitchers_list = generate_players('Pitchers', country, num_pitchers)
    batters_list = generate_players('Batters', country, num_batters)

    pitchers = [Pitcher(*pitcher_data) for pitcher_data in pitchers_list]
    batters = [Batter(*batter_data) for batter_data in batters_list]

    return Team(pitchers, batters)


def pitching_score(pitchers: List[Pitcher], pitch_count: int):
    # Sort pitchers by performance
    pitchers.sort(key=lambda x: (x.ERA, x.WHIP, x.AVG, -x.IP, -x.SO))

    # Select the first pitcher with the highest performance as p1
    p1 = pitchers[0]
    p1_pitch_count = random.randint(45, pitch_count - 45)

    # Calculate pitch count for p2 and p3
    remaining_pitch_count = pitch_count - p1_pitch_count
    p2_pitch_count = random.randint(0, remaining_pitch_count)
    p3_pitch_count = remaining_pitch_count - p2_pitch_count

    # Calculate pitch count percentage for each pitcher
    pitch_for_each = [p1_pitch_count, p2_pitch_count, p3_pitch_count]
    pitch_count_percentage = [count / pitch_count for count in pitch_for_each]

    # Calculate weighted performance score for each pitcher
    weighted_performance = []
    for percentage, pitcher in zip(pitch_count_percentage, pitchers):
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
        weighted_performance.append(percentage * performance)

    # Calculate final score
    final_score = sum(weighted_performance) / len(pitchers)
    return p1_pitch_count, round(p1_pitch_count / pitch_count, 2), final_score


def hitting_score(batters: List[Batter]) -> float:
    all_performance = []
    for batter in batters:
        # 較低的值有更好的表現
        normalized_SO = 1 - batter.SO / (SO_MAX - SO_MIN)

        # 較高的值有更好的表現
        normalized_AVG_B = batter.AVG / (AVG_B_MAX - AVG_B_MIN)
        normalized_OPS = batter.OPS / (OPS_MAX - OPS_MIN)
        normalized_RBI = batter.RBI / (RBI_MAX - RBI_MIN)
        normalized_BB = batter.BB / (BB_MAX - BB_MIN)
        normalized_SB = batter.SB / (SB_MAX - SB_MIN)

        # Calculate the performance for each pitcher
        performance = (0.25 * normalized_AVG_B) + \
                      (0.30 * normalized_OPS) + \
                      (0.15 * normalized_RBI) + \
                      (0.1 * normalized_BB) + \
                      (0.1 * normalized_SO) + \
                      (0.1 * normalized_SB)

        # Add the weighted performance score for the current pitcher to the list
        all_performance.append(performance)

    # Let final score between 0～1
    return sum(all_performance) / len(batters)


def calculate_total_score(team1: Team, team2: Team, pitch_count: int):
    p1_cnt, p1_cnt_pct, team1_pitching_score = pitching_score(team1.pitchers, pitch_count)
    team1_hitting_score = hitting_score(team1.batters)
    team1_total_score = (0.8 * team1_pitching_score) + (0.2 * team1_hitting_score)

    p2_cnt, p2_cnt_pct, team2_pitching_score = pitching_score(team2.pitchers, pitch_count)
    team2_hitting_score = hitting_score(team2.batters)
    team2_total_score = (0.8 * team2_pitching_score) + (0.2 * team2_hitting_score)

    return team1_total_score, team2_total_score, p1_cnt, p2_cnt


def monte_carlo_simulation(team1: Team, team2: Team, num_iterations: int) -> tuple[int, int, float, float]:
    team1_wins = 0
    team2_wins = 0
    p1_cnt_sum = 0
    p2_cnt_sum = 0
    p1_cnt_pct_sum = 0
    p2_cnt_pct_sum = 0
    p1_cnt_pct_list = []
    team1_results = []
    team2_results = []


    print(f'\n{"sim":<10}{"t1-Country":<15}{"t1-p1_cnt":<15}{"t1-p1_cnt_%":<15}{"t1-result":<15}{"|":<5}{"t2-Country":<15}{"t2-p1_cnt":<15}{"t2-p1_cnt_%":<15}{"t2-result":<15}')

    for i in range(num_iterations):
        random.seed()  # Reset the random seed for each iteration

        # 一場比賽共有 27 個出局數，平均每局面對打者的球數通常在 15-20 之間（面對每名打者投球次數 3.5-4 之間，每局平均面對 4 名打者）
        # 估計一場比賽所有投手可能總共需投出約 120-200 顆球
        pitch_count = random.randint(120, 200)

        team1_total_score, team2_total_score, p1_cnt, p2_cnt = calculate_total_score(team1, team2, pitch_count)
        p1_cnt_sum += p1_cnt
        p2_cnt_sum += p2_cnt
        p1_cnt_pct = p1_cnt / pitch_count
        p2_cnt_pct = p2_cnt / pitch_count
        p1_cnt_pct_sum += p1_cnt_pct
        p2_cnt_pct_sum += p2_cnt_pct
        p1_cnt_pct_list.append(p1_cnt_pct)
        team1_results.append(team1_total_score)
        team2_results.append(team2_total_score)

        if team1_total_score > team2_total_score:
            team1_wins += 1
            result = 'win'
        else:
            team2_wins += 1
            result = 'lose'

        print(f'{(i + 1):<10}{team1.pitchers[0].country:<15}{p1_cnt:<15}{round(p1_cnt_pct, 2):<15}{result:<15}{"|":<5}{team2.pitchers[0].country:<15}{p2_cnt:<15}{round(p2_cnt_pct, 2):<15}{"win" if result == "lose" else "lose":<15}')

    team1_win_rate = team1_wins / num_iterations
    team2_win_rate = team2_wins / num_iterations

    p1_avg_cnt = p1_cnt_sum / num_iterations
    p2_avg_cnt = p2_cnt_sum / num_iterations

    p1_avg_cnt_pct = p1_cnt_pct_sum / num_iterations
    p2_avg_cnt_pct = p2_cnt_pct_sum / num_iterations

    print("\nSummary Statistics")
    print("simulation times:", num_iterations)
    print(f'{"Team 1":<20}{" ":<10}{" ":<10}{" ":<10}{" ":<15}{" ":<20}{"Team 2":<20}')
    print(
        f'{"avg_1st_p_count":<20}{"avg_1st_p_cnt_%":<20}{"win_times":<15}{"lose_times":<15}{"win_rate":<15}{"avg_1st_p_count":<20}{"avg_1st_p_cnt_%":<20}{"win_times":<15}{"lose_times":<15}{"win_rate":<15}')
    print(
        f'{round(p1_avg_cnt, 2):<20}{round(p1_avg_cnt_pct, 2):<20}{team1_wins:<15}{team2_wins:<15}{round(team1_win_rate, 3):<15}{round(p2_avg_cnt, 2):<20}{round(p2_avg_cnt_pct, 2):<20}{team2_wins:<15}{team1_wins:<15}{round(team2_win_rate, 3):<15}')

    # return team1_wins, team2_wins, team1_win_rate, team2_win_rate
    return team1_wins, team2_wins, team1_win_rate, team2_win_rate, p1_cnt_pct_list, team1_results, team2_results


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

    # print(pitching_score(team1.pitchers, 300))
    # print(hitting_score(team1.batters))
    team1_wins, team2_wins, team1_win_rate, team2_win_rate, p1_cnt_pct_list, team1_results, team2_results = monte_carlo_simulation(team1, team2, num_iterations)
    create_plot(team1, team2, p1_cnt_pct_list, team1_results, team2_results)
