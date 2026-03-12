# Django Authentication System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Django-6.0.3-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge">
  <img src="https://img.shields.io/badge/Project-Active-brightgreen?style=for-the-badge">
</p>

---

## 📌 Project Description

A complete authentication system built with Django.  
This project includes user registration, login, logout, dynamic navbar, role-based user management, profile image upload, and profile page functionality.

The project demonstrates a clean Django project structure with reusable templates and modern UI using Tailwind CSS.

---

## 🖼️ Project Preview

  ![Project Preview](screenshots/Full_Page.jpeg)

---

## ✨ Features

- User Registration
- Secure Login System
- Logout System
- Dynamic Navbar
- Login with Username / Email / Phone Number
- Profile Page
- Profile Image Upload
- Custom User Model
- Role-Based Authentication
- Recruiter Profile
- Job Seeker Profile
- Django Messages Framework
- SweetAlert2 Popup Messages
- Tailwind CSS UI
- Responsive Design

---


## 🛠️ Tech Stack & Technologies Used

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **JavaScript:** For interactive UI elements
- **CSS:** For styling
- **UI Framework:** Tailwind CSS
- **Database:** SQLite3
- **Language:** Python
- **Authentication:** Django Custom User Model
- **UI Alerts:** SweetAlert2
- **Image Handling:** Pillow


---

## 📂 Project Structure

```bash
AUTH_ROLE_SYSTEM/
├── accounts/
│   ├── __pycache__/
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   └── 0002_application.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── auth_role_system/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── jobs/
│   ├── __pycache__/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── media/
│   └── profile/
│       ├── 300x300_12.2kb.jpg
│       ├── 300x300_43.2KB.jpg
│       └── 413x531_28.5kb.jpg
│
├── screenshots/
│   └── Full_Page.jpeg
│
├── templates/
│   ├── accounts/
│   │   ├── change_password.html
│   │   ├── edit_recruiter_profile.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   └── register.html
│   │
│   ├── includes/
│   │   ├── footer.html
│   │   └── header.html
│   │
│   ├── jobs/
│   │   └── create_new_jobs.html
│   │
│   └── base.html
│
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

---

## 🔐 Authentication Flow

### Logged Out User

A logged out user can access:

- Home
- Register
- Login

### Logged In User

A logged in user can access:

- Home
- Profile
- Logout

The navbar changes dynamically based on the user authentication state.

---

## 👥 User Roles

This project supports two user roles:

- **Job Seeker**
- **Recruiter**

When a user registers, a related profile is automatically created based on the selected role.

---

## 📝 Registration Form Fields

The registration form includes:

- First Name
- Last Name
- Username
- Email
- Phone Number
- Profile Picture
- Role
- Password
- Confirm Password

All fields are required.

---

## 🔑 Login System

Users can log in using:

- Username
- Email
- Phone Number

along with their password.

---

## 🔒 Password Validation

The password must contain:

- At least 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/auth_role_system.git
cd auth_role_system
```

### 2. Create virtual environment

```bash
python -m venv .venv
```

### 3. Activate virtual environment

#### Windows
```bash
.venv\Scripts\activate
```

#### Mac / Linux
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install django pillow
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Now open:

```
http://127.0.0.1:8000/
```

---

## ⚙️ Media & Static Configuration

### settings.py

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### main urls.py

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 📸 Main Pages

### Home Page

- Dynamic navbar
- Hero section
- Responsive layout

### Register Page

- Professional form UI
- Profile image upload
- Role selection
- Password validation

### Login Page

- Login using username, email, or phone number
- SweetAlert popup messages

### Profile Page

- Auto-filled user details
- Profile image display
- Role-based user information

---

## 🎯 Future Improvements

- Edit Profile
- Change Password
- Forgot Password
- Email Verification
- Role-Based Dashboard
- Profile Image Preview Before Upload
- Password Show / Hide Toggle
- Better Admin Dashboard
- Search & Filter Features
- User Authentication
- Recruiter Profile
- Job Posting System
- Job Application System
- Profile Management

---

## 💡 Why This Project?

This project was built to practice and demonstrate:

- Django Custom User Model
- Authentication System
- Role-Based Access Control
- Image Upload Handling
- Dynamic Template Rendering
- Responsive Tailwind CSS UI
- Clean Django Project Structure

---

## 👨‍💻 Author

**MD ANISUJJAMAN ONTAR**

---

## 📄 License

This project is for educational and portfolio purposes.

---

## ⭐ Support

If you like this project, consider giving it a **star** on GitHub.