import unittest
import minepygame
import pygame
#  THESE TESTS NO LONGER WORK SINCE MOVING THE INSTANTIATION OF PYGAME.DISPLAY SINCE MOVING MAINLOOP INTO MAIN FUNC AND USING IF __NAME__
#  IGNORE THESE TESTS UNTIL I HAVE DECIDED HOW TO PROCEED WITH INSTANTIATING FOR TEST PURPOSES OUTSIDE OF RUNNING THE PROGRAM AS __MAIN__

class TestMinefieldClass(unittest.TestCase):
    

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        minepygame.DEBUG = False
        pygame.init()
        screen = pygame.display.set_mode((20, 20))
        self.minefield = minepygame.Minefield(board_size=(5,5),difficulty='hard',square_size=10)
    
    def test_always_passes(self):
        self.assertTrue(True,'Something is badly wrong here!')
    
    def test_minefield_instantiation(self):
        
        self.assertTrue(len(self.minefield.board) > 0)
    
    def test_board_size(self):
        self.assertEqual(self.minefield.board_size,(5,5))
        
    def test_board_x(self):
        self.assertEqual(self.minefield.board_x,5)
        
    def test_board_(self):
        self.assertEqual(self.minefield.board_y,5)

if __name__ == '__main__':

    unittest.main()
