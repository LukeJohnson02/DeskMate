import React, { useCallback, useEffect, useMemo, useState } from "react";
import axios from "axios";
import { API_BASE_URL } from "../services/api";

const blankTicket = {
  title: "",
  description: "",
  category_id: "",
  status: "OPEN",
};

const statusLabels = {
  OPEN: "Open",
  IN_PROGRESS: "In progress",
  CLOSED: "Closed",
};

const statusStyles = {
  OPEN: "bg-amber-100 text-amber-800 ring-amber-200",
  IN_PROGRESS: "bg-blue-100 text-blue-800 ring-blue-200",
  CLOSED: "bg-emerald-100 text-emerald-800 ring-emerald-200",
};

const sortByNewest = (items) =>
  [...items].sort((a, b) => Number(b.id) - Number(a.id));

const Dashboard = () => {
  const [tickets, setTickets] = useState([]);
  const [categories, setCategories] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [form, setForm] = useState(blankTicket);
  const [editTicket, setEditTicket] = useState(null);
  const [adminCreateOpen, setAdminCreateOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deleteLoadingId, setDeleteLoadingId] = useState(null);
  const [notice, setNotice] = useState(null);
  const [error, setError] = useState(null);

  const token = localStorage.getItem("token");
  const isAdmin = currentUser?.role === "admin";

  const authHeaders = useMemo(
    () => ({ Authorization: `Bearer ${token}` }),
    [token]
  );

  const categoryNameById = useMemo(
    () =>
      categories.reduce((lookup, category) => {
        lookup[category.id] = category.name;
        return lookup;
      }, {}),
    [categories]
  );

  const groupedTickets = useMemo(
    () => ({
      open: sortByNewest(tickets.filter((ticket) => ticket.status === "OPEN")),
      active: sortByNewest(
        tickets.filter((ticket) => ticket.status === "IN_PROGRESS")
      ),
      closed: sortByNewest(
        tickets.filter((ticket) => ticket.status === "CLOSED")
      ),
    }),
    [tickets]
  );

  const visibleAdminTickets = useMemo(
    () => [...groupedTickets.open, ...groupedTickets.active],
    [groupedTickets]
  );

  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const [ticketResponse, categoryResponse, userResponse] = await Promise.all([
        axios.get(`${API_BASE_URL}/tickets/`, { headers: authHeaders }),
        axios.get(`${API_BASE_URL}/categories/`),
        axios.get(`${API_BASE_URL}/users/me`, { headers: authHeaders }),
      ]);

      setTickets(ticketResponse.data);
      setCategories(categoryResponse.data);
      setCurrentUser(userResponse.data);

      if (categoryResponse.data.length > 0) {
        setForm((prev) => ({
          ...prev,
          category_id: prev.category_id || String(categoryResponse.data[0].id),
        }));
      }
    } catch (err) {
      console.error("Dashboard load failed:", err.response?.data || err.message);
      setError("Could not load DeskMate. Please sign in again or try later.");
    } finally {
      setLoading(false);
    }
  }, [authHeaders]);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  const resetForm = () => {
    setForm({
      ...blankTicket,
      category_id: categories[0] ? String(categories[0].id) : "",
    });
  };

  const handleCreateSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError(null);
    setNotice(null);

    try {
      await axios.post(
        `${API_BASE_URL}/tickets/`,
        {
          title: form.title.trim(),
          description: form.description.trim(),
          category_id: Number(form.category_id),
        },
        { headers: authHeaders }
      );

      resetForm();
      setAdminCreateOpen(false);
      setNotice("Ticket created successfully.");
      await fetchDashboardData();
    } catch (err) {
      console.error("Create failed:", err.response?.data || err.message);
      setError("Could not create the ticket. Check the title, description, and category.");
    } finally {
      setSaving(false);
    }
  };

  const handleEdit = (ticket) => {
    setError(null);
    setNotice(null);
    setEditTicket({
      ...ticket,
      category_id: String(ticket.category_id),
    });
  };

  const handleQuickStatus = async (ticket, status) => {
    setSaving(true);
    setError(null);
    setNotice(null);

    try {
      await axios.put(
        `${API_BASE_URL}/tickets/${ticket.id}`,
        {
          title: ticket.title,
          description:
            ticket.description.length >= 10
              ? ticket.description
              : `${ticket.description} - updated`,
          category_id: Number(ticket.category_id),
          status,
        },
        { headers: authHeaders }
      );
      setNotice(`Ticket moved to ${statusLabels[status].toLowerCase()}.`);
      await fetchDashboardData();
    } catch (err) {
      console.error("Status update failed:", err.response?.data || err.message);
      setError("Could not update the ticket status.");
    } finally {
      setSaving(false);
    }
  };

  const handleEditSubmit = async (event) => {
    event.preventDefault();
    setSaving(true);
    setError(null);
    setNotice(null);

    try {
      await axios.put(
        `${API_BASE_URL}/tickets/${editTicket.id}`,
        {
          title: editTicket.title.trim(),
          description: editTicket.description.trim(),
          category_id: Number(editTicket.category_id),
          status: editTicket.status,
        },
        { headers: authHeaders }
      );

      setEditTicket(null);
      setNotice("Ticket updated successfully.");
      await fetchDashboardData();
    } catch (err) {
      console.error("Update failed:", err.response?.data || err.message);
      setError("Could not update the ticket. Check the fields and try again.");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (ticket) => {
    if (!window.confirm(`Delete ticket "${ticket.title}"?`)) return;

    setDeleteLoadingId(ticket.id);
    setError(null);
    setNotice(null);

    try {
      await axios.delete(`${API_BASE_URL}/tickets/${ticket.id}`, {
        headers: authHeaders,
      });
      setTickets((prev) => prev.filter((item) => item.id !== ticket.id));
      setNotice("Ticket deleted successfully.");
    } catch (err) {
      console.error("Delete failed:", err.response?.data || err.message);
      setError("Could not delete that ticket. Please try again.");
    } finally {
      setDeleteLoadingId(null);
    }
  };

  if (loading) {
    return (
      <main className="min-h-screen bg-slate-50 px-4 py-8 text-slate-600">
        Loading DeskMate...
      </main>
    );
  }

  const ticketList = isAdmin ? visibleAdminTickets : sortByNewest(tickets);

  return (
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 py-8">
        <div className="mb-6 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <p className="text-sm font-medium text-blue-700">
              {isAdmin ? "Support operations" : "Self-service support"}
            </p>
            <h1 className="text-3xl font-bold text-slate-950">
              {isAdmin ? "Ticket Triage" : "My Support Tickets"}
            </h1>
            {currentUser && (
              <p className="mt-1 text-sm text-slate-600">
                Signed in as {currentUser.name} ({currentUser.role})
              </p>
            )}
          </div>

          <div className="grid grid-cols-3 gap-2 text-center">
            <Metric label="Open" value={groupedTickets.open.length} tone="amber" />
            <Metric label="Active" value={groupedTickets.active.length} tone="blue" />
            <Metric label="Closed" value={groupedTickets.closed.length} tone="emerald" />
          </div>
        </div>

        {notice && (
          <div className="mb-4 rounded border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
            {notice}
          </div>
        )}
        {error && (
          <div className="mb-4 rounded border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
            {error}
          </div>
        )}

        {isAdmin ? (
          <AdminCreatePanel
            isOpen={adminCreateOpen}
            onToggle={() => setAdminCreateOpen((value) => !value)}
            form={form}
            setForm={setForm}
            categories={categories}
            saving={saving}
            onSubmit={handleCreateSubmit}
          />
        ) : (
          <TicketForm
            title="Raise a Ticket"
            description="Tell the support team what is happening and where it is blocking you."
            form={form}
            setForm={setForm}
            categories={categories}
            saving={saving}
            onSubmit={handleCreateSubmit}
          />
        )}

        <section className="mt-6">
          <div className="mb-4 flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-slate-950">
                {isAdmin ? "Open Queue" : "Your Tickets"}
              </h2>
              <p className="text-sm text-slate-600">
                {isAdmin
                  ? "Prioritise open tickets, move work into progress, and close resolved issues."
                  : "Track updates on tickets you have raised."}
              </p>
            </div>
          </div>

          {ticketList.length === 0 ? (
            <div className="rounded border border-slate-200 bg-white px-4 py-10 text-center text-slate-600">
              {isAdmin
                ? "No open or active tickets need attention."
                : "You have not raised any tickets yet."}
            </div>
          ) : (
            <div className="grid gap-3">
              {ticketList.map((ticket) => (
                <TicketCard
                  key={ticket.id}
                  ticket={ticket}
                  categoryName={
                    categoryNameById[ticket.category_id] ||
                    `Category ${ticket.category_id}`
                  }
                  isAdmin={isAdmin}
                  saving={saving}
                  deleteLoadingId={deleteLoadingId}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                  onQuickStatus={handleQuickStatus}
                />
              ))}
            </div>
          )}
        </section>

        {isAdmin && groupedTickets.closed.length > 0 && (
          <section className="mt-8">
            <h2 className="mb-3 text-lg font-semibold text-slate-950">
              Recently Closed
            </h2>
            <div className="grid gap-3 md:grid-cols-2">
              {groupedTickets.closed.slice(0, 4).map((ticket) => (
                <TicketCard
                  key={ticket.id}
                  ticket={ticket}
                  categoryName={
                    categoryNameById[ticket.category_id] ||
                    `Category ${ticket.category_id}`
                  }
                  isAdmin={isAdmin}
                  compact
                  saving={saving}
                  deleteLoadingId={deleteLoadingId}
                  onEdit={handleEdit}
                  onDelete={handleDelete}
                  onQuickStatus={handleQuickStatus}
                />
              ))}
            </div>
          </section>
        )}
      </div>

      {editTicket && (
        <div className="fixed inset-0 z-50 bg-slate-950/40">
          <aside className="ml-auto h-full w-full max-w-md overflow-y-auto bg-white p-6 shadow-xl">
            <div className="mb-5 flex items-center justify-between">
              <h2 className="text-xl font-semibold text-slate-950">Edit Ticket</h2>
              <button
                type="button"
                onClick={() => setEditTicket(null)}
                className="rounded border border-slate-300 px-3 py-1.5 text-sm text-slate-700"
              >
                Close
              </button>
            </div>

            <form onSubmit={handleEditSubmit} className="space-y-4">
              <TicketFields
                form={editTicket}
                setForm={setEditTicket}
                categories={categories}
                includeStatus
              />

              <div className="flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setEditTicket(null)}
                  className="rounded border border-slate-300 px-4 py-2 font-medium text-slate-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="rounded bg-blue-700 px-4 py-2 font-medium text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-slate-400"
                >
                  {saving ? "Saving..." : "Save Changes"}
                </button>
              </div>
            </form>
          </aside>
        </div>
      )}
    </main>
  );
};

const Metric = ({ label, value, tone }) => {
  const tones = {
    amber: "text-amber-700",
    blue: "text-blue-700",
    emerald: "text-emerald-700",
  };

  return (
    <div className="rounded border border-slate-200 bg-white px-5 py-3">
      <div className={`text-2xl font-bold ${tones[tone]}`}>{value}</div>
      <div className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </div>
    </div>
  );
};

const AdminCreatePanel = ({
  isOpen,
  onToggle,
  form,
  setForm,
  categories,
  saving,
  onSubmit,
}) => (
  <section className="rounded border border-slate-200 bg-white">
    <button
      type="button"
      onClick={onToggle}
      className="flex w-full items-center justify-between px-5 py-4 text-left"
    >
      <span>
        <span className="block text-lg font-semibold text-slate-950">
          Create Ticket
        </span>
        <span className="text-sm text-slate-600">
          Secondary admin action for logging work raised outside the portal.
        </span>
      </span>
      <span className="rounded border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700">
        {isOpen ? "Hide" : "Open"}
      </span>
    </button>

    {isOpen && (
      <div className="border-t border-slate-200 p-5">
        <TicketForm
          form={form}
          setForm={setForm}
          categories={categories}
          saving={saving}
          onSubmit={onSubmit}
        />
      </div>
    )}
  </section>
);

const TicketForm = ({
  title,
  description,
  form,
  setForm,
  categories,
  saving,
  onSubmit,
}) => (
  <section className={title ? "rounded border border-slate-200 bg-white p-5" : ""}>
    {title && (
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-slate-950">{title}</h2>
        {description && <p className="text-sm text-slate-600">{description}</p>}
      </div>
    )}

    <form onSubmit={onSubmit} className="grid gap-4 md:grid-cols-2">
      <TicketFields form={form} setForm={setForm} categories={categories} />

      <div className="md:col-span-2">
        <button
          type="submit"
          disabled={saving}
          className="rounded bg-blue-700 px-4 py-2 font-medium text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {saving ? "Saving..." : "Create Ticket"}
        </button>
      </div>
    </form>
  </section>
);

const TicketFields = ({ form, setForm, categories, includeStatus = false }) => (
  <>
    <label className="block">
      <span className="mb-1 block text-sm font-medium text-slate-700">Title</span>
      <input
        type="text"
        value={form.title}
        minLength={3}
        maxLength={120}
        onChange={(event) => setForm({ ...form, title: event.target.value })}
        className="w-full rounded border border-slate-300 px-3 py-2 focus:border-blue-600 focus:outline-none"
        required
      />
    </label>

    <label className="block">
      <span className="mb-1 block text-sm font-medium text-slate-700">
        Category
      </span>
      <select
        value={form.category_id}
        onChange={(event) => setForm({ ...form, category_id: event.target.value })}
        className="w-full rounded border border-slate-300 px-3 py-2 focus:border-blue-600 focus:outline-none"
        required
      >
        {categories.map((category) => (
          <option key={category.id} value={category.id}>
            {category.name}
          </option>
        ))}
      </select>
    </label>

    {includeStatus && (
      <label className="block md:col-span-2">
        <span className="mb-1 block text-sm font-medium text-slate-700">
          Status
        </span>
        <select
          value={form.status}
          onChange={(event) => setForm({ ...form, status: event.target.value })}
          className="w-full rounded border border-slate-300 px-3 py-2 focus:border-blue-600 focus:outline-none"
          required
        >
          {Object.entries(statusLabels).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </label>
    )}

    <label className="block md:col-span-2">
      <span className="mb-1 block text-sm font-medium text-slate-700">
        Description
      </span>
      <textarea
        value={form.description}
        minLength={10}
        maxLength={2000}
        rows={5}
        onChange={(event) =>
          setForm({ ...form, description: event.target.value })
        }
        className="w-full rounded border border-slate-300 px-3 py-2 focus:border-blue-600 focus:outline-none"
        required
      />
    </label>
  </>
);

const TicketCard = ({
  ticket,
  categoryName,
  isAdmin,
  compact = false,
  saving,
  deleteLoadingId,
  onEdit,
  onDelete,
  onQuickStatus,
}) => (
  <article className="rounded border border-slate-200 bg-white p-4">
    <div className="flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
      <div className="min-w-0">
        <div className="mb-2 flex flex-wrap items-center gap-2">
          <span
            className={`inline-flex rounded px-2 py-1 text-xs font-semibold ring-1 ${
              statusStyles[ticket.status] || "bg-slate-100 text-slate-700 ring-slate-200"
            }`}
          >
            {statusLabels[ticket.status] || ticket.status}
          </span>
          <span className="text-xs font-medium text-slate-500">
            #{ticket.id} · {categoryName}
          </span>
        </div>
        <h3 className="font-semibold text-slate-950">{ticket.title}</h3>
        <p className={`mt-1 text-sm text-slate-600 ${compact ? "line-clamp-2" : ""}`}>
          {ticket.description}
        </p>
      </div>

      <div className="flex flex-wrap gap-2 lg:justify-end">
        {isAdmin && ticket.status === "OPEN" && (
          <button
            type="button"
            onClick={() => onQuickStatus(ticket, "IN_PROGRESS")}
            disabled={saving}
            className="rounded bg-blue-700 px-3 py-1.5 text-sm font-medium text-white transition hover:bg-blue-800 disabled:bg-slate-400"
          >
            Start Work
          </button>
        )}
        {isAdmin && ticket.status !== "CLOSED" && (
          <button
            type="button"
            onClick={() => onQuickStatus(ticket, "CLOSED")}
            disabled={saving}
            className="rounded bg-emerald-700 px-3 py-1.5 text-sm font-medium text-white transition hover:bg-emerald-800 disabled:bg-slate-400"
          >
            Close
          </button>
        )}
        <button
          type="button"
          onClick={() => onEdit(ticket)}
          disabled={deleteLoadingId === ticket.id}
          className="rounded border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 transition hover:border-blue-300 hover:text-blue-700"
        >
          Edit
        </button>
        <button
          type="button"
          onClick={() => onDelete(ticket)}
          disabled={deleteLoadingId === ticket.id}
          className="rounded border border-red-200 px-3 py-1.5 text-sm font-medium text-red-700 transition hover:bg-red-50 disabled:text-slate-400"
        >
          {deleteLoadingId === ticket.id ? "Deleting..." : "Delete"}
        </button>
      </div>
    </div>
  </article>
);

export default Dashboard;
