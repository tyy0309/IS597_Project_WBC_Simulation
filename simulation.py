from dataclasses import dataclass
import random
import numpy as np
from typing import List, Tuple
from sklearn.preprocessing import MinMaxScaler

import pandas as pd


@dataclass
class Player:
    last_name: str
    first_name: str
    player_id: int
    Country: str


@dataclass
class Pitcher(Player):
    year: int
    pa: int
    bip: int
    ba: float
    est_ba: float
    est_ba_minus_ba_diff: float
    slg: float
    est_slg: float
    est_slg_minus_slg_diff: float
    woba: float
    est_woba: float
    est_woba_minus_woba_diff: float
    era: float
    xera: float
    era_minus_xera_diff: float


@dataclass
class Batter(Player):
    attempts: int
    avg_hit_angle: float
    anglesweetspotpercent: float
    max_hit_speed: float
    avg_hit_speed: float
    fbld: float
    gb: float
    max_distance: float
    avg_distance: float
    avg_hr_distance: float
    ev95plus: int
    ev95percent: float
    barrels: int
    brl_percent: float
    brl_pa: float


@dataclass
class Team:
    pitchers: List[Pitcher]
    batters: List[Batter]


def generate_players(player_type, country, num_of_players):
    if player_type not in ['Pitcher', 'Batter']:
        raise ValueError("Invalid player type. Choose either 'Pitcher' or 'Batter'.")

    if num_of_players < 1:
        raise ValueError("Number of players must be at least 1.")

    data_file = f"data/{player_type.lower()}.csv"
    players_data = pd.read_csv(data_file)
    players = players_data[players_data['Country'] == country]

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
    pitchers_list = generate_players('Pitcher', country, num_pitchers)
    batters_list = generate_players('Batter', country, num_batters)

    pitchers = [Pitcher(*pitcher_data) for pitcher_data in pitchers_list]
    batters = [Batter(*batter_data) for batter_data in batters_list]

    return Team(pitchers, batters)


def pitching_score(pitchers: List[Pitcher], pitch_count: int) -> float:
    # TODO: Make sure if it's reasonable to use only three pitchers in the first hypothesis
    # TODO: Add pitchers
    p1 = random.randint(45, pitch_count-45) #先發投手用球數
    p3 = random.randint(0, 15)  #後援投手用球數
    p2 = random.randint(0, pitch_count-p1-p3) #中繼投手用球數

    pitch_for_each = [p1, p2, p3]

    # 計算每位投手的用球數百分比
    # list
    pitch_count_percentage = [count / pitch_count for count in pitch_for_each]

    weighted_performance = []
    for percentage, pitcher in zip(pitch_count_percentage, pitchers):
        # Calculate the performance for each pitcher
        performance = (0.25 * pitcher.pa) + \
                      (0.25 * pitcher.bip) + \
                      (0.2 * pitcher.est_ba_minus_ba_diff) + \
                      (0.1 * pitcher.est_slg_minus_slg_diff) + \
                      (0.1 * pitcher.est_woba_minus_woba_diff) + \
                      (0.1 * pitcher.era_minus_xera_diff)
        # Add the weighted performance score for the current pitcher to the list
        weighted_performance.append(percentage * performance)

        # Normalize the weighted performance scores
    scaler = MinMaxScaler()
    normalized_performance = scaler.fit_transform(np.array(weighted_performance).reshape(-1, 1))

    # Calculate the final pitching score as the sum of the normalized weighted performance scores
    total_pitching_score = np.sum(normalized_performance)

    return total_pitching_score

# def hitting_score(batters: List[Batter]) -> float:
#     total_hitting_score = sum([batter.brl_percent for batter in batters])
#
#     return total_hitting_score

