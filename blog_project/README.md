# Blog API (Django REST Framework)

A complete blog backend featuring:
- JWT Authentication
- User Roles (admin/user)
- Password Reset
- Blog CRUD
- Like / Comment System

## 🔐 Authentication API

### Register
POST /api/auth/register/

### Login
POST /api/auth/token/

### Refresh Token
POST /api/auth/token/refresh/

### Reset Password
POST /api/auth/reset-password/
POST /api/auth/reset-password-confirm/

## 📝 Blog API

### List Blogs
GET /api/blogs/

### Create Blog
POST /api/blogs/

### Retrieve Blog
GET /api/blogs/<id>/

### Update Blog
PUT /api/blogs/<id>/

### Delete Blog
DELETE /api/blogs/<id>/

## ❤️ Like API
POST /api/blogs/<id>/like/

## 💬 Comment API
POST /api/blogs/<id>/comment/

## ✔ Permissions
- Public: Can read blogs
- Users: Create blogs, like, comment, edit own posts
- Admin: Can edit/delete all posts

## 🚀 Tech Stack
- Django
- Django REST Framework
- SimpleJWT
- Python 3.13
