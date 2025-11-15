from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.CharField(
        primary_key=True,
        max_length=20,
        unique=True,
        editable=False
    )
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default="user")
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = f"USR-{uuid.uuid4().hex[:7].upper()}"
        super().save(*args, **kwargs)

    def soft_delete(self):
        """Mark user as inactive without deleting from DB."""
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def __str__(self):
        return self.username
