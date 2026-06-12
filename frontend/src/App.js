import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Navbar from "./component/Navbar";
import Dashboard from "./pages/Dashboard";

/**
 * Root React component that owns the client-side route table.
 *
 * `BrowserRouter` is used because the app has normal URL paths (`/` and
 * `/dashboard`) while React still renders the page without full document reloads.
 */
function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
