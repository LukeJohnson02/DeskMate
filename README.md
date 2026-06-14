# DeskMate

DeskMate is a support ticket application with a FastAPI backend and React frontend.

## Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set SECRET_KEY=replace-with-a-local-development-secret
uvicorn main:app --reload
```

API docs are available at http://127.0.0.1:8000/docs.

## Frontend Setup

```bash
cd frontend
npm install
set REACT_APP_API_BASE_URL=http://localhost:8000
npm start
```

## Configuration

Local development can use local URLs and a disposable development secret. Production must provide real values through the deployment environment rather than committing them to the repository.

Required backend environment:

```text
SECRET_KEY=<strong-random-secret>
```

Optional backend environment:

```text
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
BACKEND_PUBLIC_URL=http://localhost:8000
FRONTEND_PUBLIC_URL=http://localhost:3000
SMTP_SERVER=<smtp-host>
SMTP_PORT=587
SMTP_USERNAME=<smtp-username>
SMTP_PASSWORD=<smtp-password>
FROM_EMAIL=<sender-address>
```

Frontend environment:

```text
REACT_APP_API_BASE_URL=http://localhost:8000
```

For production, set `CORS_ALLOWED_ORIGINS` to the deployed frontend origin, set `REACT_APP_API_BASE_URL` to the deployed backend URL before building the frontend, and use a unique `SECRET_KEY` generated for that environment.

## Continuous Integration

GitHub Actions runs the CI workflow on every push and pull request. The backend job installs Python dependencies, checks Black formatting, runs Pylint, and runs the backend test suite. The frontend job installs Node dependencies with `npm ci`, runs ESLint, runs React unit tests, and runs the production build. A Selenium end-to-end job starts both apps in CI and runs browser smoke tests for login, dashboard, ticket creation, logout, and admin ticket triage.

## Docker Compose

Docker Compose reads configuration from your shell environment. At minimum, set `SECRET_KEY` before starting the stack:

```bash
set SECRET_KEY=replace-with-a-local-development-secret
docker compose up --build
```

## Demo Data

The local SQLite database includes realistic support-desk demo data:

- 10 verified users: 7 regular users and 3 administrators
- 10 ticket categories, including hardware, network, access, email, and security
- 15 support tickets across open, in-progress, and closed states

To reset the database to this dataset after installing backend dependencies, run:

```bash
cd backend
python Tests/populate_db.py
```

## Demo Login Details

Admin:

```text
Name: Grace Miller
Email: admin1@example.com
Password: adminpass123
```

User:

```text
Name: Maya Patel
Email: user1@example.com
Password: password123
```
