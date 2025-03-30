from crewai import Task

collect_data_task = Task(
    description="Gather data from various sources, including databases and APIs.",
)

clean_data_task = Task(
    description="Process and clean raw data to ensure quality.",
)

generate_dashboard_task = Task(
    description="Create a Power BI dashboard to visualize the cleaned data.",
)
