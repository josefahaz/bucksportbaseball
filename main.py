"""FastAPI backend for Bucksport Youth Softball/Baseball program."""
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import get_session, init_db
from models import Event, Player, Team

app = FastAPI(title="Bucksport Baseball/Softball API", version="0.1.0")

# Allow Wix domain to call the API (update once your Wix domain is known)
origins = [
    "https://*.wixsite.com",
    "http://localhost:3000",  # for local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# ----------------- Team endpoints -----------------
@app.post("/teams", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team: Team, session: Session = Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@app.get("/teams", response_model=List[Team])
def read_teams(session: Session = Depends(get_session)):
    return session.exec(select(Team)).all()


# ----------------- Player endpoints -----------------
@app.post("/players", response_model=Player, status_code=status.HTTP_201_CREATED)
def register_player(player: Player, session: Session = Depends(get_session)):
    session.add(player)
    session.commit()
    session.refresh(player)
    return player


@app.get("/players/{player_id}", response_model=Player)
def read_player(player_id: int, session: Session = Depends(get_session)):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


# ----------------- Event endpoints -----------------
@app.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: Event, session: Session = Depends(get_session)):
    if event.end_time <= event.start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@app.get("/events", response_model=List[Event])
def read_events(team_id: int | None = None, session: Session = Depends(get_session)):
    query = select(Event)
    if team_id is not None:
        query = query.where(Event.team_id == team_id)
    return session.exec(query.order_by(Event.start_time)).all()
