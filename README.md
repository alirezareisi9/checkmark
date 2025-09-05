# Django Role-Based Security Management System
**Manage Users, roles, and permissions with ease**

This project is a role-based security management system built with Django.
It provides different responses and permissions depending on a user’s role within the company.

- ✅ 43 automated test cases included (all passing).
- 🚀 Deployment-ready using Gunicorn for high-performance request handling and Nginx to serve static and media    files efficiently.
- 🌐 REST Browsable API interface for easy interaction and testing.
- 🖥️ Currently not deployed to a live domain — but you can run it on your localhost or configure it for any domain.


---

## Features
**This system enforces role-based access control (RBAC) across four views.
There are three main roles plus an admin role with restricted access:**

---
### 👥 Roles
- **👑 Admin** -> Full access to the Django Admin Panel (exclusive, not available to other roles).
- **🧑‍💼 Manager** -> Manages employees and self, can create/update/delete it's own employees and self profiles.
- **📰 Reporter** -> Read-only access to users data and change password of self.
- **👤 Employee** -> Read-only access only to their own profile and change password of self.


---
### 🔑 Views & Permissions
---
1. **Users List** `/users/`
  - *📖 GET* -> Lists user profiles.
    - All roles can access ✅ , but each role only sees the profiles allowed by their permissions.
  - *✍️ POST* → Create a new user.
    - Only 🧑‍💼 Managers are allowed.
    - When a Manager creates a user:
      - A random password 🔑 is generated.
      - The user must change it on their first login (change_password = False until updated).
---
2. **Users Detail** `/users/{id}/`
  - *📖 GET* → Retrieve details of a user by ID
    - 🧑‍💼 Manager → Only their own employees and self 👥
    - 📰 Reporter → Read-only access to all users 👀
    - 👤 Employee → Only their own profile 🪪
  - ✏️ *PUT / PATCH / DELETE* → Manage user accounts
    - Allowed only for 🧑‍💼 Managers, and only for their employees and self
    - 🚫 Managers cannot modify:
      - is_active, is_superuser, is_staff, change_password, password
---
3. **Change Password** `/change-password/`
  - 🔐 POST → Change password
    - Any role (👑, 🧑‍💼, 📰, 👤) can update their own password only
    - Requires: current password + new password ✨

---
4. **Reset Password** `/reset-password/`
  - ♻️ PUT → Reset a forgotten password
    - Only 🧑‍💼 Managers can reset passwords of their employees and self
    - ❌ Employees and Reporters cannot reset others’ passwords

---
**Let's check all at a glance:**
| View / Action              | 🧑‍💼 Manager     | 📰 Reporter   | 👤 Employee   |
| -------------------------- | :-----------:  | :---------:   | :---------:   |
| **Users List – GET**       |  ✔️ Own team   |    ✔️ All     |   ✔️ Self     |
| **Users List – POST**      |   ✔️ Create    |      ❌       |      ❌       |
| **Users Detail – GET**     |  ✔️ Own team   |    ✔️ All     |   ✔️ Self     |
| **Users Detail – PUT**     |  ✔️ Own team   |      ❌       |      ❌       |
| **Users Detail – PATCH**   |  ✔️ Own team   |      ❌       |      ❌       |
| **Users Detail – DELETE**  |  ✔️ Own team   |      ❌       |      ❌       |
| **Change Password – POST** |    ✔️ Self     |   ✔️ Self     |   ✔️ Self     |
| **Reset Password – PUT**   |  ✔️ Employees  |      ❌       |      ❌       |
## 🚀 How to Run the Project

You can run this project in two ways: using **Docker** (recommended) or running it manually.
First,  clone the repository:
 ```bash
 git clone https://github.com/alirezareisi9/django-access-control.git
 cd django-access-control
 ```
---

### 🐳 Option 1: Run with Docker (Recommended)

1. Make sure you have **Docker** and **Docker Compose** installed.
2. Copy environment variables template and update values

``` bash
cp .env.example .env

```
**🔔 Note**: *Make sure the database configuration in your `.env` file
matches the database name, user, password, host, and port you want to use.*

3. Build and start the containers:
``` bash
docker compose up --build -d

```
4. Apply database migrations:
``` bash
docker compose exec django python manage.py migrate

```
5. Create a superuser (for admin access):
``` bash
docker compose exec django python manage.py createsuperuser

```
6. Access the app:

- 🌐 **API:** [`http://localhost/`](http://localhost/)
- 🔑 **Admin Panel:** [`http://localhost/admin/`](http://localhost/admin/)

---
## 💻 Run Locally (Without Docker)

Follow these steps if you want to run the project directly on your machine.

1. Create & Activate a virtual environment
``` bash
python -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows

```
3. Install dependencies
``` bash
pip install -r requirements.txt

```
4. Create a PostgreSQL database and user
(adjust commands for your OS / PostgreSQL version)
``` bash
psql -U postgres -c "CREATE DATABASE <db-name>;"
psql -U postgres -c "CREATE USER <db-user-name> WITH PASSWORD '<your-password>';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE <db-name> TO <db-user-name>;"

```
5. Copy environment variables template and update values

``` bash
cp .env.example .env

```
**🔔 Note**: *Make sure the database configuration in your `.env` file
matches the database name, user, and password you created in the steps above.*

6. Match `.env` variables with your configuration

Everything you need is explained in the `.env.example` file.  

🔑 **Important:** Set your own Django secret key.  
You can generate one by running:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

```
7. Apply database migrations
``` bash
python manage.py migrate

```
8. Create a superuser (for admin access)
``` bash
python manage.py createsuperuser

```
9. Run the development server
``` bash
python manage.py runserver

```
10. Access the app:

- 🌐 **API:** [`http://localhost:8000/`](http://localhost:8000/)  
- 🔑 **Admin Panel:** [`http://localhost:8000/admin/`](http://localhost:8000/admin/)

## 🧪 Running Tests

This project includes **43 test cases** located in the `tests/` directories of the app modules.  
Tests cover user views, manager permissions, password changes, and more.

---

### 1️⃣ Run Tests Locally (without Docker)

Run all tests
``` bash
python manage.py test

```
---
### 2️⃣ Run Tests in Docker Environment

``` bash
docker compose exec django python manage.py test

```

## 🗂 Project Structure
``` text
django-access-control
├── checkmark1
│   ├── asgi.py
│   ├── detail_viewset.py
│   ├── __init__.py
│   ├── settings_product.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── modules
│   └── authentication
|       ├── admin.py
|       ├── apps.py
|       ├── choices.py
|       ├── forms.py
|       ├── helpers.py
|       ├── __init__.py
|       ├── managers.py
|       ├── migrations
|       │   ├── 0001_initial.py
|       │   └── __init__.py
|       ├── models.py
|       ├── permissions.py
|       ├── project-structure.txt
|       ├── serializers.py
|       ├── tests
|       │   ├── __init__.py
|       │   ├── test_change_password_view.py
|       │   ├── test_managers.py
|       │   ├── test_reset_password_view.py
|       │   └── test_users_views.py
|       ├── urls.py
|       └── views.py
├── manage.py
├── docker-compose.yml
├── Dockerfile
├── staticfiles
├── media
├── nginx
│   └── default.conf
├── requirements.txt
└── README.md
```
---
