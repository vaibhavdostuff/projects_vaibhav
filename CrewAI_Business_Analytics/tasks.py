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

# Task: Clean Data
class DataCleaningTask(Task):
    def execute(self, df):
        df.dropna(inplace=True)  # Remove null values
        df["Revenue"] = df["Units Sold"] * df["Price Per Unit"]
        return df

# Task: Generate Visualization
class VisualizationTask(Task):
    def execute(self, df):
        # Assume Power BI/Tableau integration
        return "Dashboard Updated Successfully"
    