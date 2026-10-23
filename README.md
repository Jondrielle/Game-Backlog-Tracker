# Game Backlog Tracker

A full-stack web application for organizing, managing, and tracking a personal video game library.

**Status:** In Development

## Overview

Game Backlog Tracker is a personal project designed to help gamers keep track of the games they own, the games they are currently playing, and the games they have completed. The goal is to provide one place to organize a game collection, record personal ratings and notes, and monitor gaming progress.

The application uses a Vue 3 frontend, a Python FastAPI backend, and PostgreSQL for data storage. Firebase Authentication handles user sign-in, while IGDB API integration provides video game metadata.

## Features

- **User authentication:** Sign up and log in using Firebase Authentication.
- **Personal game library:** Manage game records associated with a user's account.
- **Game management:** Add, view, update, and delete games.
- **Game status tracking:** Organize games by their play or completion status.
- **Personal details:** Store information such as ratings, notes, platforms, and completion dates where implemented.
- **Search and filtering:** Find games and narrow the library by available filters, such as status, genre, and platform.
- **Pagination:** Browse game results in manageable groups.
- **Game metadata integration:** Integrate IGDB to retrieve video game information.

*Note: The project is actively being developed. Features and implementation details may change.*

## Technology Stack

### Frontend
- Vue 3
- JavaScript
- HTML
- CSS

### Backend
- Python
- FastAPI
- SQLModel
- REST API

### Database and Authentication
- PostgreSQL
- Firebase Authentication
- Firebase ID token verification

### External API
- IGDB API

### Development Tools
- Git
- GitHub
- Visual Studio Code

## Application Architecture

The application follows a frontend/backend architecture.

1. **Vue 3 frontend:** Displays the user interface and handles user interactions.
2. **Firebase Authentication:** Manages user sign-in and provides Firebase ID tokens.
3. **FastAPI backend:** Processes API requests, verifies authentication tokens, and manages game records.
4. **PostgreSQL database:** Stores application records.
5. **IGDB API:** Provides video game metadata through the backend integration.

The frontend communicates with the backend through HTTP requests to the REST API. Protected operations should verify the user's identity before allowing access to user-specific records.

## Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

Install or obtain access to the following:

- Node.js and npm
- Python 3.10 or a compatible version required by the project dependencies
- PostgreSQL
- A Firebase project with Authentication configured
- IGDB API credentials through the Twitch Developer Console
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Jondrielle/Game-Backlog-Tracker.git
cd Game-Backlog-Tracker
```

Replace the repository URL or folder name above if your actual GitHub repository uses a different name.

### 2. Set Up the Backend

Navigate to the backend directory containing the FastAPI application and its dependency file.

Create and activate a virtual environment:

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project's Python dependencies using its existing requirements file:

```bash
pip install -r requirements.txt
```

If your project uses `pyproject.toml` instead of `requirements.txt`, follow the installation instructions for that file.

### 3. Configure the Database

Create a PostgreSQL database for local development.

Configure the backend with the database connection string expected by the application. For example:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/game_backlog
```

Replace the example username, password, and database name with your local settings.

Make sure the application's SQLModel table creation or database migration process has been run before starting the application.

### 4. Configure Firebase Authentication

1. Create or open a project in the Firebase Console.
2. Enable the authentication provider used by the application.
3. Register a web application in the Firebase project.
4. Obtain the Firebase web configuration.
5. Add the configuration to the frontend using the environment variable names expected by your Firebase setup.
6. Configure backend Firebase Admin SDK credentials or application-default credentials so the API can verify Firebase ID tokens.

For a Vite-based Vue application, frontend environment variables commonly use the `VITE_` prefix. Use the exact names referenced in your Firebase configuration code.

**Security:** Never commit private service-account keys, database passwords, or IGDB client secrets to GitHub. Frontend Firebase configuration is not a substitute for backend authorization.

### 5. Configure IGDB API Access

