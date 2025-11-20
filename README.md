# da-kanmind

A Django REST Framework-based Kanban board management system that enables users to create boards, manage tasks, and collaborate with team members through an intuitive API.

## Features

- **User Authentication**: Token-based authentication with registration and login endpoints
- **Board Management**: Create, update, retrieve, and delete Kanban boards with owner and member roles
- **Task Management**: Full CRUD operations for tasks with status tracking (to-do, in-progress, review, done)
- **Task Assignment**: Assign tasks to team members and designate reviewers
- **Priority System**: Categorize tasks by priority levels (low, medium, high)
- **Comments**: Add and manage comments on tasks for better collaboration
- **Member Management**: Add or remove board members with granular permissions
- **Email Verification**: Check if users exist by email before adding them to boards
- **Filtered Views**: View tasks assigned to you or tasks you're reviewing

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mcordes92/da-kanmind.git
   cd da-kanmind
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## Usage Examples

### Authentication

**Register a new user**
```bash
curl -X POST http://127.0.0.1:8000/api/registration/ \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "repeated_password": "securepassword123"
  }'
```

Response:
```json
{
  "token": "<token>",
  "fullname": "John Doe",
  "email": "john@example.com",
  "user_id": 1
}
```

**Login**
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Board Management

**Create a new board**
```bash
curl -X POST http://127.0.0.1:8000/api/boards/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{
    "title": "Project Alpha",
    "members": [2, 3]
  }'
```

**List all boards**
```bash
curl -X GET http://127.0.0.1:8000/api/boards/ \
  -H "Authorization: Token <token>"
```

**Get board details**
```bash
curl -X GET http://127.0.0.1:8000/api/boards/1/ \
  -H "Authorization: Token <token>"
```

**Update a board**
```bash
curl -X PATCH http://127.0.0.1:8000/api/boards/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{
    "title": "Project Alpha - Updated",
    "members": [2, 3, 4]
  }'
```

**Delete a board**
```bash
curl -X DELETE http://127.0.0.1:8000/api/boards/1/ \
  -H "Authorization: Token <token>"
```

**Check if user exists by email**
```bash
curl -X GET "http://127.0.0.1:8000/api/email-check/?email=john@example.com" \
  -H "Authorization: Token <token>"
```

### Task Management

**Create a task**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{
    "board": 1,
    "title": "Implement user authentication",
    "description": "Add JWT authentication to the API",
    "status": "to-do",
    "priority": "high",
    "assignee_id": 2,
    "reviewer_id": 3,
    "due_date": "2025-12-31"
  }'
```

**Update a task**
```bash
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{
    "status": "in-progress"
  }'
```

**Delete a task**
```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/ \
  -H "Authorization: Token <token>"
```

**Get tasks assigned to me**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/assigned-to-me/ \
  -H "Authorization: Token <token>"
```

**Get tasks I'm reviewing**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/reviewing/ \
  -H "Authorization: Token <token>"
```

### Task Comments

**List comments for a task**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/1/comments/ \
  -H "Authorization: Token <token>"
```

**Add a comment to a task**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/1/comments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <token>" \
  -d '{
    "content": "This looks good, ready for review!"
  }'
```

**Delete a comment**
```bash
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/comments/5/ \
  -H "Authorization: Token <token>"
```

## API Reference

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/registration/` | Register a new user | No |
| POST | `/api/login/` | Login and receive authentication token | No |

### Board Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/boards/` | List all boards (owned or member) | Required |
| POST | `/api/boards/` | Create a new board | Required |
| GET | `/api/boards/{id}/` | Retrieve board details with tasks | Required |
| PUT/PATCH | `/api/boards/{id}/` | Update board title and members | Required |
| DELETE | `/api/boards/{id}/` | Delete a board (owner only) | Required |
| GET | `/api/email-check/?email={email}` | Check if user exists by email | Required |

### Task Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/api/tasks/` | Create a new task | Required |
| PUT/PATCH | `/api/tasks/{id}/` | Update a task | Required |
| DELETE | `/api/tasks/{id}/` | Delete a task (owner or board owner) | Required |
| GET | `/api/tasks/assigned-to-me/` | List tasks assigned to current user | Required |
| GET | `/api/tasks/reviewing/` | List tasks being reviewed by current user | Required |

### Task Comment Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/api/tasks/{task_id}/comments/` | List all comments for a task | Required |
| POST | `/api/tasks/{task_id}/comments/` | Add a comment to a task | Required |
| DELETE | `/api/tasks/{task_id}/comments/{id}/` | Delete a comment (author only) | Required |

### Data Models

**Task Status Options**: `to-do`, `in-progress`, `review`, `done`

**Task Priority Options**: `low`, `medium`, `high`

**Board Response Fields**:
- `id`, `title`, `owner_id`, `members`, `tasks`
- Computed fields: `member_count`, `ticket_count`, `tasks_to_do_count`, `tasks_high_prio_count`

**Task Response Fields**:
- `id`, `board`, `title`, `description`, `status`, `priority`
- `assignee` (user object), `reviewer` (user object), `due_date`
- `comments_count`

## Project Structure

```
da-kanmind/
├── auth_app/           # User authentication and profiles
│   ├── api/           # API views, serializers, and URLs
│   └── models.py      # Profile model
├── boards_app/        # Board management
│   ├── api/           # API views, serializers, URLs, and permissions
│   └── models.py      # Boards model
├── tasks_app/         # Task and comment management
│   ├── api/           # API views, serializers, URLs, and permissions
│   └── models.py      # Tasks and TaskComments models
├── core/              # Project settings and root URL configuration
├── db.sqlite3         # SQLite database
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Technologies Used

- **Django 5.2.7** - Web framework
- **Django REST Framework 3.16.1** - API toolkit
- **django-cors-headers 4.9.0** - CORS handling
- **drf-nested-routers 0.95.0** - Nested routing for DRF
- **Token Authentication** - Built-in DRF token authentication

## Support

For issues, questions, or suggestions, please open an issue in the GitHub repository.

## License

This project does not currently have a license file. Please contact the repository owner for licensing information.
