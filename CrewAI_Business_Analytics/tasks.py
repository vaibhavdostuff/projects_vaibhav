from crewai import Task
import pandas as pd
import sqlite3

# Task: Collect Data
class DataCollectionTask(Task):
    def execute(self):
        conn = sqlite3.connect("data/sales_data.db")
        df = pd.read_sql_query("SELECT * FROM sales", conn)
        conn.close()
        return df
