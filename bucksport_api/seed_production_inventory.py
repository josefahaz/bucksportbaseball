"""
Production-ready script to seed inventory from CSV.
This script can be run on Render or any production environment.
"""
import csv
import os
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


def seed_from_csv():
    """Seed inventory from CSV file."""
    print("=" * 60)
    print("PRODUCTION INVENTORY SEEDING")
    print("=" * 60)
    
    # Initialize database
    init_db()
    print("✓ Database initialized")
    
    # Find CSV file
    csv_path = Path(__file__).parent.parent / "inventory_upload.csv"
    if not csv_path.exists():
        print(f"ERROR: CSV file not found at {csv_path}")
        return False
    
    print(f"✓ Found CSV file: {csv_path}")
    
    items_added = 0
    
    with Session(engine) as session:
        # Check if inventory already exists
        statement = select(InventoryItem)
        existing_items = session.exec(statement).all()
        
        if existing_items:
            print(f"\nWARNING: Database already has {len(existing_items)} items")
            response = input("Clear existing items and re-import? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborting.")
                return False
            
            # Clear existing items
            for item in existing_items:
                session.delete(item)
            session.commit()
            print(f"✓ Cleared {len(existing_items)} existing items")
        
        # Import from CSV
        print("\nImporting items from CSV...")
        
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
        
        session.commit()
    
    print(f"\n✓ Successfully imported {items_added} items!")
    
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
        
        # Total items
        statement = select(InventoryItem)
        all_items = session.exec(statement).all()
        print(f"\n✓ TOTAL ITEMS IN DATABASE: {len(all_items)}")
    
    print("\n" + "=" * 60)
    print("SEEDING COMPLETE!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    # Check if running in production
    db_url = os.getenv("DATABASE_URL", "")
    if db_url and "postgres" in db_url:
        print("Running in PRODUCTION mode (PostgreSQL)")
    else:
        print("Running in DEVELOPMENT mode (SQLite)")
    
    seed_from_csv()
