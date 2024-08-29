import chess
import sys
import time

# Custom piece values
piece_value = {
    chess.PAWN: 1,
    chess.KNIGHT: 3.2,   # Custom value for Knights
    chess.BISHOP: 3.3,   # Custom value for Bishops
    chess.ROOK: 5.1,     # Custom value for Rooks
    chess.QUEEN: 8.8,    # Custom value for Queens
    chess.KING: 0        # King value typically remains 0
}

# Simple board evaluation function using custom values
def evaluate_board(board):
    if board.is_checkmate():
        return 9999 if not board.turn else -9999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    
    value = 0
    for piece in board.piece_map().values():
        value += piece_value[piece.piece_type] * (1 if piece.color == chess.WHITE else -1)
    
    return value

# Alpha-Beta Pruning algorithm
def alpha_beta(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    
    if is_maximizing:
        max_eval = -float('inf')
        for move in legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval

# Find the best move using Alpha-Beta
def find_best_move(board):
    best_move = None
    best_value = -float('inf')

    for move in board.legal_moves:
        board.push(move)
        move_value = alpha_beta(board, 3, -float('inf'), float('inf'), False)
        board.pop()
        if move_value > best_value:
            best_value = move_value
            best_move = move

    return best_move

# Game Initialization
def initialize_game():
    board = chess.Board()
    return board

# Validate a move
def validate_move(board, move):
    if move in board.legal_moves:
        return True
    return False

# Offer Draw
def offer_draw(board):
    if board.is_stalemate() or board.is_insufficient_material() or board.is_repetition() or board.halfmove_clock >= 50:
        return True
    return False

# Handle Resignation
def resign():
    print("Player resigned. Opponent wins.")
    return True

# Time control
def start_timer():
    return time.time()

def check_time(start_time, limit):
    elapsed_time = time.time() - start_time
    if elapsed_time >= limit:
        return True
    return False

# UCI loop to handle communication with the GUI
def uci_loop():
    board = initialize_game()
    while True:
        command = input()
        
        if command == "uci":
            print("id name MyAlphaBetaChessEngine")
            print("id author MyName")
            print("uciok")
        
        elif command == "isready":
            print("readyok")
        
        elif command.startswith("position"):
            parts = command.split(" ")
            if "startpos" in parts:
                board.set_fen(chess.STARTING_FEN)
            else:
                fen_index = parts.index("fen") + 1
                fen = " ".join(parts[fen_index:fen_index + 6])
                board.set_fen(fen)
            if "moves" in parts:
                move_index = parts.index("moves") + 1
                for move in parts[move_index:]:
                    board.push_uci(move)
        
        elif command.startswith("go"):
            # Start timing for the move
            start_time = start_timer()
            best_move = find_best_move(board)
            # Check if time control exceeded
            if check_time(start_time, 5 * 60):  # 5 minutes limit as example
                print("Time out. Opponent wins.")
                break
            print(f"bestmove {best_move}")
        
        elif command == "quit":
            break

if __name__ == "__main__":
    uci_loop()
