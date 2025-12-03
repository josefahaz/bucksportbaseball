"""Seed inventory data into the database."""
from sqlmodel import Session, select

from database import engine, init_db
from models import InventoryItem


INVENTORY_ITEMS = [
    {"item_name": "Jugs pitch machine", "category": "other", "division": "Shared", "quantity": 1},
    {"item_name": "Practice baseballs", "category": "ball", "division": "Baseball", "quantity": 57},
    {"item_name": "Practice tee balls", "category": "ball", "division": "Baseball", "quantity": 56},
    {"item_name": "Wiffle / Pickleball balls", "category": "ball", "division": "Shared", "quantity": 63},
    {"item_name": "Tennis balls", "category": "ball", "division": "Shared", "quantity": 33},
    {"item_name": "Hard yellow practice balls", "category": "ball", "division": "Baseball", "quantity": 20},
    {"item_name": "Little League game balls", "category": "ball", "division": "Baseball", "quantity": 38, "notes": "26 still wrapped"},
    {"item_name": "Soft compression Wilson game balls", "category": "ball", "division": "Baseball", "quantity": 11, "notes": "10 still wrapped"},
    {"item_name": "Batting helmets (one size)", "category": "helmet", "division": "Baseball", "size": "One Size", "quantity": 41, "notes": "Colors: blue, black, purple, green, white"},
    {"item_name": "Face guard shields", "category": "helmet", "division": "Baseball", "quantity": 21, "notes": "Mostly black; some silver still in packaging"},
    {"item_name": "Catcher helmets (full)", "category": "helmet", "division": "Baseball", "quantity": 10},
    {"item_name": "Catcher gloves (left hand)", "category": "glove", "division": "Baseball", "quantity": 4},
    {"item_name": "Chest protectors", "category": "other", "division": "Baseball", "size": "Various", "quantity": 14},
    {"item_name": "Leg pads (sets)", "category": "other", "division": "Baseball", "quantity": 12},
    {"item_name": "Baseball bats (USA logo)", "category": "bat", "division": "Baseball", "quantity": 12},
    {"item_name": "Tee ball bats", "category": "bat", "division": "Baseball", "quantity": 3},
    {"item_name": "Baseball bat (no USA logo)", "category": "bat", "division": "Baseball", "quantity": 1},
    {"item_name": "Hitting tees", "category": "other", "division": "Baseball", "quantity": 11, "notes": "2 still brand new"},
    {"item_name": "External umpire vest", "category": "other", "division": "Shared", "quantity": 1},
    {"item_name": "Internal umpire vest", "category": "other", "division": "Shared", "quantity": 1},
    {"item_name": "Umpire full helmet", "category": "helmet", "division": "Shared", "quantity": 1},
    {"item_name": "Older umpire masks", "category": "other", "division": "Shared", "quantity": 3},
    {"item_name": "Guide Line white field marker (bags)", "category": "other", "division": "Shared", "quantity": 45},
    {"item_name": "Infield turf (bags)", "category": "other", "division": "Shared", "quantity": 30},
    {"item_name": "12 inch game balls (new)", "category": "ball", "division": "Softball", "size": "12 inch", "quantity": 35},
    {"item_name": "11 inch game balls (new)", "category": "ball", "division": "Softball", "size": "11 inch", "quantity": 76},
    {"item_name": "12 inch practice balls", "category": "ball", "division": "Softball", "size": "12 inch", "quantity": 43},
    {"item_name": "11 inch practice balls", "category": "ball", "division": "Softball", "size": "11 inch", "quantity": 44},
    {"item_name": "Softball helmets", "category": "helmet", "division": "Softball", "quantity": 14},
    {"item_name": "Softball bats", "category": "bat", "division": "Softball", "quantity": 5},
    {"item_name": "Red first aid kits", "category": "other", "division": "Shared", "quantity": 4},
    {"item_name": "Blue first aid kit", "category": "other", "division": "Shared", "quantity": 1},
]


def seed_inventory():
    """Seed inventory items into the database."""
    init_db()
    
    with Session(engine) as session:
        statement = select(InventoryItem)
        existing_items = session.exec(statement).all()
        
        if existing_items:
            print(f"Database already has {len(existing_items)} inventory items. Skipping seed.")
            return
        
        for item_data in INVENTORY_ITEMS:
            item = InventoryItem(**item_data)
            session.add(item)
            print(f"Added: {item.item_name} ({item.division})")
        
        session.commit()
        print(f"Seeded {len(INVENTORY_ITEMS)} inventory items!")


if __name__ == "__main__":
    seed_inventory()