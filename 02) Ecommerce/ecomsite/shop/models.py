from django.db import models

# Create your models here.
class ProductsModel(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price =  models.FloatField()
    category = models.CharField(max_length=200)
    description = models.TextField()
    image = models.CharField(max_length=300)

    def __str__(self):
        return self.title
    
class OrderModel(models.Model):
    item = models.CharField(max_length=1000)


    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.IntegerField()
    city = models.CharField(max_length=50)
