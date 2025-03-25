# GameInterface

Alien Invasion - Reinforcement Learning

This project is a reinforcement learning (RL) version of the classic Alien Invasion game using Pygame and OpenAI Gym. The goal is to train an AI agent to control a spaceship and shoot down alien fleets before they reach the bottom of the screen.

## Features
	•	Manual gameplay – Play the original game using keyboard controls
	•	AI training environment – Train an agent to play using reinforcement learning
	•	Custom reward system – Encourages smart movement and shooting
	•	Scoring system – Tracks high scores and current scores separately

## How the Game Works
	•	The player (or agent) controls a spaceship that can move left, right, and shoot.
	•	The goal is to destroy all aliens before they reach the bottom.
	•	The player has 3 lives and loses a life if:
	•	An alien collides with the spaceship.
	•	The alien fleet reaches the bottom.
 	•	Scoring System:
		• The high score is displayed at the center in manual gameplay.
		• The current score is shown in the top-right corner.
		• The high score is NOT displayed during RL training or testing to prevent distractions.

## Installation
  1.	Clone the repository:

    git clone https://github.com/VaiNav06/GameInterface
    cd GameInterface


  2.	Install dependencies:

    pip install pygame gym numpy torch


  3.	Run the original game:

    python alien_invasion.py



Controls

	Key		Action
	Left Arrow (←)	Move spaceship left
	Right Arrow (→)	Move spaceship right
	Spacebar	Shoot bullets

## RL Environment (Gym Wrapper)

    The RL agent interacts with a custom OpenAI Gym environment, where:
    	• State space (observations the agent gets):
	    	- Ship position
	    	- Number of bullets on screen
	    	- Number of remaining aliens
	    	- Closest alien’s position
	    	- Player’s remaining lives
    	• Action space (what the agent can do):
	    	- Move left
	    	- Move right
	    	- Shoot
	    	- Do nothing
    	• Rewards system:
	    	- +0.5 for shooting
	    	- +0.3 for moving right, +0.2 for moving left
	    	- -50 if game over
	    	- Score-based rewards for hitting aliens

Training an RL Agent

To train an AI agent using Deep Q-Learning (DQN):

	python train_ppo.py

•	The agent will learn by playing the game repeatedly and improving over time.
•	Trained models will be saved in the models/ directory.

Testing a Trained Agent

To watch a trained RL agent play:

	python test_ppo.py

•	The agent will play automatically using the trained model.
•	High scores are hidden during testing.

## Project Structure

	GameInterface/            
	│── gym_alien_invasion.py  # Custom Gym environment                
	│── train_ppo.py           # Training script for RL agent  
	├── test_ppo.py            # Testing script for trained agent                
	│── settings.py            # Game settings  
	│── ship.py                # Player spaceship logic  
	│── alien.py               # Alien movement & logic  
	│── bullet.py              # Bullet behavior  
	│── game_stats.py          # Tracks player lives, scores, etc.  
	│── game_functions.py      # Game mechanics & screen updates  
	│── scoreboard.py          # Displays scores in-game  
	│── alien_invasion.py      # Main Pygame script  
	│── ppo_alien_invasion.zip # Trained RL models  
	│── README.md              # Project documentation  
 	│── alien.png		   # Image of alien fleets
  	│── ship.png		   # Image of user spacership
   	│── button.py		   # Displays play button 
   

## Notes
	•	Manual and AI gameplay – You can play manually or let an RL agent learn to play.
	•	Custom Gym wrapper – Works with DQN and other RL algorithms.
	•	Pygame rendering – Only enabled in human-mode rendering (during manual play).
	•	Adjustable training settings – Modify hyperparameters in train_agent.py.
