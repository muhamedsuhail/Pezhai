from .models import Product,Order,Cart,cart_quantity,ordered_quantity
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import CheckoutForm,LoginForm,RegisterForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from .product_info_scraper import product_details
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse
import random
import json
import re

# Create your views here.

def register_view(request):
    
    if request.method == "POST":
        
        form=RegisterForm(request.POST)
        
        if form.is_valid():
        
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]

            # Ensure password matches confirmation
            password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]
        
            if password != confirmation:
        
                return render(request, "Capstone/register.html", {
                    "message": "Passwords must match.",
                    'form':RegisterForm()
                })

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.save()
    
            except IntegrityError:
                return render(request, "Capstone/register.html", {
                    "message": "User already exist.",
                    'form':RegisterForm()
                })
    
            return HttpResponseRedirect(reverse("login"))
    
    else:
    
        return render(request, "Capstone/register.html",{
            'form':RegisterForm()
        })

def login_view(request):

    if request.method == "POST":
        
        # Redirect User to the same page after login
        valuenext = request.POST.get('next')
        
        # Attempt to sign user in
        form=LoginForm(request.POST)
    
        if form.is_valid():
    
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
    
        else:
            
            # Check if authentication successful
            return render(request, "Capstone/login.html", {
                "message": "Invalid email and/or password.",
                'form':LoginForm()    
            })

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
        else:
            return render(request, "Capstone/login.html",{
                'form':LoginForm(),
                'message':"Invalid Credentials"
            })    

        if valuenext == "":
            return redirect(reverse("index"))
        else:
            return redirect(valuenext)
    
    else:
    
        return render(request, "Capstone/login.html",{
            'form':LoginForm()
        })


def logout_view(request):

    valuenext = request.GET.get("next")
    logout(request)
    
    if valuenext == "":
        return redirect(reverse("index"))
    else:
        return redirect(valuenext)

@ensure_csrf_cookie
def index(request,tag="index"):

    if request.method=="POST":
        
        if request.user.is_authenticated:
            
            if request.POST["tag"]=="updateCart":
                
                # When user adds or removes a Product update it to the database.
                
                data = json.loads(request.POST["data"])
                
                try:
                    cart= Cart.objects.get(user=request.user)
                
                except ObjectDoesNotExist:
                    cart = Cart.objects.create(user=request.user,cart_total = 0)

                cart.save()
                tot = False
                if data['args']=='remove':
                
                    target = cart.cart_items.all()[data['target']]
                    cart.cart_items.remove(target)
                
                    if len(cart.cart_items.all())==0:
                        cart.delete()
                else:
                
                    for i in data['cart_items']:
                
                        try:
                            cart_q = cart_quantity.objects.get(cart=cart,item=Product.objects.get(id=i["id"]))
                        except ObjectDoesNotExist:
                            cart_q = cart_quantity.objects.create(cart=cart,item=Product.objects.get(id=i["id"]),quantity= 0 )
                            tot = True
                
                        cart_q.quantity = int(i["quantity"])
                        cart_q.save()
                
                cart.cart_total = cart.cart_total + data['cart_total'] if tot else data['cart_total']
                cart.save()


            if request.POST["tag"]=="getCartItems":
                
                # Send the data from database when user reloads the website
                
                try:
                    cart = Cart.objects.get(user=request.user)
                except ObjectDoesNotExist:
                    data = {'User_Authenticated':True,'status':"failed"}
                    return JsonResponse(data)
                
                cart_items = []
                
                for cart_item in cart.cart_items.all():
                
                    dict={}
                    dict["id"] = cart_item.id
                    dict["title"] = cart_item.name
                    
                    free_shipping = cart_item.shipping_price.split(' ')[0].lower()=="free"
                    
                    if not free_shipping:
                        dict["price"] = int(float(cart_item.price.split(' ')[1].replace(',',''))+float(cart_item.shipping_price.split(' ')[1].replace(',','')))
                    else:
                        dict["price"] = int(cart_item.price.split(' ')[1].replace(',','').split('.')[0])
                    
                    dict["img"] = cart_item.img_link
                    dict["quantity"] = cart_quantity.objects.get(item=cart_item,cart=cart).quantity
                    cart_items.append(dict)

                data = {'User_Authenticated':True,'status':"success",'cart_items': cart_items,'cart_total':int(cart.cart_total)}
                return JsonResponse(data)

            if request.POST["tag"]=="deleteOrder":
                
                # Delete an order if it is cancelled
                id = request.POST["id"]
                o = Order.objects.get(id=id)
                o.delete()

            status = {'User_Authenticated':True,'success':True}
            return JsonResponse(status)

        else:
            status = {'User_Authenticated':False}
            return JsonResponse(status)

    if tag=="search":

        # Searchbar queries reache here.

        search = request.GET.get("search")
        data = regex_search(search)

        # Paginator function which sends only 25 items per page
        paginator = Paginator(data, 25) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request,"Capstone/product_listing.html",{
            'page_obj':page_obj,
            'title':f"Search results for '{search}'"
        })

    if tag=="index":
        
        # Pick up items randomly for Deals of the day section.
        data = random.choices(Product.objects.all(),k=24)
        return render(request, "Capstone/index.html",{
            "data":data,
        }) 
        
    elif tag=="orders":

        if request.user.is_authenticated:        
            
            o = Order.objects.filter(user=request.user).order_by('-id')
            data = {}
            
            for i in o:
                data[i] ={'order':o,'items':ordered_quantity.objects.filter(order=i),'total':i.total_cost}
            
            return render(request, "Capstone/my_orders.html",{
                "data":data,
            })
        
        else:
            return HttpResponseRedirect(reverse("login"))
    
    else:
        
        # Category wise product listing
        data = Product.objects.filter(category=tag)
        paginator = Paginator(data, 25) 
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    return render(request, "Capstone/product_listing.html",{
        "page_obj":page_obj,
        "title":tag
    })
    
