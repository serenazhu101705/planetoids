# planetoids
CS 1110 Project

Game objective: destroy all the asteroids on the screen to win. If you hit an asteroid, you lose a life. Default number of lives is 3. 

## Additional Features:
Lives:
The user starts with SHIP_LIVES in consts.py. 
Default value is 3. If the ship hits an asteroid, the player loses a life.
After losing a life, the ship is reset but the asteroids remain.
**IMPORTANT**: I realized there was an issue when the player's life revives, it
would automatically die and lose another life because the asteroid was still 
touching the ship. So, to compensate for this, I made it so that 200 frames 
(approximately the time for a large asteroid to pass the ship) must pass after 
the player loses a life before they can lose another life.

Score:
Every time the user's bullet hits an asteroid, the user gains 1 point.

Restart:
After the user either completes the game or runs out of lives, they can choose
to restart the game.

High Score:
In every round of plays, there is a high score. When the user restarts the game, the
current score is compared to the high score, which is initially 0. If the score is 
higher than the previous score, it becomes the new high score.

Labels:
There is a label for asteroids left, lives left, score, and high score on the screen. The
number of asteroids left is the length of the asteroids list in wave.py.
