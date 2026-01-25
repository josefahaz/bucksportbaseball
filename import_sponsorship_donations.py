"""
Import sponsorship and donation data from Excel spreadsheet into the database.
This script reads the sponsorship spreadsheet and creates donation records for each year.
"""
import os
import sys
import pandas as pd
from datetime import date, datetime
from sqlmodel import Session, create_engine, select

# Add bucksport_api to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'bucksport_api'))

from models import Donation

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, echo=False)

def import_sponsorships():
    """Import sponsorship data from Excel file."""
    
    # Load the Excel file
    xl = pd.ExcelFile('Softball AND Baseball Banner & Sponsorship Log.xlsx')
    
    with Session(engine) as session:
        # Clear existing donations
        print("Clearing existing donation records...")
        existing = session.exec(select(Donation)).all()
        for donation in existing:
            session.delete(donation)
        session.commit()
        print(f"Cleared {len(existing)} existing records.")
        
        total_imported = 0
        
        # Process Master Sponsor List
        print("\nProcessing Master Sponsor List...")
        df_master = pd.read_excel(xl, sheet_name='Master Sponsor List')
        
        for _, row in df_master.iterrows():
            company_name = row.get('Company Name')
            if pd.isna(company_name) or company_name == '':
                continue
            
            # Process each year column
            for year in ['2025', '2024', '2023', '2022', '2021', '2020']:
                amount = row.get(year)
                if pd.notna(amount):
                    try:
                        amount_float = float(amount)
                        if amount_float > 0:
                            donation = Donation(
                                name=str(company_name),
                                amount=amount_float,
                                donation_type='Sponsorship',
                                date=date(int(year), 1, 1),  # Use Jan 1 of that year
                                division=row.get('Division') if pd.notna(row.get('Division')) else None,
                                contact_person=row.get('Contact Person') if pd.notna(row.get('Contact Person')) else None,
                                phone=row.get('Phone') if pd.notna(row.get('Phone')) else None,
                                email=row.get('Email') if pd.notna(row.get('Email')) else None,
                                address=row.get('Address') if pd.notna(row.get('Address')) else None,
                                notes=f"{row.get('Sponsor Type', '')} - {row.get('Notes', '')}" if pd.notna(row.get('Notes')) else row.get('Sponsor Type', '')
                            )
                            session.add(donation)
                            total_imported += 1
                    except (ValueError, TypeError):
                        # Skip non-numeric amounts
                        continue
        
        # Process Softball Banners - Current
        print("Processing Softball Banners - Current...")
        df_softball = pd.read_excel(xl, sheet_name='Softball Banners - Current')
        
        for _, row in df_softball.iterrows():
            business = row.get('Business')
            if pd.isna(business) or business == '':
                continue
            
            for year in ['2025', '2024', '2023', '2022', '2021']:
                amount = row.get(year)
                if pd.notna(amount):
                    try:
                        amount_float = float(amount)
                        if amount_float > 0:
                            donation = Donation(
                                name=str(business),
                                amount=amount_float,
                                donation_type='Sponsorship',
                                date=date(int(year), 1, 1),
                                division='Softball',
                                contact_person=row.get('Business Contact ') if pd.notna(row.get('Business Contact ')) else None,
                                address=row.get('Mailing Address / Contact Info') if pd.notna(row.get('Mailing Address / Contact Info')) else None,
                                notes=row.get('Notes') if pd.notna(row.get('Notes')) else None
                            )
                            session.add(donation)
                            total_imported += 1
                    except (ValueError, TypeError):
                        continue
        
        # Process Softball Banners - Team Sponsor
        print("Processing Softball Banners - Team Sponsor...")
        df_softball_team = pd.read_excel(xl, sheet_name='Softball Banners - Team Sponsor')
        
        for _, row in df_softball_team.iterrows():
            company = row.get('Company Name')
            if pd.isna(company) or company == '':
                continue
            
            for year in [2025, 2024, 2023, 2022, 2021, 2020]:
                amount = row.get(year)
                if pd.notna(amount):
                    try:
                        amount_float = float(amount)
                        if amount_float > 0:
                            donation = Donation(
                                name=str(company),
                                amount=amount_float,
                                donation_type='Sponsorship',
                                date=date(year, 1, 1),
                                division='Softball',
                                contact_person=row.get('Company Contact') if pd.notna(row.get('Company Contact')) else None,
                                phone=row.get('Phone') if pd.notna(row.get('Phone')) else None,
                                email=row.get('Email') if pd.notna(row.get('Email')) else None,
                                address=row.get('Address') if pd.notna(row.get('Address')) else None,
                                notes=row.get('Notes:') if pd.notna(row.get('Notes:')) else None
                            )
                            session.add(donation)
                            total_imported += 1
                    except (ValueError, TypeError):
                        continue
        
        # Process Baseball Banners - Current
        print("Processing Baseball Banners - Current...")
        df_baseball = pd.read_excel(xl, sheet_name='Baseball Banners - Current')
        
        for _, row in df_baseball.iterrows():
            business = row.get('Business')
            if pd.isna(business) or business == '':
                continue
            
            amount = row.get('2025')
            if pd.notna(amount):
                try:
                    amount_float = float(amount)
                    if amount_float > 0:
                        donation = Donation(
                            name=str(business),
                            amount=amount_float,
                            donation_type='Sponsorship',
                            date=date(2025, 1, 1),
                            division='Baseball',
                            contact_person=row.get('Business Contact ') if pd.notna(row.get('Business Contact ')) else None,
                            address=row.get('Mailing Address / Contact Info') if pd.notna(row.get('Mailing Address / Contact Info')) else None,
                            notes=row.get('Notes') if pd.notna(row.get('Notes')) else None
                        )
                        session.add(donation)
                        total_imported += 1
                except (ValueError, TypeError):
                    continue
        
        # Commit all donations
        session.commit()
        print(f"\n✅ Successfully imported {total_imported} donation records!")
        
        # Show summary
        print("\nSummary by year:")
        for year in [2025, 2024, 2023, 2022, 2021, 2020]:
            count = session.exec(
                select(Donation).where(Donation.date >= date(year, 1, 1)).where(Donation.date < date(year + 1, 1, 1))
            ).all()
            total = sum(d.amount for d in count)
            print(f"  {year}: {len(count)} donations, ${total:,.2f}")

if __name__ == "__main__":
    print("Importing sponsorship data from Excel spreadsheet...")
    print("=" * 80)
    import_sponsorships()
    print("\n" + "=" * 80)
    print("Import complete!")
