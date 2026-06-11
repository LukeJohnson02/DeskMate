import { Link, useLocation, useNavigate } from "react-router-dom";
import Logo from "../component/common/Logo";

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("token");
  const isLoginPage = location.pathname === "/";

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
        <Link to={token ? "/dashboard" : "/"} className="text-xl font-bold text-blue-700">
          <Logo />
        </Link>

        {!isLoginPage && token && (
          <div className="flex items-center gap-4">
            <Link to="/dashboard" className="text-sm font-medium text-slate-700 hover:text-blue-700">
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
