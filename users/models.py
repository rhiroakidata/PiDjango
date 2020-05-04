from django.db import models

class User(models.Model):
    name = models.CharField("Name", max_length=255)
    cpf = models.IntegerField()
    email = models.EmailField()
    password = models.TextField()
    phone = models.CharField(max_length=20)
    address =  models.TextField(blank=True, null=True)
    picture = models.ImageField(
        upload_to='{name}-{cpf}'.format(name=name, cpf=cpf), 
        blank=True
    )
    createdAt = models.DateTimeField("Created At", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name