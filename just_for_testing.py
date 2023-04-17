"""
just_for_testing.py
-
We consider two key performance metrics being used in the simulation - pitting and hitting.
"""
from __future__ import annotations

import csv
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
    pitcher: Pitcher
    batters: List[Batter]

    def calculate_pitching_performance(self):
        return self.pitcher.pa / (self.pitcher.pa + self.pitcher.bip) * (1 - self.pitcher.era)

    def calculate_hitting_performance(self):
        hits = sum(batter.attempts * batter.avg_hit_angle / 10 for batter in self.batters)
        return hits / (hits + self.pitcher.pa) * sum(
            batter.attempts * batter.avg_hit_angle / 10 for batter in self.batters)

    def calculate_win_rate(self):
        pitching_performance = self.calculate_pitching_performance()
        hitting_performance = self.calculate_hitting_performance()
        return (pitching_performance + hitting_performance) / 2

    def get_random_pitcher(country: str, year: int, pitcher_data: pd.DataFrame) -> Pitcher:
        filtered_pitcher_data = pitcher_data[(pitcher_data['Country'] == country) & (pitcher_data['year'] == year)]
        random_pitcher_row = filtered_pitcher_data.sample(n=1).iloc[0]
        return Pitcher(**random_pitcher_row)

    def get_random_batters(country1: str, country2: str, batter_data: pd.DataFrame) -> Tuple[List[Batter], List[Batter]]:
        filtered_batter_data1 = batter_data[batter_data['Country'] == country1]
        filtered_batter_data2 = batter_data[batter_data['Country'] == country2]
        random_batters1 = [Batter(**row) for _, row in filtered_batter_data1.sample(n=9).iterrows()]
        random_batters2 = [Batter(**row) for _, row in filtered_batter_data2.sample(n=9).iterrows()]
        return random_batters1, random_batters2
@dataclass
class Simulator:
    team1: Team
    team2: Team

    def simulate(self, num_simulations: int):
        win_count1 = 0
        win_count2 = 0
        for i in range(num_simulations):
            win_rate1 = self.team1.calculate_win_rate()
            win_rate2 = self.team2.calculate_win_rate()
            if win_rate1 > win_rate2:
                win_count1 += 1
            elif win_rate2 > win_rate1:
                win_count2 += 1
        return win_count1 / num_simulations, win_count2 / num_simulations


if __name__ == '__main__':
    countries = ["Australia", "Canada", "China", "Cuba", "Dominican Republic", "Israel", "Italy", "Japan", "Korea",
                 "Mexico", "Netherlands", "Puerto Rico", "Chinese Taipei", "United States", "Venezuela"]

    # 讓使用者輸入兩個對戰國家
    while True:
        print("Please choose two countries to match up:")
        print(" ".join([f"{i + 1}. {country}" for i, country in enumerate(countries)]))
        country1 = countries[int(input("Enter the number of country 1: ")) - 1]
        country2 = countries[int(input("Enter the number of country 2: ")) - 1]
        if country1 == country2:
            print("Error: You can't choose the same country!")
        else:
            break

    # 讓使用者輸入 simulation 次數
    while True:
        num_simulations = int(input("Enter the number of simulations: "))
        if num_simulations <= 0:
            print("Error: Number of simulations should be a positive integer!")
        else:
            break

    # 讀取 pitcher 和 batter 資料
    pitcher_data = pd.read_csv("data/pitcher.csv")
    batter_data = pd.read_csv("data/batter.csv")

    # 隨機挑選出兩個隊伍的選手
    team1_pitcher = Team.get_random_pitcher(country1, 2019, pitcher_data)
    print(team1_pitcher)
    # team1_batters = [Team.get_random_batter(country1, batter_data) for _ in range(9)]
    # team1 = Team(team1_pitcher, team1_batters)
    #
    # team2_pitcher = Team.get_random_pitcher(country2, 2019, pitcher_data)
    # team2_batters = [Team.get_random_batter(country2, batter_data) for _ in range(9)]
    # team2 = Team(team2_pitcher, team2_batters)
    #
    # # 進行比賽並輸出勝率結果
    # simulator = Simulator(team1, team2)
    # win_rate1, win_rate2 = simulator.simulate(num_simulations)
    # print(f"{country1} win rate: {win_rate1:.2%}")
    # print(f"{country2} win rate: {win_rate2:.2%}")
