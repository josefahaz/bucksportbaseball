"""Import inventory items from CSV file into the database."""
import csv
from pathlib import Path
from sqlmodel import Session, select
from database import engine, init_db
from models import InventoryItem
from datetime import datetime


def normalize_category(category):
    """Normalize category to ensure it's valid."""
    valid_categories = ['jersey', 'pants', 'hat', 'cleats', 'bat', 'ball', 'glove', 'helmet', 'other']
    category = category.lower().strip()
    return category if category in valid_categories else 'other'


def determine_division(item_name, category, notes):
    """Determine division based on item details."""
    item_lower = item_name.lower()
    notes_lower = (notes or '').lower()
    
    # Softball indicators
    if 'softball' in item_lower or 'softball' in notes_lower:
        return 'Softball'
    
    # Baseball indicators
    if 'baseball' in item_lower or 'tee ball' in item_lower:
        return 'Baseball'
    
    # Shared equipment
    if any(word in item_lower for word in ['umpire', 'field', 'first aid', 'marker', 'turf']):
        return 'Shared'
    
    # Default based on category
    if category in ['ball', 'bat']:
        # Check size for softballs
        if '11 inch' in item_lower or '12 inch' in item_lower:
            return 'Softball'
        return 'Baseball'
    
    return 'Shared'


def import_from_csv(csv_path):
    """Import inventory items from CSV file."""
    init_db()
    
    items_added = 0
    items_updated = 0
    
    with Session(engine) as session:
        # Clear existing inventory to avoid duplicates
        print("Clearing existing inventory...")
        statement = select(InventoryItem)
        existing_items = session.exec(statement).all()
        for item in existing_items:
            session.delete(item)
        session.commit()
        print(f"Cleared {len(existing_items)} existing items")
        
        # Read and import from CSV
        print(f"\nImporting from {csv_path}...")
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Skip empty rows
                if not row.get('Item Name') or not row['Item Name'].strip():
                    continue
                
                # Normalize the category from CSV
                category = normalize_category(row.get('Category', 'other'))
                
                # Determine division
                division = determine_division(
                    row['Item Name'],
                    category,
                    row.get('Notes', '')
                )
                
                # Handle quantity
                try:
                    quantity = int(row.get('Quantity', 1))
                except (ValueError, TypeError):
                    quantity = 1
                
                # Create inventory item
                item = InventoryItem(
                    item_name=row['Item Name'].strip(),
                    category=category,
                    division=division,
                    size=row.get('Size', '').strip() or None,
                    team=row.get('Team', '').strip() or None,
                    assigned_coach=row.get('Assigned Coach', 'Unassigned').strip() or 'Unassigned',
                    quantity=quantity,
                    status=row.get('Status', 'Available').strip() or 'Available',
                    notes=row.get('Notes', '').strip() or None,
                    last_updated=datetime.utcnow()
                )
                
                session.add(item)
                items_added += 1
                
                print(f"Added: {item.item_name} ({item.category}, {item.division}) - Qty: {item.quantity}")
        
        session.commit()
    
    print(f"\n✓ Successfully imported {items_added} items into the database!")
    return items_added


def main():
    """Main function to run the import."""
    base_path = Path(__file__).parent.parent
    csv_path = base_path / "inventory_upload.csv"
    
    if not csv_path.exists():
        print(f"Error: CSV file not found at {csv_path}")
        return
    
    print("=" * 60)
    print("INVENTORY DATABASE IMPORT")
    print("=" * 60)
    
    items_added = import_from_csv(csv_path)
    
    print("\n" + "=" * 60)
    print(f"Import complete! Total items in database: {items_added}")
    print("=" * 60)
    
    # Verify the import
    print("\nVerifying import...")
    with Session(engine) as session:
        # Check pants
        statement = select(InventoryItem).where(InventoryItem.category == "pants")
        pants = session.exec(statement).all()
        print(f"  - Pants items: {len(pants)}")
        
        # Check jerseys
        statement = select(InventoryItem).where(InventoryItem.category == "jersey")
        jerseys = session.exec(statement).all()
        print(f"  - Jersey items: {len(jerseys)}")
        
        # Check by division
        for div in ['Baseball', 'Softball', 'Shared']:
            statement = select(InventoryItem).where(InventoryItem.division == div)
            div_items = session.exec(statement).all()
            print(f"  - {div} items: {len(div_items)}")


if __name__ == "__main__":
    main()
