import sys
import chess
from MyChessEngine import MyChessEngine
import chess.engine

def simulate_uci_commands(engine, board):
    """
    Simulate UCI commands to make the engine play against itself.
    """
    print("Initializing self-play session.")
    
    # Simulate "uci" and "isready" commands
    print("Engine ID: MyPythonChessEngine, Author: MyName")
    print("Engine ready and waiting for commands.")

    while not board.is_game_over(claim_draw=True):
        # Simulate "position" command
        fen = board.fen()
        print(f"Current position: {fen}")

        # Simulate "go" command
        best_move = engine.find_best_move(board, depth=4)  # Adjust depth as needed
        if best_move:
            print(f"Best move by engine: {best_move}")
            move = best_move
            if move in board.legal_moves:
                board.push(move)
                print(board)
            else:
                print("Engine recommended an illegal move, stopping.")
                break
        else:
            print("Engine did not return a move, stopping.")
            break

    print("Game Over. Result:", board.result())

def main():
    board = chess.Board()
    engine = MyChessEngine()  # Initialize your engine

    simulate_uci_commands(engine, board)

if __name__ == "__main__":
    main()