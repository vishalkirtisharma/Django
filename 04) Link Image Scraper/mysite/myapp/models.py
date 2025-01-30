from django.db import models

# Create your models here.

class LinkModel(models.Model):
    address = models.URLField(null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name



class ImageModel(models.Model):
    address = models.URLField(null=True,blank=True)
    name = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name
