import React, { useEffect, useState } from "react";

const apiBase =
  process.env.REACT_APP_API_URL ||
  (typeof window !== "undefined" ? window.location.origin : "");
const API = `${apiBase.replace(/\/$/, "")}/api`;

export default function Game() {
  const [gameId, setGameId] = useState(null);
  const [board, setBoard] = useState([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    newGame();
    const onKey = (e) => {
      if (e.key === "ArrowUp") move("up");
      if (e.key === "ArrowDown") move("down");
      if (e.key === "ArrowLeft") move("left");
      if (e.key === "ArrowRight") move("right");
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  async function newGame() {
    try {
      const r = await fetch(`${API}/new`, { method: "POST" });
      if (!r.ok) throw new Error(`Request failed: ${r.status}`);
      const j = await r.json();
      setGameId(j.game_id);
      setBoard(j.board);
      setScore(j.score);
      setGameOver(false);
      setError("");
    } catch (e) {
      console.error("Failed to start new game", e);
      setError("无法连接服务器，请确认后端已启动并允许访问。");
    }
  }

  async function move(action) {
    if (!gameId) return;
    try {
      const r = await fetch(`${API}/move/${gameId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action })
      });
      if (!r.ok) throw new Error(`Request failed: ${r.status}`);
      const j = await r.json();
      setBoard(j.board);
      setScore(j.score);
      setGameOver(j.game_over);
      setError("");
    } catch (e) {
      console.error("Failed to make move", e);
      setError("请求失败，请检查网络或后端服务。");
    }
  }

  return (
    <div>
      <div style={{ marginBottom: 10 }}>
        <button onClick={() => newGame()}>New Game</button>
        <span style={{ marginLeft: 10 }}>Score: {score}</span>
      </div>
      <div style={{ display: "inline-block", background: "#bbada0", padding: 10, borderRadius: 6 }}>
        {board.map((row, i) => (
          <div key={i} style={{ display: "flex" }}>
            {row.map((cell, j) => (
              <div key={j} style={{
                width: 60, height: 60, margin: 6, background: "#cdc1b4",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 20, fontWeight: "bold", borderRadius: 4
              }}>
                {cell === 0 ? "" : cell}
              </div>
            ))}
          </div>
        ))}
      </div>
      {gameOver && <div style={{ marginTop: 10 }}>Game Over</div>}
      {error && <div style={{ marginTop: 10, color: "red" }}>{error}</div>}
      <div style={{ marginTop: 10 }}>
        <button onClick={() => move("up")}>Up</button>
        <button onClick={() => move("down")}>Down</button>
        <button onClick={() => move("left")}>Left</button>
        <button onClick={() => move("right")}>Right</button>
      </div>
    </div>
  );
}
