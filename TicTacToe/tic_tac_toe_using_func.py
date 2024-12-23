def print_board(board):
    """Print the current state of the board."""
    for row in board:
        print("|".join(row))
        print("-" * 5)


def check_winner(board):
    """Check if there is a winner."""
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]

    return None


def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != " " for row in board for cell in row)


def tic_tac_toe():
    """Main function to play Tic Tac Toe."""
    # Initialize the board
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0

    print("Welcome to Tic Tac Toe!")
    print_board(board)

    while True:
        print(f"Player {players[current_player]}'s turn.")
        try:
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
            if board[row][col] != " ":
                print("This cell is already taken. Try again.")
                continue
        except (ValueError, IndexError):
            print("Invalid input. Please enter numbers between 0 and 2.")
            continue

        # Make the move
        board[row][col] = players[current_player]
        print_board(board)

        # Check for a winner
        winner = check_winner(board)
        if winner:
            print(f"Player {winner} wins!")
            break

        # Check for a draw
        if is_draw(board):
            print("It's a draw!")
            break

        # Switch player
        current_player = 1 - current_player


if __name__ == "__main__":
    tic_tac_toe()