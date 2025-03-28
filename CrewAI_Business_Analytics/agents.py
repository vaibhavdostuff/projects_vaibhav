from crewai import Agent
from tasks import collect_data_task, clean_data_task, generate_dashboard_task

data_collector = Agent(
    name="Data Collector",
    role="Extracting data",
    goal="Collect relevant business data from databases and APIs.",
    backstory="An AI-powered assistant skilled in gathering structured and unstructured data efficiently.",
    tasks=[collect_data_task]
)

data_cleaner = Agent(
    name="Data Cleaner",
    role="Data preprocessing",
    goal="Clean and structure the raw data to ensure accuracy.",
    backstory="A meticulous AI responsible for filtering and standardizing data for analysis.",
    tasks=[clean_data_task]
)

visualization_agent = Agent(
    name="Visualization Expert",
    role="Data visualization",
    goal="Create insightful dashboards to present business analytics.",
    backstory="An AI that specializes in converting raw data into meaningful visual insights using Power BI.",
    tasks=[generate_dashboard_task]
)
