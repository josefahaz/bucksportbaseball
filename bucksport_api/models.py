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
