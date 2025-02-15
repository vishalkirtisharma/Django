from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class FoodModel(models.Model):
    name = models.CharField(max_length=100)
    carbs = models.FloatField()
    protine = models.FloatField()
    fats = models.FloatField()
    calories = models.IntegerField()

    def __str__(self):
        return self.name
    

class Consume(models.Model):
    food_consumed = models.ForeignKey(FoodModel,on_delete=models.CASCADE,related_name='food_consumed')
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Consume'  # Corrected Meta option
    
    def __str__(self):
        return f"{self.user.username} consumed {self.food_consumed.name}"

