from crewai import Crew
from agents import get_agents
from tasks import collect_data_task, clean_data_task, generate_dashboard_task

# Get the agents dynamically
data_collector, data_cleaner, visualization_agent = get_agents()

# Create a crew with agents
crew = Crew(agents=[data_collector, data_cleaner, visualization_agent])

# Assign tasks
crew.assign_tasks([collect_data_task, clean_data_task, generate_dashboard_task])

# Run the crew
crew.run()
