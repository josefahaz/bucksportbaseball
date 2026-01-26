import math
from datetime import date, datetime

import pandas as pd
from sqlmodel import Session, select

from bucksport_api.database import engine
from bucksport_api.models import SponsorshipSheetMeta, SponsorshipSheetRow


EXCEL_FILE = "Softball AND Baseball Banner & Sponsorship Log.xlsx"
SHEETS = [
    "Master Sponsor List",
    "Softball Banners - Current",
    "Softball Banners - Team Sponsor",
    "Baseball Banners - Current",
]


def _json_safe(value):
    if value is None:
        return ""

    # pandas NA
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    # convert numpy scalars
    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            pass

    # float nan
    if isinstance(value, float) and math.isnan(value):
        return ""

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    return value


def import_sheet(session: Session, sheet_name: str) -> int:
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, dtype=object)

    # Preserve exact column headers, including multiline strings.
    columns = [str(c) for c in df.columns]

    meta = session.get(SponsorshipSheetMeta, sheet_name)
    if not meta:
        meta = SponsorshipSheetMeta(sheet_name=sheet_name, columns=columns)
    else:
        meta.columns = columns
        meta.updated_at = datetime.utcnow()

    session.add(meta)
    session.commit()

    # Replace existing rows for this sheet
    existing_rows = session.exec(
        select(SponsorshipSheetRow).where(SponsorshipSheetRow.sheet_name == sheet_name)
    ).all()
    for r in existing_rows:
        session.delete(r)
    session.commit()

    inserted = 0
    for idx, row in df.iterrows():
        row_data = {str(col): _json_safe(row[col]) for col in df.columns}

        # Keep Excel-like row numbering (header row is 1, first data row is 2)
        excel_row_index = int(idx) + 2

        session.add(
            SponsorshipSheetRow(
                sheet_name=sheet_name,
                row_index=excel_row_index,
                data=row_data,
                updated_at=datetime.utcnow(),
            )
        )
        inserted += 1

    session.commit()
    return inserted


def main() -> None:
    with Session(engine) as session:
        total = 0
        for sheet in SHEETS:
            inserted = import_sheet(session, sheet)
            print(f"✅ Imported {inserted} rows for sheet: {sheet}")
            total += inserted

        print(f"\n✅ Done. Total rows imported: {total}")


if __name__ == "__main__":
    main()
