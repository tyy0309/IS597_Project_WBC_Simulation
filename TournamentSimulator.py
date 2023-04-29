import csv

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

def pitching_score():
    with open('random_generated/pitcher_records_AUS.csv', newline='') as f:
        reader = csv.reader(f)
        next(reader)
        player_data = {}
        for row in reader:
            player = row[0]
            if player not in player_data:
                player_data[player] = []
            player_data[player].append(row[1:])
    return player_data

player_data = pitching_score()

key_order = ["LiamDoolan", "SamHolland", "MitchNeunborn"]
sorted_dict = {k: player_data[k] for k in key_order}

weighted_performance = []
percentage = [0.7, 0.2, 0.1]


def pitching_score(pitchers: List[Pitcher], pitch_count: int, sim_index):
    # Sort pitchers by performance
    pitchers.sort(key=lambda x: (x.ERA, x.WHIP, x.AVG, -x.IP, -x.SO))

    # # Select the first pitcher with the highest performance as p1
    # p1_pitch_count = random.randint(45, pitch_count - 45)
    #
    # # Calculate pitch count for p2 and p3
    # remaining_pitch_count = pitch_count - p1_pitch_count
    # p2_pitch_count = random.randint(0, remaining_pitch_count)
    # p3_pitch_count = remaining_pitch_count - p2_pitch_count
    p1 = random.randint(45, pitch_count - 45)  # 先發投手用球數
    p3 = random.randint(0, 15)  # 後援投手用球數
    p2 = random.randint(0, pitch_count - p1 - p3)  # 中繼投手用球數

    # Calculate pitch count percentage for each pitcher
    # pitch_for_each = [p1_pitch_count, p2_pitch_count, p3_pitch_count]
    pitch_for_each = [p1, p2, p3]

    pitch_count_percentage = [count / pitch_count for count in pitch_for_each]

    for player in player_data.keys():
        normalized_ERA = 1 - float(player_data[player][sim_index][1]) / (ERA_MAX - ERA_MIN)
        normalized_WHIP = 1 - float(player_data[player][sim_index][2]) / (WHIP_MAX - WHIP_MIN)
        normalized_BAA = 1 - float(player_data[player][sim_index][3]) / (AVG_MAX - AVG_MIN)

        performance = (0.4 * normalized_ERA) + \
                      (0.35 * normalized_WHIP) + \
                      (0.25 * normalized_BAA)

        print(player, performance)

        print('----------')


