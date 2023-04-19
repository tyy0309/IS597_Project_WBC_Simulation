from dataclasses import dataclass
import random
from typing import List

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


def simulate_game(team1: Team, team2: Team, pitch_count: int) -> tuple[float, float]:

    # TO-DO
    team1_win_rate = 0
    team2_win_rate = 0

    return team1_win_rate, team2_win_rate


def monte_carlo_simulation(team1: Team, team2: Team, num_iterations: int, pitch_count: int) -> tuple[float, float]:
    team1_wins = 0
    team2_wins = 0

    for i in range(num_iterations):
        team1_win_rate, team2_win_rate = simulate_game(team1, team2, pitch_count)
        if team1_win_rate > team2_win_rate:
            team1_wins += 1
        else:
            team2_wins += 1

    team1_win_rate = team1_wins / num_iterations
    team2_win_rate = team2_wins / num_iterations

    return team1_win_rate, team2_win_rate

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

    team1_win_rate, team2_win_rate = monte_carlo_simulation(team1, team2, num_iterations=10000,
                                                            pitch_count=random.randint(50, 100))

    print(f"Team 1 ({team1.pitchers[0].Country}) win rate: {team1_win_rate}")
    print(f"Team 2 ({team2.pitchers[0].Country}) win rate: {team2_win_rate}")
