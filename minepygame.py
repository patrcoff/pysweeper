import pygame

from pygame.locals import (
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)
# Initialize pygame
import random
DEBUG = False

def print_if(str):
    if DEBUG:
        print(str)

class Cell(pygame.sprite.Sprite):
    '''
    An individual cell in the minefield. Inherits from Sprite class to handle rendering to screen.

    Each cell can be thought of as a tile in the minesweeper board, and can be set, or armed as a bomb.
    Methods are available to allow for calculating neighbouring bombs and revealing the cell/tile when clicked.
    If a cell is clicked which has 0 bomb neighbours, it will recursively reveal all neighbouring cells up to
    a perimeter of non-zero cells. Othwerise it reveals the number of neighbouring cells containing bombs.
    If it is a bomb, the bomb animation plays - at time of writing, the bombs do not cause an end-game event.

    The Cell and Minefield classes are heavily intertwined and one does not really ever exist without the other
    As such, you will see in the doctests contained within these docstrings that I am instantiating a Minefield
    instance in order to access the Cell instances so that they have access to their parent object 
    (not in the inheritence meaning of the term) - which is generally required in most method calls.
    In practice, instantiating the Minefield class instantiates all required Cell objects needed.
    Cell objects have a required argument of parent so it is not possible to instantiate a Cell without a Minefield
    '''
    
    def __init__(self,ordinate,parent,square_size) -> None:
        super(Cell, self).__init__()
        self.surf = self.surf = pygame.image.load("img/earth.png").convert()
        self.rect = self.surf.get_rect()
        self.square_size = square_size
        self.ordinate = ordinate
        self.parent = parent
        self.is_bomb = False
        self.clicked = False
        self.flagged = False
        self.neighbours = -1
        self.exploded = False
        self.explode_frame_count = 0
    
    def set_bomb(self):
        '''
        Sets the cell is_bomb boolean to True

        Example
        -------
        >>> from minepygame import Cell, Minefield
        >>> screen = pygame.display.set_mode((20, 20))
        >>> parent = Minefield() # default size is 10x10 cells
        >>> cell = Cell(1000,parent,20)
        >>> cell.is_bomb
        False
        >>> cell.set_bomb()
        >>> cell.is_bomb
        True
        
        '''
        self.is_bomb = True

    def explode(self,screen):
        print_if("boom!")
        self.exploded = True
        self.exploded_images = ["img/bomb1.png","img/bomb2.png","img/bomb3.png","img/bomb4.png"]
        self.surf = pygame.image.load(self.exploded_images[self.explode_frame_count]).convert()
        self.explode_frame_count += 1        
        self.rect = self.surf.get_rect()
        self.render(screen)
        #game.quit()

    def to_coordinate(self,ord):
        '''Returns the coordinate values for a given ordinate value relative to the x and y max values specified in the parent object
        
        Example
        -------
        >>> from minepygame import Cell, Minefield
        >>> screen = pygame.display.set_mode((20, 20))
        >>> parent = Minefield() # default size is 10x10 cells
        >>> cell1 = parent.board[0][0]
        >>> cell1.ordinate
        0
        >>> cell1.to_coordinate(cell1.ordinate)
        (0, 0)
        
        '''
        y1 = ord // self.parent.board_y
        x1 = ord % self.parent.board_x
        return x1, y1

    def get_neighbours(self):
        '''
        Populates a list of neighbours to the calling cell
        
        Example
        -------
        >>> from minepygame import Cell, Minefield
        >>> screen = pygame.display.set_mode((20, 20))
        >>> parent = Minefield() # default size is 10x10 cells
        >>> cell1 = parent.board[0][0]
        >>> cell1.ordinate
        0
        >>> cell1.get_neighbours()
        [1, 10, 11]
        '''
        self.neighbours = []
        funcs = [
                    lambda x: x - (self.parent.board_x + 1),
                    lambda x: x - self.parent.board_x,
                    lambda x: x - (self.parent.board_x - 1),
                    lambda x: x - 1,
                    lambda x: x + 1,
                    lambda x: x + (self.parent.board_x - 1),
                    lambda x: x + self.parent.board_x,
                    lambda x: x + (self.parent.board_x + 1)
                ]
        for func in funcs:
            # sides
            # - 1
            # + 1
            
            # above
            # -(x + 1)
            # - x
            # - (x -1)

            # below
            # + (x - 1)
            # + x
            # + (x + 1)
            ord = func(self.ordinate)
            if 0 <= ord < self.parent.get_board_area() and not self.opposite_side(self.ordinate,ord):
                self.neighbours.append(ord)
        print_if(f'{self.ordinate} - {self.to_coordinate(ord)} - {self.neighbours}')
        return self.neighbours
    
    def opposite_side(self,o1,o2):
        '''
        Takes two ordinate cell references (int) and checks if they are on opposite sides of the board.

        This is necessary in order to exclude cells which are one ordinate away from the cell checking its neighbours
        but actually exist on the other side of the board and are thus not neighbours. This is due to the layout of cells:

        0   1  2  3  4
        5   6  7  8  9
        10 11 12 13 14 - where 5 is not a neighbour to 4 for example.
        
        Example
        -------
        >>> from minepygame import Cell, Minefield
        >>> screen = pygame.display.set_mode((20, 20))
        >>> parent = Minefield() # default size is 10x10 cells
        >>> cell1 = parent.board[0][0]
        >>> cell1.ordinate
        0
        >>> cell2 = parent.board[9][9]
        >>> cell2.ordinate
        99
        >>> cell1.opposite_side(cell1.ordinate,cell2.ordinate)
        True
        '''
                
        left_side = [y * self.parent.board_x for y in range(0,self.parent.board_y)]
        right_side = [y * self.parent.board_x + self.parent.board_x - 1 for y in range(0,self.parent.board_y)]
        if (o1 in left_side and o2 in right_side) or (o1 in right_side and o2 in left_side):
            return True
        return False

    def count_neighbours(self):
        '''
        Counts the number of neighbouring cells which contain bombs
        
        Example
        -------
        >>> from minepygame import Cell, Minefield
        >>> screen = pygame.display.set_mode((20, 20))
        >>> parent = Minefield() # default size is 10x10 cells
        >>> cell = parent.board[1][1]
        >>> 0 <= cell.count_neighbours() <= 8
        True
        '''
        neighbours_count = 0
        for cell_ref in self.neighbours:
            print_if(f'cell_ref: {cell_ref}')
            x, y = self.to_coordinate(cell_ref)
            cell = self.parent.board[y][x]
            neighbours_count += int(cell.is_bomb)
        return neighbours_count

    def recursive_unhide_neighbours(self,screen):
        for cell_ref in self.neighbours:
            x, y = self.to_coordinate(cell_ref)
            cell = self.parent.board[y][x]
            if not cell.clicked:
                cell.unhide((True,False,False),screen)
        return

    def unhide(self,mouse_btn,screen):
        self.clicked = True
        print_if(f'{self.ordinate} - btn - {mouse_btn}')
        if self.is_bomb and mouse_btn[0]: #leftclick
            self.explode(screen)
        if (not self.is_bomb) and mouse_btn[0]:
            print_if('entered clicked')
            
            neighbours_count = self.count_neighbours()
            match neighbours_count:
                case 0:
                    self.surf = pygame.image.load("img/zero.png").convert()
                    self.recursive_unhide_neighbours(screen)
                case 1:
                    self.surf = pygame.image.load("img/one.png").convert()
                case 2:
                    self.surf = pygame.image.load("img/two.png").convert()
                case 3:
                    self.surf = pygame.image.load("img/three.png").convert()
                case 4:
                    self.surf = pygame.image.load("img/four.png").convert()
                case 5:
                    self.surf = pygame.image.load("img/five.png").convert()
                case 6:
                    self.surf = pygame.image.load("img/six.png").convert()            

        if mouse_btn[2]:
            self.toggle_flag()

        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.render(screen)

    def toggle_flag(self):
        '''
        Toggles the cell image between default unclicked background and the flag image.

        Example
        -------
        >>> from minepygame import Cell, Minefield
        >>> screen = pygame.display.set_mode((20, 20))
        >>> parent = Minefield()
        >>> cell = Cell(5,parent,20)
        >>> cell.flagged = True
        >>> cell.toggle_flag()
        >>> cell.flagged
        False
        '''
        if self.flagged:
            self.flagged = False
            self.clicked = False
            self.surf = pygame.image.load("img/earth.png").convert()
        else:
            self.flagged = True
            self.surf = pygame.image.load("img/flag.png").convert()
        
    def render(self, screen):
        x , y = self.to_coordinate(self.ordinate) 
        screen.blit(self.surf, self.parent.scale(x, y, self.square_size))


