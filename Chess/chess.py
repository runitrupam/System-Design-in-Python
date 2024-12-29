'''
Design Chess

FR :-
2 Players can play chess.
at a time 1 player can play
Game outcome - Ongoing, Draw, Checkmate, Stalemate(Draw) (if one player cannot move the chess pieces)
Winner - if piece = king dies

x --> column wise iterate
y --> row wise iterate

'''

from abc import ABC, abstractmethod
from enum import Enum


class PieceType(Enum):
    King = 'King'
    Rook = 'Rook'
    Pawn = 'Pawn'
    Bishop = 'Bishop'
    Knight = 'Knight'
    Queen = 'Queen'


class ColorType(Enum):
    White = 'White'
    Black = 'Black'


class Piece(ABC):

    def __init__(self, color: ColorType):
        self.piece_type = None
        self.color = color

    def __str__(self):
        return f'{self.color.name[0]}_{self.piece_type.name[:2]}'

    @abstractmethod
    def can_move(self, start_x, start_y, end_x, end_y):
        pass


class King(Piece):
    def __init__(self, color: ColorType):
        self.piece_type = PieceType.King
        self.color = color

    def can_move(self, start_x, start_y, end_x, end_y):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        if (dx == 0 and dy == 1) or (dx == 1 and dy == 0) or (dx == 1 and dy == 1):
            return True
        return False


class Queen(Piece):
    def __init__(self, color: ColorType):
        self.piece_type = PieceType.Queen
        self.color = color

    def can_move(self, start_x, start_y, end_x, end_y):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        if (dx == 0 and dy != 0) or (dx != 0 and dy == 0) or (dx == dy):
            return True
        return False


class Rook(Piece):
    def __init__(self, color: ColorType):
        self.piece_type = PieceType.Rook
        self.color = color

    def can_move(self, start_x, start_y, end_x, end_y):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        if (dx == 0 and dy != 0) or (dx != 0 and dy == 0):
            return True
        return False


class Bishop(Piece):
    def __init__(self, color: ColorType):
        self.piece_type = PieceType.Bishop
        self.color = color

    def can_move(self, start_x, start_y, end_x, end_y):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        if (dx == dy):
            return True
        return False


class Knight(Piece):
    def __init__(self, color: ColorType):
        self.piece_type = PieceType.Knight
        self.color = color

    def can_move(self, start_x, start_y, end_x, end_y):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
            return True
        return False


class Pawn(Piece):
    def __init__(self, color: ColorType):
        self.piece_type = PieceType.Pawn
        self.color = color

    def can_move(self, start_x, start_y, end_x, end_y):
        dx = abs(start_x - end_x)
        dy = start_y - end_y  # if -ve then Black
        if self.color == ColorType.White:
            direction = 1
        else:
            direction = -1
        if direction == 1:
            if dy == 2 and start_y == 1 and dx == 0:  # at the start Rook can move 2 steps
                return True
            elif dy == 1 and (dx == 0 or dx == 1):
                return True
        else:
            if dy == -2 and start_y == 6 and dx == 0:
                return True
            elif dy == -1 and (dx == 0 or dx == 1):
                return True
        return False


class Cell:
    def __init__(self, piece: Piece, x: int, y: int):
        self.piece = piece
        self.x = x
        self.y = y

    def is_empty(self):
        return self.piece is None

    def __str__(self):
        return str(self.piece) if self.piece else ".   "


