from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from typing import Dict
from .game import Game2048

app = FastAPI(title="2048 API")

# in-memory store: game_id -> Game2048
games: Dict[str, Game2048] = {}

class NewGameResponse(BaseModel):
    game_id: str
    board: list
    score: int

class MoveRequest(BaseModel):
    action: str

class MoveResponse(BaseModel):
    board: list
    score: int
    moved: bool
    game_over: bool

@app.post("/api/new", response_model=NewGameResponse)
def new_game():
    g = Game2048()
    game_id = str(uuid.uuid4())
    games[game_id] = g
    return NewGameResponse(game_id=game_id, board=g.to_list(), score=g.score)

@app.get("/api/state/{game_id}", response_model=NewGameResponse)
def get_state(game_id: str):
    g = games.get(game_id)
    if not g:
        raise HTTPException(status_code=404, detail="game not found")
    return NewGameResponse(game_id=game_id, board=g.to_list(), score=g.score)

@app.post("/api/move/{game_id}", response_model=MoveResponse)
def do_move(game_id: str, req: MoveRequest):
    g = games.get(game_id)
    if not g:
        raise HTTPException(status_code=404, detail="game not found")
    if g.is_game_over():
        return MoveResponse(board=g.to_list(), score=g.score, moved=False, game_over=True)
    if req.action not in ("up","down","left","right"):
        raise HTTPException(status_code=400, detail="invalid action")
    moved, _ = g.move(req.action)
    return MoveResponse(board=g.to_list(), score=g.score, moved=moved, game_over=g.is_game_over())
