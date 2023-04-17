from dataclasses import dataclass
import random
from typing import List


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


def simulate_game(team1: Team, team2: Team, pitch_count: int) -> tuple[float, float]:
    if random.randint(0, 1) == 0:
        starting_pitcher = team1.pitcher
        opposing_team = team2
    else:
        starting_pitcher = team2.pitcher
        opposing_team = team1

    pitching_performance = starting_pitcher.pa / (starting_pitcher.bip * pitch_count) * (
            1 - starting_pitcher.est_ba_minus_ba_diff) * (1 - starting_pitcher.est_slg_minus_slg_diff) * (
                                   1 - starting_pitcher.est_woba_minus_woba_diff) * starting_pitcher.era / starting_pitcher.xera

    hitting_performance = 0
    for batter in opposing_team.batters:
        hitting_performance += (batter.barrels / batter.attempts) * (batter.ev95plus / 100) * (
                batter.avg_hit_speed / 100) * (batter.avg_distance / 400)

    team1_win_rate = pitching_performance + hitting_performance
    team2_win_rate = 2 - team1_win_rate
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


if __name__ == "__main__":
    # Example usage
    pitcher_data = ["Kershaw", "Clayton", 477132, 2023, 73, 51, 0.239, 0.25, -0.011, 0.418, 0.453, -0.035, 0.306, 0.323,
                    -0.017, 3.5, 4.33, -0.83, "Australia"]
    batter_data1 = ["Freeman", "Freddie", 518692, 47, 11.6, 55.3, 107.0, 90.6, 93.2, 86.3, 425, 186, 396.0, 19, 41.3, 4,
                    8.5, 6.3, "Australia"]
    batter_data2 = ["Smith", "Will", 669257, 37, 13.7, 40.5, 110.8, 90.0, 95.3, 84.0, 390, 191, 373.0, 17, 47.2, 3, 8.1,
                    6.3, "Australia"]
    batter_data3 = ['Outman', "James", 681546, 25, 5.5, 44.0, 110.7, 91.2, 95.7, 86.9, 423, 179, 410.0, 11, 44.0, 6,
                    24.0, 12.2, "Australia"]

    pitcher = Pitcher(*pitcher_data)
    batter1 = Batter(*batter_data1)
    batter2 = Batter(*batter_data2)
    batter3 = Batter(*batter_data3)
    team1 = Team(pitcher, [batter1, batter2, batter3])

    # Create a second team for comparison
    pitcher_data_ = ["Matz", "Steven", 571927, 2023, 76, 51, 0.328, 0.287, 0.041, 0.507, 0.447, 0.06, 0.392, 0.359,
                     0.033, 6.48, 5.51, 0.97, "USA"]
    batter_data1_ = ["Goldschmidt", "Paul", 502671, 41, 18.6, 36.6, 110.4, 95.4, 98.0, 91.8, 398, 192, 398.0, 24, 58.5,
                     5, 12.2, 7.9, "USA"]
    batter_data2_ = ["Neill", "Tyler", 641933, 30, 10.1, 40.0, 109.0, 92.7, 94.8, 90.1, 461, 168, 461.0, 16, 55.2, 4,
                     13.3, 8.2, "USA"]
    batter_data3_ = ["Helsley", "Ryan", 664854, 28, 16.6, 50.0, 110.3, 91.8, 95.6, 88.4, 446, 197, 411.0, 14,
                     50.0, 4, 14.3, 8.5, "USA"]

    pitcher_ = Pitcher(*pitcher_data_)
    batter1_ = Batter(*batter_data1_)
    batter2_ = Batter(*batter_data2_)
    batter3_ = Batter(*batter_data3_)
    team2 = Team(pitcher_, [batter1_, batter2_, batter3_])

    team1_win_rate, team2_win_rate = monte_carlo_simulation(team1, team2, num_iterations=1000,
                                                            pitch_count=random.randint(50, 100))

    print(f"Team 1 ({team1.pitcher.Country}) win rate: {team1_win_rate}")
    print(f"Team 2 ({team2.pitcher.Country}) win rate: {team2_win_rate}")