class Minefield:
    '''The main game map or \'minefield\' class, handles setting up the board, generating the cells and randomly placing bombs in a certain proportion of cells.'''

    def __init__(self,board_size = (10,10),difficulty = "medium", square_size = 20) -> None:  # here we should take cell size in from outside and calculate square_size (for displaying the cell itself) from it
        self.difficulty = difficulty
        self.square_size = square_size
        x, y = board_size
        self.set_board_size(x, y)
        self.reset()

    def set_board_size(self,x,y):
        self.board_size  = (x,y)
        self.board_x, self.board_y = self.board_size
        

    def get_board_area(self):
        return self.board_x * self.board_y

    def calculate_bombs(self,difficulty):
        if difficulty.lower() == "easy":
            self.no_of_bombs = int(0.1 * self.board_x * self.board_y) # 10% of board
        elif difficulty.lower() == "medium":
            self.no_of_bombs = int(0.15 * self.board_x * self.board_y) # 15% of board
        elif difficulty.lower() == "hard":
            self.no_of_bombs = int(0.2 * self.board_x * self.board_y) # 20% of board
    
    def populate_bombs(self):
        #print_if(self.board)
        for x in range(self.no_of_bombs):
            self.place_bomb()
    
    def place_bomb(self):  # CAREFUL - if this is called and all available cells are already bombs, it will loop forever, though this should never be the case in practice
        while True:
            x = random.randint(0,self.board_x-1)
            y = random.randint(0,self.board_y-1)
            print_if(f'{x},{y} - attempting to set bomb')
            if not self.board[y][x].is_bomb:
                print_if(f'{x},{y} - setting bomb')
                self.board[y][x].set_bomb()
                break

    def get_neighbours(self):
        for row in self.board:
            for cell in row:
                cell.get_neighbours()

    def handle_click(self, mouse_pos, mouse_btn, game):
        x, y = mouse_pos
        if self.board[y][x].clicked and mouse_btn[0]:
            return
        else:
            self.board[y][x].unhide(mouse_btn, game)

    def reset(self):
        #x_max, y_max = self.board_size
        self.calculate_bombs(self.difficulty)
        self.board = [ [ Cell((x + (self.board_x * y)),self,self.square_size) for x in range(0,self.board_y) ] for y in range(0,self.board_y) ]
        self.populate_bombs()
        self.get_neighbours()

    def scale(self,x,y,factor):
        '''A helper function to convert the screen coordinate system to the cells/minefield coordinate system
        i.e. multiply/divide by no. of pixels in a cell.
        
        Using a positive factor will return x and y multiplied by said factor
        Using a negative factor will return x and y divided by said factor

        Example
        -------
        >>> from minepygame import Cell, Minefield
        >>> screen = pygame.display.set_mode((20, 20))
        >>> map = Minefield()     
        >>> map.scale(5,5,10)
        (50, 50)
        >>> map.scale(50,50,-10)
        (5, 5)

        '''
        if factor > 0:
            return x*factor,y*factor
        elif factor < 0:
            return int(x/-factor), int(y/-factor)

