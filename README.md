# GraphGameSeniorProj
Spring 2024 Final Project Graph Game Repo for Caleb and Nico
This game showcases a graph of nodes which represent planets, and ships that can take them over.
Many AI strategies are implemented in order to make the gameplay more engaging.
Read documentation for more information.

Deployment instructions:
    - Run "pip install -r requirements.txt" in command lind
    - Run main.py

How to play:
Load up the executable
Select your desired game mode: Single Player, Multiplayer, Computer (Appendix A, C)
Once Selected, choose your AI settings and difficulty
For multiplayer, one user will host the game and the other will join
The user who hosts will present their IP, listed on screen, to the user who will enter the IP and join
Then it's time to play, press start!
Once in game, your objective is to capture the other teams home planet on the other side of the map
Using the “Shop” button on the top of the screen, you are able to purchase a new ship every 200 points. More ships, more damage!
Using your mouse, right click on the planet you'd like your ships to travel to. It will be illuminated green.
Once on a planet, it will automatically attempt to capture.
Watch out! If you attempt to capture a planet with enemy ships, they will engage in combat. The side with the most ships on the planet will win so prepare for attack!
 Continue this until you have reached the opponents home planet, then you win!
Explanations for the CPUs:
The CPUs are designed to complete the game with two user selected conditions: Settings and Difficulty.
The user is able to choose if the AI they face uses Depth First Search (DFS), Breadth First Search (BFS), looks for the best move first, looks for the worst move first, looks for the highest scoring first move first, or the lowest scoring move first.
The user can then select the AI difficulty: Easy, Medium, Hard.
Using the debug menu:
The Debug menu was designed and implemented to test the product to its limit. It allows us to quickly reach the max ship count possible, force wins, etc to ensure the product can pass any test and edge case.
Commands can be inserted by clicking left control. There are two commands:
addships <playernum> <ship amount>
forcewin <playernum>
