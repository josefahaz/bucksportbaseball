from datetime import date, datetime
from typing import Optional
from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    division: Optional[str] = None
    coach: Optional[str] = None

    players: list["Player"] = Relationship(back_populates="team")
    events: list["Event"] = Relationship(back_populates="team")


class PlayerBase(SQLModel):
    first_name: str
    last_name: str
    birthdate: date
    email: str = Field(unique=True, index=True)
    phone: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")

    @validator('birthdate', pre=True)
    def parse_birthdate(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError as e:
                raise ValueError("Date must be in YYYY-MM-DD format") from e
        return value


class Player(PlayerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team: Optional[Team] = Relationship(back_populates="players")


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="events")


class InventoryItem(SQLModel, table=True):
    """Equipment inventory item."""
    id: Optional[int] = Field(default=None, primary_key=True)
    item_name: str = Field(index=True)
    category: str = Field(index=True)  # jersey, pants, hat, cleats, bat, ball, glove, helmet, other
    size: Optional[str] = None
    team: Optional[str] = None
    assigned_coach: Optional[str] = "Unassigned"
    quantity: int = Field(default=1)
    status: str = Field(default="Available")  # Available, Checked Out, Needs Repair, Retired
    notes: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class BoardMember(SQLModel, table=True):
    """Board member for the league."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    position: str  # President, Vice President, Treasurer, etc.
    division: Optional[str] = None  # Baseball, Softball, or None for league-wide
    email: Optional[str] = "N/A"
    phone: Optional[str] = "N/A"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Coach(SQLModel, table=True):
    """Coach for the league."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: Optional[str] = "N/A"
    phone: Optional[str] = "N/A"
    team_name: Optional[str] = None  # Team they coach
    division: Optional[str] = None  # Baseball or Softball
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ScheduleEvent(SQLModel, table=True):
    """Scheduled event (game, practice, etc.)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    date: str  # YYYY-MM-DD format
    time: str  # e.g., "5:30 PM"
    event_type: str  # game, practice, event
    location: str
    team_id: Optional[int] = None
    coach_id: Optional[int] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Location(SQLModel, table=True):
    """Available locations/fields."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
