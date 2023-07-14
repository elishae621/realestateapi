from django.shortcuts import render
from realtor.realtor.spiders.realtorspider import scrape

def home(request):
    scrape()
    render(request, "<h1>Running</h1>", context={})