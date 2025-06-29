from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    division: Optional[str] = None
    coach: Optional[str] = None

    players: list["Player"] = Relationship(back_populates="team")
    events: list["Event"] = Relationship(back_populates="team")


class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    birthdate: date
    email: str = Field(index=True)
    phone: Optional[str] = None

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
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
