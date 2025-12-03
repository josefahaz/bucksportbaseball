"""FastAPI backend for Bucksport Youth Softball/Baseball program."""
from datetime import datetime
from typing import List
import logging
import os
from pathlib import Path

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlmodel import Session, select
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from database import get_session, init_db
from models import Event, Player, PlayerBase, Team, InventoryItem, BoardMember, Coach, Location, ScheduleEvent
from auth_routes import router as auth_router
from seed_users import seed_users
from seed_inventory import seed_inventory
from seed_board_coaches import seed_all as seed_board_coaches
from update_inventory_divisions import update_divisions

# Load environment-specific .env file
# Set ENVIRONMENT=production on production server
environment = os.getenv('ENVIRONMENT', 'development')
if environment == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(f"Running in {environment} mode")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully")
        
        # Seed data on startup (will skip if already seeded)
        logger.info("Seeding users...")
        seed_users()
        logger.info("Seeding inventory...")
        seed_inventory()
        logger.info("Seeding board members and coaches...")
        seed_board_coaches()
        logger.info("Updating inventory divisions...")
        update_divisions()
        logger.info("Startup complete!")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        # Don't re-raise - allow app to start even if seeding fails
    yield

# Create the FastAPI app
app = FastAPI(
    title="Bucksport Baseball/Softball API",
    version="0.2.0",
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

# Include routers
app.include_router(auth_router)

# Resolve static directory path
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "local_site"

# Health check endpoint (for keeping server warm)
@app.get("/api/health")
def health_check():
    """Simple health check endpoint to wake up the server."""
    return {"status": "ok", "message": "Server is running"}

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

# ----------------- Board Members endpoints (DATABASE) -----------------
@app.get("/api/board-members")
def get_board_members(session: Session = Depends(get_session)):
    """Get all board members from database."""
    statement = select(BoardMember)
    members = session.exec(statement).all()
    return [
        {
            "id": m.id,
            "name": m.name,
            "position": m.position,
            "division": m.division,
            "email": m.email,
            "phone": m.phone
        }
        for m in members
    ]

@app.put("/api/board-members/{member_id}")
def update_board_member(member_id: int, member_data: dict, session: Session = Depends(get_session)):
    """Update a board member in the database."""
    member = session.get(BoardMember, member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Board member not found")
    
    # Update fields
    if "name" in member_data:
        member.name = member_data["name"]
    if "position" in member_data:
        member.position = member_data["position"]
    if "division" in member_data:
        member.division = member_data["division"]
    if "email" in member_data:
        member.email = member_data["email"]
    if "phone" in member_data:
        member.phone = member_data["phone"]
    
    member.updated_at = datetime.utcnow()
    session.add(member)
    session.commit()
    session.refresh(member)
    
    logger.info(f"Updated board member {member_id}: {member.name}")
    
    return {
        "id": member.id,
        "name": member.name,
        "position": member.position,
        "division": member.division,
        "email": member.email,
        "phone": member.phone
    }

# ----------------- Coaches endpoints (DATABASE) -----------------
@app.get("/api/coaches")
def get_coaches(session: Session = Depends(get_session)):
    """Get all coaches from database."""
    statement = select(Coach)
    coaches = session.exec(statement).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone,
            "team_name": c.team_name,
            "division": c.division
        }
        for c in coaches
    ]

@app.put("/api/coaches/{coach_id}")
def update_coach(coach_id: int, coach_data: dict, session: Session = Depends(get_session)):
    """Update a coach in the database."""
    coach = session.get(Coach, coach_id)
    if not coach:
        raise HTTPException(status_code=404, detail="Coach not found")
    
    # Update fields
    if "name" in coach_data:
        coach.name = coach_data["name"]
    if "email" in coach_data:
        coach.email = coach_data["email"]
    if "phone" in coach_data:
        coach.phone = coach_data["phone"]
    if "team_name" in coach_data:
        coach.team_name = coach_data["team_name"]
    if "division" in coach_data:
        coach.division = coach_data["division"]
    
    coach.updated_at = datetime.utcnow()
    session.add(coach)
    session.commit()
    session.refresh(coach)
    
    logger.info(f"Updated coach {coach_id}: {coach.name}")
    
    return {
        "id": coach.id,
        "name": coach.name,
        "email": coach.email,
        "phone": coach.phone,
        "team_name": coach.team_name,
        "division": coach.division
    }

@app.post("/api/coaches")
def create_coach(coach_data: dict, session: Session = Depends(get_session)):
    """Create a new coach."""
    coach = Coach(
        name=coach_data.get("name", ""),
        email=coach_data.get("email", "N/A"),
        phone=coach_data.get("phone", "N/A"),
        team_name=coach_data.get("team_name"),
        division=coach_data.get("division")
    )
    session.add(coach)
    session.commit()
    session.refresh(coach)
    
    logger.info(f"Created coach: {coach.name}")
    
    return {
        "id": coach.id,
        "name": coach.name,
        "email": coach.email,
        "phone": coach.phone,
        "team_name": coach.team_name,
        "division": coach.division
    }

