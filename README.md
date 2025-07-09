Readme tesing branch1
# 📰 Personal Blog Website (Django + DRF)

A full-stack personal blogging platform built with Django and Django REST Framework. Users can register, log in, create blog posts with images, comment on posts, and interact via a secure and RESTful API.

---

## 🚀 Features

- 🔐 JWT Authentication (Login / Register)
- 📝 Create, edit, and delete blog posts
- 🗂️ Post categories managed by admin
- 💬 Comment system (modal-based UI)
- 🌐 REST API for all core operations
- 📸 Optional image upload for blog posts
- 🧑‍💼 Admin panel access for content moderation

---

## 🛠️ Tech Stack

- **Backend**: Django 4.x
- **API**: Django REST Framework (DRF)
- **Auth**: JWT via Simple JWT
- **Frontend**: HTML, CSS (custom responsive design)
- **Database**: SQLite (development)

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Yassiine20/django-blogWebsite.git
   cd django-blogWebsite
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root folder:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ```

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

---

## 🔗 API Endpoints

| Action            | Endpoint                 | Method |
|-------------------|--------------------------|--------|
| Register user     | `/api/register/`         | POST   |
| Get JWT token     | `/api/token/`            | POST   |
| List posts        | `/api/posts/`            | GET    |
| Post detail       | `/api/posts/<id>/`       | GET    |
| Create post       | `/api/posts/`            | POST   |
| Update post       | `/api/posts/<id>/`       | PUT/PATCH |
| Delete post       | `/api/posts/<id>/`       | DELETE |
| List categories   | `/api/categories/`       | GET    |
| List comments     | `/api/comments/`         | GET    |
| Add comment       | `/api/comments/`         | POST   |

---

## 📁 Project Structure

```
   project/
├── blogapp/
│   ├── models.py         # Post, Category, Comment models
│   ├── views.py          # Web + API views
│   ├── forms.py          # Forms for user input
│   ├── serializers.py    # DRF Serializers
│   ├── templates/        # HTML templates
│   └── static/           # CSS, images, assets
├── blog/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
├── .env.example
├── manage.py
├── .gitignore
├── requirements.txt
```

---

## 🙌 Acknowledgments

This project was developed as part of a Django internship. It serves as a foundation for future projects and a reference for building full-stack Django + DRF applications.

---

## 📃 License

This project is open-source and available under the [MIT License](LICENSE).
