"""Seed inventory data into the database."""
from sqlmodel import Session, select

from database import engine, init_db
from models import InventoryItem


# Baseball Inventory - Fall 2025
INVENTORY_ITEMS = [
    # Equipment
    {"item_name": "Jugs pitch machine", "category": "other", "quantity": 1},
    {"item_name": "Practice baseballs", "category": "ball", "quantity": 57},
    {"item_name": "Practice tee balls", "category": "ball", "quantity": 56},
    {"item_name": "Softball", "category": "ball", "quantity": 1},
    {"item_name": "Wiffle / Pickleball balls", "category": "ball", "quantity": 63},
    {"item_name": "Tennis balls", "category": "ball", "quantity": 33},
    {"item_name": "Hard yellow practice balls", "category": "ball", "quantity": 20},
    {"item_name": "Little League game balls", "category": "ball", "quantity": 38, "notes": "26 still wrapped"},
    {"item_name": "Soft compression Wilson game balls", "category": "ball", "quantity": 11, "notes": "10 still wrapped"},
    
    # Batting Helmets
    {"item_name": "Batting helmet - Blue", "category": "helmet", "size": "One Size", "quantity": 10, "notes": "Some with face guards attached"},
    {"item_name": "Batting helmet - Black", "category": "helmet", "size": "One Size", "quantity": 15, "notes": "Some with face guards attached"},
    {"item_name": "Batting helmet - Purple", "category": "helmet", "size": "One Size", "quantity": 14, "notes": "Some with face guards attached"},
    {"item_name": "Batting helmet - Green", "category": "helmet", "size": "One Size", "quantity": 1},
    {"item_name": "Batting helmet - White", "category": "helmet", "size": "One Size", "quantity": 1},
    {"item_name": "Face guard shield - Black", "category": "helmet", "quantity": 18},
    {"item_name": "Face guard shield - Silver", "category": "helmet", "quantity": 3, "notes": "Still in packaging"},
    
    # Catcher Gear
    {"item_name": "Catcher helmet (full)", "category": "helmet", "quantity": 10, "notes": "One new with tags; one older in poor condition"},
    {"item_name": "Catcher glove (left hand)", "category": "glove", "quantity": 4},
    {"item_name": "Chest protector", "category": "other", "size": "Various", "quantity": 14, "notes": "Several in excellent condition"},
    {"item_name": "Leg pads (set)", "category": "other", "quantity": 12, "notes": "Several in excellent condition"},
    
    # Bats
    {"item_name": "Baseball bat (USA logo)", "category": "bat", "quantity": 12},
    {"item_name": "Tee ball bat", "category": "bat", "quantity": 3},
    {"item_name": "Baseball bat (no USA logo)", "category": "bat", "quantity": 1},
    
    # Training
    {"item_name": "Hitting tee", "category": "other", "quantity": 9},
    {"item_name": "Hitting tee (new in package)", "category": "other", "quantity": 2, "notes": "Brand new in packages"},
    
    # Umpire Gear
    {"item_name": "External umpire vest", "category": "other", "quantity": 1},
    {"item_name": "Internal umpire vest", "category": "other", "quantity": 1},
    {"item_name": "Umpire full helmet", "category": "helmet", "quantity": 1},
    {"item_name": "Umpire mask (older)", "category": "other", "quantity": 3},
    {"item_name": "Umpire leg pads set", "category": "other", "quantity": 1},
    {"item_name": "Umpire additional leg pad", "category": "other", "quantity": 1},
    
    # Field Supplies
    {"item_name": "Guide Line white field marker (bags)", "category": "other", "quantity": 45, "notes": "Stacked on pallet - approximate count"},
    {"item_name": "Infield turf (bags)", "category": "other", "quantity": 30, "notes": "Stacked on pallet - approximate count"},
    {"item_name": "White spray cans", "category": "other", "quantity": 0, "notes": "Harold took inside to keep warm - count unknown"},
    
    # Apparel - Jerseys
    {"item_name": "Blue jersey (no logo)", "category": "jersey", "size": "Small Youth", "quantity": 14},
    {"item_name": "Gray Easton youth tee", "category": "jersey", "size": "Youth", "quantity": 5, "notes": "Wrapped in new packaging"},
    {"item_name": "Maroon tee", "category": "jersey", "size": "2XL Youth", "quantity": 1, "notes": "Wrapped in new packaging"},
    {"item_name": "Blue jersey", "category": "jersey", "size": "Youth L", "quantity": 2, "notes": "Wrapped in new packaging"},
    {"item_name": "Gray jersey", "category": "jersey", "size": "Youth L", "quantity": 8, "notes": "Wrapped in new packaging"},
    {"item_name": "Yellow GB tee with number", "category": "jersey", "quantity": 10, "notes": "Numbers on back"},
    
    # Purple Game Jerseys
    {"item_name": "Purple game jersey", "category": "jersey", "size": "Youth S", "quantity": 2},
    {"item_name": "Purple game jersey", "category": "jersey", "size": "Youth M", "quantity": 5},
    {"item_name": "Purple game jersey", "category": "jersey", "size": "Youth L", "quantity": 8},
    {"item_name": "Purple game jersey", "category": "jersey", "size": "Youth XL", "quantity": 2},
    {"item_name": "Purple game jersey", "category": "jersey", "size": "Mens S", "quantity": 3},
    {"item_name": "Purple game jersey", "category": "jersey", "size": "Mens M", "quantity": 3},
    {"item_name": "Purple game jersey", "category": "jersey", "size": "Mens L", "quantity": 5},
    {"item_name": "Purple game jersey", "category": "jersey", "size": "Mens XL", "quantity": 5},
    
    # All Stars Jerseys
    {"item_name": "Purple Bucksport All Stars Henley", "category": "jersey", "size": "Youth M", "quantity": 4, "notes": "Gold lettering; all star patch on sleeve"},
    {"item_name": "Purple Bucksport All Stars Henley", "category": "jersey", "size": "Youth L", "quantity": 7, "notes": "Gold lettering; all star patch on sleeve"},
    {"item_name": "Purple Bucksport All Stars Henley", "category": "jersey", "size": "Adult S", "quantity": 1, "notes": "Gold lettering; all star patch on sleeve"},
    {"item_name": "Purple Bucksport All Stars Henley", "category": "jersey", "size": "Adult M", "quantity": 1, "notes": "Gold lettering; all star patch on sleeve"},
    {"item_name": "Purple all star jersey", "category": "jersey", "size": "Adult S", "quantity": 2, "notes": "All star patch on sleeve"},
    {"item_name": "Purple all star jersey", "category": "jersey", "size": "Adult M", "quantity": 3, "notes": "All star patch on sleeve"},
    {"item_name": "Purple all star jersey", "category": "jersey", "size": "Adult L", "quantity": 1, "notes": "All star patch on sleeve"},
    {"item_name": "Purple all star jersey", "category": "jersey", "size": "Adult XL", "quantity": 1, "notes": "All star patch on sleeve"},
    
    # Accessories
    {"item_name": "Yellow socks (package)", "category": "other", "quantity": 1},
    {"item_name": "Purple socks (package)", "category": "other", "quantity": 1},
    {"item_name": "Black baseball belt", "category": "other", "quantity": 11},
    
    # Pants
    {"item_name": "Gray pants with blue piping", "category": "pants", "size": "Youth XL", "quantity": 23, "notes": "Most/all wrapped in new packaging"},
    {"item_name": "Gray pants", "category": "pants", "size": "Size 30", "quantity": 3, "notes": "Wrapped in new packaging"},
    {"item_name": "Used gray pants (tote)", "category": "pants", "size": "Various", "quantity": 1, "notes": "Tote of used pants"},
    {"item_name": "Gray pants", "category": "pants", "size": "Youth S/XS", "quantity": 1, "notes": "Tote of pants"},
    {"item_name": "Gray pants", "category": "pants", "size": "Medium", "quantity": 1, "notes": "In separate tote"},
    
    # Golden Bucks Tees
    {"item_name": "Purple cotton tee (Golden Bucks)", "category": "jersey", "size": "Youth Various", "quantity": 16},
    {"item_name": "Gold cotton tee (Golden Bucks)", "category": "jersey", "size": "Youth Various", "quantity": 12},
    
    # ============ SOFTBALL INVENTORY - Fall 2025 ============
    {"item_name": "Batting tee", "category": "other", "quantity": 1, "notes": "Softball inventory"},
    
    # Softball Balls
    {"item_name": "12 inch game balls (new in boxes)", "category": "ball", "size": "12 inch", "quantity": 35, "notes": "Softball"},
    {"item_name": "11 inch game balls (new in boxes)", "category": "ball", "size": "11 inch", "quantity": 28, "notes": "Softball"},
    {"item_name": "11 inch game balls (cardboard boxes)", "category": "ball", "size": "11 inch", "quantity": 48, "notes": "Softball"},
    {"item_name": "12 inch practice balls", "category": "ball", "size": "12 inch", "quantity": 43, "notes": "Softball"},
    {"item_name": "11 inch practice balls", "category": "ball", "size": "11 inch", "quantity": 44, "notes": "Softball"},
    {"item_name": "11 inch PXS sponge core balls", "category": "ball", "size": "11 inch", "quantity": 23, "notes": "Softball"},
    {"item_name": "12 inch practice soft balls", "category": "ball", "size": "12 inch", "quantity": 10, "notes": "Softball"},
    {"item_name": "11 inch practice soft balls", "category": "ball", "size": "11 inch", "quantity": 7, "notes": "Softball"},
    {"item_name": "12 inch pitching machine balls", "category": "ball", "size": "12 inch", "quantity": 12, "notes": "Softball - in a box"},
    {"item_name": "Wiffle balls", "category": "ball", "quantity": 1, "notes": "Softball - plastic bag"},
    
    # Softball Helmets & Bats
    {"item_name": "Softball helmet", "category": "helmet", "size": "6.5-7.5", "quantity": 14, "notes": "All but one with face guard; most older; most lack current approval stickers"},
    {"item_name": "Softball bat (USSSA)", "category": "bat", "quantity": 4, "notes": "Older bats"},
    {"item_name": "Softball bat (no logo)", "category": "bat", "quantity": 1, "notes": "Older bat"},
    {"item_name": "Baseball bat", "category": "bat", "quantity": 2, "notes": "Softball inventory"},
    {"item_name": "Tee ball bat", "category": "bat", "quantity": 1, "notes": "Softball inventory"},
    
    # Softball Catcher Gear - Blue Bin
    {"item_name": "Leg pads (size 17)", "category": "other", "size": "Size 17", "quantity": 1, "notes": "Blue bin - softball"},
    {"item_name": "Leg pads (larger)", "category": "other", "quantity": 1, "notes": "Blue bin - softball"},
    {"item_name": "Chest protector", "category": "other", "quantity": 2, "notes": "Blue bin - softball"},
    {"item_name": "Face mask (no full helmet)", "category": "helmet", "quantity": 2, "notes": "Blue bin - softball"},
    
    # Softball Catcher Gear - Black Bin
    {"item_name": "Small leg pads", "category": "other", "size": "Small", "quantity": 1, "notes": "Black bin - softball"},
    {"item_name": "Chest protector", "category": "other", "quantity": 1, "notes": "Black bin - softball"},
    {"item_name": "Leg pads with knee savers", "category": "other", "size": "Size 13", "quantity": 1, "notes": "Black bin - blue Rawlings bag"},
    {"item_name": "Chest protector", "category": "other", "quantity": 1, "notes": "Black bin - blue Rawlings bag"},
    {"item_name": "Full helmet", "category": "helmet", "quantity": 1, "notes": "Black bin - blue Rawlings bag"},
    
    # Softball Catcher Gear - Easton Bag
    {"item_name": "Leg pads", "category": "other", "quantity": 1, "notes": "Black Easton bag"},
    {"item_name": "Chest protector", "category": "other", "quantity": 1, "notes": "Black Easton bag"},
    {"item_name": "Full helmet", "category": "helmet", "quantity": 1, "notes": "Black Easton bag"},
    
    # Softball Catcher Gear - Dicks Bag
    {"item_name": "Full helmet (large)", "category": "helmet", "size": "Large", "quantity": 1, "notes": "Dicks Sporting Goods bag"},
    {"item_name": "Knee pads", "category": "other", "quantity": 1, "notes": "Dicks Sporting Goods bag"},
    {"item_name": "Chest pads", "category": "other", "quantity": 1, "notes": "Dicks Sporting Goods bag"},
    
    # Softball Umpire Gear - Black Sea Bag
    {"item_name": "Umpire shirt", "category": "other", "quantity": 1, "notes": "Black sea bag"},
    {"item_name": "Umpire leg pads", "category": "other", "quantity": 1, "notes": "Black sea bag"},
    {"item_name": "Umpire chest protector", "category": "other", "quantity": 1, "notes": "Black sea bag"},
    {"item_name": "Umpire face mask (non-helmet)", "category": "other", "quantity": 2, "notes": "Black sea bag"},
    {"item_name": "Ball and strike counter", "category": "other", "quantity": 1, "notes": "Black sea bag"},
    {"item_name": "Plate brush", "category": "other", "quantity": 1, "notes": "Black sea bag"},
    
    # Softball Pants
    {"item_name": "Girls pants - Gray", "category": "pants", "size": "Girls S", "quantity": 3, "notes": "Some new with tags; most older/used"},
    {"item_name": "Girls pants - Gray", "category": "pants", "size": "Girls M", "quantity": 2, "notes": "Some new with tags; most older/used"},
    {"item_name": "Girls pants - Black", "category": "pants", "size": "Girls M", "quantity": 1},
    {"item_name": "Girls pants - Gray", "category": "pants", "size": "Girls L", "quantity": 3, "notes": "Some new with tags; most older/used"},
    {"item_name": "Womens pants - Gray", "category": "pants", "size": "Womens M", "quantity": 1},
    {"item_name": "Womens pants - Gray", "category": "pants", "size": "Womens XL", "quantity": 1},
    
    # Softball Misc
    {"item_name": "Bennett Painting coaches jersey", "category": "jersey", "size": "Adult", "quantity": 4},
    {"item_name": "Left handed glove", "category": "glove", "size": "Various", "quantity": 5, "notes": "Donated bin - catch with left hand"},
    {"item_name": "Cleats", "category": "cleats", "size": "Youth 1-8.5", "quantity": 10, "notes": "Donated bin - mostly good condition; some older/poor"},
    {"item_name": "Dura Stripe marking paint cans", "category": "other", "quantity": 11, "notes": "Open case"},
    {"item_name": "Red first aid kit", "category": "other", "quantity": 4, "notes": "Very close to full with bandages and basic essentials"},
    {"item_name": "Blue first aid kit", "category": "other", "quantity": 1, "notes": "Very close to full with bandages and basic essentials"},
]


def seed_inventory():
    """Seed inventory items into the database."""
    # Initialize database
    init_db()
    
    with Session(engine) as session:
        # Check if inventory already exists
        statement = select(InventoryItem)
        existing_items = session.exec(statement).all()
        
        if existing_items:
            print(f"Database already has {len(existing_items)} inventory items. Skipping seed.")
            return
        
        # Create inventory items
        for item_data in INVENTORY_ITEMS:
            item = InventoryItem(**item_data)
            session.add(item)
            print(f"Added: {item.item_name} ({item.category}) - Qty: {item.quantity}")
        
        session.commit()
        print(f"\n✅ Successfully seeded {len(INVENTORY_ITEMS)} inventory items!")


if __name__ == "__main__":
    seed_inventory()
