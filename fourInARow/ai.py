
from copy import deepcopy
import random
import math

COLUMN_NUMBER = 7
ROW_NUMBER = 6
WINDOW_SIZE = 4
CENTER = 3


class AI:
    """ this class runs our AI object"""

    def __init__(self, game, player):
        self.__game = game
        self.__player = player


    def find_legal_move(self, timeout=None):
        """ this function finds the best move the AI can do"""
        if self.__game.get_winner() is None:
            legal_col = self.find_legal_column()
            best_score_col = -math.inf
            self.__best_move = random.choice(legal_col)
            for col in legal_col:
                temp_game = deepcopy(self.__game)
                temp_game.make_move(col)
                board_score = self.get_score(temp_game, self.__player)
                if board_score > best_score_col:
                    best_score_col, self.__best_move = board_score, col
            return self.__best_move
        else:
            raise Exception("No possible AI moves.")

    def get_last_found_move(self):
        """this function returns the last move the ai checked"""
        return self.__best_move

    def center_score(self, board_lst, player, score):
        """this function checks the score for disks in the central column"""
        center = [i[CENTER] for i in board_lst]
        appearance = center.count(player)
        score += appearance * 4
        return score

    def rows_score(self, board_lst, player, score):
        """ this function checks the score for the rows"""
        for row_n in range(ROW_NUMBER):
            row = [i for i in board_lst[row_n]]
            for col_n in range(COLUMN_NUMBER - 3):
                window = row[col_n:col_n + WINDOW_SIZE]
                score += self.window_score(window, player)
        return score

    def column_score(self, board_lst, player, score):
        """ this function checks the score for the columns"""
        for col_n in range(COLUMN_NUMBER):
            temp = [j[col_n] for j in board_lst]
            col = [i for i in temp]
            for row_n in range(ROW_NUMBER - 3):
                window = col[row_n: row_n + WINDOW_SIZE]
                score += self.window_score(window, player)
        return score

    def diagonal_right_score(self, board_lst, player, score):
        """this function checks the score for the diagonals"""
        for row_n in range(ROW_NUMBER - 3):
            for col_n in range(COLUMN_NUMBER - 3):
                window = \
            [board_lst[row_n + i][col_n + i] for i in range(WINDOW_SIZE)]
                score += self.window_score(window, player)
        return score

    def diagonal_left_score(self, board_lst, player, score):
        """this function checks the score for the diagonals"""
        for row_n in range(ROW_NUMBER - 3):
            for col_n in range(COLUMN_NUMBER - 3):
                window = \
                    [board_lst[row_n + 3 - i][col_n + i] for i in range(4)]
                score += self.window_score(window, player)
        return score

    def get_score(self, game, player):
        """ this function checks the score for a given player"""
        board_lst = self.get_board_lst(game)
        score = 0
        score += self.center_score(board_lst, player, score)
        score += self.rows_score(board_lst, player, score)
        score += self.column_score(board_lst, player, score)
        score += self.diagonal_right_score(board_lst, player, score)
        score += self.diagonal_left_score(board_lst, player, score)
        return score

    def window_score(self, window, player):
        """this function checks the score for given quartet of points in the
        game"""
        score = 0
        second_player = 2 if player == 1 else 1
        if window.count(player) == 4:
            score += 10000
        elif window.count(player) == 3 and window.count(None) == 1:
            score += 10
        elif window.count(player) == 2 and window.count(None) == 2:
            score += 5
        if window.count(second_player) == 3 and window.count(None) == 1:
            score -= 1000
        elif window.count(second_player) == 2 and window.count(None) == 2:
            score -= 40
        return score

    def get_board_lst(self, game):
        """this function returns the board as a list"""
        board_lst = []
        for i in range(ROW_NUMBER - 1, -1, -1):
            row = []
            for j in range(COLUMN_NUMBER):
                row.append(game.get_player_at(i, j))
            board_lst.append(row)
        return board_lst

    def find_legal_column(self):
        """ this function finds all columns where it is possible to make a
        legal move"""
        legal_col = []
        for col in range(COLUMN_NUMBER):
            temp = self.__game.get_player_at(0, col)
            if temp is None:
                legal_col.append(col)
        return legal_col