def main():
    pygame.init()
    clock = pygame.time.Clock()
    X = 20
    Y = 20
    # to be provided by a menu screen at some point, hardcoded for now as target is core gameplay first

    cell_size = 20
    SCREEN_WIDTH = X*20  # each cell in the minefield is to occupy a 20x20 pixel space, at least for now - not yet decided on visual aspects so this is liable to change after core gameplay is written and tested
    SCREEN_HEIGHT = Y*20
    colour = (0,0,0)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def generate_map(x,y):
        map = Minefield(board_size=(x,y))
        return map

    def refresh_board(map):
        for row in map.board:
            for cell in row:
                x, y = cell.to_coordinate(cell.ordinate)
                screen.blit(cell.surf, map.scale(x, y, cell_size))
                pygame.display.flip()

    def pause():
        surf = pygame.image.load("img/paused.png").convert()
        rect = surf.get_rect()
        screen.blit(surf,rect)
        pygame.display.flip()

    map = generate_map(X,Y)
    pause()

    running = True
    game = False
    bomb =  None
    while running:


        while game:
            if bomb:
                if bomb.explode_frame_count < 4:
                    bomb.explode(screen)

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause()
                        game = False

                elif event.type == QUIT:
                    running = False
                    game = False
            
            if any(pygame.mouse.get_pressed()):
                x, y = pygame.mouse.get_pos()
                x_scaled, y_scaled = map.scale(x, y, -cell_size)
                cell = map.board[y_scaled][x_scaled]
                print_if(f'{pygame.mouse.get_pos()} - {map.scale(x, y, -cell_size)} - {pygame.mouse.get_pressed()} - attributes - {vars(cell)}')
                map.handle_click((x_scaled,y_scaled),pygame.mouse.get_pressed(),screen)
                if map.board[y_scaled][x_scaled].exploded:
                    bomb = map.board[y_scaled][x_scaled]
        
            pygame.display.flip()
            clock.tick(10)

        if not running:
            break

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    refresh_board(map)
                    game = True
            elif event.type == QUIT:
                running = False

        LEFT = pygame.mouse.get_pressed()[0]
        RIGHT = pygame.mouse.get_pressed()[2]

        if LEFT:
            screen.fill(colour)
            pygame.display.flip()
            refresh_board(map)
            game = True
        elif RIGHT:
            screen.fill(colour)
            pygame.display.flip()
            map.reset()
            #map = generate_map(X,Y)
            refresh_board(map)
            
        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()