> [!NOTE]
> This project is unfinished.
> It was created as part of self education fairly long ago and is not intended for public use.
> I am keeping all of my old self-education projects public for transparancy and posterity.
> I do not recommend attempting to deploy this software in the real world and while it can be
> used to track my personal and professional progress, it should not be seen as a good example
> of coding or devops best practice. As such, I do not recommend beginers use this project for
> educational purposes or guidance.
> In particular, this project makes very bad use of classes and objects. I may revisit this in
> the future to refactor it into better code, but I may not...

# PySweeper

To run the game, simply install the requirements (PyGame, Python 3.10+) and run the file 'minepygame.py'. The file 'minesweeper.py' was an early prototype using Tkinter and is much more limited in functionality but helped develop the core logic of generating a board of cells (or minefield of mines).

~~At present, running the program dives straight into a game (only one game, you need to exit to start a new game), including the functionality to left and right click on individual cells to reveal their number of neighbouring bombs / if it is a bomb, or flag the cell.~~

Currently, the game features very basic menu controls. Upon running the game you are presented with a view showing the word "Paused". 
A left mouse click will take you to a new game or return to an ongoing game. A right mouse click from the pause menu creates a new game.
Pressing esc toggles between the game mode (current game) and pause screen. More functionality will be added later to allow for different game controls.

Clicking on a bomb does not currently end the game, so the current state of the game can be used to practice playing the game as you can't 'lose' - I may add this as a feature to be able to switch modes for the purpose of practicing (I'm really good at accidentally clicking the opposite mouse button from what I intend to!)

# The game currently has the following missing features / existing bugs:

- [x] ~~Missing ability to toggle flags~~
- [ ] Missing end game handling (for both lose and win scenarios)
- [x] ~~There is a bug where clicking the same bomb twice crashes the game - this will be fixed by the previous point~~
- [ ] There are only number images for 1 - 5, but theoretically up to 8 cell neighbours could be a bomb so need to make these images at some point too.

# An example of a completed game and a paused game:

![A completed game](/documentation/a_completed_game.PNG)
![A paused game](/documentation/a_paused_game.PNG)
