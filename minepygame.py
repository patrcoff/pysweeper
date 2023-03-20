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
DEBUG = True

def print_if(str):
    if DEBUG:
        print(str)

class Cell(pygame.sprite.Sprite):
    '''An individual cell in the minefield, with methods to handle detection of bombs and counting bombs in neighbouring cells. Inherits from Sprite class to handle rendering to screen.'''
    
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
        y1 = ord // self.parent.board_y
        x1 = ord % self.parent.board_x
        return x1, y1

    def get_neighbours(self):
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
            
            #above
            # -(x + 1)
            # - x
            # - (x -1)

            #below
            # + (x - 1)
            # + x
            # + (x + 1)
            ord = func(self.ordinate)
            if 0 <= ord < self.parent.get_board_area() and not self.opposite_side(self.ordinate,ord):
                self.neighbours.append(ord)
        print_if(f'{self.ordinate} - {self.to_coordinate(ord)} - {self.neighbours}')
        return self.neighbours
    
    def opposite_side(self,o1,o2):
        left_side = [y * self.parent.board_x for y in range(0,self.parent.board_y)]
        right_side = [y * self.parent.board_x + self.parent.board_x - 1 for y in range(0,self.parent.board_y)]
        if (o1 in left_side and o2 in right_side) or (o1 in right_side and o2 in left_side):
            return True
        return False

    def count_neighbours(self):
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
            

        if mouse_btn[2]:
            self.toggle_flag()

        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.render(screen)

    def toggle_flag(self):
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
        self.reset(size = board_size,diff = difficulty, square_size = square_size)            # unless we are only using images with no borders between them - let's see what that looks like...

    def set_board_size(self,x,y):
        self.board_size  = (x,y)
        self.board_x = self.board_size[0]
        self.board_y = self.board_size[1]

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
            print_if(f'{x},{y}')
            if not self.board[y][x].is_bomb:
                self.board[y][x].set_bomb()
                break

    def get_neighbours(self):
        for row in self.board:
            for cell in row:
                cell.get_neighbours()

    def handle_click(self, mouse_pos, mouse_btn, game):
        if self.board[mouse_pos[1]][mouse_pos[0]].clicked and mouse_btn[0]:
            return
        else:
            self.board[mouse_pos[1]][mouse_pos[0]].unhide(mouse_btn, game)

    def reset(self,size,diff,square_size):
        self.set_board_size(size[0],size[1])
        self.calculate_bombs(diff)
        self.board = [ [ Cell((x + (size[0] * y)),self,square_size) for x in range(0,size[0]) ] for y in range(0,size[1]) ]
        self.populate_bombs()
        self.get_neighbours()

    def scale(self,x,y,factor):
        '''A helper function to convert the screen coordinate system to the cells/minefield coordinate system, i.e. multiply/divide by no. of pixels in a cell.'''
        if factor > 0:
            return x*factor,y*factor
        elif factor < 0:
            return int(x/-factor), int(y/-factor)


#def scale(x,y,factor):  # to do: remove this and change calls to it in the mainloop to calls to the scale func of the Minefield instance
#    '''A helper function to convert the screen coordinate system to the cells/minefield coordinate system, i.e. multiply/divide by no. of pixels in a cell.'''
#    if factor > 0:
#        return x*factor,y*factor
#    elif factor < 0:
#        return int(x/-factor), int(y/-factor)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    x = 20  # to be provided by a menu screen at some point, hardcoded for now as target is core gameplay first
    y = 20
    cell_size = 20
    SCREEN_WIDTH = x*20  # each cell in the minefield is to occupy a 20x20 pixel space, at least for now - not yet decided on visual aspects so this is liable to change after core gameplay is written and tested
    SCREEN_HEIGHT = y*20

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    map = Minefield(board_size=(x,y))
    def refresh_board():
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
                    running = False
                    break
            elif event.type == QUIT:
                running = False
        
        if any(pygame.mouse.get_pressed()):
            refresh_board()
            game = True

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()


