import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axios from "axios";
import Dashboard from "./Dashboard";
import { API_BASE_URL } from "../services/api";

jest.mock("axios");

const categories = [
  { id: 1, name: "Hardware" },
  { id: 2, name: "Software" },
];

const userTickets = [
  {
    id: 1,
    title: "Laptop issue",
    description: "Laptop will not turn on.",
    category_id: 1,
    status: "OPEN",
  },
  {
    id: 2,
    title: "VPN issue",
    description: "VPN disconnects during calls.",
    category_id: 2,
    status: "CLOSED",
  },
];

const adminTickets = [
  ...userTickets,
  {
    id: 3,
    title: "Printer queue stuck",
    description: "Print jobs are not moving.",
    category_id: 1,
    status: "IN_PROGRESS",
  },
];

beforeEach(() => {
  jest.clearAllMocks();
  localStorage.clear();
  localStorage.setItem("token", "dashboard-token");
});

const mockDashboardLoad = ({ user, tickets = userTickets }) => {
  axios.get.mockImplementation((url) => {
    if (url.endsWith("/tickets/")) {
      return Promise.resolve({ data: tickets });
    }
    if (url.endsWith("/categories/")) {
      return Promise.resolve({ data: categories });
    }
    if (url.endsWith("/users/me")) {
      return Promise.resolve({ data: user });
    }
    return Promise.reject(new Error(`Unexpected GET ${url}`));
  });
};

const renderDashboard = async () => {
  render(<Dashboard />);
  await waitFor(() => expect(screen.queryByText("Loading DeskMate...")).not.toBeInTheDocument());
};

test("loads and renders the user dashboard", async () => {
  mockDashboardLoad({
    user: { name: "user1", role: "user" },
  });

  await renderDashboard();

  expect(screen.getByRole("heading", { name: /my support tickets/i })).toBeInTheDocument();
  expect(screen.getByText("Signed in as user1 (user)")).toBeInTheDocument();
  expect(screen.getByRole("heading", { name: /raise a ticket/i })).toBeInTheDocument();
  expect(screen.getByText("Laptop issue")).toBeInTheDocument();
  expect(screen.getByText("VPN issue")).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: /start work/i })).not.toBeInTheDocument();
});

test("shows an error when dashboard data cannot load", async () => {
  axios.get.mockRejectedValue(new Error("Network error"));

  await renderDashboard();

  expect(
    screen.getByText("Could not load DeskMate. Please sign in again or try later.")
  ).toBeInTheDocument();
});

test("creates a ticket using the selected category", async () => {
  mockDashboardLoad({
    user: { name: "user1", role: "user" },
  });
  axios.post.mockResolvedValueOnce({ data: { id: 4 } });

  await renderDashboard();

  await userEvent.type(screen.getByTestId("ticket-title"), "New monitor request");
  userEvent.selectOptions(screen.getByTestId("ticket-category"), "2");
  await userEvent.type(
    screen.getByTestId("ticket-description"),
    "The monitor flickers and needs support."
  );
  userEvent.click(screen.getByRole("button", { name: /create ticket/i }));

  await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
      `${API_BASE_URL}/tickets/`,
      {
        title: "New monitor request",
        description: "The monitor flickers and needs support.",
        category_id: 2,
      },
      { headers: { Authorization: "Bearer dashboard-token" } }
    );
  });
  expect(await screen.findByText("Ticket created successfully.")).toBeInTheDocument();
});

test("renders admin triage controls and starts work on an open ticket", async () => {
  mockDashboardLoad({
    user: { name: "admin1", role: "admin" },
    tickets: adminTickets,
  });
  axios.put.mockResolvedValueOnce({ data: {} });

  await renderDashboard();

  expect(screen.getByRole("heading", { name: /ticket triage/i })).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /open/i })).toBeInTheDocument();

  userEvent.click(screen.getByRole("button", { name: /start work/i }));

  await waitFor(() => {
      expect(axios.put).toHaveBeenCalledWith(
      `${API_BASE_URL}/tickets/1`,
      {
        title: "Laptop issue",
        description: "Laptop will not turn on.",
        category_id: 1,
        status: "IN_PROGRESS",
      },
      { headers: { Authorization: "Bearer dashboard-token" } }
    );
  });
  expect(await screen.findByText("Ticket moved to in progress.")).toBeInTheDocument();
});

test("opens the edit drawer and saves ticket changes", async () => {
  mockDashboardLoad({
    user: { name: "user1", role: "user" },
  });
  axios.put.mockResolvedValueOnce({ data: {} });

  await renderDashboard();

  const laptopCard = screen.getByTestId("ticket-card-1");
  userEvent.click(within(laptopCard).getByRole("button", { name: /edit/i }));
  const editTitle = screen.getAllByTestId("ticket-title").at(-1);
  const editDescription = screen.getAllByTestId("ticket-description").at(-1);
  userEvent.clear(editTitle);
  await userEvent.type(editTitle, "Updated laptop issue");
  userEvent.clear(editDescription);
  await userEvent.type(
    editDescription,
    "Updated ticket description."
  );
  userEvent.click(screen.getByRole("button", { name: /save changes/i }));

  await waitFor(() => {
    expect(axios.put).toHaveBeenCalledWith(
      `${API_BASE_URL}/tickets/1`,
      {
        title: "Updated laptop issue",
        description: "Updated ticket description.",
        category_id: 1,
        status: "OPEN",
      },
      { headers: { Authorization: "Bearer dashboard-token" } }
    );
  });
  expect(await screen.findByText("Ticket updated successfully.")).toBeInTheDocument();
});

test("deletes a ticket after confirmation", async () => {
  mockDashboardLoad({
    user: { name: "user1", role: "user" },
  });
  axios.delete.mockResolvedValueOnce({ data: {} });
  jest.spyOn(window, "confirm").mockReturnValueOnce(true);

  await renderDashboard();

  const laptopCard = screen.getByTestId("ticket-card-1");
  userEvent.click(within(laptopCard).getByRole("button", { name: /delete/i }));

  await waitFor(() => {
    expect(axios.delete).toHaveBeenCalledWith(
      `${API_BASE_URL}/tickets/1`,
      { headers: { Authorization: "Bearer dashboard-token" } }
    );
  });
  await waitFor(() => {
    expect(screen.queryByText("Laptop issue")).not.toBeInTheDocument();
  });
  expect(screen.getByText("Ticket deleted successfully.")).toBeInTheDocument();
});

test("does not delete when confirmation is cancelled", async () => {
  mockDashboardLoad({
    user: { name: "user1", role: "user" },
  });
  jest.spyOn(window, "confirm").mockReturnValueOnce(false);

  await renderDashboard();

  const laptopCard = screen.getByTestId("ticket-card-1");
  userEvent.click(within(laptopCard).getByRole("button", { name: /delete/i }));

  expect(axios.delete).not.toHaveBeenCalled();
  expect(screen.getByText("Laptop issue")).toBeInTheDocument();
});
