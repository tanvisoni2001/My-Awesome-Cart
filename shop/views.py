from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact,Order,OrderUpdate
from math import ceil
import json 



# Create your views here.
MERCHANT_KEY = 'kbzk1DSbJiV_03p5'

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
       form = Contact(request.POST)
       thank = True
       return render(request, 'shop/contactUs.html', {'thank': thank})
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
        amount = request.POST.get('amount', '')

        order = Order(name = name, email = email,phone = phone, address = address,
                       address_2 = address_2,city = city, state = state, zip_code = zip_code,
                       item_json = itemJson, amount = amount)
        order.save() 
        id = order.order_id
        update = OrderUpdate(order_id= id, update_desc = "The order has been placed!")
        update.save()
        thank = True 
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html')

def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.sub_category.lower():
        return True 
    else:
       return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category = cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        print(prod)


        n = len(prod)
        nSlides = n//4 + ceil((n/4) - (n//4))
        if len(prod) != 0: 
            allProds.append([prod,range(1,nSlides), nSlides])

    params = {'allProds':allProds, 'msg': ""}
    if len(allProds) == 0 or len(query) < 4:
        params = {'msg':"Please make sure to enter relevant search query"} 
    return render(request, 'shop/search.html', params)
       
        