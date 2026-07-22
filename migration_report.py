# 1. Run SQL
# 2. Export data
# 3. Zip the file

import pyodbc
import pandas as pd
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED

timestamp = datetime.now().strftime("%Y%m")

# Masked paths
base_path = r"C:\Path\To\SQL\Scripts"
export_path = rf"C:\Path\To\Exports\MigrationReport_{timestamp}.csv"
zip_file_path = rf"C:\Path\To\Exports\MigrationReport_{timestamp}.zip"

# Masked server + database
server = "YOUR_SERVER_NAME"
database = "YOUR_DATABASE_NAME"

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Masked SQL file names
sql_files = [
    "Step01.sql",
    "Step02.sql",
    "Step03.sql"
]

def run_sql_files():
    for file in sql_files:
        try:
            with open(f"{base_path}\\{file}", "r") as f:
                sql = f.read()
            cursor.execute(sql)
            conn.commit()
            print(f"{file} completed")
        except Exception as e:
            print(f"{file} failed")
            print(e)
            break

def export_file():
    try:
        query = "SELECT * FROM dbo.FinalTable"  # Masked table name
        df = pd.read_sql(query, conn)
        df.to_csv(export_path, index=False)
        print("Export success")
    except Exception as e:
        print(e)

def zip_exported_file():
    try:
        with ZipFile(zip_file_path, "w", ZIP_DEFLATED) as zipf:
            zipf.write(export_path, arcname=f"MigrationReport_{timestamp}.csv")
        print("Zip success")
    except Exception as e:
        print(e)

run_sql_files()
export_file()
zip_exported_file()
