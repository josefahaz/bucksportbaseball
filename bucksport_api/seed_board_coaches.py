"""Seed board members and coaches into the database."""
from sqlmodel import Session, select

from database import engine, init_db
from models import BoardMember, Coach, Location


# Board Members - as of Fall 2025
BOARD_MEMBERS = [
    # League-wide positions
    {"name": "Katie Littlefield", "position": "President", "division": None, "email": "N/A", "phone": "N/A"},
    {"name": "Erick Kennard", "position": "Vice President", "division": None, "email": "N/A", "phone": "N/A"},
    {"name": "Kim Burgess", "position": "Treasurer", "division": None, "email": "N/A", "phone": "N/A"},
    {"name": "Joe Hazlett", "position": "Fundraising/Marketing Coordinator", "division": None, "email": "N/A", "phone": "N/A"},
    {"name": "Jamie Bowden", "position": "Umpire in Chief", "division": None, "email": "N/A", "phone": "N/A"},
    {"name": "John Robinson", "position": "Equipment Coordinator", "division": None, "email": "N/A", "phone": "N/A"},
    # Baseball division
    {"name": "Ryan Lighthouse", "position": "Secretary", "division": "Baseball", "email": "N/A", "phone": "N/A"},
    {"name": "Harold Littlefield", "position": "Coaching Coordinator", "division": "Baseball", "email": "N/A", "phone": "N/A"},
    {"name": "Whitney Wentworth", "position": "Player Agent", "division": "Baseball", "email": "N/A", "phone": "N/A"},
    {"name": "Ashley Kennard", "position": "Concessions Manager", "division": "Baseball", "email": "N/A", "phone": "N/A"},
    # Softball division
    {"name": "Shelby Emery", "position": "Vice President", "division": "Softball", "email": "N/A", "phone": "N/A"},
    {"name": "Lisa Hazlett", "position": "Secretary", "division": "Softball", "email": "N/A", "phone": "N/A"},
    {"name": "Chris Remick", "position": "Coaching Coordinator", "division": "Softball", "email": "N/A", "phone": "N/A"},
    {"name": "Taylor Beaulieu", "position": "Player Agent", "division": "Softball", "email": "N/A", "phone": "N/A"},
    {"name": "VACANT", "position": "Concession Manager", "division": "Softball", "email": "N/A", "phone": "N/A"},
]

# Coaches - initial list
COACHES = [
    {"name": "Rob Wadleigh", "email": "N/A", "phone": "N/A", "team_name": None, "division": None},
]

# Locations/Fields
LOCATIONS = [
    {"name": "Bucksport Field 1"},
    {"name": "Bucksport Field 2"},
    {"name": "Bucksport Softball Field"},
    {"name": "Miles Lane Complex"},
    {"name": "Away - Ellsworth"},
    {"name": "Away - Brewer"},
    {"name": "Away - Bangor"},
]


def seed_board_members():
    """Seed board members into the database."""
    init_db()
    
    with Session(engine) as session:
        # Check if board members already exist
        statement = select(BoardMember)
        existing = session.exec(statement).all()
        
        if existing:
            print(f"Database already has {len(existing)} board members. Skipping seed.")
            return
        
        # Create board members
        for member_data in BOARD_MEMBERS:
            member = BoardMember(**member_data)
            session.add(member)
            print(f"Added board member: {member.name} - {member.position}")
        
        session.commit()
        print(f"\n✅ Successfully seeded {len(BOARD_MEMBERS)} board members!")


def seed_coaches():
    """Seed coaches into the database."""
    init_db()
    
    with Session(engine) as session:
        # Check if coaches already exist
        statement = select(Coach)
        existing = session.exec(statement).all()
        
        if existing:
            print(f"Database already has {len(existing)} coaches. Skipping seed.")
            return
        
        # Create coaches
        for coach_data in COACHES:
            coach = Coach(**coach_data)
            session.add(coach)
            print(f"Added coach: {coach.name}")
        
        session.commit()
        print(f"\n✅ Successfully seeded {len(COACHES)} coaches!")


def seed_locations():
    """Seed locations into the database."""
    init_db()
    
    with Session(engine) as session:
        # Check if locations already exist
        statement = select(Location)
        existing = session.exec(statement).all()
        
        if existing:
            print(f"Database already has {len(existing)} locations. Skipping seed.")
            return
        
        # Create locations
        for loc_data in LOCATIONS:
            location = Location(**loc_data)
            session.add(location)
            print(f"Added location: {location.name}")
        
        session.commit()
        print(f"\n✅ Successfully seeded {len(LOCATIONS)} locations!")


def seed_all():
    """Seed all board members, coaches, and locations."""
    seed_board_members()
    seed_coaches()
    seed_locations()


if __name__ == "__main__":
    seed_all()
