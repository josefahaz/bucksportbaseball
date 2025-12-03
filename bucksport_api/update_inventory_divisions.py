"""Update existing inventory items with division field."""
from sqlmodel import Session, select

from database import engine, init_db
from models import InventoryItem


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
            
            # Determine division based on item name and notes
            name_lower = item.item_name.lower()
            notes_lower = (item.notes or "").lower()
            
            # Check for softball indicators
            if "softball" in name_lower or "softball" in notes_lower:
                item.division = "Softball"
            elif "girls" in name_lower or "womens" in name_lower:
                item.division = "Softball"
            elif "11 inch" in name_lower or "12 inch" in name_lower:
                item.division = "Softball"
            # Check for shared items
            elif "wiffle" in name_lower or "tennis" in name_lower:
                item.division = "Shared"
            elif "jugs" in name_lower or "pitch machine" in name_lower:
                item.division = "Shared"
            elif "first aid" in name_lower:
                item.division = "Shared"
            elif "marking paint" in name_lower or "field marker" in name_lower or "turf" in name_lower:
                item.division = "Shared"
            elif "umpire" in name_lower:
                item.division = "Shared"
            # Default to Baseball for remaining items
            else:
                item.division = "Baseball"
            
            session.add(item)
            updated_count += 1
            print(f"Updated: {item.item_name} -> {item.division}")
        
        session.commit()
        print(f"\n✅ Updated {updated_count} inventory items with division!")


if __name__ == "__main__":
    update_divisions()
