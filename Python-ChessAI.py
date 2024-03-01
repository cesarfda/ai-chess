import chess
import chess.svg

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
# Modify piece_position_scores to use the python-chess square representation (0 to 63)
# Adjusted to python-chess's square indexing which goes from 0 (a1) to 63 (h8)

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

CHECKMATE = float('inf')
STALEMATE = 0
DEPTH = 3  # Adjust depth as needed, deeper searches will take more time

def evaluate_board(board):
    """
    Evaluate the board score.
    """
    if board.is_checkmate():
        if board.turn:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE  # White wins
    if board.is_stalemate():
        return STALEMATE
    if board.is_insufficient_material():
        return STALEMATE

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            piece_type = piece.symbol().upper()
            color = piece.color
            if piece_type != 'K':  # Skip king since its score is constant
                piece_position_score = get_piece_position_score(piece, square)
                if color == chess.WHITE:
                    score += piece_score[piece_type] + piece_position_score
                else:
                    score -= piece_score[piece_type] + piece_position_score
    return score

def get_piece_position_score(piece, square):
    """
    Get specific piece position score based on the provided scoring tables.
    """
    row = square // 8
    col = square % 8

    if piece.symbol() == 'N':
        return knight_scores[row][col] if piece.color == chess.WHITE else knight_scores[::-1][row][col]
    elif piece.symbol() == 'B':
        return bishop_scores[row][col] if piece.color == chess.WHITE else bishop_scores[::-1][row][col]
    elif piece.symbol() == 'R':
        return rook_scores[row][col] if piece.color == chess.WHITE else rook_scores[::-1][row][col]
    elif piece.symbol() == 'Q':
        return queen_scores[row][col] if piece.color == chess.WHITE else queen_scores[::-1][row][col]
    elif piece.symbol().upper() == 'P':
        return pawn_scores[row][col] if piece.color == chess.WHITE else pawn_scores[::-1][row][col]
    return 0  # No additional score for kings or unrecognized pieces

def find_best_move(board, depth):
    """
    Find the best move based on negamax with alpha-beta pruning.
    """
    best_move = None
    best_score = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    # Corrected move ordering - prioritize captures, and check for promotions
    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda move: (board.is_capture(move), move.promotion is not None), reverse=True)

    for move in legal_moves:
        board.push(move)
        score = -negamax_alpha_beta(board, depth - 1, -beta, -alpha)
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
    
    return best_move

def negamax_alpha_beta(board, depth, alpha, beta):
    """
    NegaMax algorithm with alpha-beta pruning.
    """
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    max_score = float('-inf')
    for move in board.legal_moves:
        board.push(move)
        score = -negamax_alpha_beta(board, depth - 1, -beta, -alpha)
        board.pop()
        max_score = max(max_score, score)
        alpha = max(alpha, score)
        if alpha >= beta:
            break
    return max_score

def main():
    board = chess.Board()
    turn = 0  # Keep track of who's turn it is; 0 for white, 1 for black
    
    while not board.is_game_over():
        print("Current board:")
        print(board)
        
        move = find_best_move(board, DEPTH)
        
        if move:
            print(f"{'White' if turn == 0 else 'Black'} moves: {move}")
            board.push(move)
        else:
            print("No move found. Game over.")
            break
        
        # Switch turn
        turn = 1 - turn

    print("Final board position:")
    print(board)
    result = "1/2-1/2" if board.is_stalemate() else "1-0" if board.result() == "1-0" else "0-1"
    print(f"Game over. Result: {result}")


if __name__ == "__main__":
    main()
