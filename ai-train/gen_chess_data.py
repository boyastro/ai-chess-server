import chess
import json
import time
import random
import chess.engine
from multiprocessing import Pool

# Đánh giá ngẫu nhiên, thay bằng model nếu có
def random_evaluation(board):
    return random.uniform(-10000, 100000)


# Chọn nước đi tốt nhất bằng Stockfish

def play_game(args):
    game_id, engine_path = args
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        board = chess.Board()
        moves = []
        while not board.is_game_over():
            move = engine.play(board, chess.engine.Limit(time=0.1)).move
            board.push(move)
            fen = board.fen()
            evaluation = random_evaluation(board)
            move_dict = {
                "fen": fen,
                "move": {
                    "from": {"x": chess.square_file(move.from_square), "y": chess.square_rank(move.from_square)},
                    "to": {"x": chess.square_file(move.to_square), "y": chess.square_rank(move.to_square)}
                },
                "evaluation": evaluation
            }
            moves.append(move_dict)
        result = board.result()
        reason = board.outcome().termination.name if board.outcome() else "unknown"
        return {
            "id": game_id,
            "moves": moves,
            "result": result,
            "reason": reason,
            "timestamp": int(time.time() * 1000)
        }

# Sinh một ván cờ tự động
def play_game(args):
    game_id, engine_path = args
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        board = chess.Board()
        moves = []
        while not board.is_game_over():
            move = engine.play(board, chess.engine.Limit(time=0.1)).move
            board.push(move)
            fen = board.fen()
            evaluation = random_evaluation(board)
            move_dict = {
                "fen": fen,
                "move": {
                    "from": {"x": chess.square_file(move.from_square), "y": chess.square_rank(move.from_square)},
                    "to": {"x": chess.square_file(move.to_square), "y": chess.square_rank(move.to_square)}
                },
                "evaluation": evaluation
            }
            moves.append(move_dict)
        result = board.result()
        reason = board.outcome().termination.name if board.outcome() else "unknown"
        return {
            "id": game_id,
            "moves": moves,
            "result": result,
            "reason": reason,
            "timestamp": int(time.time() * 1000)
        }

if __name__ == "__main__":
    # Đọc dữ liệu cũ nếu có
    try:
        with open("data/games_play.json", "r") as f:
            games = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        games = []

    engine_path = "/opt/homebrew/bin/stockfish"
    num_games = 20
    num_workers = 4  # Số tiến trình song song, tùy CPU

    args_list = [(f"game_{int(time.time()*1000)}_{i}", engine_path) for i in range(num_games)]
    with Pool(num_workers) as pool:
        new_games = pool.map(play_game, args_list)
        games.extend(new_games)
        with open("data/games_play.json", "w") as f:
            json.dump(games, f, indent=2)
