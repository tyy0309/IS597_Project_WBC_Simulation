import random


class Player:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.winner = None

    def simulate_match(self):
        # TODO: update winner formula
        self.winner = random.choice([self.player1, self.player2])
        print(self.player1, self.player2, " Winner: ", self.winner)


class Tournament:
    def __init__(self, players):
        self.players = players
        self.matches = []
        self.winners_bracket = []
        self.losers_bracket = []

    def simulate_first_round(self):
        random.shuffle(self.players)
        print("FIRST ROUND BEGINS")
        for i in range(0, len(self.players), 2):
            match = Match(self.players[i], self.players[i + 1])
            match.simulate_match()
            self.matches.append(match)

            if match.winner == match.player1:
                self.winners_bracket.append(match.player1)
                self.losers_bracket.append(match.player2)
            else:
                self.winners_bracket.append(match.player2)
                self.losers_bracket.append(match.player1)

    def simulate_winners_bracket(self):
        print("WINNERS BRACKET BEGINS")
        while len(self.winners_bracket) > 1:
            match = Match(self.winners_bracket.pop(0), self.winners_bracket.pop(0))
            match.simulate_match()
            self.matches.append(match)

            if match.winner == match.player1:
                self.winners_bracket.append(match.player1)
                self.losers_bracket.append(match.player2)
            else:
                self.winners_bracket.append(match.player2)
                self.losers_bracket.append(match.player1)

    def simulate_losers_bracket(self):
        """
        There are two types of matches:
            1. Losers vs Losers
            2. Losers vs Losers from Winner Brackets
        For this to work flexible, find an algorithm the following parameters:
            1. number of matches
            2. type1 match number
            3. type2 matches number
        Example:
            If there are 8 players:
                num_matches = 6
                type1_match = [2,5]
                type2_match = [4]
        """
        num_matches = 6
        type1_match = [2, 5]
        type2_match = [4]
        count = 0
        loser_tmp = []
        print("LOSERS BRACKET BEGINS")
        while count < num_matches:
            match = Match(self.losers_bracket.pop(0), self.losers_bracket.pop(0))
            match.simulate_match()
            self.matches.append(match)
            loser_tmp.append(match.winner)
            count += 1
            if count in type1_match:
                while loser_tmp:
                    self.losers_bracket.insert(1, loser_tmp.pop(0))
            if count in type2_match:
                while loser_tmp:
                    self.losers_bracket.insert(0, loser_tmp.pop(0))
        self.losers_bracket = loser_tmp

    def simulate_championship(self):
        print("FINALS")
        championship_match = Match(self.winners_bracket.pop(), self.losers_bracket.pop())
        championship_match.simulate_match()
        self.matches.append(championship_match)
        self.champion = championship_match.winner

    def run_tournament(self):
        self.simulate_first_round()
        self.simulate_winners_bracket()
        self.simulate_losers_bracket()
        self.simulate_championship()

        print(f"The winner of the tournament is {self.champion.name}")


# Create four players
players = [Player('AUS'), Player('CUB'), Player('ITA'), Player('JPN'), Player('MEX'),
           Player('PUR'), Player('USA'), Player('VEN')]

# Create the tournament object
tournament = Tournament(players)

# Run the tournament
tournament.run_tournament()