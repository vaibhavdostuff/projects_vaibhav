from crewai import Task

def get_tasks(data_collector, data_cleaner, visualization_agent):
    collect_data_task = Task(
        name="Collect Data",
        agent=data_collector,
        description="Gather data from an API and save it to a CSV file.",
        execute="from utils import collect_data; collect_data()"
    )

    clean_data_task = Task(
        name="Clean Data",
        agent=data_cleaner,
        description="Clean the collected data and remove inconsistencies.",
        execute="from utils import clean_data; clean_data()"
    )

    generate_dashboard_task = Task(
        name="Generate Dashboard",
        agent=visualization_agent,
        description="Create a visual dashboard using cleaned data.",
        execute="from utils import generate_dashboard; generate_dashboard()"
    )

    return collect_data_task, clean_data_task, generate_dashboard_task
