# Blackjack Simulator and Analysis [WIP]

The Blackjack Simulator simulates games of Blackjack, a popular gambling game. After running, the game analysis provides insights into how to well a player performed with metrics and statistical tests.  [Description of the game.](https://www.britannica.com/topic/blackjack-card-game)	

Currently, I am developing a Streamlit app, where people can simulate a Blackjack game according to their wishes and then look at the statistics. 


#### Next steps:
- build app MVP
- extend data analysis 
- add more Blackjack strategies and card-counting

## Description

The project consists of two parts. First, there is the implementation of the game itself. This is done using OOP in Python. The game is played according to the specified parameters. Players act following a given strategy. Everything is done automatically. Then, there is the option to save the game results as the following csv files:

1. hands_log.csv: tracking important information on every hand 
2. game_log.csv: basic information about the game parameters and results
3. player_log.csv: basic information about the players and their final balance

The second part works with that data. The goal is to analyze how each player performed, which includes basic metrics, like number of wins, average return per hand and of course the final balance. However, I try to find more meaningful insights. Currently, I implemented significance tests for a player's win rate and average return. In addition, there is also a test comparing the performance of two strategies. I also plan to add logistic regression to predict the outcome of a hand, visualizations and much more.

## Game Parameters 

The simulator can be personalised. Currently, the following parameters can be modified:


**1. Player settings**

* Number of players
* Strategy for each player (Basic Strategy, No Bust Strategy)
* Number of hands per player per round
* Bet size

**2. General settings**

* Seed for shoe shuffles
* Number of rounds to be played
* Dealer stands or hits a soft 17
* Shoe size
* Shuffle mode (deck penetration, random-card)
* Allow resplitting of aces 
* Blackjack payout 

## CSV structure

1. hands_log.csv: ["round_id", "hand_no", "player_id", "dealer_upcard", "dealer_hand_value", "hand_start_value", "hand_final_value", "hand_result", "actions", "cards", "bet", "profit/loss"]

2. game_log.csv: ["seed", "players", "rounds", "dealer_rule", "blackjack_pays", "decks", "penetration_rate", "dealer_balance", "shuffles"]

3. player_log.csv: ["player_id", "hands_played", "bet_size", "strategy", "final_balance"]

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install -- tbi --
```

## Usage

```python
import blackjack as bj

# creates game instance with given settings
game = bj.Game(player_no: int, hands_per_player: int, rounds: int, 
blackjack_pays: float = 1.5, 
ace_resplit: bool = True, seed: Any | None = None)

# starts the game
game.start()

# creates csv files with game data
game.export_as_csv()

```


## License

[MIT](https://choosealicense.com/licenses/mit/)
