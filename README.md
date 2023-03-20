# PySweeper

To run the game, simply install the requirements (PyGame, Python 3.10+) and run the file 'minepygame.py'. The file 'minesweeper.py' was an early prototype using Tkinter and is much more limited in functionality but helped develop the core logic of generating a board of cells (or minefield of mines).

At present, running the program dives straight into a game (only one game, you need to exit to start a new game), including the functionality to left and right click on individual cells to reveal their number of neighbouring bombs / if it is a bomb, or flag the cell. Clicking on a bomb does not currently end the game, so the current state of the game can be used to practice playing the game as you can't 'lose' - I may add this as a feature to be able to switch modes for the purpose of practicing (I'm really good at accidentally clicking the opposite mouse button from what I intend to!)

# The game currently has the following missing features / existing bugs:

- Missing ability to toggle flags
- Missing end game handling (for both lose and win scenarios)
- Their is a bug where clicking the same bomb twice crashes the game - this will be fixed by the previous point
- There are only number images for 1 - 5, but theoretically up to 8 cell neighbours could be a bomb so need to make these images at some point too.
