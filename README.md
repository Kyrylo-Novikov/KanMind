# KanMind – Kanban Task Management System (Backend)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Django](https://img.shields.io/badge/Django-REST%20Framework-green?style=flat&logo=django)

KanMind is an interactive Kanban-style task management application. This repository contains the **Django REST API backend** which serves as the data and authentication provider.

The corresponding **Frontend Repository** can be found here: [Link to Frontend Repo](https://github.com/Developer-Akademie-Backendkurs/project.KanMind).

---

## 🛠️ Technologies

- **Backend Framework:** Python, Django, Django REST Framework (DRF)
- **Database:** SQLite (for local development)
- **Authentication:** Token-based Authentication
- **API Documentation:** Swagger / drf-spectacular

---

## ✨ Features

- **Task Management:** Create, update, delete, and move tasks across different status columns (e.g., To-Do, In Progress, Review, Done).
- **User & Authentication:** Secure registration, token-based login, and role management.
- **RESTful API:** Clean and versioned endpoints for handling tasks, users, and boards.
- **Interactive API Documentation:** Integrated Swagger UI for easy endpoint testing and exploration.

---

## 📁 Project Structure

```text
kanmind/
├── backend/                  # Main backend application directory
│   ├── auth_app/             # Authentication & user management apps
│   ├── board_app/            # Task, board, and column management apps
│   ├── core/                 # Django settings and core configuration
│   ├── .env.example          # Environment variables template
│   ├── manage.py             # Django execution script
│   └── requirements.txt      # Python dependencies
├── .gitignore                # Ignored files (database, .env, venv, etc.)
├── LICENSE.md                # License and legal terms
└── README.md                 # Project documentation
```

---

## 🚀 Installation & Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Kyrylo-Novikov/kanmind.git
cd kanmind
```

### 2. Navigate to the Backend Directory

```bash
cd backend
```

### 3. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

- **Windows:**
  ```cmd
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables (.env)

For security reasons, sensitive data like the Django `SECRET_KEY` is kept out of version control. You need to set this up locally:

1. Copy the provided template:

   ```bash
   cp .env.example .env
   ```

   _(On Windows Command Prompt, use: `copy .env.example .env`)_

2. Open the newly created `.env` file and define your specific variables (e.g., set a secure `SECRET_KEY`).

### 6. Run Database Migrations

_(Note: The SQLite database file is intentionally excluded from the repository via `.gitignore`. Running migrations will generate a fresh local database for you.)_

```bash
python manage.py migrate
```

### 7. Create a Superuser (Recommended)

To access the built-in Django Admin panel and manage users/boards easily, create an admin account:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your admin credentials.

### 8. Start the Development Server

```bash
python manage.py runserver
```

The API is now running locally at `http://127.0.0.1:8000/`.

---

## 📖 API Documentation (Swagger)

This backend features automatically generated API documentation. This is best practice for testing endpoints and understanding the expected request/response payloads without needing external tools like Postman.

Once the server is running, you can explore and test the endpoints directly in your browser:

- **Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **OpenAPI Schema:** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)

---

## 📜 License & Legal Notice

Developed as part of the advanced training program at Developer Akademie GmbH.

- **Backend:** Independent development effort.
- **Frontend & Assets:** Provided by Developer Akademie GmbH under the "Developer Akademie Learning License (Non-commercial)".

For full license terms, please refer to the `LICENSE.md` file included in this repository.
