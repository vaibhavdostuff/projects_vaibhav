import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect("data/sales_data.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            units_sold INTEGER,
            price_per_unit REAL
        )
    ''')