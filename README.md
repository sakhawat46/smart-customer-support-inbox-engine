# Smart Customer Support Inbox Engine

A Django Rest Framework backend engine designed for a smart customer support inbox. This project provides a robust API for managing conversations, real-time messaging, rule-based AI reply suggestions, and background analytics using Celery and Redis. It is fully containerized using Docker and utilizes PostgreSQL for the primary database.

## Features

- **JWT Authentication**: Secure endpoints using JSON Web Tokens.
- **Conversation Management**: Paginated listing, strict status filtering, and search functionality.
- **Thread History**: Chronologically ordered message logs for conversations.
- **Real-Time Messaging**: WebSocket integration via Django Channels & Daphne for real-time delivery of messages.
- **Mock AI Suggestion Engine**: Extensible rule-based engine to provide suggested replies to agents.
- **Background Analytics**: Non-blocking sentiment analysis pipeline using Celery and Redis.
- **Distributed Locking**: Redis-backed concurrency control with auto-expiring 5-minute locks to prevent race conditions among agents.
- **Robust Testing**: Comprehensive test suite with high coverage for unit and API integration tests.

## Tech Stack

- **Framework**: Django 5.2, Django Rest Framework (DRF)
- **Database**: PostgreSQL 15
- **Broker / Cache / Websocket Backend**: Redis 7
- **Asynchronous Task Queue**: Celery
- **Real-Time Layer**: Django Channels, Daphne, `channels-redis`
- **Authentication**: `djangorestframework-simplejwt`

## Running the Project

The easiest way to run the project is using Docker Compose. The `docker-compose.yml` file defines all necessary services: PostgreSQL, Redis, Django Web Server (Daphne), and Celery worker.

### Prerequisites
- Docker
- Docker Compose

### Step 1: Start the Services

Open a terminal in the project root and run:

```bash
docker compose up --build
```
Or to run in detached mode (in the background):
```bash
docker compose up -d --build
```

**What happens during startup?**
1. Docker builds the Python environment and installs dependencies.
2. PostgreSQL and Redis containers start.
3. The `web` container runs database migrations (`python manage.py migrate`).
4. The `web` container seeds the initial admin user (`python manage.py seed_admin`).
5. The `web` container starts the Daphne server on port 8000.
6. The `celery` container starts processing background tasks.

### Step 2: Accessing the Application

- **API Base URL**: `http://localhost:8000/api/`
- **Default Admin Account**:
  - Email: `admin@test.com`
  - Password: `admin123`

### Stopping the Services

To stop the running containers:

```bash
docker compose down
```

## API Endpoints

### Authentication
- `POST /api/token/` - Obtain JWT access and refresh tokens.
- `POST /api/token/refresh/` - Refresh JWT token.

### Conversations
- `GET /api/conversations/` - List conversations (supports `?page=1`, `?search=Name`, `?status=open`).
- `POST /api/conversations/create/` - Create a new conversation (Customer initiates).
- `GET /api/conversations/{id}/messages/` - Get chronological thread history.
- `POST /api/conversations/{id}/reply/` - Agent sends a reply (triggers Celery sentiment analysis; blocked if locked by another agent).

### Distributed Locking
- `POST /api/conversations/{id}/lock/` - Acquire a 5-minute lock on a conversation.
- `POST /api/conversations/{id}/unlock/` - Release an owned lock.
- `GET /api/conversations/{id}/lock-status/` - View current lock state and owner.

### AI Suggestions
- `POST /api/conversations/{id}/suggest-reply/` - Get a mock AI suggested reply based on keyword mapping.

## Testing

To run the test suite locally (if running outside Docker):

```bash
python manage.py test apps --verbosity=2
```

To run tests inside the Docker container:

```bash
docker compose exec web python manage.py test apps --verbosity=2
```
