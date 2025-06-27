import React, { useEffect, useState, useCallback } from "react";
import axios from "axios";

const Dashboard = () => {
  const [tickets, setTickets] = useState(null);
  const [error, setError] = useState(null);
  const [editTicket, setEditTicket] = useState(null);
  const [editError, setEditError] = useState(null);
  const [deleteLoadingId, setDeleteLoadingId] = useState(null);
  const [deleteError, setDeleteError] = useState(null);

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
    setDeleteError(null);
    setDeleteLoadingId(id);

    try {
      await axios.delete(`http://localhost:8000/tickets/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTickets((prev) => prev.filter((ticket) => ticket.id !== id));
    } catch (err) {
      console.error("Delete failed:", err);
      setDeleteError(`Failed to delete ticket #${id}. Please try again.`);
    } finally {
      setDeleteLoadingId(null);
    }
  };

  const handleEdit = (ticket) => {
    setEditError(null);
    setEditTicket({ ...ticket });
  };

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    setEditError(null);

    try {
      const params = new URLSearchParams({
        title: editTicket.title,
        description: editTicket.description,
        status: editTicket.status,
      }).toString();

      await axios.put(
        `http://localhost:8000/tickets/${editTicket.id}?${params}`,
        null,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setEditTicket(null);
      fetchTickets();
    } catch (err) {
      console.error("Update failed:", err.response?.data || err.message);
      setEditError("Failed to update ticket. Please check your input.");
    }
  };

  if (error) return <div className="text-red-600">{error}</div>;
  if (!tickets) return <div>Loading...</div>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
      {deleteError && (
        <div className="mb-4 text-red-600 font-medium">{deleteError}</div>
      )}
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
                  onClick={() => handleEdit(ticket)}
                  className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700 transition"
                  disabled={deleteLoadingId === ticket.id}
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(ticket.id)}
                  className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 transition"
                  disabled={deleteLoadingId === ticket.id}
                >
                  {deleteLoadingId === ticket.id ? "Deleting..." : "Delete"}
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {editTicket && (
        <div className="fixed top-0 right-0 w-full max-w-md h-full bg-white shadow-lg z-50 p-6 overflow-y-auto transition-transform duration-300">
          <h3 className="text-xl font-bold mb-4">Edit Ticket</h3>
          {editError && (
            <div className="mb-3 text-red-600 font-medium">{editError}</div>
          )}
          <form onSubmit={handleEditSubmit}>
            <label className="block mb-2">
              Title:
              <input
                type="text"
                value={editTicket.title}
                onChange={(e) =>
                  setEditTicket({ ...editTicket, title: e.target.value })
                }
                className="w-full border px-2 py-1 mt-1"
                required
              />
            </label>

            <label className="block mb-2">
              Description:
              <textarea
                value={editTicket.description}
                onChange={(e) =>
                  setEditTicket({ ...editTicket, description: e.target.value })
                }
                className="w-full border px-2 py-1 mt-1"
                required
              />
            </label>

            <label className="block mb-2">
              Status:
              <select
                value={editTicket.status}
                onChange={(e) =>
                  setEditTicket({ ...editTicket, status: e.target.value })
                }
                className="w-full border px-2 py-1 mt-1"
                required
              >
                <option value="OPEN">OPEN</option>
                <option value="IN_PROGRESS">IN_PROGRESS</option>
                <option value="CLOSED">CLOSED</option>
              </select>
            </label>

            <div className="flex justify-end space-x-2">
              <button
                type="button"
                onClick={() => setEditTicket(null)}
                className="px-4 py-2 border rounded"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
              >
                Save
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
