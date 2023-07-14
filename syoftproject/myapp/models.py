from django.db import models

# Create your models here.

class User(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )

    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    inventory_count = models.PositiveIntegerField()

    def __str__(self):
        return self.title