IGDB API access requires Twitch application credentials.

1. Register an application through the Twitch Developer Console.
2. Obtain the required client ID and client secret.
3. Configure the backend to obtain and use the appropriate access token.
4. Keep the client secret on the backend rather than exposing it in frontend code.

Use the variable names expected by your implementation. Example placeholders:

```env
IGDB_CLIENT_ID=your_client_id
IGDB_CLIENT_SECRET=your_client_secret
```

Do not use these example values as real credentials.

### 6. Set Up the Frontend

Navigate to the frontend directory containing `package.json`:

```bash
npm install
```

Configure the frontend's API base URL to point to the local FastAPI backend. If the frontend uses Vite environment variables, an example configuration might be:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Use this only if the frontend code is configured to read that variable. Otherwise, update the existing API configuration to use the correct URL.

### 7. Run the Application

Start the backend from the directory containing the FastAPI application:

```bash
uvicorn main:app --reload
```

Replace `main:app` if the FastAPI application is defined in another module.

Start the frontend in a separate terminal:

```bash
npm run dev
```

Open the local frontend URL printed by the development server.

The FastAPI interactive API documentation is commonly available at:

```text
http://127.0.0.1:8000/docs
```

This URL is available when the backend is running locally and its documentation route is enabled.

## Environment Variables

The following table lists example configuration values. Actual variable names depend on the project's implementation.

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL database connection |
| `IGDB_CLIENT_ID` | IGDB/Twitch application client ID |
| `IGDB_CLIENT_SECRET` | Private IGDB/Twitch application secret |
| Firebase frontend configuration | Connects the frontend to Firebase |
| Firebase Admin credentials | Allows backend token verification |
| Frontend API base URL | Specifies the backend API address |

Create local environment files as required by the project. Keep secrets out of source control, and provide a sanitized example file such as `.env.example` when appropriate.

## API Overview

The FastAPI backend provides REST endpoints for managing game records and supporting the frontend.

Depending on the current implementation, endpoints may support operations such as:

- Retrieving a user's game library
- Adding a game
- Retrieving an individual game
- Updating game information
- Deleting a game
- Searching for external game metadata

Consult the FastAPI documentation at `/docs` to inspect the actual routes, request parameters, and response formats.

Protected endpoints should validate Firebase ID tokens and enforce user-level access controls.

## Project Structure

The exact directory structure may differ depending on how the repository is organized. A typical layout is:

```text
game-backlog-tracker/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── .env.example
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
└── README.md
```

This is an illustrative structure. Adjust it to match the actual files in the repository.

## Security Considerations

- Verify Firebase ID tokens on the backend.
- Enforce authorization so users can only access their own records.
- Keep private API credentials and database secrets out of frontend code.
- Do not commit `.env` files containing real secrets.
- Validate incoming request data on the backend.
- Use HTTPS and appropriate production configuration when deploying the application.

## Future Improvements

Potential improvements include:

- Complete and refine IGDB metadata integration.
- Improve the game library's visual design and responsive behavior.
- Expand sorting, search, and filtering options.
- Add richer gaming statistics and progress summaries.
- Improve error handling and automated testing.
- Add deployment configuration and production monitoring.
- Improve documentation and setup automation.

These are planned or potential improvements, not claims that the features are already implemented.

## Learning Goals

This project provides practical experience with:

- Building a frontend using Vue 3.
- Creating REST APIs with Python and FastAPI.
- Modeling and managing relational data with SQLModel and PostgreSQL.
- Integrating Firebase Authentication with a backend API.
- Connecting an application to an external API.
- Organizing a full-stack application and managing configuration.

## Author

**Jondrielle Wilson**

- GitHub: https://github.com/Jondrielle
- LinkedIn: https://www.linkedin.com/in/jondrielle-wilson
- Portfolio: https://jondriellewilson.wixsite.com/jondrielle-wilson

