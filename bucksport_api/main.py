"""FastAPI backend for Bucksport Youth Softball/Baseball program."""
from datetime import datetime
from typing import List
import logging
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from database import get_session, init_db
from models import Event, Player, PlayerBase, Team

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# Create the FastAPI app
app = FastAPI(
    title="Bucksport Baseball/Softball API",
    version="0.1.0",
    lifespan=lifespan,
)

# Apply CORS middleware to allow all origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve static directory path
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "local_site"

# Serve the main page
@app.get("/", response_class=FileResponse, include_in_schema=False)
async def read_index():
    return str(STATIC_DIR / "index.html")

# ----------------- Team endpoints -----------------
@app.post("/api/teams", response_model=Team, status_code=status.HTTP_201_CREATED)
def create_team(team: Team, session: Session = Depends(get_session)):
    session.add(team)
    session.commit()
    session.refresh(team)
    return team

@app.get("/api/teams", response_model=List[Team])
def read_teams(session: Session = Depends(get_session)):
    return session.exec(select(Team)).all()

# ----------------- Player endpoints -----------------
@app.post("/api/players", response_model=Player, status_code=status.HTTP_201_CREATED)
def register_player(player_data: PlayerBase, session: Session = Depends(get_session)):
    try:
        logger.info(f"Received player registration: {player_data.dict()}")
        player = Player.from_orm(player_data)
        session.add(player)
        session.commit()
        session.refresh(player)
        logger.info(f"Player registered successfully: {player.id}")
        return player
    except Exception as e:
        session.rollback()
        logger.error(f"Error registering player: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/players", response_model=List[Player])
def read_players(session: Session = Depends(get_session)):
    return session.exec(select(Player)).all()

@app.get("/api/players/{player_id}", response_model=Player)
def read_player(player_id: int, session: Session = Depends(get_session)):
    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

# ----------------- Event endpoints -----------------
@app.post("/api/events", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(event: Event, session: Session = Depends(get_session)):
    if event.end_time <= event.start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

@app.get("/api/events", response_model=List[Event])
def read_events(team_id: int | None = None, session: Session = Depends(get_session)):
    query = select(Event)
    if team_id is not None:
        query = query.where(Event.team_id == team_id)
    return session.exec(query.order_by(Event.start_time)).all()

# ----------------- Schedule Page endpoints (NEW) -----------------
@app.get("/api/schedule")
def get_schedule():
    # Dummy data for demonstration. Replace with database queries.
    return [
        {"id": 1, "date": "2025-07-20", "time": "18:00", "type": "game", "title": "Bucksport Blue Jays vs. Orland Orcas", "location": "Field A", "team_id": 1, "coach_id": 1, "notes": "Championship game!"},
        {"id": 2, "date": "2025-07-21", "time": "17:30", "type": "practice", "title": "Softball Team Practice", "location": "Field B", "team_id": 2, "coach_id": 2, "notes": "Focus on fielding drills."},
        {"id": 3, "date": "2025-07-20", "time": "16:00", "type": "game", "title": "Minor League All-Stars", "location": "Field C", "team_id": 3, "coach_id": 3, "notes": ""},
    ]

@app.get("/api/locations")
def get_locations():
    # Dummy data. In a real app, query distinct locations from the events table.
    return ["Field A", "Field B", "Field C", "Community Park"]

@app.get("/api/coaches")
def get_coaches():
    # Dummy data. In a real app, this would come from a 'coaches' table.
    return [
        {"id": 1, "name": "Coach Bob"},
        {"id": 2, "name": "Coach Sarah"},
        {"id": 3, "name": "Coach Mike"}
    ]

class EventRequest(BaseModel):
    event_title: str
    event_date: str
    event_time: str
    event_location: str
    event_team: str
    event_coach: str
    event_type: str
    event_notes: str | None = None

@app.post("/api/schedule/request")
def request_new_event(request: EventRequest):
    logger.info(f"Received new event request: {request.model_dump_json(indent=2)}")
    # In a real app, you would save this request to the database for admin approval.
    return {"status": "success", "message": "Event request received and logged."}


# Mount the static directory to serve frontend files. This should be last.
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

