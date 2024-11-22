#### Preamble ####
# Purpose: Cleans the raw grocery data
# Author: Kevin Cai
# Date: Dec 1, 2024
# Contact: kev.cai@mail.utoronto.ca
# License: MIT
# Pre-requisites: 02-download_data

import sqlite3
import os


def execute_and_transfer(source_db, target_db):
    # Connect to the source SQLite database
    source_conn = sqlite3.connect(source_db)
    source_cursor = source_conn.cursor()

    # Create or connect to the target SQLite database
    if os.path.exists(target_db):
        os.remove(target_db)  # Remove if it exists to create a fresh database
    target_conn = sqlite3.connect(target_db)
    target_cursor = target_conn.cursor()

    try:
        # Get all tables in the source database
        source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = source_cursor.fetchall()

        for table_name in tables:
            table_name = table_name[0]  # Extract table name
            print(f"Processing table: {table_name}")

            # Create the table structure in the target database
            source_cursor.execute(
                f"SELECT sql FROM sqlite_master WHERE name='{table_name}' AND type='table';"
            )
            create_table_sql = source_cursor.fetchone()[0]
            target_cursor.execute(create_table_sql)

            # Transfer data
            source_cursor.execute(f"SELECT * FROM {table_name}")
            rows = source_cursor.fetchall()
            if rows:
                placeholders = ", ".join(["?"] * len(rows[0]))
                target_cursor.executemany(
                    f"INSERT INTO {table_name} VALUES ({placeholders})", rows
                )

        # Commit changes to the target database
        target_conn.commit()
        print(f"Data successfully transferred to {target_db}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close connections
        source_conn.close()
        target_conn.close()


source_db = "../data/01-raw_data/grocery_data.sqlite"
target_db = "../data/01-raw_data/grocery_clean.sqlite"
execute_and_transfer(source_db, target_db)
