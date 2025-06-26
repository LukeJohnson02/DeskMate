import { Link, useNavigate, useLocation } from "react-router-dom";
import Logo from "../component/common/Logo"

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const isLoginPage = location.pathname === "/";

  return (
    <nav className="bg-white shadow-md p-4 flex justify-between items-center">
      {/* Logo */}
      <div className="text-xl font-bold text-blue-600">
        <Link to="/">
          <Logo/>
        </Link>
      </div>

      {/* If NOT on login page AND logged in, show links */}
      {!isLoginPage && token && (
        <div className="flex gap-6 items-center">
          <Link to="/dashboard" className="text-gray-700 hover:text-blue-600">
            Dashboard
          </Link>
          <Link to="/tickets" className="text-gray-700 hover:text-blue-600">
            Tickets
          </Link>
          <button
            onClick={handleLogout}
            className="text-red-500 hover:underline text-sm"
          >
            Logout
          </button>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
