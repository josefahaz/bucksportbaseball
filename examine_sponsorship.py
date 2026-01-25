import pandas as pd

# Load the Excel file
xl = pd.ExcelFile('Softball AND Baseball Banner & Sponsorship Log.xlsx')

print('Sheet names:')
for name in xl.sheet_names:
    print(f'  - {name}')

print('\n' + '='*80 + '\n')

# Examine each sheet
for sheet_name in xl.sheet_names:
    print(f'Sheet: {sheet_name}')
    df = pd.read_excel(xl, sheet_name=sheet_name)
    print(f'Columns: {list(df.columns)}')
    print(f'Rows: {len(df)}')
    print('\nFirst 3 rows:')
    print(df.head(3))
    print('\n' + '='*80 + '\n')
