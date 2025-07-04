# Django Blog Project – Report & Documentation

## Overview
This project is a personal blog application built with Django and Django REST Framework. It allows users to register, log in, create and manage blog posts with images, organize them by category, and comment on posts. The application provides both a modern web interface and a secure REST API for all main features.

---

## Features
- **User Registration & Authentication**: Users can register (with email), log in, log out, and manage their profile.
- **Blog Posts**: Authenticated users can create, edit, and delete their own posts. Each post can have a title, content, category, and an optional image.
- **Categories**: Posts are organized by categories. Categories can be managed by the admin.
- **Comments**: Authenticated users can comment on any post. Comments are displayed under each post.
- **Responsive Web Interface**: Clean, modern HTML/CSS templates for all main pages (list, detail, create, login, register, profile).
- **REST API**: All main operations (register, login, CRUD for posts, categories, comments) are available via a RESTful API (JWT authentication).

---

## Project Structure
- `blogapp/models.py`: Models for Category, Post, and Comment.
- `blogapp/views.py`: Views for HTML pages and API endpoints.
- `blogapp/serializers.py`: DRF serializers for API data.
- `blogapp/forms.py`: Django forms for registration, login, post creation, and comments.
- `blogapp/templates/blogapp/`: HTML templates for all main pages.
- `blogapp/static/blogapp/style.css`: Main CSS file for styling.
- `blogapp/urls.py`: URL routing for both web and API endpoints.

---

## Main API Endpoints
- `POST   /api/register/` – Register a new user
- `POST   /api/token/` – Obtain JWT token (login)
- `POST   /api/token/refresh/` – Refresh JWT token
- `GET    /api/posts/` – List all posts
- `POST   /api/posts/` – Create a new post
- `GET    /api/posts/<id>/` – Retrieve a post
- `PUT/PATCH /api/posts/<id>/` – Update a post
- `DELETE /api/posts/<id>/` – Delete a post
- `GET    /api/categories/` – List categories
- `GET    /api/comments/` – List comments
- `POST   /api/comments/` – Create a comment

**Note:** For protected endpoints, use `Authorization: Bearer <access_token>` header.

---

## How to Run
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create a superuser: `python manage.py createsuperuser`
4. Start the server: `python manage.py runserver`
5. Access the app at `http://127.0.0.1:8000/api/`

---

## Usage Notes
- Register and log in to access all features.
- Use the web interface for a user-friendly experience, or test the API with tools like Insomnia/Postman.
- Admins can manage categories and all content via the Django admin panel.

---

## License
This project is for educational purposes and can be freely reused or extended. 