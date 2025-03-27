from crewai import Task
from agents import data_collector, data_cleaner, visualization_agent

# Task for data collection
collect_data_task = Task(name="Fetch Sales Data",
                         agent=data_collector)

# Task for data cleaning
clean_data_task = Task(name="Clean and Process Data",
                       agent=data_cleaner)

# Task for visualization
generate_dashboard_task = Task(name="Create Power BI Dashboard",
                               agent=visualization_agent)
