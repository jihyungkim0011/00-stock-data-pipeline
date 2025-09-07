import React, { useState, useEffect } from 'react';
import { getStockData } from '../api/stockApi';

function StockData() {
  const [stockData, setStockData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStockData = async () => {
      try {
        const data = await getStockData('AAPL'); // Example: Fetch data for Apple
        setStockData(data);
      } catch (error) {
        console.error("Error fetching stock data:", error);
      }
      setLoading(false);
    };

    fetchStockData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!stockData) {
    return <div>No stock data available.</div>;
  }

  return (
    <div>
      <h2>{stockData.name} ({stockData.symbol})</h2>
      <p>Price: {stockData.price}</p>
      <p>Change: {stockData.change}</p>
    </div>
  );
}

export default StockData;
