"""
加载训练好的模型文件（与 train.py 中的网络结构一致），
然后通过后端的 REST API 对一个远程/本地游戏进行自动下棋示例。
"""
import argparse
import torch
import numpy as np
import requests
from train import board_to_input, Net, device

ACTION_MAP = ["up","down","left","right"]

def play(model_path, base_url):
    net = Net(16)
    net.load_state_dict(torch.load(model_path, map_location=device))
    net.eval()
    r = requests.post(f"{base_url}/api/new")
    r.raise_for_status()
    js = r.json()
    game_id = js["game_id"]
    print("Started game", game_id)
    while True:
        r = requests.get(f"{base_url}/api/state/{game_id}")
        r.raise_for_status()
        state = r.json()
        board = np.array(state["board"])
        s = board_to_input(board)
        with torch.no_grad():
            t = torch.tensor(s, dtype=torch.float32).unsqueeze(0)
            q = net(t)
            action_idx = int(torch.argmax(q[0]).cpu().numpy())
        action = ACTION_MAP[action_idx]
        r = requests.post(f"{base_url}/api/move/{game_id}", json={"action": action})
        r.raise_for_status()
        mr = r.json()
        print("action", action, "moved", mr["moved"], "score", mr["score"])
        if mr["game_over"]:
            print("Game over. Final score:", mr["score"])
            break

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--game-url", default="http://localhost:8000")
    args = p.parse_args()
    play(args.model, args.game_url)
