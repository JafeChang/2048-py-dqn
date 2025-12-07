# 2048 - 前后端分离 + PyTorch 自动训练示例

这是一个示例项目，实现了前后端分离的 2048 游戏（React 前端 + FastAPI 后端），并提供了一个基于 PyTorch 的简单 DQN 训练脚本与自动下棋脚本。

快速目录
- backend/
  - app/
    - main.py
    - game.py
    - __init__.py
  - requirements.txt
  - train.py
  - play_via_api.py
- frontend/
  - package.json
  - public/
    - index.html
  - src/
    - index.js
    - App.jsx
    - Game.jsx
- models/ (你选择将 models 提交到仓库，此处包含占位文件)
- LICENSE
- .gitignore

快速运行（macOS）
1. 克隆或在本地创建并进入项目目录：
   git clone https://github.com/JafeChang/2048-py-dqn.git
   cd 2048-py-dqn

2. 后端（FastAPI）
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   后端默认地址: http://localhost:8000

3. 前端（React）
   cd ../frontend
   npm install
   npm start
   前端默认地址: http://localhost:3000

4. 训练（可选）
   在 backend 虚拟环境中：
   python3 train.py --episodes 2000 --save-dir ../models
   训练结束后模型会保存到 models/ 下。

5. 使用训练模型自动下棋（play via API）
   python3 play_via_api.py --model ../models/dqn_final.pth --game-url http://localhost:8000

注意
- 你选择把 models/ 提交到仓库：如果模型文件很大，建议使用 Git LFS、Releases 或外部存储。
