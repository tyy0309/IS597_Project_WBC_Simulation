import random


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.eliminated = False


class Match:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.winner = None
        self.loser = None

    def play(self):
        # TODO: fix the formula
        winner = random.choice(self.players)
        self.winner = winner
        self.loser = self.players[0] if winner == self.players[1] else self.players[1]


class DualElimination:
    def __init__(self, players):
        self.players = [Player(name) for name in players]
        self.winners_bracket = []
        self.losers_bracket = []

    def play(self):
        # Shuffle players and initialize winners and losers brackets
        random.shuffle(self.players)
        self.winners_bracket = [(self.players[i], self.players[i+1]) for i in range(0, len(self.players)-1, 2)]
        self.losers_bracket = []
        self.matches = []

        # 先把player全放到winners_bracket裡面
        for i in self.winners_bracket:
            print(i[0].name, i[1].name)

        # Play matches in winners bracket
        for player1, player2 in self.winners_bracket:
            match = Match(player1, player2)
            match.play()
            match.winner.score += 1
            self.matches.append(match)
            self.losers_bracket.append(match.loser)
        for j in self.losers_bracket:
            print("Loser: ", j.name)

        # Continue playing matches until there is only one player left in the winners bracket
        while len(self.winners_bracket) > 1:
            # 講第一次比賽的兩個winner放入matches
            # Update winners bracket
            self.winners_bracket = [(self.matches[i].winner, self.matches[i + 1].winner) for i in
                                    range(0, len(self.matches) - 1, 2)]
            for i in self.winners_bracket:
                print(i[0].name, i[1].name)
            self.losers_bracket.extend([self.matches[i].loser for i in range(0, len(self.matches), 2)])

            # Clear match list
            for j in self.losers_bracket:
                print("Loser: ", j.name)

            # Play matches in winners bracket
            for match in self.winners_bracket:
                match.play()
                match.winner.score += 1
                self.losers_bracket.append(match.loser)

        # Play matches in losers bracket
        while len(self.losers_bracket) > 1:
            self.losers_bracket = [(self.losers_bracket[i], self.losers_bracket[i+1]) for i in range(0, len(self.losers_bracket)-1, 2)]
            for match in self.losers_bracket:
                match.play()
                match.winner.score += 1

        # Final match
        final_match = Match(self.winners_bracket[0].winner, self.losers_bracket[0])
        final_match.play()
        final_match.winner.score += 1

        # Return winner
        return max(self.players, key=lambda player: player.score)


# Example usage with 8 players
players = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5', 'Player 6', 'Player 7', 'Player 8']
tournament = DualElimination(players)
winner = tournament.play()
print("Winner:", winner.name)