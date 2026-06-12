import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import axios from "axios";
import Login from "./Login";
import { API_BASE_URL } from "../services/api";

jest.mock("axios");

const mockNavigate = jest.fn();

jest.mock(
  "react-router-dom",
  () => ({
    useNavigate: () => mockNavigate,
  }),
  { virtual: true }
);

const renderLogin = () => render(<Login />);

beforeEach(() => {
  jest.clearAllMocks();
  localStorage.clear();
});

test("renders the login form", () => {
  renderLogin();

  expect(screen.getByRole("heading", { name: /welcome to deskmate/i })).toBeInTheDocument();
  expect(screen.getByTestId("login-email")).toBeInTheDocument();
  expect(screen.getByTestId("login-password")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
  expect(screen.getByRole("link", { name: /forgot your password/i })).toHaveAttribute(
    "href",
    "/forgot-password"
  );
});

test("submits credentials, stores token, and navigates to dashboard", async () => {
  axios.post.mockResolvedValueOnce({ data: { access_token: "unit-test-token" } });

  renderLogin();

  await userEvent.type(screen.getByTestId("login-email"), "user1@example.com");
  await userEvent.type(screen.getByTestId("login-password"), "password123");
  userEvent.click(screen.getByRole("button", { name: /login/i }));

  await waitFor(() => {
    expect(axios.post).toHaveBeenCalledWith(
      `${API_BASE_URL}/auth/login`,
      "username=user1%40example.com&password=password123",
      {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      }
    );
  });
  expect(localStorage.getItem("token")).toBe("unit-test-token");
  expect(mockNavigate).toHaveBeenCalledWith("/dashboard");
});

test("shows a helpful error when login fails", async () => {
  axios.post.mockRejectedValueOnce(new Error("Invalid credentials"));

  renderLogin();

  await userEvent.type(screen.getByTestId("login-email"), "user1@example.com");
  await userEvent.type(screen.getByTestId("login-password"), "wrong-password");
  userEvent.click(screen.getByRole("button", { name: /login/i }));

  expect(await screen.findByText("Invalid email or password")).toBeInTheDocument();
  expect(localStorage.getItem("token")).toBeNull();
  expect(mockNavigate).not.toHaveBeenCalled();
});
