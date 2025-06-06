<img width="1070" alt="GitHub Repo Cover" src="https://github.com/corbado/corbado-php/assets/18458907/aa4f9df6-980b-4b24-bb2f-d71c0f480971">

# Svelte and FastAPI Passkey Example App

This is a sample implementation of the [Corbado passkeys-first authentication solution](https://www.corbado.com) using
Svelte and FastAPI. The following packages are being used:

- [Corbado web-js](https://github.com/corbado/javascript/tree/develop/packages/web-js)
- [Corbado Python](https://github.com/corbado/corbado-python)

[![integration-guides](https://github.com/user-attachments/assets/7859201b-a345-4b68-b336-6e2edcc6577b)](https://app.corbado.com/integration-guides/svelte-fastapi)

## File structure

- `frontend`: Separate directory for the Svelte frontend
- `frontend/.env.example`: Example file for environment variables
- `frontend/src/routes`: Contains all routes used in the frontend
- `frontend/src/router/index.ts`: Contains the route definitions
- `frontend/src/stores/user.svelte.ts`: Global store for user data from Corbado and our own backend
- `backend`: Separate directory for the FastAPI backend
- `backend/.env.example`: Example file for environment variables
- `backend/app/main.py`: Entry point for the FastAPI app
- `backend/app/core/config.py`: Configuration file for the Express app
- `backend/app/utils`: Collection of utility functions, e.g. helper functions for authentication
- `backend/app/routes`: Directory configuring the routes for the app
- `backend/app/db`: Database configuration and queries

## Setup

### Prerequisites

Please follow the steps in [Getting started](https://docs.corbado.com/overview/getting-started) to create and configure
a project in the [Corbado developer panel](https://app.corbado.com/).

You need to have [Node](https://nodejs.org/en/download) and `npm` installed to run it.

### Configure environment variables

Use the values you obtained in [Prerequisites](#prerequisites) to configure the following variables inside a `.env`
file you create in frontend and backend directories respectively:

#### Backend

The backend needs an api secret to authenticate with the Corbado backend API.

```dotenv
CORBADO_PROJECT_ID=pro-XXX
CORBADO_API_SECRET=corbado1_XXX
CORBADO_FRONTEND_API=https://{$CORBADO_PROJECT_ID}.frontendapi.cloud.corbado.io
CORBADO_BACKEND_API=https://backendapi.cloud.corbado.io
```

#### Frontend

The frontend needs the project ID and the backend base URL.

```dotenv
VITE_CORBADO_PROJECT_ID=pro-XXX
VITE_BACKEND_BASE_URL=http://localhost:3001
```

## Usage

### Run the project locally

On macOS and Linux, run the following command in the root directory

```bash
(cd frontend && npm install)
(cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && alembic upgrade head)
```

to install all dependencies and initialize the database.

Activating the virtual environment will be different for Windows users.

Finally, you can run the project locally by individually starting up the frontend and backend.

#### Running frontend and backend individually

In one terminal session, run the following command in the `frontend` directory:

```bash
npm run dev
```

In another terminal session, run the following command in the `backend` directory with an activated virtual environment:

```bash
fastapi dev --port 3001
```

### Troubleshooting

If you encounter any issues regarding imports in the backend, make sure to set your python path:

```bash
export PYTHONPATH=$(pwd)
```

## Passkeys support

- Community for Developer Support: https://bit.ly/passkeys-community
- Passkeys Debugger: https://www.passkeys-debugger.io/
- Passkey Subreddit: https://www.reddit.com/r/passkey/

## Telemetry

This example application uses telemetry. By gathering telemetry data, we gain a more comprehensive understanding of how our SDKs, components, and example applications are utilized across various scenarios. This information is crucial in helping us prioritize features that are beneficial and impactful for the majority of our users. Read our [official documentation](https://docs.corbado.com/corbado-complete/other/telemetry) for more details.

To disable telemetry, add the following line to your `frontend/.env` file:

```sh
VITE_CORBADO_TELEMETRY_DISABLED=true
```