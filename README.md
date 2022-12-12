# Tic-Tac-Toe-using-Reinforcement-Learning
<pre>
The name of our project is Tic-tac-toe and the realm of AI that it uses is reinforcement learning.The objective of our project is to 
create an intelligent system that can optimally play Tic-Tac-Toe using two phases which are as follows:
1.Training phase, during which two different AI agents can play against each other and 
2.Test phase, during which the trained AI Model will play against a human being.
As mentioned earlier, the chosen approach is reinforcement learning and the elements of any problem to be solved are as follows: 
State, Action, and Reward. It works to reward the agent based on the action it has taken on a state. Therefore, we will first train 
the Model and then allow it to play against a human being.

These are the steps involved in Setting-up the game of Tic-Tac-Toe: 
-Two agents play against each other in 5000 random games
-Rewards are provided based on action
-Policy is setup based on this reward
-Model becomes ready to play against human
-Human being plays against the Model

The technology which has been used is Python, IDE used is VS Code and the version Control is GitHub.

Reinforcement learning, used to complete this project, works in the following way: 
There are certain number of states of any problem to be solved. One of these states is the 'goal' state, which is to be ideally 
achieved. Then there is another factor called an action, which is taken over a state. The system is supposed to take an action 
on the current state, which may not may not lead to the goal state. While training, our system acts, and receives a reward based
on whether that action leads to the goal state or not. Based on these rewards, the system learns what actions should be taken on 
what state. 

The project can be evaluated based on accurate Functioning of AI agent without any failures during the game in a major way. 
Along with that the final goal and actions of the agent should be based on defeating the opponent agent while training and 
the human/user while actual implementation.The agent should be trained in such a way that while playing with a human player,
it should seem as if two human brains are playing.

Lets Play the Game:
Scenario 1: Agent Wins Against Human
training...
Rounds 0
Rounds 1000
Rounds 2000
Rounds 3000
Rounds 4000
-------------
|   |   |   | 
------------- 
|   | x |   |
-------------
|   |   |   |
-------------
Input your action row:0
Input your action col:0
-------------
| o |   |   |
-------------
|   | x |   |
-------------
|   |   |   |
-------------
-------------
| o | x |   |
-------------
|   | x |   |
-------------
|   |   |   |
-------------
Input your action row:0
Input your action col:2
-------------
| o | x | o |
-------------
|   | x |   |
-------------
|   |   |   |
-------------
| o | x | o |
-------------
|   | x |   |
-------------
|   | x |   |
-------------
computer wins!

Scenario 2: Tie between Agent and Human
training...
Rounds 0
Rounds 1000
Rounds 2000
Rounds 3000
Rounds 4000
-------------
|   |   |   |         
-------------
|   | x |   |         
-------------
|   |   |   |         
-------------
Input your action row:0
Input your action col:0
------------- 
| o |   |   | 
------------- 
|   | x |   | 
-------------
|   |   |   |
-------------
-------------
| o | x |   |
-------------
|   | x |   |
-------------
|   |   |   |
-------------
Input your action row:2
Input your action col:1
-------------
| o | x |   |
-------------
|   | x |   |
-------------
|   | o |   |
-------------
-------------
| o | x |   |
-------------
| x | x |   |
-------------
|   | o |   |
-------------
Input your action row:1
Input your action col:2
-------------
| o | x |   |
-------------
| x | x | o |
-------------
|   | o |   |
-------------
-------------
-------------
| x | x | o |
-------------
|   | o |   |
-------------
Input your action row:2
Input your action col:1
Input your action row:2
Input your action col:0
-------------
| o | x | x |
-------------
| x | x | o |
-------------
| o | o |   |
-------------
-------------
| o | x | x |
-------------
| x | x | o |
-------------
| o | o | x |
-------------
tie!
</pre>
