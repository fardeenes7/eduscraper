from django.shortcuts import render, redirect
from scraper.scripts import manitoba, toronto
# Create your views here.


def scrape_manitoba(request):
    manitoba.scrape()
    return redirect('admin:index')


def scrape_toronto(request):
    toronto.scrape()
    return redirect('admin:index')