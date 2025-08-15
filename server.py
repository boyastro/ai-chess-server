import tensorflow as tf
import chess
import numpy as np
from flask import Flask, request, jsonify

# Load model
model = tf.keras.models.load_model("model_move_quality.h5")

app = Flask(__name__)

def board_to_input(board: chess.Board):
    # TODO: Chuyển trạng thái bàn cờ sang input cho model
    # Ví dụ: encode FEN hoặc mảng 1D tuỳ theo model
    # Dưới đây là placeholder, cần chỉnh lại cho đúng với model
    return np.zeros((model.input_shape[1],), dtype=np.float32)

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
