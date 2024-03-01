import chess
import time

class MyChessEngine:
    def __init__(self):
        self.piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}
        # The rest of the piece and position scores are initialized similarly
        self.knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]] # Complete the initialization as in the original code
        self.bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]
        self.rook_scores = [
    [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
    [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
    [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]
]
        self.queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]
        self.pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]
        self.CHECKMATE = float('inf')
        self.STALEMATE = 0
        self.DEPTH = 3  # Adjustable depth

    def evaluate_board(self, board):
        if board.is_checkmate():
            if board.turn:
                return -self.CHECKMATE  # Black wins
            else:
                return self.CHECKMATE  # White wins
        if board.is_stalemate() or board.is_insufficient_material():
            return self.STALEMATE

        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_type = piece.symbol().upper()
                color = piece.color
                if piece_type != 'K':  # Skip king
                    piece_position_score = self.get_piece_position_score(piece, square)
                    if color == chess.WHITE:
                        score += self.piece_score[piece_type] + piece_position_score
                    else:
                        score -= self.piece_score[piece_type] + piece_position_score
        return score

    def get_piece_position_score(self, piece, square):
        row, col = square // 8, square % 8
        if piece.symbol() == 'N':
            return self.knight_scores[row][col] if piece.color == chess.WHITE else self.knight_scores[7-row][col]
        elif piece.symbol() == 'B':
            return self.bishop_scores[row][col] if piece.color == chess.WHITE else self.bishop_scores[7-row][col]
        elif piece.symbol() == 'R':
            return self.rook_scores[row][col] if piece.color == chess.WHITE else self.rook_scores[7-row][col]
        elif piece.symbol() == 'Q':
            return self.queen_scores[row][col] if piece.color == chess.WHITE else self.queen_scores[7-row][col]
        elif piece.symbol().upper() == 'P':
            return self.pawn_scores[row][col] if piece.color == chess.WHITE else self.pawn_scores[7-row][col]
        return 0

    def find_best_move(self, board, depth):
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Prioritize captures and promotions in move ordering
        legal_moves = list(board.legal_moves)
        legal_moves.sort(key=lambda move: (board.is_capture(move), move.promotion is not None), reverse=True)

        for move in legal_moves:
            board.push(move)
            score = -self.negamax_alpha_beta(board, depth - 1, -beta, -alpha)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)

        return best_move

    def negamax_alpha_beta(self, board, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        max_score = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            score = -self.negamax_alpha_beta(board, depth - 1, -beta, -alpha)
            board.pop()
            max_score = max(max_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        return max_score

    def play_self_game(self, depth=3):
        board = chess.Board()
        while not board.is_game_over():
            start_time = time.time()
            move = self.find_best_move(board, depth)
            end_time = time.time()
            if move:
                print(f"Move: {move} | Time Taken: {end_time - start_time:.2f} seconds")
                board.push(move)
            else:
                print("No move found or game over.")
                break
            print(board)
        print("Game Over. Result:", board.result())

# Example usage
if __name__ == "__main__":
    engine = MyChessEngine()
    print("Playing a game against itself...")
    engine.play_self_game(depth=4)  # Adjust the depth as needed