# ----------------- Schedule endpoints (DATABASE) -----------------
@app.get("/api/schedule")
def get_schedule(session: Session = Depends(get_session)):
    """Get all scheduled events from database."""
    try:
        statement = select(ScheduleEvent)
        events = session.exec(statement).all()
        
        # If no events in DB, return sample data for now
        if not events:
            return [
                {"id": 1, "title": "Opening Day", "date": "2025-04-05", "time": "10:00 AM", "type": "event", "location": "Bucksport Field 1", "team_id": None, "coach_id": None, "notes": "Season opener - all teams"},
                {"id": 2, "title": "Majors Practice", "date": "2025-04-07", "time": "5:30 PM", "type": "practice", "location": "Bucksport Field 1", "team_id": 1, "coach_id": 1, "notes": ""},
                {"id": 3, "title": "Minors Practice", "date": "2025-04-08", "time": "5:30 PM", "type": "practice", "location": "Bucksport Field 2", "team_id": 2, "coach_id": 1, "notes": ""},
                {"id": 4, "title": "Majors vs Ellsworth", "date": "2025-04-12", "time": "1:00 PM", "type": "game", "location": "Bucksport Field 1", "team_id": 1, "coach_id": 1, "notes": "Home game"},
                {"id": 5, "title": "Tee Ball Practice", "date": "2025-04-09", "time": "5:00 PM", "type": "practice", "location": "Bucksport Field 2", "team_id": 3, "coach_id": 1, "notes": ""},
            ]
        
        return [
            {
                "id": e.id,
                "title": e.title,
                "date": e.date,
                "time": e.time,
                "type": e.event_type,
                "location": e.location,
                "team_id": e.team_id,
                "coach_id": e.coach_id,
                "notes": e.notes
            }
            for e in events
        ]
    except Exception as e:
        logger.error(f"Error fetching schedule: {e}")
        # Return sample data on error
        return [
            {"id": 1, "title": "Opening Day", "date": "2025-04-05", "time": "10:00 AM", "type": "event", "location": "Bucksport Field 1", "team_id": None, "coach_id": None, "notes": "Season opener - all teams"},
        ]

@app.get("/api/locations")
def get_locations(session: Session = Depends(get_session)):
    """Get all locations from database."""
    statement = select(Location)
    locations = session.exec(statement).all()
    
    # If no locations in DB, return default list
    if not locations:
        return [
            "Bucksport Field 1",
            "Bucksport Field 2", 
            "Bucksport Softball Field",
            "Miles Lane Complex",
            "Away - Ellsworth",
            "Away - Brewer",
            "Away - Bangor"
        ]
    
    return [loc.name for loc in locations]

class EventRequest(BaseModel):
    title: str
    date: str
    time: str
    location: str
    team_id: str | None = None
    coach_id: str | None = None
    type: str
    notes: str | None = None

@app.post("/api/schedule/request")
def request_new_event(request: EventRequest, session: Session = Depends(get_session)):
    """Create a new scheduled event."""
    event = ScheduleEvent(
        title=request.title,
        date=request.date,
        time=request.time,
        location=request.location,
        event_type=request.type,
        team_id=int(request.team_id) if request.team_id and request.team_id.isdigit() else None,
        coach_id=int(request.coach_id) if request.coach_id and request.coach_id.isdigit() else None,
        notes=request.notes
    )
    session.add(event)
    session.commit()
    session.refresh(event)
    
    logger.info(f"Created new event: {event.title} on {event.date}")
    return {"status": "success", "message": "Event created successfully.", "id": event.id}

@app.delete("/api/schedule/{event_id}")
def delete_event(event_id: int, session: Session = Depends(get_session)):
    """Delete a scheduled event."""
    event = session.get(ScheduleEvent, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    session.delete(event)
    session.commit()
    logger.info(f"Deleted event: {event.title} (ID: {event_id})")
    return {"status": "success", "message": "Event deleted successfully."}

# ----------------- Inventory endpoints -----------------
@app.get("/api/inventory")
def get_inventory(session: Session = Depends(get_session)):
    """Get all inventory items."""
    statement = select(InventoryItem)
    items = session.exec(statement).all()
    return [
        {
            "id": item.id,
            "name": item.item_name,  # Frontend expects 'name'
            "category": item.category,
            "division": item.division,  # Baseball, Softball, or Shared
            "size": item.size,
            "team": {"id": None, "name": item.team} if item.team else None,
            "assigned_coach": {"id": None, "name": item.assigned_coach} if item.assigned_coach else None,
            "quantity": item.quantity,
            "status": item.status.lower().replace(" ", "-"),  # Convert to lowercase with dashes for badge styling
            "notes": item.notes,
            "last_updated": item.last_updated.isoformat() if item.last_updated else None
        }
        for item in items
    ]

@app.get("/api/inventory/summary")
def get_inventory_summary(session: Session = Depends(get_session)):
    """Get inventory summary statistics."""
    statement = select(InventoryItem)
    items = session.exec(statement).all()
    
    total_quantity = sum(item.quantity for item in items)
    available = sum(item.quantity for item in items if item.status == "Available")
    checked_out = sum(item.quantity for item in items if item.status == "Checked Out")
    needs_repair = sum(item.quantity for item in items if item.status == "Needs Repair")
    
    return {
        "total_items": total_quantity,
        "available": available,
        "checked_out": checked_out,
        "needs_repair": needs_repair
    }

@app.get("/api/inventory/categories")
def get_inventory_categories():
    # Return standard equipment categories
    return ["jersey", "pants", "hat", "cleats", "bat", "ball", "glove", "helmet", "other"]

@app.get("/api/inventory/statuses")
def get_inventory_statuses():
    # Return standard inventory statuses
    return ["Available", "Checked Out", "Needs Repair", "Retired"]

# Mount the static directory to serve frontend files. This should be last.
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
