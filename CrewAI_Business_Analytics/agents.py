from crewai import Agent

def get_agents():
    data_collector = Agent(
        name="Data Collector",
        role="Extracting Data",
        goal="Gather raw data from APIs and databases",
        backstory="An AI expert in data extraction and web scraping."
    )

    data_cleaner = Agent(
        name="Data Cleaner",
        role="Cleaning Data",
        goal="Process and clean data to ensure accuracy",
        backstory="A data scientist skilled in data preprocessing."
    )

    visualization_agent = Agent(
        name="Visualization Expert",
        role="Creating Dashboards",
        goal="Generate meaningful visualizations from processed data",
        backstory="A visualization expert with a keen eye for data trends."
    )

    return data_collector, data_cleaner, visualization_agent
