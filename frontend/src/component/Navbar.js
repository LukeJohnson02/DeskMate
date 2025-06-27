import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import Logo from "../component/common/Logo";
import axios from "axios";

const Navbar = ({ onTicketCreated }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("token");

  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", category_id: 1 });
  const [createError, setCreateError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const isLoginPage = location.pathname === "/";

  const handleCreateSubmit = async (e) => {
    e.preventDefault();
    setCreateError(null);
    setLoading(true);

    try {
      const params = new URLSearchParams(form).toString();
      await axios.post(`http://localhost:8000/tickets/?${params}`, null, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setShowCreate(false);
      setForm({ title: "", description: "", category_id: 1 });
      if (onTicketCreated) onTicketCreated(); // notify parent to refresh tickets
    } catch (err) {
      console.error("Create failed:", err.response?.data || err.message);
      setCreateError("Failed to create ticket. Please check your input.");
    } finally {
      setLoading(false);
    }
  };

  if (isLoginPage) {
    return (
      <nav className="bg-white shadow-md p-4 flex justify-between items-center">
        <div className="text-xl font-bold text-blue-600">
          <Link to="/">
            <Logo />
          </Link>
        </div>
      </nav>
    );
  }

  return (
    <nav className="bg-white shadow-md p-4 flex justify-between items-center relative">
      <div className="text-xl font-bold text-blue-600">
        <Link to="/">
          <Logo />
        </Link>
      </div>

      <div className="flex gap-6 items-center">
        <Link to="/dashboard" className="text-gray-700 hover:text-blue-600">
          Dashboard
        </Link>

        <button
          onClick={() => setShowCreate(true)}
          className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 transition"
        >
          Create Ticket
        </button>

        <button
          onClick={handleLogout}
          className="text-red-500 hover:underline text-sm"
        >
          Logout
        </button>
      </div>

      {showCreate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded shadow-lg w-full max-w-md relative">
            <button
              onClick={() => setShowCreate(false)}
              className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
              aria-label="Close"
            >
              &times;
            </button>
            <h3 className="text-xl font-bold mb-4">Create Ticket</h3>
            {createError && (
              <div className="mb-3 text-red-600 font-medium">{createError}</div>
            )}
            <form onSubmit={handleCreateSubmit}>
              <label className="block mb-2">
                Title:
                <input
                  type="text"
                  value={form.title}
                  onChange={(e) => setForm({ ...form, title: e.target.value })}
                  className="w-full border px-2 py-1 mt-1"
                  required
                  disabled={loading}
                />
              </label>

              <label className="block mb-2">
                Description:
                <textarea
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  className="w-full border px-2 py-1 mt-1"
                  required
                  disabled={loading}
                />
              </label>

              <div className="flex justify-end space-x-2 mt-4">
                <button
                  type="button"
                  onClick={() => setShowCreate(false)}
                  className="px-4 py-2 border rounded"
                  disabled={loading}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
                  disabled={loading}
                >
                  {loading ? "Creating..." : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
