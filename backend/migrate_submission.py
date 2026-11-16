
import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "judgeai.db"

connection = sqlite3.connect(db_path)

existing = {
    row[1]
    for row in connection.execute("PRAGMA table_info(submissions)")
}

new_columns = {
    "query": "TEXT",
    "reference_answer": "TEXT",
    "tool_trace": "JSON",
}

for column, data_type in new_columns.items():
    if column not in existing:
        connection.execute(
            f"ALTER TABLE submissions ADD COLUMN {column} {data_type}"
        )
        print(f"Added column: {column}")

connection.commit()
connection.close()

print("Migration complete.")
