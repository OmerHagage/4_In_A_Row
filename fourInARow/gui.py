
import tkinter as tk
from fourInARow.game import Game
from fourInARow.ai import AI


PLAY_OPTIONS = ["human vs human", "human vs AI", 'AI vs human', "AI vs AI"]
MOVE_LST = [0, 1, 2, 3, 4, 5, 6]
PLAYERS_COLORS = ["red", "blue"]
WINDOW_SIZE = 4
MIDDLE_COLUMN = 4
MIDDLE_ROW = 3


class Graphic:
    """ this class runs our graphic manager objects"""

    def __init__(self, game):
        self.__game = game
        self.__game_over = False
        self.__canvas_lst = [[] for i in range(7)]
        self.__ai_1 = AI(self.__game, 1)
        self.__ai_2 = AI(self.__game, 2)
        self.__parent = tk.Tk()
        self.__parent.configure(bg="papayawhip")
        label_text = tk.Label(self.__parent, bg="papayawhip", text="CONNECT 4",
                              font=("tahoma", 50, "bold"), fg="blue4")
        label_text.pack(side=tk.TOP)
        self.__play_choice = self.choose_players()
        if self.__game_over == False:
            self.check_play_choice()
        self.__parent.protocol("WM_DELETE_WINDOW", self.exit_game)
        tk.mainloop()

    def choose_players(self):
        """ this function chooses who will play the game, according to given
        input"""
        self.__button_1 = tk.Button(self.__parent, text=PLAY_OPTIONS[0],
                                    width=15, fg="blue4", command=
                                    lambda: self.press(PLAY_OPTIONS[0]))
        self.__button_2 = tk.Button(self.__parent, text=PLAY_OPTIONS[1],
                                    width=15, fg="blue4", command=
                                    lambda: self.press(PLAY_OPTIONS[1]))
        self.__button_3 = tk.Button(self.__parent, text=PLAY_OPTIONS[2],
                                    width=15, fg="blue4", command=
                                    lambda: self.press(PLAY_OPTIONS[2]))
        self.__button_4 = tk.Button(self.__parent, text=PLAY_OPTIONS[3],
                                    width=15, fg="blue4", command=
                                    lambda: self.press(PLAY_OPTIONS[3]))
        self.__button_1.pack(side=tk.TOP)
        self.__button_2.pack(side=tk.TOP)
        self.__button_3.pack(side=tk.TOP)
        self.__button_4.pack(side=tk.TOP)

    def press(self, choice):
        """ this function deals with the players choice of who will play,
        destroying the window in order to start playing"""
        self.__play_choice = choice
        self.__button_1.destroy()
        self.__button_2.destroy()
        self.__button_3.destroy()
        self.__button_4.destroy()
        self.create_board()

    def create_board(self):
        """ this function creates the graphic board"""
        self.__upper_frame = tk.Frame(self.__parent,  bg="black")
        self.__upper_frame.pack(side=tk.TOP)
        self.__lower_frame = tk.Frame(self.__parent)
        self.__lower_frame.pack(side=tk.BOTTOM)
        for i in range(42):
            canvas = tk.Canvas(self.__upper_frame, width=89, height=89,
                               bg='brown')
            canvas.grid(row=i//7, column=i % 7)
            canvas.create_oval(5, 5, 89, 89, fill='white')
            self.__canvas_lst[i % 7].append([canvas, 0])
        for j in range(1, 8):
            button = tk.Button(self.__lower_frame, text=("column", j),
                               width=10, height=2, fg="blue4",
                               command=self.prepare_move(j-1))
            button.grid(row=0, column=j-1)
        self.__parent.after(1000, self.check_play_choice)

    def prepare_move(self, j):
        """ this function prepares a move on the board"""
        def move():
            try:
                if ((self.__play_choice == PLAY_OPTIONS[1] and
                     self.__game.get_current_player() == 1) or
                    (self.__play_choice == PLAY_OPTIONS[2] and
                     self.__game.get_current_player() == 2) or
                    self.__play_choice == PLAY_OPTIONS[0]) and not \
                        self.__game_over:
                    current_player = self.__game.get_current_player()
                    self.__game.make_move(j)
                    for can in self.__canvas_lst[j][::-1]:
                        if can[1] == 0:
                            can[1] = current_player
                            can[0].create_oval(5, 5, 89, 89, fill=
                            PLAYERS_COLORS[current_player-1])
                            break
                    possible_win_location = (self.__canvas_lst[j].index(can),
                                             j)
                    self.check_winning(possible_win_location)
            except Exception as msg:
                error_frame = tk.Frame(self.__parent, bg="black")
                error_frame.pack(side=tk.BOTTOM)
                label_text = tk.Label(error_frame, bg="papayawhip",
                                      text=msg,
                                      font=("tahoma", 50, "bold"), fg="blue4")
                label_text.pack()
                self.__parent.after(1500, error_frame.destroy)
        return move

    def check_play_choice(self):
        """ this function deals with the choice of players, and switches
        between the players"""
        if self.__game.get_winner() is None:
            if self.__play_choice == PLAY_OPTIONS[1]:
                if self.__game.get_current_player() == 2:
                        self.ai_move(self.__ai_2.find_legal_move())
            elif self.__play_choice == PLAY_OPTIONS[2]:
                if self.__game.get_current_player() == 1:
                    self.ai_move(self.__ai_1.find_legal_move())
            elif self.__play_choice == PLAY_OPTIONS[3]:
                if self.__game.get_current_player() == 1:
                    self.ai_move(self.__ai_1.find_legal_move())
                else:
                    self.ai_move(self.__ai_2.find_legal_move())

    def ai_move(self, move):
        """ this function makes a move when it is the computer's turn to play
        """
        current_player = self.__game.get_current_player()
        self.__game.make_move(move)
        for can in self.__canvas_lst[move][::-1]:
            if can[1] == 0:
                can[1] = current_player
                can[0].create_oval(5, 5, 89, 89,
                                   fill=PLAYERS_COLORS[current_player - 1])
                break
        possible_win_location = (self.__canvas_lst[move].index(can), move)
        self.check_winning(possible_win_location)

    def check_winning(self, win_location):
        """ this function checks if there is a win on the board"""
        if self.__game.get_winner() is not None:
            self.winner(self.__game.get_winner(), win_location)
        else:
            self.__parent.after(1000, self.check_play_choice)

    def winner(self, win_type, win_location):
        """ this function deals with a win, showing who won and where"""
        self.__game_over = True
        self.__win_msg = tk.Tk()
        self.__win_msg.protocol("WM_DELETE_WINDOW", self.exit_game_after_play)
        msg = tk.Label(self.__win_msg,width=20,height=5)
        if win_type == 1:
            msg.configure(text="red player won!!", font=("tahoma", 30, "bold"),
                          fg="red")
            self.draw_winning(win_location, win_type)
        elif win_type == 2:
            msg.configure(text="blue player won!!", font=("tahoma", 30, "bold")
                          , fg="blue")
            self.draw_winning(win_location, win_type)
        else:
            msg.configure(text="it is a tie", font=("tahoma", 50, "bold"),
                          fg="black")
        msg.pack(side=tk.TOP)
        new_game = tk.Button(self.__win_msg, text="new game?",
                             font=("tahoma", 13, "bold"), width=20,
                             fg="black", command=self.new_game)
        exit_game = tk.Button(self.__win_msg, text="exit?",
                              font=("tahoma", 13, "bold"), width=20,
                              fg="black", command=self.exit_game_after_play)
        new_game.pack()
        exit_game.pack()

    def row_check(self, win_location, win_type):
        """this function checks if there is a win on a row in the graph"""
        row = [col[win_location[0]] for col in self.__canvas_lst]
        window1 = [row[i:i + WINDOW_SIZE] for i in range(MIDDLE_COLUMN)]
        for win in window1:
            flag = True
            for p in range(WINDOW_SIZE):
                if win[p][1] != win_type:
                    flag = False
            if flag:
                for p in range(WINDOW_SIZE):
                    win[p][0].create_oval(5, 5, 89, 89,
                                          fill=PLAYERS_COLORS[win_type - 1],
                                          outline="pink", width=7)
                return True
        return False

    def col_check(self, win_location, win_type):
        """this function checks is there is a win on the column in the graph"""
        col = self.__canvas_lst[win_location[1]]
        window2 = [col[i:i + WINDOW_SIZE] for i in range(MIDDLE_ROW)]
        for win in window2:
            flag = True
            for p in range(WINDOW_SIZE):
                if win[p][1] != win_type:
                    flag = False
            if flag:
                for p in range(WINDOW_SIZE):
                    win[p][0].create_oval(5, 5, 89, 89,
                                          fill=PLAYERS_COLORS[win_type - 1],
                                          outline="pink", width=7)
                return True
        return False

    def diagonal_right_check(self, win_type):
        """this function checks if there is a win on a daigonal in the graph"""
        for i in range(len(self.__canvas_lst)):
            for j in range(len(self.__canvas_lst[0])):
                if j >= 3 and i <=3 and self.__canvas_lst[i][j][1] == win_type:
                    flag = True
                    for z in range(1, 4):
                        if win_type != self.__canvas_lst[i+z][j-z][1]:
                            flag = False
                    if flag:
                        for p in range(4):
                            self.__canvas_lst[i+p][j-p][0].\
                                create_oval(5, 5, 89, 89,
                                            fill=PLAYERS_COLORS[win_type - 1],
                                            outline="pink", width=7)
                        return True
        return False

    def diagonal_left_check(self, win_type):
        """this function checks if there is a win on a diagonal in the graph"""
        for i in range(len(self.__canvas_lst)):
            for j in range(len(self.__canvas_lst[0])):
                if j >= 3 and i >= 3 and self.__canvas_lst[i][j][1] == \
                        win_type:
                    flag1 = True
                    for z in range(1, 4):
                        if win_type != self.__canvas_lst[i-z][j-z][1]:
                            flag1 = False
                    if flag1:
                        for p in range(4):
                            self.__canvas_lst[i-p][j-p][0].\
                                create_oval(5, 5, 89, 89,
                                            fill=PLAYERS_COLORS[win_type - 1],
                                            outline="pink", width=7)

    def draw_winning(self, win_location, win_type):
        """ this function draws on the graph the winning disks"""
        if not self.row_check(win_location, win_type):
            if not self.col_check(win_location, win_type):
                if not self.diagonal_right_check(win_type):
                    self.diagonal_left_check(win_type)

    def new_game(self):
        """ this function creates a new game"""
        self.__win_msg.destroy()
        self.__game_over = False
        self.__game = Game()
        self.__canvas_lst = [[] for i in range(7)]
        self.__ai_1 = AI(self.__game, 1)
        self.__ai_2 = AI(self.__game, 2)
        self.__upper_frame.destroy()
        self.__lower_frame.destroy()
        self.choose_players()

    def exit_game_after_play(self):
        """ this function creates a game after the play"""
        self.__win_msg.destroy()
        self.__parent.destroy()

    def exit_game(self):
        """this function exits the game"""
        self.__parent.destroy()
