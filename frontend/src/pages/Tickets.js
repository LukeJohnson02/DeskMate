import React, { useEffect, useState, useCallback} from "react";
import axios from "axios";

const Tickets = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAdmin, setIsAdmin] = useState(false);
  const [newTicketTitle, setNewTicketTitle] = useState("");
  const [newTicketDescription, setNewTicketDescription] = useState("");

  const token = localStorage.getItem("token");

  const fetchTickets = useCallback(() => {
    axios
      .get("http://localhost:8000/tickets/", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setTickets(res.data);
        setLoading(false);
      })
      .catch(() => {
        setError("Failed to fetch tickets");
        setLoading(false);
      });
  }, [token]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/users/me", {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then((res) => {
        setIsAdmin(res.data.is_admin);
        fetchTickets();
      })
      .catch(() => {
        setError("Failed to fetch user info");
        setLoading(false);
      });
  }, [fetchTickets, token]);

  const handleCreateTicket = (e) => {
    e.preventDefault();
    setError(null);

    axios
      .post(
        "http://localhost:8000/tickets/",
        {
          title: newTicketTitle,
          description: newTicketDescription,
          // add any other required fields like category_id if needed
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      )
      .then(() => {
        setNewTicketTitle("");
        setNewTicketDescription("");
        fetchTickets();
      })
      .catch(() => setError("Failed to create ticket"));
  };

  if (loading) return <p>Loading tickets...</p>;
  if (error) return <p className="text-red-600">{error}</p>;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Tickets</h2>

      {!isAdmin && (
        <form onSubmit={handleCreateTicket} className="mb-6 space-y-3">
          <input
            type="text"
            placeholder="Ticket title"
            value={newTicketTitle}
            onChange={(e) => setNewTicketTitle(e.target.value)}
            required
            className="border p-2 rounded w-full"
          />
          <textarea
            placeholder="Ticket description"
            value={newTicketDescription}
            onChange={(e) => setNewTicketDescription(e.target.value)}
            required
            className="border p-2 rounded w-full"
          />
          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
          >
            Create Ticket
          </button>
        </form>
      )}

      {tickets.length === 0 ? (
        <p>No tickets found.</p>
      ) : (
        <ul>
          {tickets.map((ticket) => (
            <li
              key={ticket.id}
              className="border p-4 mb-3 rounded flex justify-between items-center"
            >
              <div>
                <strong>{ticket.title}</strong> - Status: {ticket.status}
              </div>
              {/* Add edit/delete buttons here if needed */}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Tickets;