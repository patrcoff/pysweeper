import random

class Cell:
    def __init__(self,ordinate) -> None:
        self.ordinate = ordinate
        self.is_bomb = False
        self.clicked = False
        self.neighbours = -1
    
    def set_bomb(self):
        self.is_bomb = True

    def explode(self, game):
        print("boom!")
        game.quit()

    def to_coordinate(self,x,y):
        y1 = self.ordinate // y
        x1 = self.ordinate % x
        return x1, y1

    def count_neighbours(self,board):
        #x,y = self.to_coordinate(self.ordinate,board.board_x,board.board_y)
        neighbours = []
        #print(self.ordinate, self.to_coordinate(board.board_x,board.board_y))
        funcs = [

                    lambda x: x - (board.board_x + 1),
                    lambda x: x - board.board_x,
                    lambda x: x - (board.board_x - 1),
                    lambda x: x - 1,
                    lambda x: x + 1,
                    lambda x: x + (board.board_x - 1),
                    lambda x: x + board.board_x,
                    lambda x: x + (board.board_x + 1)
                ]
        for func in funcs:
            # sides
            # - 1
            # + 1
            
            #above
            # -(x + 1)
            # - x
            # - (x -1)

            #below
            # + (x - 1)
            # + x
            # + (x + 1)
            ord = func(self.ordinate)
            if 0 <= ord < board.get_board_size() and not self.opposite_side(self.ordinate,ord,board):
                neighbours.append(ord)
        print(self.ordinate, " - ", self.to_coordinate(board.board_x,board.board_y), " - ", neighbours)
    
    def opposite_side(self,o1,o2,board):
        left_side = [y * board.board_x for y in range(0,board.board_y)]
        right_side = [y * board.board_x + board.board_x - 1 for y in range(0,board.board_y)]
        if (o1 in left_side and o2 in right_side) or (o1 in right_side and o2 in left_side):
            return True
        return False

class Minefield:
    def __init__(self,board_size = (10,10),difficulty = "medium") -> None:
        self.reset(size = board_size,diff = difficulty)

    def set_board_size(self,x,y):
        self.board_size  = (x,y)
        self.board_x = self.board_size[0]
        self.board_y = self.board_size[1]

    def get_board_size(self):
        return self.board_x * self.board_y

    def calculate_bombs(self,difficulty):
        if difficulty.lower() == "easy":
            self.no_of_bombs = int(0.1 * self.board_x * self.board_y) # 10% of board
        elif difficulty.lower() == "medium":
            self.no_of_bombs = int(0.15 * self.board_x * self.board_y) # 15% of board
        elif difficulty.lower() == "hard":
            self.no_of_bombs = int(0.2 * self.board_x * self.board_y) # 20% of board
    
    def populate_bombs(self):
        #print(self.board)
        for x in range(self.no_of_bombs):
            self.place_bomb()
    
    def place_bomb(self):  # CAREFUL - if this is called and all available cells are already bombs, it will loop forever, though this should never be the case in practice
        while True:
            x = random.randint(0,self.board_x-1)
            y = random.randint(0,self.board_y-1)
            print(x,y)
            if not self.board[y][x].is_bomb:
                self.board[y][x].set_bomb()
                break

    def count_neighbours(self):
        for row in self.board:
            for cell in row:
                cell.count_neighbours(self)

    def reset(self,size,diff):
        self.set_board_size(size[0],size[1])
        self.calculate_bombs(diff)
        self.board = [ [ Cell(ordinate=(x + (size[0] * y))) for x in range(0,size[0]) ] for y in range(0,size[1]) ]
        self.populate_bombs()
        self.count_neighbours()

















#--------------------------------------------
test = Minefield(board_size=(13,11))

for row in test.board:
    print([cell.ordinate for cell in row])