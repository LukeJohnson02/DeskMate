import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
  const [tickets, setTickets] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const token = localStorage.getItem("token");

    const fetchTickets = useCallback(() => {
        axios
        .get("http://localhost:8000/tickets/", {
            headers: { Authorization: `Bearer ${token}` },
        })
        .then((res) => setTickets(res.data))
        .catch((err) => {
            console.error("Dashboard error:", err);
            setError("Failed to load dashboard data");
        });
    }, [token]);

    useEffect(() => {
        fetchTickets();
    }, [fetchTickets]);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this ticket?")) return;

    try {
      await axios.delete(`http://localhost:8000/tickets/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      // Remove deleted ticket from state to update UI
      setTickets((prev) => prev.filter((ticket) => ticket.id !== id));
    } catch (err) {
      console.error("Delete failed:", err);
      alert("Failed to delete ticket");
    }
  };

  const handleEdit = (id) => {
    navigate(`/tickets/${id}/edit`); // Adjust route as needed
  };

  if (error) return <div className="text-red-600">{error}</div>;
  if (!tickets) return <div>Loading...</div>;

return (
  <div>
    <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
    {tickets.length === 0 ? (
      <p>No tickets found.</p>
    ) : (
      <ul>
        {tickets.map((ticket) => (
          <li
            key={ticket.id}
            className="flex justify-between items-center border p-4 mb-3 rounded-lg"
          >
            <div>
              <strong>{ticket.title}</strong> - Status: {ticket.status}
            </div>
            <div className="space-x-2">
              <button
                onClick={() => handleEdit(ticket.id)}
                className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(ticket.id)}
                className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 transition"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    )}
  </div>
);
};

export default Dashboard;
