from django.db import models
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import Group, Permission


# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.city}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()


class Meta:
    permissions = [
        ("can_publish", "Can publish posts"),
    ]

# Create a new group
# editor_group, created = Group.objects.get_or_create(name='Editors')
# # Assign permissions to the group
# permission = Permission.objects.get(codename='can_publish')
# editor_group.permissions.add(permission)
