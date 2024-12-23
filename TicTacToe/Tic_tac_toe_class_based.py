from enum import Enum


class PlayerType(Enum):
    EMPTY = " "
    X = "X"
    O = "O"
    A = "A"  # Example of an additional symbol
    B = "B"  # Example of another symbol


class PlaneBoard:
    def __init__(self, size_length):
        self.size = size_length
        self.board = [[PlayerType.EMPTY for _ in range(size_length)] for _ in range(size_length)]

    def print_board(self):
        """Print the current state of the board."""
        for row in self.board:
            print("|".join([x.value for x in row]))
        print("-" * (self.size * 2 - 1))

    def make_move(self, x: int, y: int, player: PlayerType) -> bool:
        if self.board[x][y] == PlayerType.EMPTY:
            self.board[x][y] = player
            return True
        return False

    def is_draw(self):
        for row in self.board:
            if row.count(PlayerType.EMPTY) == 0:
                return True
        return False

    def check_winner(self):

        # row iteration
        for i in range(self.size):
            temp_player = self.board[i][0]
            winner_found = True
            for j in range(self.size):
                if temp_player != self.board[i][0] or self.board[i][0] == PlayerType.EMPTY:
                    winner_found = False
                    break
            if winner_found:
                return temp_player

        # column iteration
        for j in range(self.size):
            temp_player = self.board[0][j]
            if temp_player != PlayerType.EMPTY and \
                    all([(self.board[i][j] == temp_player) for i in range(self.size)]):
                return temp_player

        # diagonal iteration
        temp_player = self.board[0][0]
        if temp_player!= PlayerType.EMPTY and all([(self.board[i][i] == temp_player) for i in range(self.size)]):
            return temp_player
        temp_player = self.board[self.size - 1][0]
        if temp_player!= PlayerType.EMPTY and all([(self.board[self.size - 1 - i][i] == temp_player) for i in range(self.size)]):
            return temp_player


class TicTacToe:
    def __init__(self, size_length: int, players: list):
        self.board = PlaneBoard(size_length)
        self.players = players
        self.current_player = 0

    def get_player_move(self):
        row = int(input("Enter the row number"))
        col = int(input("Enter the column number"))
        return row, col


    def start_game(self):
        """Start the Tic Tac Toe game."""
        print("Welcome to Tic Tac Toe!")
        self.board.print_board()

        while True:
            current_player = self.players[self.current_player]
            print(f"Player {current_player.value}'s turn.")
            try:
                row = int(input(f"Enter the row (0-{self.board.size - 1}): "))
                col = int(input(f"Enter the column (0-{self.board.size - 1}): "))
                if not (0 <= row < self.board.size and 0 <= col < self.board.size):
                    print("Invalid input. Please try again.")
                    continue

                if not self.board.make_move(row, col, current_player):
                    print("Cell is already taken. Try again.")
                    continue

                self.board.print_board()

                # Check for a winner
                winner = self.board.check_winner()
                if winner:
                    print(f"Player {winner.value} wins!")
                    break

                # Check for a draw
                if self.board.is_draw():
                    print("It's a draw!")
                    break

                # Switch player
                self.current_player = (self.current_player + 1) % len(self.players)

            except ValueError:
                print("Invalid input. Please enter numbers only.")


if __name__ == "__main__":
    # Define players and board size
    players = [PlayerType.X, PlayerType.O]
    game = TicTacToe(size_length=3, players=players)
    game.start_game()


'''
Output:- 
Welcome to Tic Tac Toe!
 | | 
 | | 
 | | 
-----
Player X's turn.
Enter the row (0-2): 1
Enter the column (0-2): 1
 | | 
 |X| 
 | | 
-----
Player O's turn.
Enter the row (0-2): 22
Enter the column (0-2): 2
Invalid input. Please try again.
Player O's turn.
Enter the row (0-2): 2
Enter the column (0-2): 2
 | | 
 |X| 
 | |O
-----
Player X's turn.
Enter the row (0-2): 0
Enter the column (0-2): 1
 |X| 
 |X| 
 | |O
-----
Player O's turn.
Enter the row (0-2): 1
Enter the column (0-2): 2
 |X| 
 |X|O
 | |O
-----
Player X's turn.
Enter the row (0-2): 2
Enter the column (0-2): 1
 |X| 
 |X|O
 |X|O
-----
Player X wins!


'''