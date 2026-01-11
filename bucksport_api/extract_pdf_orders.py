"""Extract inventory items from PDF order files."""
import PyPDF2
import re
import sys
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

def parse_order_items(text, order_date):
    """Parse inventory items from order text."""
    items = []
    
    # Common patterns for order items
    # This is a basic parser - may need adjustment based on actual PDF format
    lines = text.split('\n')
    
    for line in lines:
        # Skip empty lines and headers
        if not line.strip() or 'TOTAL' in line.upper() or 'SUBTOTAL' in line.upper():
            continue
        
        # Look for quantity patterns (number at start or after description)
        qty_match = re.search(r'(\d+)\s*x?\s*(.+)', line)
        if qty_match:
            qty = int(qty_match.group(1))
            description = qty_match.group(2).strip()
            
            # Try to extract size information
            size = None
            size_match = re.search(r'(Youth|Adult|Mens|Womens|Girls|Boys)?\s*(XS|S|M|L|XL|XXL|2XL|\d+)', description, re.IGNORECASE)
            if size_match:
                size = size_match.group(0).strip()
            
            items.append({
                'description': description,
                'quantity': qty,
                'size': size,
                'order_date': order_date
            })
    
    return items

def main():
    base_path = Path(__file__).parent.parent
    
    pdf_files = [
        (base_path / "softball order 10.14.25.pdf", "2025-10-14"),
        (base_path / "softball order 11.20.25.pdf", "2025-11-20")
    ]
    
    all_items = []
    
    for pdf_path, order_date in pdf_files:
        if not pdf_path.exists():
            print(f"Warning: {pdf_path} not found")
            continue
        
        print(f"\nProcessing {pdf_path.name}...")
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            items = parse_order_items(text, order_date)
            all_items.extend(items)
            print(f"Found {len(items)} items in {pdf_path.name}")
            
            # Print items for review
            for item in items:
                print(f"  - {item['quantity']}x {item['description']} (Size: {item['size'] or 'N/A'})")
    
    print(f"\n\nTotal items extracted: {len(all_items)}")
    
    # Save to a temporary file for review
    output_file = base_path / "extracted_order_items.txt"
    with open(output_file, 'w') as f:
        for item in all_items:
            f.write(f"{item['quantity']}\t{item['description']}\t{item['size'] or ''}\t{item['order_date']}\n")
    
    print(f"\nExtracted items saved to: {output_file}")
    return all_items

if __name__ == "__main__":
    main()
