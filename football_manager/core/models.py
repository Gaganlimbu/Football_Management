from django.db import models
from django.utils import timezone

class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    team = models.CharField(max_length=100)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class MatchPerformance(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='performances')
    date = models.DateField()
    opponent = models.CharField(max_length=100)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.player.name} vs {self.opponent} on {self.date}"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('featured', 'Featured'),
        ('sale', 'On Sale'),
        ('new', 'New Arrivals'),
        ('bestseller', 'Bestsellers'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='featured')

    def __str__(self):
        return self.name

