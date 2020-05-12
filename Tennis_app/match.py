class Match:

    points = [0, 15, 30, 40]
    games = [0, 1, 2, 3, 4, 5, 6, 7]
    sets = [0, 1, 2]

    def __init__(self, player1, player2):

        self.player1 = player1
        self.player2 = player2
        print(player1.get_name())

    def points_win(self, winner, opponent):
        if winner.games_amount == 6 and opponent.games_amount == 6:
            winner.points_amount += 1
            if winner.points_amount < 7 or abs(winner.points_amount - opponent.points_amount) < 2:
                pass
            else:
                winner.points_amount = 0
                opponent.points_amount = 0
                winner.games_amount = 0
                opponent.games_amount = 0
                self.sets_win(winner)
        elif winner.points_amount == 40 and opponent.points_amount != 40 and opponent.points_amount != 'AD' \
                or winner.points_amount == 'AD':
            winner.points_amount = 0
            opponent.points_amount = 0
            return self.games_win(winner, opponent)

        else:

            if opponent.points_amount == 40 and winner.points_amount == 40:
                winner.points_amount = 'AD'
            elif opponent.points_amount == 'AD' and winner.points_amount == 40:
                opponent.points_amount = 40
            else:
                index = Match.points.index(winner.points_amount)
                winner.points_amount = Match.points[index + 1]
                print('{} a {}pts'.format(winner.get_name(), winner.get_points_amount()))

    def games_win(self, winner, opponent):

        if winner.games_amount == 5 and opponent.games_amount < 5:
            winner.games_amount = 0
            opponent.games_amount = 0
            return self.sets_win(winner)

        elif winner.games_amount == 5 and opponent.games_amount == 6:
            winner.games_amount = 6
            return self.tie_break(winner, opponent)
        elif winner.games_amount == 6 and opponent.games_amount == 5:
            winner.games_amount = 0
            opponent.games_amount = 0
            return self.sets_win(winner)
        else:
            index = Match.games.index(winner.games_amount)
            winner.games_amount = Match.games[index + 1]

    def sets_win(self, winner):
        index = Match.sets.index(winner.sets_amount)
        winner.sets_amount = Match.sets[index + 1]
        if winner.sets_amount == 2:
            print('Fin du match')

    def tie_break(self, winner, opponent):
        winner.points_amount = 0
        opponent.points_amount = 0