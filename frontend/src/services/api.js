/**
 * Base URL used by frontend API calls.
 *
 * Create React App only exposes variables prefixed with `REACT_APP_`, so this
 * fallback keeps local development working while CI/production can inject a
 * different backend URL without changing source code.
 */
export const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";
