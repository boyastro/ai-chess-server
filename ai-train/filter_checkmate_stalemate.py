import json

# Đọc dữ liệu gốc
with open("data/games_play.json", "r") as f:
    games = json.load(f)

# Lọc các trận có reason là CHECKMATE hoặc STALEMATE
filtered_games = [g for g in games if g.get("reason") in ["CHECKMATE", "STALEMATE"]]

# Ghi ra file mới
with open("data/traindatachess.json", "w") as f:
    json.dump(filtered_games, f, indent=2)
