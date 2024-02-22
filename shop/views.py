from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from math import ceil

# Create your views here.

def index(request):
    products = Product.objects.all()
    n = len(products)
    nSlides = n//4 + ceil((n/4) - (n//4))
    params = {"product":products, 'nSlides':nSlides, 'range':range(1,nSlides)}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/aboutUs.html')

def contact(request):
    pass 

def tracker(request):
    pass 

def prodView(request):
    pass

def checkout(request):
    pass