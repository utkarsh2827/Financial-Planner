from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from .alpha_vantage_interaction import curr_p
class Stock(models.Model):
    WATCHLIST = 'W'
    MAIN_PORTFOLIO = 'P'
    ENTITY_CHOICE = [("WATCHLIST", WATCHLIST),("MAIN_PORTFOLIO",MAIN_PORTFOLIO)]
    symbol = models.CharField(max_length=10)
    name = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    quantity_owned = models.IntegerField(default = 0)
    initial_price = models.DecimalField(max_digits=10,decimal_places=3,default = 0.0)
    choice = models.CharField(max_length = 20, choices = ENTITY_CHOICE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('financial_planner-portfolio-list')
    @property
    def curr_price(self):
        f = curr_p(self.symbol)
        return float(f)

class Funds(models.Model):
    WATCHLIST = 'W'
    MAIN_PORTFOLIO = 'P'
    ENTITY_CHOICE = [
        ("WATCHLIST", WATCHLIST),
        ("MAIN_PORTFOLIO",MAIN_PORTFOLIO)
    ]
    name = models.TextField()
    type = models.CharField(max_length = 20)
    investment = models.DecimalField(max_digits=10,decimal_places=3,default = 0.0)
    choice = models.CharField(max_length = 20, choices = ENTITY_CHOICE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)





