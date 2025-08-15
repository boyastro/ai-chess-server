import tensorflow as tf
# BƯỚC 1: Luôn bật Eager Execution. Nó cần thiết cho TF 2.x và không ảnh hưởng đến việc load model cũ.
tf.compat.v1.enable_eager_execution()

import json
import numpy as np
import chess
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

# Đọc dữ liệu từ games.json
with open('data/traindatachess.json', 'r') as f:
    games = json.load(f)

# Tiền xử lý: lấy FEN và move
fen_list = []
move_quality_labels = []  # 1: tốt (dẫn đến thắng), 0: xấu (dẫn đến thua), 0.5: hòa
for game in games:
    result = game.get('result')
    if result in ['1-0', '0-1', '1/2-1/2'] and 'moves' in game:
        if result == '1-0':
            label = 1.0
        elif result == '0-1':
            label = 0.0
        else:
            label = 0.5
        for m in game['moves']:
            fen = m.get('fen')
            if fen: # Chỉ cần fen để đánh giá thế cờ
                fen_list.append(fen)
                move_quality_labels.append(label)

# Chuyển FEN thành ma trận 8x8, mỗi ô là số đại diện cho quân cờ
def fen_to_matrix(fen):
    board = chess.Board(fen)
    piece_map = board.piece_map()
    matrix = np.zeros((8, 8), dtype=int)
    for square, piece in piece_map.items():
        row = 7 - (square // 8)
        col = square % 8
        matrix[row, col] = piece.piece_type * (1 if piece.color else -1)
    return matrix.flatten()

# Chuyển FEN thành ma trận
X = np.array([fen_to_matrix(fen) for fen in fen_list])
y = np.array(move_quality_labels)

# Chia tập train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load lại mô hình cũ nếu có, nếu không thì tạo mới
MODEL_PATH = 'model_move.h5'
model = None
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print("Đã load lại mô hình cũ để tiếp tục huấn luyện.")
else:
    model = Sequential([
        Dense(256, activation='relu', input_shape=(X.shape[1],)),
        Dense(128, activation='relu'),
        Dense(1, activation='sigmoid') # Sigmoid hợp lý vì output là [0, 1]
    ])
    print("Tạo mới mô hình để huấn luyện.")

# BƯỚC 2: Compile lại model (kể cả khi đã load) và dùng hàm loss phù hợp hơn
# Vì nhãn là 0, 0.5, 1 (giá trị thực), đây là bài toán hồi quy -> dùng 'mean_squared_error'
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

print("Bắt đầu huấn luyện mô hình...")
model.fit(X_train, y_train, epochs=10, batch_size=64, validation_split=0.1)

# Đánh giá mô hình
loss, acc = model.evaluate(X_test, y_test)
print(f"Neural Network move quality evaluation - Loss: {loss:.4f}, Accuracy: {acc:.4f}")

# Lưu mô hình sau khi huấn luyện
model.save(MODEL_PATH)
print(f"Đã lưu mô hình vào file {MODEL_PATH}")