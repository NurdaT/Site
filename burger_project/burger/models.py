from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    avatar = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return f"Profile of {self.user.username}"


class Burger(models.Model):
    name = models.CharField("Name", max_length=100)
    price = models.DecimalField("Price", max_digits=6, decimal_places=2)
    description = models.TextField("Description", blank=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    image = models.ImageField("Image", upload_to="burgers/", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Burger"
        verbose_name_plural = "Burgers"