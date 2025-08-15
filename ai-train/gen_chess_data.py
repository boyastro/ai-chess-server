import chess
import json
import time
import random
import chess.engine

# Đánh giá ngẫu nhiên, thay bằng model nếu có
def random_evaluation(board):
    return random.uniform(-10000, 100000)


# Chọn nước đi tốt nhất bằng Stockfish
def best_move_stockfish(board, engine):
    result = engine.play(board, chess.engine.Limit(time=0.1))
    return result.move

# Sinh một ván cờ tự động
def play_game(game_id, engine):
    board = chess.Board()
    moves = []
    while not board.is_game_over():
        move = best_move_stockfish(board, engine)
        board.push(move)
        fen = board.fen()
        evaluation = random_evaluation(board)  # Có thể thay bằng đánh giá của engine nếu muốn
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

    # Khởi động engine một lần
    engine_path = "/opt/homebrew/bin/stockfish"
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
        for i in range(20):
            game = play_game(f"game_{int(time.time()*1000)}_{i}", engine)
            games.append(game)
            # Lưu ngay sau mỗi ván
            with open("data/games_play.json", "w") as f:
                json.dump(games, f, indent=2)
