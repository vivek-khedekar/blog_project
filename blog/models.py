from django.db import models
from django.utils import timezone
import uuid
from django.conf import settings

User = settings.AUTH_USER_MODEL


class BlogPost(models.Model):
    id = models.CharField(primary_key=True, max_length=20, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # ✅ New
    is_deleted = models.BooleanField(default=False)  # ✅ New

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"BLG-{uuid.uuid4().hex[:7].upper()}"
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=20, editable=False)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # ✅ New
    is_deleted = models.BooleanField(default=False)  # ✅ New

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"CMT-{uuid.uuid4().hex[:7].upper()}"
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Comment by {self.author.username}"

 


class Like(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=20,
        unique=True,
        editable=False
    )
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"LIKE-{uuid.uuid4().hex[:7].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} liked {self.post}"
