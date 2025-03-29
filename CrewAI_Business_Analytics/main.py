from crewai import Crew
from agents import get_agents
from tasks import get_tasks

# Load agents
data_collector, data_cleaner, visualization_agent = get_agents()

# Load tasks
collect_data_task, clean_data_task, generate_dashboard_task = get_tasks(
    data_collector, data_cleaner, visualization_agent
)

# Create and run the crew
crew = Crew(agents=[data_collector, data_cleaner, visualization_agent])
crew.assign_tasks([collect_data_task, clean_data_task, generate_dashboard_task])
crew.run()

print("✅ Process Completed! Dashboard saved at output/dashboard.png")
