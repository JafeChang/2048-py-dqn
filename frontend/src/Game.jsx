import React, { useEffect, useState } from "react";

const API = "http://localhost:8000/api";

export default function Game() {
  const [gameId, setGameId] = useState(null);
  const [board, setBoard] = useState([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]);
  const [score, setScore] = useState(0);
  const [gameOver, setGameOver] = useState(false);

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
    const r = await fetch(`${API}/new`, { method: "POST" });
    const j = await r.json();
    setGameId(j.game_id);
    setBoard(j.board);
    setScore(j.score);
    setGameOver(false);
  }

  async function move(action) {
    if (!gameId) return;
    const r = await fetch(`${API}/move/${gameId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action })
    });
    const j = await r.json();
    setBoard(j.board);
    setScore(j.score);
    setGameOver(j.game_over);
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
      <div style={{ marginTop: 10 }}>
        <button onClick={() => move("up")}>Up</button>
        <button onClick={() => move("down")}>Down</button>
        <button onClick={() => move("left")}>Left</button>
        <button onClick={() => move("right")}>Right</button>
      </div>
    </div>
  );
}
