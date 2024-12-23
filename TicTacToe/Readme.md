
# Tic Tac Toe Game

This repository contains the implementation of a Tic Tac Toe game in Python. The game is designed with modular and scalable code principles, incorporating patterns and SOLID design principles.

---

## Patterns Used

1. **Enum Pattern**:
   - The `PlayerType` class uses the `Enum` pattern to define constant values representing cell states (`EMPTY`, `X`, `O`, etc.).

2. **Strategy Pattern**:
   - The game supports multiple player types (`PlayerType.X`, `PlayerType.O`, etc.). Each player's behavior is encapsulated independently.

3. **Model-View-Controller (MVC)**:
   - **Model**: `PlaneBoard` handles the game state and rules.
   - **View**: `print_board` provides a visual representation of the board.
   - **Controller**: `TicTacToe` manages player turns, inputs, and game flow.

4. **Iterator Pattern**:
   - Iterates over rows, columns, and diagonals in `check_winner` to find a winner.

5. **Input Validation**:
   - Ensures user inputs are numeric, within range, and target cells are empty.

---

## SOLID Principles Applied

1. **Single Responsibility Principle (SRP)**:
   - Each class has one responsibility:
     - `PlaneBoard`: Handles board state and logic.
     - `TicTacToe`: Manages game flow and player interactions.

2. **Open-Closed Principle (OCP)**:
   - Adding new symbols (e.g., `PlayerType.A`, `PlayerType.B`) is easy without modifying existing code.

3. **Liskov Substitution Principle (LSP)**:
   - Any `PlayerType` value can be used interchangeably without breaking functionality.

4. **Interface Segregation Principle (ISP)**:
   - Responsibilities are distributed across classes, avoiding bloated methods.

5. **Dependency Inversion Principle (DIP)**:
   - `TicTacToe` depends on `PlaneBoard` abstraction, not concrete implementation.

---

## UML Diagram

Below is a detailed UML diagram description:

```
+---------------------+                  +---------------------+
|     PlayerType      |                  |    PlaneBoard       |
|---------------------|                  |---------------------|
| + EMPTY: Enum       | 1   manages   1 | - size: int         |
| + X: Enum           +----------------->| - board: List[List] |
| + O: Enum           |                  |---------------------|
| + A: Enum           |                  | + __init__(size)    |
| + B: Enum           |                  | + print_board()     |
+---------------------+                  | + make_move(x, y)   |
                                         | + check_winner()    |
                                         | + is_draw()         |
                                         +---------------------+
                                                   ^
                                                   |
                                                   |
                                          +------------------+
                                          |   TicTacToe      |
                                          |------------------|
                                          | - board: PlaneBoard |
                                          | - players: List[PlayerType] |
                                          | - current_player: int       |
                                          |-----------------------------|
                                          | + __init__(size, players)   |
                                          | + start_game()              |
                                          | + get_player_move()         |
                                          +-----------------------------+
```

### UML Explanation
1. **Composition** (Solid Line with Diamond): 
   - `PlaneBoard` is composed of `PlayerType` values in its grid.
   - `TicTacToe` is composed of a `PlaneBoard` instance.

2. **Association** (Solid Line):
   - `PlayerType` is associated with `PlaneBoard` to represent cell states.

3. **Generalization** (Arrow with Open Triangle):
   - `PlaneBoard` and `TicTacToe` interact, but their responsibilities are independent.

---

## Type Annotations in Python

Yes, Python allows the definition of types using type hints introduced in [PEP 484](https://peps.python.org/pep-0484/).

For example, in the code:

```python
board: List[PlayerType]
```

- `List[PlayerType]` indicates that `board` is a list containing elements of type `PlayerType`.

Type hints improve code readability and enable static type checking using tools like `mypy`. However, they are not enforced at runtime.

---

## How to Run the Code

1. Clone the repository.
2. Run the Python file:
   ```bash
   python tic_tac_toe.py
   ```
3. Follow the prompts to play the game.

---

## Future Enhancements

1. Add support for customizable board sizes.
2. Implement a GUI using libraries like Tkinter or PyQt.
3. Enhance input validation and error handling.
