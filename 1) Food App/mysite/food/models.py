from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Item model representing a food item in the application.
class Item(models.Model):
    # The name of the item.
    item_name = models.CharField(max_length=100)
    
    # A description of the item.
    item_desc = models.TextField()
    
    # The price of the item.
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # URL of the item's image.
    image = models.URLField(default='https://media.istockphoto.com/id/1409329028/vector/no-picture-available-placeholder-thumbnail-icon-illustration-design.jpg?s=612x612&w=0&k=20&c=_zOuJu755g2eEUioiOUdz_mHKJQJn-tDgIAhQzyeKUQ=', null=True)
    
    # The user who created the item.
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        """Return the string representation of the item."""
        return self.item_name
    
    def get_absolute_url(self):
        """Return the URL to access a detail view for this item."""
        return reverse("food:detail", kwargs={"pk": self.pk})
