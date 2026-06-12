import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import Logo from "../component/common/Logo";

/**
 * Top navigation shown across the application.
 *
 * The component reads the token from `localStorage` because authentication is
 * currently client-token based, and `useLocation` lets it hide navigation links
 * on the login screen where they would be distracting.
 */
const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const isLoginPage = location.pathname === "/";

  useEffect(() => {
    setToken(localStorage.getItem("token"));
  }, [location.pathname]);

  /**
   * Clear the browser token and return the user to the login route.
   */
  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    navigate("/", { replace: true });
  };

  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link
          to={token ? "/dashboard" : "/"}
          className="text-xl font-bold text-blue-700"
        >
          <Logo />
        </Link>

        {!isLoginPage && token && (
          <div className="flex items-center gap-4">
            <Link
              to="/dashboard"
              className="text-sm font-medium text-slate-700 hover:text-blue-700"
            >
              Dashboard
            </Link>
            <button
              type="button"
              data-testid="logout-button"
              onClick={handleLogout}
              className="rounded border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 transition hover:border-red-300 hover:text-red-600"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
