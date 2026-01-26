"""Assign fundraising_coordinator role to specific users."""
import os
from sqlmodel import Session, select
from database import engine
from auth_models import User

# Users who should have fundraising_coordinator role
FUNDRAISING_COORDINATORS = [
    "jhazlett@bucksportll.org",  # Joseph Hazlett - Fundraising Coordinator
    "klittlefield@bucksportll.org",  # Katie Littlefield - President
    "ekennard@bucksportll.org",  # Erick Kennard - Vice President
]


def assign_fundraising_roles():
    """Assign fundraising_coordinator role to specified users."""
    with Session(engine) as session:
        for email in FUNDRAISING_COORDINATORS:
            user = session.exec(select(User).where(User.email == email)).first()
            
            if user:
                # If user is already admin, keep them as admin
                if user.role != "admin":
                    user.role = "fundraising_coordinator"
                    session.add(user)
                    print(f"✓ Updated {user.first_name} {user.last_name} ({email}) to fundraising_coordinator")
                else:
                    print(f"✓ {user.first_name} {user.last_name} ({email}) is already admin (higher permission)")
            else:
                print(f"✗ User not found: {email}")
                print(f"  This user needs to log in first to create their account")
        
        session.commit()
        print("\n✓ Fundraising roles assigned successfully!")


if __name__ == "__main__":
    assign_fundraising_roles()
