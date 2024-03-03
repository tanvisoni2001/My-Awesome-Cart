from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact,Order,OrderUpdate
from math import ceil
import json

# Create your views here.

def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {items['category'] for items in catprods}
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        allProds.append([prod,range(1,nSlides), nSlides])

    params = {'allProds' : allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/aboutUs.html')

def contact(request):
    if request.method == "POST":
       name = request.POST.get('name','')
       email = request.POST.get('email', '')
       phone = request.POST.get('phone', '')
       desc = request.POST.get('desc', '')
       contact = Contact(name = name, email = email, phone = phone, desc = desc)
       contact.save()
       return HttpResponse('Form submit successfully!')
    return render(request, 'shop/contactUs.html') 

def tracker(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        orderId = request.POST.get('orderId', '')
        try:
            order = Order.objects.filter(order_id= orderId, email = email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id = orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time':item.timestamp})
                    response = json.dumps([updates,order[0].item_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')    
                
    return render(request, 'shop/tracker.html')

def prodView(request,myid):
    product = Product.objects.filter(id = myid)
    params = {'prod':product[0]}
    return render(request,'shop/productView.html',params)

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address','')
        address_2 = request.POST.get('address_2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zipcode','')
        itemJson = request.POST.get('itemJson','')

        order = Order(name = name, email = email,phone = phone, address = address,
                       address_2 = address_2,city = city, state = state, zip_code = zip_code,
                       item_json = itemJson)
        order.save() 
        id = order.order_id
        update = OrderUpdate(order_id= id, update_desc = "The order has been placed!")
        update.save()
        thank = True 
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html')