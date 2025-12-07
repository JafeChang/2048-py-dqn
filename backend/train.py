"""
简单的 DQN baseline 用于 2048 的教学示例。
- 该实现是简化版：小型网络、单线程训练、最低限度的 replay buffer。
- 适合快速上手与演示。
"""
import argparse
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from app.game import Game2048
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Net(nn.Module):
    def __init__(self, input_size, hidden=128, output_size=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, output_size)
        )
    def forward(self, x):
        return self.net(x)

def board_to_input(board):
    b = np.array(board, dtype=float)
    b[b == 0] = 0
    nonzero = b > 0
    b[nonzero] = np.log2(b[nonzero])
    return b.flatten()

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buf = []
        self.capacity = capacity
    def push(self, transition):
        if len(self.buf) >= self.capacity:
            self.buf.pop(0)
        self.buf.append(transition)
    def sample(self, batch_size):
        return random.sample(self.buf, min(batch_size, len(self.buf)))
    def __len__(self):
        return len(self.buf)

def train(args):
    env = Game2048()
    input_size = env.size * env.size
    net = Net(input_size).to(device)
    target = Net(input_size).to(device)
    target.load_state_dict(net.state_dict())
    opt = optim.Adam(net.parameters(), lr=1e-3)
    replay = ReplayBuffer(20000)
    gamma = 0.99
    eps = 1.0
    min_eps = 0.05
    eps_decay = 0.9995

    for ep in range(args.episodes):
        g = Game2048()
        state = board_to_input(g.board)
        total_reward = 0
        steps = 0
        while not g.is_game_over():
            if random.random() < eps:
                action_idx = random.randrange(4)
            else:
                with torch.no_grad():
                    s = torch.tensor(state, dtype=torch.float32).to(device).unsqueeze(0)
                    q = net(s)
                    action_idx = int(torch.argmax(q[0]).cpu().numpy())
            action = ["up","down","left","right"][action_idx]
            moved, reward = g.move(action)
            next_state = board_to_input(g.board)
            r = reward if moved else -1.0
            replay.push((state, action_idx, r, next_state, g.is_game_over()))
            state = next_state
            total_reward += r
            steps += 1

            if len(replay) >= 128:
                batch = replay.sample(64)
                states = torch.tensor([b[0] for b in batch], dtype=torch.float32).to(device)
                actions = torch.tensor([b[1] for b in batch], dtype=torch.int64).to(device)
                rewards = torch.tensor([b[2] for b in batch], dtype=torch.float32).to(device)
                next_states = torch.tensor([b[3] for b in batch], dtype=torch.float32).to(device)
                dones = torch.tensor([b[4] for b in batch], dtype=torch.float32).to(device)

                q_values = net(states)
                q_val = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
                with torch.no_grad():
                    next_q = target(next_states).max(1)[0]
                expected = rewards + gamma * next_q * (1 - dones)
                loss = nn.functional.mse_loss(q_val, expected)
                opt.zero_grad()
                loss.backward()
                opt.step()

        eps = max(min_eps, eps * eps_decay)
        if ep % 20 == 0:
            target.load_state_dict(net.state_dict())
        if ep % 100 == 0:
            print(f"Episode {ep} reward={total_reward:.1f} steps={steps} eps={eps:.3f}")
        if (ep + 1) % args.save_every == 0:
            os.makedirs(args.save_dir, exist_ok=True)
            path = os.path.join(args.save_dir, f"dqn_ep{ep+1}.pth")
            torch.save(net.state_dict(), path)
            print("Saved model", path)
    os.makedirs(args.save_dir, exist_ok=True)
    final_path = os.path.join(args.save_dir, "dqn_final.pth")
    torch.save(net.state_dict(), final_path)
    print("Training complete. Model saved to", final_path)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--episodes", type=int, default=2000)
    p.add_argument("--save-every", type=int, default=500)
    p.add_argument("--save-dir", type=str, default="models")
    args = p.parse_args()
    train(args)