# TODO: value generated is not randomized rn, need to be fixed (Batter could be random generated)
def hitting_score(batters: List[Batter]) -> float:
    # performance = (0.35 * avg_hit_speed) + (0.25 * max_distance) + (0.2 * ev95plus) + (0.1 * barrels) + (0.1 * brl_percent)
    scaler = MinMaxScaler()

    # Normalize the variables
    normalized_variables = scaler.fit_transform([
        [batter.avg_hit_speed, batter.max_hit_speed, batter.ev95plus, batter.barrels, batter.brl_percent]
        for batter in batters
    ])

    # Compute the performance scores for all batters
    performances = []
    for i, batter in enumerate(batters):
        performance = (0.35 * normalized_variables[i][0]) + \
                      (0.25 * normalized_variables[i][1]) + \
                      (0.2 * normalized_variables[i][2]) + \
                      (0.1 * normalized_variables[i][3]) + \
                      (0.1 * normalized_variables[i][4])
        performances.append(performance)

    # Calculate the total hitting score as the sum of the performances
    total_hitting_score = np.sum(performances)

    return total_hitting_score


def calculate_total_score(team1: Team, team2: Team, pitch_count: int) -> Tuple[float, float]:
    team1_pitching_score = pitching_score(team1.pitchers, pitch_count)
    team1_hitting_score = hitting_score(team1.batters)
    team1_total_score = team1_pitching_score + team1_hitting_score
    print(pitch_count, team1_pitching_score, team1_hitting_score)
    print(' ')

    team2_pitching_score = pitching_score(team2.pitchers, pitch_count)
    team2_hitting_score = hitting_score(team2.batters)
    team2_total_score = team2_pitching_score + team2_hitting_score
    print(pitch_count, team2_pitching_score, team2_hitting_score)
    print('------')


    # team1_win_rate = team1_total_score/(team1_total_score+team2_total_score)
    # team2_win_rate = team2_total_score/(team1_total_score+team2_total_score)

    # team1_win_rate, team2_win_rate = normalize_scores(team1_total_score, team2_total_score)

    return team1_total_score, team2_total_score


def monte_carlo_simulation(team1: Team, team2: Team, num_iterations: int) -> tuple[int, int, float, float]:
    team1_wins = 0
    team2_wins = 0

    for i in range(num_iterations):
        random.seed() # Reset the random seed for each iteration
        # TODO: pitch_count range should be checked
        pitch_count = random.randint(81, 200) # 三位投手總投球數
        # team1_win_rate, team2_win_rate = calculate_win_rate(team1, team2, pitch_count)
        # if team1_win_rate > team2_win_rate:
        #     team1_wins += 1
        # else:
        #     team2_wins += 1

        team1_total_score, team2_total_score = calculate_total_score(team1, team2, pitch_count)
        if team1_total_score > team2_total_score:
            team1_wins += 1
        else:
            team2_wins += 1

    team1_win_rate = team1_wins / num_iterations
    team2_win_rate = team2_wins / num_iterations

    return team1_wins, team2_wins, team1_win_rate, team2_win_rate


# TODO: define a function that print all the required data
# def generate_report():
# output:    Team 1                                                         Team 2
# sim_index  country   tot_p_cnt   1st_p_count    1st_p_cnt_pct   result    country   tot_p_cnt   1st_p_count   1st_p_cnt_ pct   result
# 1          USA       300         80             0.27            win        Japan     400         90            0.225           lose
# 2          USA       345         75             0.22            lose       Japan     325         85            0.26            win
# ....
# Summary Statistics
# simulation times: 1000
# Team 1                                                        Team 2
# avg_1st_p_count    win_times     lose_times     win_rate      avg_1st_p_count    win_times     lose_times     win_rate
# 80                 543           457            0.543         75                 457           543            0.457



if __name__ == "__main__":

    countries = ["Australia", "Cuba", "Italy", "Japan", "Mexico", "Puerto Rico", "USA", "Venezuela"]

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
    print("\n")

    team1 = generate_team(countryA, 3, 9)
    team2 = generate_team(countryB, 3, 9)


    team1_wins, team2_wins, team1_win_rate, team2_win_rate = monte_carlo_simulation(team1, team2, num_iterations)

    print(f"Team 1 ({team1.pitchers[0].Country}) win times: {team1_wins}")
    print(f"Team 2 ({team2.pitchers[0].Country}) win times: {team2_wins}")

    print(f"Team 1 ({team1.pitchers[0].Country}) win rate: {team1_win_rate}")
    print(f"Team 2 ({team2.pitchers[0].Country}) win rate: {team2_win_rate}")
