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