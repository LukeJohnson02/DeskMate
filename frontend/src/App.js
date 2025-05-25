import './index.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Tickets from "./pages/Tickets";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/tickets" element={<Tickets />} />
        {/* other routes */}
      </Routes>
    </Router>
  );
}

export default App;