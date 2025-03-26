from crewai import Agent

# Agent to collect data from databases
data_collector = Agent(name="Data Collector",
                       description="Pulls sales data from databases and APIs.")

# Agent to clean and process the data
data_cleaner = Agent(name="Data Cleaner",
                     description="Cleans and prepares dataset for analysis.")

# Agent to generate visual dashboards
visualization_agent = Agent(name="Visualization Agent",
                            description="Creates Power BI/Tableau dashboards.")