class Board:
    def __init__(self):
        self.board = [[Cell(None, i, j) for j in range(8)] for i in range(8)]
        self.initialize_board()

    def initialize_board(self):
        self.board[0][0] = Cell(Rook(ColorType.White), 0, 0)
        self.board[0][1] = Cell(Knight(ColorType.White), 0, 1)
        self.board[0][2] = Cell(Bishop(ColorType.White), 0, 2)
        self.board[0][3] = Cell(Queen(ColorType.White), 0, 3)
        self.board[0][4] = Cell(King(ColorType.White), 0, 4)
        self.board[0][5] = Cell(Bishop(ColorType.White), 0, 5)
        self.board[0][6] = Cell(Knight(ColorType.White), 0, 6)
        self.board[0][7] = Cell(Rook(ColorType.White), 0, 7)

        self.board[7][0] = Cell(Rook(ColorType.Black), 7, 0)
        self.board[7][1] = Cell(Knight(ColorType.Black), 7, 1)
        self.board[7][2] = Cell(Bishop(ColorType.Black), 7, 2)
        self.board[7][3] = Cell(Queen(ColorType.Black), 7, 3)
        self.board[7][4] = Cell(King(ColorType.Black), 7, 4)
        self.board[7][5] = Cell(Bishop(ColorType.Black), 7, 5)
        self.board[7][6] = Cell(Knight(ColorType.Black), 7, 6)
        self.board[7][7] = Cell(Rook(ColorType.Black), 7, 7)

        for i in range(8):
            self.board[1][i] = Cell(Pawn(ColorType.White), 1, i)
            self.board[6][i] = Cell(Pawn(ColorType.Black), 6, i)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.board[x][y]

    def set_cell(self, x: int, y: int, piece: Piece):
        self.board[x][y].piece = piece

    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print()

    def find_king(self, color):
        """Find the position of the king of the given color."""
        for row in self.board:
            for cell in row:
                if isinstance(cell.piece, King) and cell.piece.color == color:
                    return cell
        return None

    def is_in_check(self, color):
        """Check if the king of the given color is in check."""
        king_cell = self.find_king(color)
        if not king_cell:
            return False

        # Check if any opponent piece can attack the king's position
        for row in self.board:
            for cell in row:
                if cell.piece and cell.piece.color != color:
                    if cell.piece.can_move(cell, king_cell, self):
                        return True
        return False

    def has_valid_moves(self, color):
        """Check if the player has any valid moves left."""
        for row in self.board:
            for cell in row:
                if cell.piece and cell.piece.color == color:
                    for x in range(8):
                        for y in range(8):
                            target_cell = self.board[x][y]
                            if cell.piece.can_move(cell, target_cell, self):
                                # Simulate the move and check if it's valid
                                original_piece = target_cell.piece
                                target_cell.piece = cell.piece
                                cell.piece = None

                                is_still_in_check = self.is_in_check(color)

                                # Revert the move
                                cell.piece = target_cell.piece
                                target_cell.piece = original_piece

                                if not is_still_in_check:
                                    return True
        return False

    def move_piece(self, start_x: int, start_y: int, end_x: int, end_y: int):
        start_cell = self.get_cell(start_x, start_y)
        end_cell = self.get_cell(end_x, end_y)
        if start_cell.piece and start_cell.piece.can_move(start_x, start_y, end_x, end_y):
            if end_cell.piece is None or \
                    (end_cell.piece and end_cell.piece.color != start_cell.piece.color):
                self.set_cell(end_x, end_y, start_cell.piece)
                self.set_cell(start_x, start_y, None)
                return True
            else:
                print("Invalid move. Same color piece.")
        else:
            print("Invalid move. Not your piece or not a valid move.")
        return False


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.board.initialize_board()
        self.current_turn = "white"

    def get_current_turn(self) -> str:
        return self.current_turn

    def switch_turn(self):
        if self.current_turn == "white":
            self.current_turn = "black"
        else:
            self.current_turn = "white"

    def check_game_status(self):
        """Check for checkmate, stalemate, or if the game continues."""
        if self.board.is_in_check(self.current_turn):
            if not self.board.has_valid_moves(self.current_turn):
                print(f"Checkmate! {self.current_turn} loses!")
                return True
            else:
                print(f"{self.current_turn} is in check!")
        else:
            if not self.board.has_valid_moves(self.current_turn):
                print("Stalemate! The game is a draw.")
                return True
        return False

    def start_game(self):
        while True:
            self.board.print_board()
            print(f"{self.current_turn}'s turn")
            try:
                start_x = int(input("Enter start x: "))
                start_y = int(input("Enter start y: "))
                end_x = int(input("Enter end x: "))
                end_y = int(input("Enter end y: "))

                start_cell = self.board.board[start_x][start_y]
                if start_cell.piece and start_cell.piece.color != self.current_turn:
                    print("You cannot move your opponent's piece!")
                    continue

                if self.board.move_piece(start_x, start_y, end_x, end_y):
                    if self.check_game_status():
                        break
                    self.current_turn = "black" if self.current_turn == "white" else "white"
            except (ValueError, IndexError):
                print("Invalid input. Try again.")


if __name__ == "__main__":
    game = ChessGame()
    game.start_game()
