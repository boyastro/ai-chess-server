import subprocess
import sys

steps = [
    [sys.executable, "ai-train/gen_chess_data.py"],
    [sys.executable, "ai-train/filter_checkmate_stalemate.py"],
    [sys.executable, "ai-train/train_move_model.py"],
]

try:
    repeat = int(input("Nhập số lần lặp lại pipeline (mặc định 1): ") or "1")
except Exception:
    repeat = 1

for r in range(1, repeat+1):
    print(f"\n=== Lần chạy pipeline thứ {r}/{repeat} ===")
    for i, cmd in enumerate(steps, 1):
        print(f"\n--- Bước {i}: {' '.join(cmd)} ---")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            print(f"Lỗi ở bước {i}, dừng quy trình.")
            sys.exit(result.returncode)
print(f"\nĐã hoàn tất {repeat} lần chạy pipeline!")
