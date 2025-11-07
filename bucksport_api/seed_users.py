"""Seed initial users into the database."""
from sqlmodel import Session, select

from database import engine, init_db
from auth_models import User


# Initial users from the provided list
INITIAL_USERS = [
    # Admins
    {"first_name": "Erick", "last_name": "Kennard", "email": "ekennard@bucksportll.org", "role": "admin"},
    {"first_name": "Jamie", "last_name": "Bowden", "email": "jbowden@bucksportll.org", "role": "admin"},
    {"first_name": "Joby", "last_name": "Robinson", "email": "jrobinson@bucksportll.org", "role": "admin"},
    {"first_name": "Joseph", "last_name": "Hazlett", "email": "jhazlett@bucksportll.org", "role": "admin"},
    {"first_name": "Katie", "last_name": "Littlefield", "email": "klittlefield@bucksportll.org", "role": "admin"},
    {"first_name": "Kim", "last_name": "Burgess", "email": "kburgess@bucksportll.org", "role": "admin"},
    
    # Board Members
    {"first_name": "Ashley", "last_name": "Kennard", "email": "akennard@bucksportll.org", "role": "board_member"},
    {"first_name": "Christopher", "last_name": "Rennick", "email": "crennick@bucksportll.org", "role": "board_member"},
    {"first_name": "Harold", "last_name": "Littlefield", "email": "hlittlefield@bucksportll.org", "role": "board_member"},
    {"first_name": "Lisa", "last_name": "Hazlett", "email": "lhazlett@bucksportll.org", "role": "board_member"},
    {"first_name": "Ryan", "last_name": "Lightbody", "email": "rlightbody@bucksportll.org", "role": "board_member"},
    {"first_name": "Shelby", "last_name": "Emery", "email": "semery@bucksportll.org", "role": "board_member"},
    {"first_name": "Taylor", "last_name": "Beaulieu", "email": "tbeaulieu@bucksportll.org", "role": "board_member"},
    {"first_name": "Whitney", "last_name": "Wentworth", "email": "wwentworth@bucksportll.org", "role": "board_member"},
]


def seed_users():
    """Seed initial users into the database."""
    # Initialize database
    init_db()
    
    with Session(engine) as session:
        # Check if users already exist
        statement = select(User)
        existing_users = session.exec(statement).all()
        
        if existing_users:
            print(f"Database already has {len(existing_users)} users. Skipping seed.")
            return
        
        # Create users
        for user_data in INITIAL_USERS:
            user = User(**user_data)
            session.add(user)
            print(f"Added user: {user.first_name} {user.last_name} ({user.email}) - {user.role}")
        
        session.commit()
        print(f"\n✅ Successfully seeded {len(INITIAL_USERS)} users!")


if __name__ == "__main__":
    seed_users()
