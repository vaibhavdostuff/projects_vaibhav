from flask import Flask, jsonify
from agents import crew
from database import init_db, get_sales_data

# Initialize Flask App
app = Flask(__name__)

# Initialize Database
init_db()

@app.route("/run", methods=["GET"])
def run_agents():
    df = get_sales_data()
    insights, dashboard_status = crew.run(df)
    
    return jsonify({"Dashboard Status": dashboard_status, "Insights": insights})

if __name__ == "__main__":
    app.run(debug=True)

