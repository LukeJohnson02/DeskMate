/**
 * Base URL used by frontend API calls.
 *
 * Create React App only exposes variables prefixed with `REACT_APP_` at build
 * time. Static deployments can also inject `window.__DESKMATE_API_BASE_URL__`
 * before the app bundle loads.
 */
export const API_BASE_URL =
  window.__DESKMATE_API_BASE_URL__ ||
  process.env.REACT_APP_API_BASE_URL ||
  "http://localhost:8000";
