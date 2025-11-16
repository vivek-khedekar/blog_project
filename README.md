# BLOG PROJECT - FULL DOCUMENTATION

## 📌 Overview
This is a complete Blog Backend API built using **Django** and **Django REST Framework**.  
It includes:

- JWT authentication  
- Blogs  
- Likes  
- Comments  
- User roles (admin/user)

---

# 🧩 SECTION 1: FEATURES
- User Registration  
- User Login (JWT Authentication)  
- Access Token + Refresh Token  
- Create, Read, Update, Delete Blogs  
- Like / Unlike Blog Posts  
- Comment on Blogs  
- Role-Based Access Control  
- Secure PBKDF2 Password Hashing  
- Clean REST API Architecture  

---

# 🛠 SECTION 2: TECHNOLOGIES USED
- Python 3.x  
- Django  
- Django REST Framework  
- SimpleJWT  
- SQLite  
- CORS Headers  

---

# 📂 SECTION 3: PROJECT STRUCTURE

```
blog_project/
│
├── blog_project/      # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── users/             # Custom user authentication app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── blog/              # Blog, Likes, Comments app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
│
├── manage.py
└── README.md
```

---

# ⚙️ SECTION 4: INSTALLATION

### 1️⃣ Clone the repository
```
git clone <repo-url>
```

### 2️⃣ Enter the project
```
cd blog_project
```

### 3️⃣ Create virtual environment
```
python -m venv .venv
```

### 4️⃣ Activate environment (Windows)
```
.\.venv\Scripts\activate
```

### 5️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 6️⃣ Run migrations
```
python manage.py migrate
```

### 7️⃣ Start server
```
python manage.py runserver
```

---

# 🔐 SECTION 5: AUTHENTICATION API

## 1. Register User
**POST:** `/api/auth/register/`

## 2. Login (Get Tokens)
**POST:** `/api/auth/token/`

### Response:
```
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

## 3. Refresh Token
**POST:** `/api/auth/token/refresh/`

---

# 📝 SECTION 6: BLOG API

### ✔ Get All Blogs
`GET /api/blogs/`

### ✔ Create Blog (Requires Login)
`POST /api/blogs/`

### ✔ Get Blog by ID
`GET /api/blogs/<id>/`

### ✔ Update Blog  
`PUT /api/blogs/<id>/`

### ✔ Delete Blog  
`DELETE /api/blogs/<id>/`

---

# ❤️ SECTION 7: LIKE & COMMENT API

### ✔ Like Blog
`POST /api/blogs/<id>/like/`

### ✔ Add Comment
`POST /api/blogs/<id>/comment/`

Body:
```
{
  "content": "Nice blog!"
}
```

---

# 👤 SECTION 8: USER ROLES

## USER
- Create blogs  
- Like blogs  
- Comment  
- Update only OWN posts  
- Cannot delete others' blogs  

## ADMIN
- Full access  
- Edit/Delete ANY blog  
- Manage users  

---

# 🔐 SECTION 9: PASSWORD HASHING (SECURITY)

Django uses:

### ⭐ **PBKDF2 + SHA256 (390,000 iterations)**

This gives:
- Salted hashing  
- Slow brute-force resistance  
- Industry-standard security  

---

# 🔑 SECTION 10: JWT TOKEN FLOW

1. User logs in  
2. System returns Access Token + Refresh Token  
3. Access token expires quickly  
4. Refresh token generates a new access token  
5. Used in Authorization header:
```
Authorization: Bearer <access_token>
```

---

# 🧪 SECTION 11: TROUBLESHOOTING

### ❌ Token invalid
→ refresh expired or incorrect token

### ❌ 401 Unauthorized
→ missing Authorization header

### ❌ Cannot assign AnonymousUser
→ user not authenticated

### ❌ ModuleNotFoundError
→ missing Python packages

---

# 📧 SECTION 12: CONTACT

**Author:** Vivek Khedekar  
**GitHub:** https://github.com/vivek-khedekar  
**Email:** vivek@apexiq.ai  

---

# ✅ END OF DOCUMENTATION
