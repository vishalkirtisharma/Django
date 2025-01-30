from django.db import models

# Create your models here.

class ProfileModel(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    degree = models.CharField(max_length=200,default="")
    summary = models.TextField(null=True,blank=True)
    school = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    previous_work = models.TextField()
    skill = models.TextField()
    
    def __str__(self):
        return self.name