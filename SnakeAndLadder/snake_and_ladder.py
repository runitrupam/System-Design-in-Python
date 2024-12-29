'''

FR:-
Any number of player can play simultaneously.
no. of cells given by at the start

snakes will bring a player to lower cells
ladder will bring a player above
game ends when the player reaches the last cell


Entity --
SnakeAndLadderManager
Dice
Snake
Ladder
Board


	You don’t need locks or a singleton because the game state is unique for each thread.
	•	As long as each thread gets its own instances of Board, Player, and SnakeAndLadder,
	 threads will operate independently and there’s no risk of race conditions.


    •	You only need locks or a singleton if threads share resources (like a global scoreboard or a shared Dice instance).
		Here I am adding a lock , Singleton ,I want to update the scores on the scoreboard.


'''

from typing import List, Dict
import random


class Dice:
    @staticmethod
    def roll() -> int:
        return random.randint(1, 6)


class Snake:
    def __init__(self, start_cell, end_cell):
        self.start_cell = start_cell
        self.end_cell = end_cell


class Ladder:
    def __init__(self, start_cell, end_cell):
        self.start_cell = start_cell
        self.end_cell = end_cell


class Player:
    def __init__(self, name, current_position):
        self.name = name
        self.current_position = current_position


class Board:
    def __init__(self, num_cells,
                 snakes: list[Snake] = [], ladders: list[Ladder] = []):
        self.num_cells = num_cells
        self.cells = [None] * num_cells
        self.snakes: list(Snake) = snakes
        self.ladders: list(Ladder) = ladders

    def add_snake(self, snake: Snake):
        self.snakes.append(snake)

    def add_ladder(self, ladder: Ladder):
        self.ladders.append(ladder)

    def is_cell_valid(self, new_position: int):
        return True if new_position <= self.num_cells else False

    def is_winner(self, new_position: int):
        return True if new_position == self.num_cells else False

    def get_new_position(self, new_position: int):
        snake = next((snake for snake in self.snakes if snake.start_cell == new_position), None)
        if snake:
            new_position = snake.end_cell
        ladder = next((ladder for ladder in self.ladders if ladder.start_cell == new_position), None)
        if ladder:
            new_position = ladder.end_cell
        return new_position


class SnakeAndLadder:
    def __init__(self, board: Board, players: List[Player], ):
        self.board = board
        self.players = players

    def start_game(self):
        while True:
            for player in self.players:
                new_position = player.current_position + Dice.roll()
                new_position = self.board.get_new_position(new_position)
                print(
                    f"{player.name} player.current_position = {player.current_position}, new_position = {new_position} !")
                if self.board.is_cell_valid(new_position):
                    player.current_position = new_position
                    print(f"{player.name} moved to cell {new_position}")
                    if self.board.is_winner(new_position):
                        print(f"{player.name} wins!")
                        return


if __name__ == "__main__":
    num_cells = 100
    snakes = [Snake(14, 3), Snake(36, 17), Snake(55, 25)]
    ladders = [Ladder(1, 38), Ladder(4, 14), Ladder(9, 31), Ladder(21, 42), Ladder(37, 56), Ladder(58, 84)]
    board = Board(num_cells, snakes, ladders)

    num_players = int(input("Enter the number of players: "))
    players = [Player(f"Player {i + 1}", 1) for i in range(num_players)]

    # players = [Player("Player 1", 1), Player("Player 2", 1)]
    game = SnakeAndLadder(board, players)
    game.start_game()
