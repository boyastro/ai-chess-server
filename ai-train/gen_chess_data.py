import chess
import json
import time
import random

# Đánh giá ngẫu nhiên, thay bằng model nếu có
def random_evaluation(board):
    return random.uniform(-10000, 100000)

# Chọn nước đi ngẫu nhiên
def random_move(board):
    return random.choice(list(board.legal_moves))

# Sinh một ván cờ tự động
def play_game(game_id):
    board = chess.Board()
    moves = []
    while not board.is_game_over():
        move = random_move(board)
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

    # Thêm dữ liệu mới
    for i in range(10):
        games.append(play_game(f"game_{int(time.time()*1000)}_{i}"))

    # Ghi lại toàn bộ dữ liệu
    with open("data/games_play.json", "w") as f:
        json.dump(games, f, indent=2)
