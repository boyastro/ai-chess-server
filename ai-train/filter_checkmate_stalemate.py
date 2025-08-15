import json

# Đọc dữ liệu gốc
with open("data/games_play.json", "r") as f:
    games = json.load(f)

# Lọc các trận có reason là CHECKMATE hoặc STALEMATE
filtered_games = [g for g in games if g.get("reason") in ["CHECKMATE", "STALEMATE"]]

# Đọc dữ liệu cũ nếu có
try:
    with open("data/traindatachess.json", "r") as f:
        old_games = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    old_games = []

# Nối dữ liệu mới vào dữ liệu cũ
all_games = old_games + filtered_games

# Ghi ra file mới (nối tiếp)
with open("data/traindatachess.json", "w") as f:
    json.dump(all_games, f, indent=2)