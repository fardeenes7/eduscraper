from django.urls import path, include
from .views import scrape_manitoba, scrape_toronto

urlpatterns = [
    path('manitoba/', scrape_manitoba, name='manitoba'),
    path('toronto/', scrape_toronto, name='toronto')
]