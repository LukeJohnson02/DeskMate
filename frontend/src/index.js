import React from "react";
import ReactDOM from "react-dom/client";
import "./fontawesome";
import "./index.css";
import App from "./App";

/**
 * Mount the React application into the static HTML template.
 *
 * `createRoot` is the React 18+ rendering API; wrapping in `StrictMode` helps
 * surface unsafe lifecycle and side-effect patterns during development.
 */
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
