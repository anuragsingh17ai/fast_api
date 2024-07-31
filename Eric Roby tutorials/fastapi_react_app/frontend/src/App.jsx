import React, { useState, useEffect } from "react";
import api from './api';

const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [formData, setFormData] = useState({
    amount: "",
    category: "",
    description: "",
    is_income: false,
    date: ""
  });

  const fetchTransactions = async () => {
    const response = await api.get('/transactions/');
    setTransactions(response.data);
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleInputChange = (event) => {
    const value = event.target.type === "checkbox" ? event.target.checked : event.target.value;
    setFormData({
      ...formData,
      [event.target.name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post('/transactions/', formData);
    fetchTransactions();
    setFormData({
      amount: "",
      category: "",
      description: "",
      is_income: false,
      date: ""
    });
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <nav className="bg-blue-600 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <a className="text-white text-2xl font-bold" href="#">
            Finance App
          </a>
        </div>
      </nav>

      <div className="container mx-auto mt-6 bg-white p-8 rounded-lg shadow-md">
        <form onSubmit={handleFormSubmit}>
          <div className="mb-4">
            <label htmlFor="amount" className="block text-gray-700 text-sm font-medium mb-2">
              Amount
            </label>
            <input 
              type="text" 
              id="amount" 
              name="amount"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              onChange={handleInputChange} 
              value={formData.amount}
            />
          </div>

          <div className="mb-4">
            <label htmlFor="category" className="block text-gray-700 text-sm font-medium mb-2">
              Category
            </label>
            <input 
              type="text" 
              id="category" 
              name="category"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              onChange={handleInputChange} 
              value={formData.category}
            />
          </div>

          <div className="mb-4">
            <label htmlFor="description" className="block text-gray-700 text-sm font-medium mb-2">
              Description
            </label>
            <input 
              type="text" 
              id="description" 
              name="description"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              onChange={handleInputChange} 
              value={formData.description}
            />
          </div>

          <div className="mb-4 flex items-center">
            <input 
              type="checkbox" 
              id="is_income" 
              name="is_income"
              className="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              onChange={handleInputChange} 
              checked={formData.is_income}
            />
            <label htmlFor="is_income" className="ml-2 text-gray-700 text-sm font-medium">
              Income
            </label>
          </div>

          <div className="mb-4">
            <label htmlFor="date" className="block text-gray-700 text-sm font-medium mb-2">
              Date
            </label>
            <input 
              type="text" 
              id="date" 
              name="date"
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              onChange={handleInputChange} 
              value={formData.date}
            />
          </div>

          <button 
            type="submit" 
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default App;
