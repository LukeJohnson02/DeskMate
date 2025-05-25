import React, { useEffect, useState } from "react";
import axios from "axios";

const Tickets = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/tickets/")
      .then(res => {
        setTickets(res.data);
        setLoading(false);
      })
      .catch(err => {
        setError("Failed to fetch tickets");
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading tickets...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>Tickets</h2>
      {tickets.length === 0 ? (
        <p>No tickets found.</p>
      ) : (
        <ul>
          {tickets.map(ticket => (
            <li key={ticket.id}>
              <strong>{ticket.title}</strong> - Status: {ticket.status}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Tickets;