"""
DataScreen

This module contains the DataScreen class and all the classes which are related to it.
This screen contains and shows all the statistics of a tennis match.
"""


from kivy.properties import StringProperty

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.behaviors import RectangularElevationBehavior


def safe_div(num1, num2):
    """Returns an integer division.
    Avoids error if division by zero."""
    if num2 <= 0:
        return 0
    return int(num1 / num2)


def number_comparison(col1, col3, highlight='max'):
    """Highlights the right statistic depending on number values"""
    result = None, None
    if highlight == 'ratio':  # Highlights the greatest number ratio
        ratio1 = col1.ids.label.text
        div_numbers1 = list(map(int, ratio1.split('/')))
        quotient1 = safe_div(div_numbers1[0], div_numbers1[1])
        ratio2 = col3.ids.label.text
        div_numbers2 = list(map(int, ratio2.split('/')))
        quotient2 = safe_div(div_numbers2[0], div_numbers2[1])
        if quotient1 > quotient2:
            result = col1, col3
        elif quotient2 > quotient1:
            result = col3, col1
    elif highlight in ('max', 'min'):
        final_num1 = int(col1.ids.label.text.split(' ')[0])
        final_num2 = int(col3.ids.label.text.split(' ')[0])
        if highlight == 'max':  # Highlights the greatest number
            if final_num1 > final_num2:
                result = col1, col3
            elif final_num2 > final_num1:
                result = col3, col1
        else:  # Highlights the lowest number
            if final_num1 > final_num2:
                result = col3, col1
            elif final_num2 > final_num1:
                result = col1, col3
    return result


class Rows(MDBoxLayout):
    """Rows of a table (MDGridLayout)"""
    highlight = StringProperty('max')
    """
    The name of the highlighting system.

    :attr:`highlight` is a :class:`~kivy.properties.StringProperty`
    and defaults to `'max'`.
    """


class DataLine(MDBoxLayout, RectangularElevationBehavior):
    """Line that contains the result of a match"""


class LeaderBoard(MDGridLayout):
    """Table which contains DataLines"""


class DataScreen(MDScreen):
    """Shows the data of a match"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()

    def show_scoreboard(self, data):
        """Shows a scoreboard with the result of the tennis match"""
        players = [self.ids.player1, self.ids.player2]
        stats = [data['player1_stats'], data['player2_stats']]
        for player, name, stat in zip(players, [data['player1_name'], data['player2_name']], stats):
            player.ids.player_name.text = name
            player.ids.set1.ids.label.text = str(stat['total_games'][0])
            player.ids.set2.ids.label.text = str(stat['total_games'][1])
            player.ids.set3.ids.label.text = str(stat['total_games'][2])
            self.change_square_design(name, player, data)

    def change_square_design(self, player_name, line_score, data):
        """Changes the square design if a player wins a set"""
        squares = [line_score.ids.set1, line_score.ids.set2, line_score.ids.set3]
        for (index, square) in zip(range(3), squares):
            if player_name == data['sets_winners'][index]:
                square.md_bg_color = (0.91, 0.46, 0.07, 1)
                square.ids.label.text_color = (1, 1, 1, 1)
                square.elevation = 5
            else:
                square.md_bg_color = (self.app.get_rgba_from_hex('#f1f1f1'))
                square.ids.label.text_color = (0, 0, 0, 1)
                square.elevation = 0

    def show_stats(self, data):
        """Shows all statistics of a tennis match"""
        caption = ['VS', 'Aces', 'Double Faults', '1st Serve in (%)', '1st Serve Pts Won (%)',
                   '2nd Serve Pts Won (%)', 'Break points converted', 'Winners', 'Net points',
                   'Return points won', 'Unforced Errors', 'Points won']

        highlights = ['name', 'max', 'min', 'max', 'max', 'max', 'ratio', 'max', 'max', 'ratio', 'min', 'max']
        # highlight property of each row
        players = ['player1', 'player2']
        leaderboard = [self.ids.set1_stats, self.ids.set2_stats, self.ids.set3_stats]

        for manche in range(3):
            for row, i in zip(leaderboard[manche].ids.values(), range(len(caption))):
                row.ids.col2.text = caption[i]  # Writes all the captions
                row.highlight = highlights[i]
            for player in players:
                name = data[str(player + '_name')]
                full_stats = data[str(player + '_stats')]
                serving_stats = full_stats['service_stats']
                double_faults = serving_stats['double_faults'][manche]
                aces = serving_stats['ace'][manche]
                service_pts_played = serving_stats['service_points_played'][manche]
                nbr_first_service_in = service_pts_played - serving_stats['second_service'][manche]
                ratio_first_service_in = safe_div(nbr_first_service_in * 100,
                                                  service_pts_played)
                ratio_first_service_won = safe_div(
                    serving_stats['first_service_won'][manche] * 100, nbr_first_service_in)
                ratio_second_service_won = safe_div(
                    serving_stats['second_service_won'][manche] * 100,
                    serving_stats['second_service_in'][manche])
                break_points = full_stats['break_points'][manche]
                #  break_points_conv = safe_div(
                #  full_stats['return_game_won'][manche] * 100, break_points)
                break_points_ratio = '{}/{}'.format(
                    full_stats['return_game_won'][manche], break_points)

                return_ratio = '{}/{}'.format(full_stats['return_points_won'][manche],
                                              full_stats['return_points_played'][manche])
                stats = [name, aces, double_faults, ratio_first_service_in, ratio_first_service_won,
                         ratio_second_service_won, break_points_ratio, full_stats['winners'][manche],
                         full_stats['net_points'][manche], return_ratio,
                         full_stats['unforced_errors'][manche], full_stats['total_points'][manche]]

                stats = list(map(str, stats))
                for row, j in zip(leaderboard[manche].ids.values(), range(len(caption))):
                    cols = []
                    for col in row.ids.values():
                        cols.append(col)
                    cols.pop(1)
                    cols[players.index(player)].ids.label.text = stats[j]
                    if stats[j] == name:
                        cols[players.index(player)].size_hint = 1, 1
                        cols[players.index(player)].md_bg_color = (1, 1, 1, 1)

    def check_stat_winner(self):
        """Highlights the best statistic between both players"""

        sets = [self.ids.set1_stats, self.ids.set2_stats, self.ids.set3_stats]
        for manche in sets:
            for row in manche.ids.values():
                cols = [row.ids.col1, row.ids.col3]
                winner_col, looser_col = number_comparison(cols[0], cols[1], row.highlight)
                if winner_col is not None and looser_col is not None:
                    winner_col.md_bg_color = (0.91, 0.46, 0.07, 1)
                    winner_col.ids.label.text_color = (1, 1, 1, 1)
                    winner_col.elevation = 5
                    self.reset_square_design(looser_col)
                else:
                    self.reset_square_design(cols[0])
                    self.reset_square_design(cols[1])

                if row.highlight == 'name':
                    cols[0].size_hint_x = 1
                    cols[0].md_bg_color = (1, 1, 1, 1)
                    cols[1].size_hint_x = 1
                    cols[1].md_bg_color = (1, 1, 1, 1)

    def reset_square_design(self, square):
        """Resets the design of the Square"""
        square.md_bg_color = (self.app.get_rgba_from_hex('#f1f1f1'))
        square.ids.label.text_color = (0, 0, 0, 1)
        square.elevation = 0
