import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const Dashboard = () => {
  const [salesData, setSalesData] = useState([]);
  const [insights, setInsights] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/sales/")
      .then((res) => res.json())
      .then((data) => setSalesData(data.sales.map(sale => ({
        name: sale[1],
        sales: sale[2]
      }))))
      .catch((err) => console.error("Error fetching sales data:", err));
  }, []);

  const fetchInsights = () => {
    fetch("http://localhost:8000/crewai-sales-insights/")
      .then((res) => res.json())
      .then((data) => setInsights(data.crewai_insight))
      .catch((err) => console.error("Error fetching insights:", err));
  };

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Sales Dashboard</h1>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={salesData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="sales" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
      <button onClick={fetchInsights} className="mt-4 p-2 bg-blue-500 text-white rounded">
        Get AI Insights
      </button>
      {insights && <p className="mt-4 p-2 bg-white shadow rounded">{insights}</p>}
    </div>
  );
};

export default Dashboard;