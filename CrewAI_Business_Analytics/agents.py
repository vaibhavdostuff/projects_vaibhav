from crewai import Crew, Agent
from tasks import DataCollectionTask, DataCleaningTask, VisualizationTask

# Define AI Agents
data_collector = Agent(name="Data Collector", task=DataCollectionTask)
data_cleaner = Agent(name="Data Cleaner", task=DataCleaningTask)
visualizer = Agent(name="Visualization Agent", task=VisualizationTask)

# Define Crew
crew = Crew(agents=[data_collector, data_cleaner, visualizer])
