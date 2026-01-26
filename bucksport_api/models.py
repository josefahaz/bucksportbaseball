from datetime import date, datetime
from typing import Optional
from pydantic import validator
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column
from sqlalchemy.types import JSON


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
    division: Optional[str] = Field(default=None, index=True)  # Baseball, Softball, Shared
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


class ActivityLog(SQLModel, table=True):
    """Activity log for tracking all user actions across the system."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    action: str = Field(index=True)  # e.g., "Item Updated", "Item Deleted", "Item Added"
    details: str  # Description of what changed
    user: str = Field(index=True)  # User who performed the action
    page: str = Field(index=True)  # Page where action occurred (inventory, schedule, etc.)
    item_id: Optional[int] = None  # Optional reference to the item that was modified


class Donation(SQLModel, table=True):
    """Fundraising and sponsorship donations."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # Company/person name
    amount: float
    donation_type: str = Field(index=True)  # Donation, Sponsorship, Fundraiser
    date: date
    division: Optional[str] = None  # Baseball, Softball, or Both
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SponsorshipSheetMeta(SQLModel, table=True):
    sheet_name: str = Field(primary_key=True)
    columns: list[str] = Field(sa_column=Column(JSON))
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SponsorshipSheetRow(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sheet_name: str = Field(index=True)
    row_index: int = Field(index=True)
    data: dict = Field(sa_column=Column(JSON))
    updated_at: datetime = Field(default_factory=datetime.utcnow)
