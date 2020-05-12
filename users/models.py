from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None

    name = models.CharField("Name", max_length=255)
    cpf = models.IntegerField()
    email = models.EmailField(blank=False, unique=True)
    password = models.BinaryField(blank=False)
    phone = models.CharField(max_length=20)
    address =  models.TextField(blank=True, null=True)
    picture = models.ImageField(
        upload_to='{name}-{cpf}'.format(name=name, cpf=cpf), 
        blank=True
    )
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name