import time
import chess
import chess.svg
import random

# Initialize Zobrist keys
ZOB_KEYS = {
    'pieces': {},
    'castling': {},
    'en_passant': {},
    'turn': None
}
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
DEPTH = 4  # Adjust depth as needed, deeper searches will take more time
random.seed(42) # Seed for reproducibility
positions_evaluated = 0
transposition_table = {} # Transposition table (using FEN string for simplicity)

# Generate keys for pieces on each square
for piece in chess.PIECE_TYPES:
    for color in [chess.WHITE, chess.BLACK]:
        for square in chess.SQUARES:
            ZOB_KEYS['pieces'][(piece, color, square)] = random.getrandbits(64)

# Generate keys for castling rights
for color in [chess.WHITE, chess.BLACK]:
    for castling in ['K', 'Q']:
        ZOB_KEYS['castling'][(color, castling)] = random.getrandbits(64)

# Generate keys for en passant squares
for square in chess.SQUARES:
    ZOB_KEYS['en_passant'][square] = random.getrandbits(64)

# Generate key for the side to move
ZOB_KEYS['turn'] = random.getrandbits(64)

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

def compute_zobrist_hash(board):
    zobrist_hash = 0

    # Pieces
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            zobrist_hash ^= ZOB_KEYS['pieces'][(piece.piece_type, piece.color, square)]

    # Castling rights
    for color in [chess.WHITE, chess.BLACK]:
        if board.has_kingside_castling_rights(color):
            zobrist_hash ^= ZOB_KEYS['castling'][(color, 'K')]
        if board.has_queenside_castling_rights(color):
            zobrist_hash ^= ZOB_KEYS['castling'][(color, 'Q')]

    # En passant square
    if board.ep_square:
        zobrist_hash ^= ZOB_KEYS['en_passant'][board.ep_square]

    # Side to move
    if board.turn == chess.WHITE:
        zobrist_hash ^= ZOB_KEYS['turn']

    return zobrist_hash

def negamax_alpha_beta(board, depth, alpha, beta, move_history):
    global positions_evaluated
    zobrist_hash = compute_zobrist_hash(board)
    
    # Check transposition table
    if zobrist_hash in transposition_table and transposition_table[zobrist_hash]['depth'] >= depth:
        return transposition_table[zobrist_hash]['score']
    
    if depth == 0 or board.is_game_over():
        positions_evaluated += 1
        score = evaluate_board(board)
        # Store the score in the transposition table using Zobrist hash as the key
        transposition_table[zobrist_hash] = {'score': score, 'depth': depth, 'move': move_history[0] if depth == DEPTH else None}
        return score

    max_score = float('-inf')
    legal_moves = list(board.legal_moves)
    # Simple heuristic for move ordering: prioritize captures and promotions
    legal_moves.sort(key=lambda move: (board.is_capture(move), move.promotion is not None), reverse=True)
    for move in legal_moves:
        board.push(move)
        score = -negamax_alpha_beta(board, depth - 1, -beta, -alpha, move_history + [move])
        board.pop()
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                move_history[0] = move  # Store the best move at root
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    # Update transposition table
    transposition_table[zobrist_hash] = {'score': max_score, 'depth': depth, 'move': move_history[0] if depth == DEPTH else None}
    return max_score

def find_best_move_with_iterative_deepening(board, max_depth):
    best_move = None
    move_history = [None]  # Placeholder for the best move
    alpha = float('-inf')
    beta = float('inf')
    for depth in range(1, max_depth + 1):
        global positions_evaluated
        positions_evaluated = 0
        negamax_alpha_beta(board, depth, alpha, beta, move_history)
        best_move = move_history[0]
    return best_move

def play_self_game(depth=3):
    board = chess.Board()
    while not board.is_game_over():
        start_time = time.time()
        move = find_best_move_with_iterative_deepening(board, depth)
        end_time = time.time()
        if move:
            print(f"Move: {move} | Time Taken: {end_time - start_time:.2f} seconds")
            board.push(move)
        else:
            print("No move found or game over.")
            break
        print(board)
    print("Game Over. Result:", board.result())

def main():
    # Play a game against itself
    print("Playing a game against itself...")
    play_self_game(depth=3)  # You can adjust the depth based on your testing needs


if __name__ == "__main__":
    main()
