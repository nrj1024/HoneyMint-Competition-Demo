from django.db import models

# Create your models here.
class Contestant(models.Model):
    first_name = models.CharField(max_length=48)
    last_name = models.CharField(max_length=48)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True) #Applied [0-9]{10} in HTML input RegEx pattern so Char type would be fine here.
    entries = models.IntegerField()
    invby = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name