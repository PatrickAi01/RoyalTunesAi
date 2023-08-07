from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=30)
    #email = models.EmailField()
    phone = models.CharField(max_length=15)
    desc = models.TextField()

    def __str__(self):
        return self.name


class Customer(models.Model):
    username = models.CharField(max_length=15)
    email = models.EmailField()
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)

    def __str__(self):
        return self.username