def product_page(request,product_id):     

    product = Product.objects.get(id=product_id)

    return render(request, "Capstone/product_page.html",{
        "product":product,
        "product_details":product_details(product.url),
    })

def checkout(request):
    
    if request.user.is_authenticated:        
    
        if request.method=="POST":
            
            form = CheckoutForm(request.POST)
    
            if form.is_valid():
    
                cleaned_data = form.cleaned_data
                cart = Cart.objects.get(user=request.user)
                orders = Order.objects.filter(user=request.user,status=False)
    
                for i in orders:

                    # If the user cancelled the order and tries again to place the order pick up the previosly created object instead of creating a new one
                    if i.total_cost == cart.cart_total and len(i.ordered_items.all())==len(cart.cart_items.all()):
                        o = i
    
                else:
    
                    o = Order.objects.create(user=request.user,contact = cleaned_data["mobile_number"],status=False)
                    o.shipping_address = ''
                    
                    for i in cleaned_data:
                    
                        if i!="mobile_number":
                            o.shipping_address  += cleaned_data[i]+','
                        else:
                            o.shipping_address  += "Contact: "+cleaned_data[i]
                    
                    if cleaned_data["landmark"]!="":
                        o.shipping_address  += "Landmark: "+cleaned_data["landmark"]

                    o.total_cost = cart.cart_total
                    o.save()
                    
                    for i,j in zip(cart.cart_items.all(),cart_quantity.objects.filter(cart=cart)):
                        q = ordered_quantity.objects.create(order=o,item=i,quantity=j.quantity)
                        q.save()
                
                request.session['order_id'] = o.id
                return redirect('process_payment')

            else:
                
                return render(request, "Capstone/checkout_page.html",{
                    "form":CheckoutForm(),
                    "message":"Something went Wrong!Please Try again."
                })
        
        return render(request, "Capstone/checkout_page.html",{
            "form":CheckoutForm()
        })
    
    else:
        return HttpResponseRedirect(reverse("login"))

def process_payment(request):
    
    if request.method=="POST":
        
        order = get_object_or_404(Order, id=request.POST["id"])    
        if request.POST["status"]=="success":
            
            # On successfull transaction Update order status and delete the Cart.
            order.status = True
            order.save()
            cart = Cart.objects.get(user=request.user)
            cart.delete()
        else:

            # Delete the order if the payment is Cancelled by the user.
            order.delete()
        
        return JsonResponse('Payment Completed')
    
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    return render(request, 'Capstone/process_payment.html', {'order': order})

# Payment Acknowledgement message

@csrf_exempt
def payment_done(request):
    return render(request, 'Capstone/payment_acknowledgement.html',{'msg':"Payment Done","status":True})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'Capstone/payment_acknowledgement.html',{'msg':"Payment Cancelled","status":False})


def regex_search(search):

    # Search across the database for the Search query.
    ls=[]
    for i in Product.objects.all():
        if re.search(f"{search}+",i.name,re.IGNORECASE):
            ls.append(i)
        else:
            s = search.split(' ')
            if len(s)>1:
                for j in s:
                    if re.search(f"{j}+",i.name,re.IGNORECASE):
                        ls.append(i)
    return ls