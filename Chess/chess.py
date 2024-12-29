'''

FR:-
2 players having two colors: White or Black.
 (King, Queen, Rook, Bishop, Knight, and Pawn).
8x8 chessboard

Pieces movement
attack
validate the move of pieces


class Diagram :-
	•	Aggregation (<>): Shows that the ChessGame class contains a Board, and the Board contains multiple Cell objects.
	•	Inheritance (<|--): Shows that the King, Queen, Rook, etc., inherit from the Piece class.
	•	Dependency (->): Indicates that Board depends on Piece for movement validation, and each Cell depends on Piece to hold a chess piece (or None if empty).


'''


from abc import ABC, abstractmethod
from enum import Enum
from typing import List

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
    def can_move(self, start_x, start_y, end_x, end_y, board):
        pass

    def is_path_clear(self, start_x, start_y, end_x, end_y, board):
        dx = end_x - start_x
        dy = end_y - start_y
        step_x = (dx // abs(dx)) if dx != 0 else 0
        step_y = (dy // abs(dy)) if dy != 0 else 0

        x, y = start_x + step_x, start_y + step_y
        while x != end_x or y != end_y:
            if not board[y][x].is_empty():
                return False
            x += step_x
            y += step_y
        return True


class King(Piece):
    def __init__(self, color: ColorType):
        super().__init__(color)
        self.piece_type = PieceType.King

    def can_move(self, start_x, start_y, end_x, end_y, board):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        return max(dx, dy) == 1


class Queen(Piece):
    def __init__(self, color: ColorType):
        super().__init__(color)
        self.piece_type = PieceType.Queen

    def can_move(self, start_x, start_y, end_x, end_y, board):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        if dx == dy or dx == 0 or dy == 0:
            return self.is_path_clear(start_x, start_y, end_x, end_y, board)
        return False


class Rook(Piece):
    def __init__(self, color: ColorType):
        super().__init__(color)
        self.piece_type = PieceType.Rook

    def can_move(self, start_x, start_y, end_x, end_y, board):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        if dx == 0 or dy == 0:
            return self.is_path_clear(start_x, start_y, end_x, end_y, board)
        return False


class Bishop(Piece):
    def __init__(self, color: ColorType):
        super().__init__(color)
        self.piece_type = PieceType.Bishop

    def can_move(self, start_x, start_y, end_x, end_y, board):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        if dx == dy:
            return self.is_path_clear(start_x, start_y, end_x, end_y, board)
        return False


class Knight(Piece):
    def __init__(self, color: ColorType):
        super().__init__(color)
        self.piece_type = PieceType.Knight

    def can_move(self, start_x, start_y, end_x, end_y, board):
        dx = abs(start_x - end_x)
        dy = abs(start_y - end_y)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)


class Pawn(Piece):
    def __init__(self, color: ColorType):
        super().__init__(color)
        self.piece_type = PieceType.Pawn

    def can_move(self, start_x, start_y, end_x, end_y, board):
        dx = abs(start_x - end_x)
        dy = end_y - start_y if self.color == ColorType.White else start_y - end_y
        target_cell = board[end_y][end_x]
        print(f"Pawn Move: dx={dx}, dy={dy}, target_cell_empty={target_cell.is_empty()}, color = {self.color}, start_x, start_y, end_x, end_y {(start_x, start_y, end_x, end_y)}")

        # Movement logic
        if dx == 0 and target_cell.is_empty():
            if (dy == 1) or (dy == 2 and ((start_y == 1 and self.color == ColorType.White) or (
                    start_y == 6 and self.color == ColorType.Black))):
                return True
        elif dx == 1 and dy == 1 and target_cell.piece and target_cell.piece.color != self.color:
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


class PieceFactory:
    @staticmethod
    def create_piece(piece_type: PieceType, color: ColorType):
        if piece_type == PieceType.King:
            return King(color)
        elif piece_type == PieceType.Queen:
            return Queen(color)
        elif piece_type == PieceType.Rook:
            return Rook(color)
        elif piece_type == PieceType.Bishop:
            return Bishop(color)
        elif piece_type == PieceType.Knight:
            return Knight(color)
        elif piece_type == PieceType.Pawn:
            return Pawn(color)
        else:
            raise ValueError("Invalid piece type")


class Board:
    def __init__(self):
        self.board : List[Cell] = [[Cell(None, i, j) for j in range(8)] for i in range(8)]
        self.initialize_board()

    def initialize_board(self):
        for color, row, pawn_row in [(ColorType.White, 0, 1), (ColorType.Black, 7, 6)]:
            self.board[row][0] = Cell(PieceFactory.create_piece(PieceType.Rook, color), row, 0)
            self.board[row][1] = Cell(PieceFactory.create_piece(PieceType.Knight, color), row, 1)
            self.board[row][2] = Cell(PieceFactory.create_piece(PieceType.Bishop, color), row, 2)
            self.board[row][3] = Cell(PieceFactory.create_piece(PieceType.Queen, color), row, 3)
            self.board[row][4] = Cell(PieceFactory.create_piece(PieceType.King, color), row, 4)
            self.board[row][5] = Cell(PieceFactory.create_piece(PieceType.Bishop, color), row, 5)
            self.board[row][6] = Cell(PieceFactory.create_piece(PieceType.Knight, color), row, 6)
            self.board[row][7] = Cell(PieceFactory.create_piece(PieceType.Rook, color), row, 7)

            for col in range(8):
                self.board[pawn_row][col] = Cell(PieceFactory.create_piece(PieceType.Pawn, color), pawn_row, col)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.board[y][x]

    def print_board(self):
        i = 0
        print(" ","    ".join([str(x) for x in range(8)]))
        for row in self.board:
            print(i," ".join(str(cell) for cell in row))
            i += 1
        print()

    def move_piece(self, start_x, start_y, end_x, end_y):
        start_cell = self.get_cell(start_x, start_y)
        end_cell = self.get_cell(end_x, end_y)

        if start_cell.piece and start_cell.piece.can_move(start_x, start_y, end_x, end_y, self.board):
            if end_cell.is_empty() or end_cell.piece.color != start_cell.piece.color:
                end_cell.piece = start_cell.piece
                start_cell.piece = None
                return True
        return False


class ChessGame:
    def __init__(self):
        self.board = Board()
        self.current_turn = ColorType.White

    def start_game(self):
        while True:
            self.board.print_board()
            print(f"{self.current_turn.name}'s turn")
            try:
                start_x = int(input("Enter start x: "))
                start_y = int(input("Enter start y: "))
                end_x = int(input("Enter end x: "))
                end_y = int(input("Enter end y: "))

                if self.board.move_piece(start_x, start_y, end_x, end_y):
                    self.current_turn = ColorType.Black if self.current_turn == ColorType.White else ColorType.White
                else:
                    print("Invalid move!")
            except (ValueError, IndexError):
                print("Invalid input! Try again.")


if __name__ == "__main__":
    game = ChessGame()
    game.start_game()