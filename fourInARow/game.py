
from fourInARow.board import Board


PLAYER_ONE = 1
PLAYER_TWO = 2
DEFAULT_LENGTH = 7
DEFAULT_WIDTH = 6


class Game:
    """ this class runs the objects of the game"""

    def __init__(self):
        self.__current_player = 1
        self.__board = Board(DEFAULT_LENGTH, DEFAULT_WIDTH)
        self.__game_over = False

    def make_move(self, column):
        """this function makes a move"""
        if not self.__game_over:
            try:
                self.__board.add_point(column, self.get_current_player())
            except Exception as msg:
                raise Exception(msg)
            else:
                if self.get_winner() in [1, 2, 0]:
                    self.__game_over = True
                self.change_player()
        else:
            raise Exception("Illegal move")

    def get_winner(self):
        """ this function checks if there is a winner in the game"""
        return self.__board.check_win()

    def get_player_at(self, row, col):
        """this function checks which player is occupying the given space"""
        try:
            player = self.__board.check_data_at_point(row, col)
        except Exception as msg:
            print(msg)
        else:
            return player

    def get_current_player(self):
        """ this func checks who the current player is"""
        return self.__current_player

    def change_player(self):
        """this function changes turns between the players"""
        if self.__current_player == PLAYER_ONE:
            self.__current_player = PLAYER_TWO
        else:
            self.__current_player = PLAYER_ONE






