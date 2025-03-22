from fastapi import FastAPI
from routes import router as sales_router
from crewai_agents import get_sales_insights

app = FastAPI()

app.include_router(sales_router)

@app.get("/crewai-sales-insights/")
def crewai_sales_insights():
    insights = get_sales_insights()
    return {"crewai_insight": insights}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

