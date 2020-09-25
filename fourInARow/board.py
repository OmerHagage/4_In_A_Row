
MIDDLE_NUMBER = 3
#middle number for standard connect 4 board

class Board:
    """ this class runs board objects"""

    def __init__(self, length, width):
        self.__length = length
        self.__width = width
        self.__points_lst = []
        self.__legal_additions = self.legal_additions()

    def legal_additions(self):
        """ this function returns a list of legal placements of a disk"""
        legal = []
        for i in range(self.__length):
            legal.append([5, i])
        return legal

    def board_locations(self):
        """this function returns a list of the possible board locations"""
        locations = []
        for row in range(self.__width):
            for col in range(self.__length):
                locations.append((row, col))
        return locations

    def add_point(self, column, player_name):
        """this function adds a point on the board according to player's choice
        """
        for co in range(len(self.__legal_additions)):
            if self.__legal_additions[co][1] == column and\
                    self.__legal_additions[co][0] >= 0:
                self.__points_lst.append(Point(self.__legal_additions[co][0],
                                               column, player_name))
                self.__legal_additions[co][0] -= 1
                return True
        raise Exception("Illegal move")

    def check_data_at_point(self, row, col):
        """ this function checks the data at a given point on the board"""
        if row in range(self.__width) and col in range(self.__length):
            for point in self.__points_lst:
                if point.get_location() == (row, col):
                    return point.get_data()
            return None
        else:
            raise Exception("Illegal location")

    def check_win_up(self, location):
        """ this function checks if there is a win on the vertical positions
        on the board"""
        point_data = self.check_data_at_point(location[0], location[1])
        if point_data:
            for i in range(1, 4):
                if point_data != self.check_data_at_point(location[0] - i,
                                                          location[1]):
                    return False
            return True
        return False

    def check_win_right(self, location):
        """this function checks if there is a win on the horizontal positions
        """
        point_data = self.check_data_at_point(location[0], location[1])
        if point_data:
            for i in range(1, 4):
                if point_data != self.check_data_at_point(location[0],
                                                          location[1] + i):
                    return False
            return True
        return False

    def check_diagonal_right(self, location):
        """ this function checks if there is a diagonal win"""
        point_data = self.check_data_at_point(location[0], location[1])
        if point_data:
            for i in range(1, 4):
                if point_data != self.check_data_at_point(location[0] - i,
                                                          location[1] + i):
                    return False
            return True
        return False

    def check_diagonal_left(self, location):
        """ this function checks if there is a diagonal win"""
        point_data = self.check_data_at_point(location[0], location[1])
        if point_data:
            for i in range(1, 4):
                if point_data != self.check_data_at_point(location[0] - i,
                                                          location[1] - i):
                    return False
            return True
        return False

    def is_full(self):
        """ this function checks if the board is full"""
        flag = True
        for point in self.__legal_additions:
            if point[0] >= 0:
                flag = False
                break
        return flag

    def check_win(self):
        """ this function checks if there is a win or tie"""
        for location in self.board_locations()[::-1]:
            if location[0] >= MIDDLE_NUMBER:
                if self.check_win_up(location):
                    return self.check_data_at_point(location[0], location[1])
            if location[1] <= MIDDLE_NUMBER:
                if self.check_win_right(location):
                    return self.check_data_at_point(location[0], location[1])
            if location[0] >= MIDDLE_NUMBER and location[1] <= MIDDLE_NUMBER:
                if self.check_diagonal_right(location):
                    return self.check_data_at_point(location[0], location[1])
            if location[0] >= MIDDLE_NUMBER and location[1] >= MIDDLE_NUMBER:
                if self.check_diagonal_left(location):
                    return self.check_data_at_point(location[0], location[1])
        if self.is_full():
            return 0

class Point:
    """ this function runs the point objects, representing a point on the
    board"""

    def __init__(self, line, column, player_name):
        self.__data = player_name
        self.__line = line
        self.__column = column

    def get_location(self):
        """  this function returns the location of the point on the board"""
        return self.__line, self.__column

    def get_data(self):
        """ this function returns which player is holding the point"""
        return self.__data


