# Django Role-Based Security Management System
**Manage Users, roles, and permissions with ease**

This project is a role-based security management system built with Django.
It provides different responses and permissions depending on a user’s role within the company.

- ✅ 43 automated test cases included (all passing).
- 🚀 Deployment-ready using Gunicorn for high-performance request handling and Nginx to serve static and media    files efficiently.
- 🌐 REST Browsable API interface for easy interaction and testing.
- 🖥️ Currently not deployed to a live domain — but you can run it on your localhost or configure it for any domain.

## Features
This system enforces role-based access control (RBAC) across four views.
There are three main roles plus an admin role with restricted access:

### 👥 Roles
- **👑 Admin** -> Full access to the Django Admin Panel (exclusive, not available to other roles).
- **🧑‍💼 Manager** -> Manages employees and self, can create/update/delete it's own employees and self profiles.
- **📰 Reporter** -> Read-only access to users data and change password of self.
- **👤 Employee** -> Read-only access only to their own profile and change password of self.


---
### 🔑 Views & Permissions
1- **Users List** (/users/)
  - *📖 GET* -> Lists user profiles.
    - All roles can access ✅ , but each role only sees the profiles allowed by their permissions.
  - *✍️ POST* → Create a new user.
    - Only 🧑‍💼 Managers are allowed.
    - When a Manager creates a user:
      - A random password 🔑 is generated.
      - The user must change it on their first login (change_password = False until updated).

2- **Users Detail** (/users/{id}/)
  - *📖 GET* → Retrieve details of a user by ID
    - 🧑‍💼 Manager → Only their own employees and self 👥
    - 📰 Reporter → Read-only access to all users 👀
    - 👤 Employee → Only their own profile 🪪
  - ✏️ *PUT / PATCH / DELETE* → Manage user accounts
    - Allowed only for 🧑‍💼 Managers, and only for their employees and self
    - 🚫 Managers cannot modify:
      - is_active, is_superuser, is_staff, change_password, password

3- **Change Password** (/change-password/)
  - 🔐 POST → Change password
    - Any role (👑, 🧑‍💼, 📰, 👤) can update their own password only
    - Requires: current password + new password ✨

4- **Reset Password** (/reset-password/)
  - ♻️ PUT → Reset a forgotten password
    - Only 🧑‍💼 Managers can reset passwords of their employees and self
    - ❌ Employees and Reporters cannot reset others’ passwords

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
