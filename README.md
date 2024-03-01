# Chess Engine with Python-Chess

This project is a simple chess engine implemented using the Python-Chess library. It evaluates chess board positions and uses the NegaMax algorithm with alpha-beta pruning to find the best move.

## Features

- Evaluation of chess board positions based on piece values and positional scores for different types of pieces.
- NegaMax algorithm implementation with alpha-beta pruning to efficiently search the best moves.
- Utilizes Python-Chess for chess board management and move generation.

## Installation

Before you can run this chess engine, you need to install Python and the necessary Python packages. The primary dependency is the `python-chess` package.

1. Ensure you have Python installed on your system. Python 3.6 or higher is recommended.

2. Install the `python-chess` library using pip:

   ```bash
   pip install python-chess
   ```

## Usage
To use the chess engine, simply run the Python script. The engine will automatically play a game against itself, displaying each move and the final board position.

   ```bash
   python Python-ChessAI.py
   ```

## How it works

- __Piece Values__: Each piece type (Pawn, Knight, Bishop, Rook, Queen) is assigned a base value. These values are used to evaluate the material balance on the board.
- __Positional Scores__: Each piece type has a positional score table that gives bonus points based on the piece's position on the board. These scores encourage the engine to improve the positioning of its pieces.
- __Board Evaluation__: Combines the material balance with the positional scores to get a total evaluation of the board from the engine's perspective.
- __NegaMax with Alpha-Beta Pruning__: This algorithm is a variant of the minimax algorithm optimized for two-player games like chess. Alpha-beta pruning is used to reduce the number of nodes evaluated in the search tree, improving efficiency.