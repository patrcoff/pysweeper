# PySweeper

To run the game, simply install the requirements (PyGame, Python 3.10+) and run the file 'minepygame.py'.

At present, this dives straight into a game, including the functionality to left and right click on individual cells to reveal their number of neighbouring bombs / if it is a bomb, or flag the cell.
The game currently has the following missing features / existing bugs:

- Missing ability to toggle flags
- Missing end game handling (for both lose and win scenarios)
- Their is a bug where clicking the same bomb twice crashes the game - this will be fixed by the previous point
- There are only number images for 1 - 5, but theoretically up to 8 cell neighbours could be a bomb so need to make these images at some point too.
