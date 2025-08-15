import tensorflow as tf
import chess
import numpy as np
from flask import Flask, request, jsonify

# Load model
model = tf.keras.models.load_model("model_move.h5")

app = Flask(__name__)

def board_to_input(board: chess.Board):
    # Chuyển trạng thái bàn cờ sang mảng 1D 64 số, giống như khi train
    piece_map = board.piece_map()
    matrix = np.zeros((8, 8), dtype=int)
    for square, piece in piece_map.items():
        row = 7 - (square // 8)
        col = square % 8
        matrix[row, col] = piece.piece_type * (1 if piece.color else -1)
    return matrix.flatten()

@app.route("/bestmove", methods=["POST"])
def best_move():
    fen = request.json.get("fen")
    try:
        board = chess.Board(fen)
        moves = list(board.legal_moves)
        best_score = -float("inf")
        best_move = None

        for move in moves:
            board.push(move)
            input_data = board_to_input(board)
            score = model.predict(np.array([input_data]))[0][0]
            if score > best_score:
                best_score = score
                best_move = move.uci()
            board.pop()

        return jsonify({"best_move": best_move, "score": float(best_score)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
