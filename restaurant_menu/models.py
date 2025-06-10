from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

MEAL_TYPE = (
    ("starters", "Starters"),
    ("salads", "Salads"),
    ("main_dishes", "Main Dishes"),
    ("deserts", "Deserts")
)

STATUS = (
    (0, "Unavailable"),
    (1, "Available")
)

class Item(models.Model):
    meal = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    meal_type = models.CharField(choices=MEAL_TYPE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=1)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.meal



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField(default='')
    created_at = models.DateTimeField(default=timezone.now)

