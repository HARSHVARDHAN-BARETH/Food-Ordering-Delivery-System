from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Product
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CreateUserForm, ProfileForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user



def home(request):

    return render(request, 'home.html')

# @login_required(login_url='login')
def edit(request):
    return render(request, 'edit.html')

@login_required(login_url='login')
def profilePage(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, Your Profile is Updated')
            return redirect("/profile/")   
    else:
        form = ProfileForm(instance=request.user.profile)

    context = {'form': form}
    return render(request, 'edit.html', context)

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'{username}, You are logged in.')
            return redirect("/")
        else:
            messages.info(request, 'Wrong passwrod or username')
            return redirect('/login/')
    return render(request, 'login.html')

@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Account is created.')
            return redirect('/login/')
        else:
            context = {'form': form}
            messages.info(request, 'Invalid credentials')
            return render(request, 'signin.html', context)

    context = {'form': form}
    return render(request, 'signin.html', context)

@login_required(login_url='login')
def logOut(request):
    logout(request)
    messages.info(request, 'You logged out successfully')
    return redirect('/login/')


# def loginPage(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
         
#         if not User.objects.filter(username = username).exists():
#             messages.error(request, "Invalid UserName")
#             return redirect('/login/')
#         user = authenticate(username = username, password = password)
        
#         if user is None:
#             messages.error(request, "Invalid Password")
#             return redirect('/login/')
#         else:
#             login(request, user)
#             return redirect('/')

            
#     return render(request, "login.html")
# def register(request):
#     if request.method == "POST":
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         username = request.POST.get("username")
#         password = request.POST.get("password")
        
#         user = User.objects.filter(username = username)
        
#         if user.exists():
#             messages.info(request, "User Name Already! Taken.")
#             return redirect('/login/')
        
#         user = User.objects.create(
#             first_name = first_name,
#             last_name = last_name,
#             username = username
#         ) 
#         user.set_password(password)
#         user.save()
#         messages.info(request, "Account Created Successfully!")

#         return redirect('/sign/')
#     return render(request, "signin.html")


# def add_to_cart(request):
#     cart = request.session.get('cart', {})

def cart(request):
    return render(request, "cart.html")

# def cart_view(request):
#     cart = request.session.get('cart', {})
#     product_id = request.GET.get('prod_id')
#     product_name = Product.objects.get(id=product_id)
#     product = Product.objects.filter(id=product_id)
    
#     for i in product:
#         name = i.name
#         price = i.price
#         description = i.description
#         image = i.image
#         Product(name=name, price=price, description = description, image=image).save()
#         return redirect("/")
    # Get the product IDs from the cart
    # product_ids = cart.keys()
    
    # # Fetch the products based on their IDs
    # products_in_cart = Product.objects.filter(id__in=product_ids)
    # print(products_in_cart)
    
    # # Create a dictionary to map product IDs to their details
    # cart_with_details = {}
    # for product in products_in_cart:
    #     cart_with_details[product.id] = {
    #         'name': product.name,
    #         'image': product.image.url,  # Assuming image is a field in your Product model
    #         'price': product.price,
    #         'quantity': cart[str(product.id)],  # Get quantity from the cart
    #     }
    
    # # Pass the detailed product information to the cart template
    # return render(request, 'cart.html', {'cart': cart_with_details})

def menu(request):
    if request.method=="POST": 
        product=request.POST.get('product') 
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('/')
        return redirect('home')


    prs = Product.get_all_products()
    print(prs)
    return render(request, 'menu.html', {"product":prs})

def cart_view(request):
    cart = request.session.get('cart', {})
    
    # Get the product IDs from the cart
    product_ids = cart.keys()
    
    # Fetch the products based on their IDs
    products_in_cart = Product.objects.filter(id__in=product_ids)
    print(products_in_cart)
    
    # Create a dictionary to map product IDs to their details
    cart_with_details = {}
    for product in products_in_cart:
        cart_with_details[product.id] = {
            'name': product.name,
            'image': product.image.url,  # Assuming image is a field in your Product model
            'price': product.price,
            'quantity': cart[str(product.id)],  # Get quantity from the cart
        }
    
    # Pass the detailed product information to the cart template
    return render(request, 'cart.html', {'cart': cart_with_details})
