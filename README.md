# Blackjack Simulator and Analysis

The Blackjack Simulator simulates games of Blackjack, a popular gambling game. After running, the game analysis provides insights into how to well a player performed with metrics and statistical tests.  [Description of the game.](https://www.britannica.com/topic/blackjack-card-game)	


## Description

The simulator can be personalised. Currently, the following parameters can be modified:


**1. Player settings**

* Number of players
* Strategy for each player (Basic Strategy, No Bust Strategy)
* Number of hands per player per round
* Bet size

**2. General settings**

* Number of rounds to be played
* Dealer stands or hits a soft 17
* Shoe size
* Shuffle mode (deck penetration, random-card)
* Allow resplitting of aces 
* Blackjack payout 

## Installation


## Usage

```python
import blackjack as bj
# creates game instance with given settings
game = Game(player_no: int, hands_per_player: int, rounds: int, 
blackjack_pays: float = 1.5, 
ace_resplit: bool = True, seed: Any | None = None)
bj.game('word')

# creates csv files with game data
game.export_as_csv()


```


## License

[MIT](https://choosealicense.com/licenses/mit/)
