from dataclasses import dataclass
import random
from typing import List, Tuple

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
    # To-Do 投手的最低用球數？可以只投一顆嗎？
    p1 = random.randint(10, pitch_count-10) #先發投手用球數
    p2 = random.randint(10, pitch_count-10-p1) #中繼投手用球數
    p3 = pitch_count - p1 - p2  #後援投手用球數

    pitch_for_each = [p1, p2, p3]

    # 計算每位投手的用球數百分比
    # list
    pitch_count_percentage = [count / pitch_count for count in pitch_for_each]

    # 計算每位投手的加權表現
    # TO-DO 公式
    # list
    weighted_performance = [percentage * pitcher.era_minus_xera_diff for percentage, pitcher in
                            zip(pitch_count_percentage, pitchers)]

    return sum(weighted_performance)


def hitting_score(batters: List[Batter]) -> float:
    total_hitting_score = sum([batter.brl_percent for batter in batters])

    return total_hitting_score


def normalize_scores(score1: float, score2: float) -> Tuple[float, float]:
    total_score = score1 + score2
    return score1 / total_score, score2 / total_score


def calculate_win_rate(team1: Team, team2: Team, pitch_count: int) -> Tuple[float, float]:
    team1_pitching_score = pitching_score(team1.pitchers, pitch_count)
    team1_hitting_score = hitting_score(team1.batters)
    # team1_total_score = team1_pitching_score + team1_hitting_score
    print(pitch_count, team1_pitching_score, team1_hitting_score)
    print(' ')

    team2_pitching_score = pitching_score(team2.pitchers, pitch_count)
    team2_hitting_score = hitting_score(team2.batters)
    # team2_total_score = team2_pitching_score + team2_hitting_score
    print(pitch_count, team2_pitching_score, team2_hitting_score)
    print('------')

    # team1_win_rate, team2_win_rate = normalize_scores(team1_total_score, team2_total_score)

    return team1_win_rate, team2_win_rate


def monte_carlo_simulation(team1: Team, team2: Team, num_iterations: int) -> tuple[float, float]:
    team1_wins = 0
    team2_wins = 0

    for i in range(num_iterations):
        pitch_count = random.randint(300, 500) # 三位投手總投球數
        team1_win_rate, team2_win_rate = calculate_win_rate(team1, team2, pitch_count)
        if team1_win_rate > team2_win_rate:
            team1_wins += 1
        else:
            team2_wins += 1

    team1_win_rate = team1_wins / num_iterations
    team2_win_rate = team2_wins / num_iterations

    return team1_win_rate, team2_win_rate



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

    team1 = generate_team(countryA, 3, 9)
    team2 = generate_team(countryB, 3, 9)

    # To-Do: Pitch Count 可以改成使用者輸入
    team1_win_rate, team2_win_rate = monte_carlo_simulation(team1, team2, num_iterations=10)

    print(f"Team 1 ({team1.pitchers[0].Country}) win rate: {team1_win_rate}")
    print(f"Team 2 ({team2.pitchers[0].Country}) win rate: {team2_win_rate}")
