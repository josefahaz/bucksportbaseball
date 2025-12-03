"""Update existing inventory items with division field based on inventory list."""
from sqlmodel import Session, select

from database import engine, init_db
from models import InventoryItem


# Mapping of item name patterns to divisions based on the inventory CSV
SOFTBALL_ITEMS = [
    "batting tee", "12 inch", "11 inch", "softball", "girls", "womens", "women's",
    "bennett painting", "knee savers", "pxs sponge", "pitching machine balls",
    "blue bin", "black bin", "easton bag", "dicks bag", "rawlings bag", "sea bag"
]

SHARED_ITEMS = [
    "jugs pitch machine", "wiffle", "tennis balls", "first aid", "marking paint",
    "field marker", "turf", "spray cans", "dura stripe", "donated", "cleats",
    "left handed gloves", "umpire"
]


def update_divisions():
    """Update inventory items with their division (Baseball, Softball, or Shared)."""
    init_db()
    
    with Session(engine) as session:
        statement = select(InventoryItem)
        items = session.exec(statement).all()
        
        if not items:
            print("No inventory items found.")
            return
        
        updated_count = 0
        for item in items:
            # Skip if already has division
            if item.division:
                continue
            
            name_lower = item.item_name.lower()
            notes_lower = (item.notes or "").lower()
            combined = name_lower + " " + notes_lower
            
            # Check for softball indicators
            is_softball = any(pattern in combined for pattern in SOFTBALL_ITEMS)
            is_shared = any(pattern in combined for pattern in SHARED_ITEMS)
            
            if is_shared:
                item.division = "Shared"
            elif is_softball:
                item.division = "Softball"
            else:
                item.division = "Baseball"
            
            session.add(item)
            updated_count += 1
            print(f"Updated: {item.item_name} -> {item.division}")
        
        session.commit()
        print(f"\n✅ Updated {updated_count} inventory items with division!")


if __name__ == "__main__":
    update_divisions()
