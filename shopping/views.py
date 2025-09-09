
from django.shortcuts import render,redirect
from .models import Category,SubCategory, Product,CartItem
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ContactForm
from .models import Contact
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# display all product,Category to template and cart length
   
def index(request):
   
    
    categories = Category.objects.all()
    return render(request,'index.html',{
        'categories':categories,
        # 'cart_count': cart_count
        })

# add item to cart also increase the quantiry is not in the cart

@login_required(login_url='login') 
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, user=request.user)
        if cart_item.quantity < 7:
         cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem(product=product, user=request.user, quantity=1)

    cart_item.save()
    return redirect('/')
    # return render(request,'index.html')


# display cart items

@login_required(login_url='login')
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = 0
    tax = 0

    for item in cart_items:
        item.total = item.product.price * item.quantity 
        item.subtotal = item.product.price * item.quantity
        item.tax = 20 * item.quantity  

        subtotal += item.subtotal
        tax += item.tax

    grand_total = subtotal + tax

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'grand_total': grand_total,
        }
    return render(request, 'cartdetails.html', context)

    
# for remove item form cart

def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id,user=request.user)
    cart_item.delete()
    return redirect('cartdetails')

def increase_quantity(request, item_id):
    cart_item = CartItem.objects.get(product_id=item_id, user=request.user)
    if cart_item.quantity < 7:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cartdetails')


# for decrease
def decrease_quantity(request, item_id):
    cart_item = CartItem.objects.get(product_id=item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cartdetails')


def search(request):
    categories = Category.objects.all()
    query = request.GET.get("q", "").strip()
    products = []
    base_query = query

    if query:
        if query.endswith("s"):  
            base_query = query[:-1]  
        else:  
            base_query = query

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(name__icontains=base_query) |
        Q(subcategory__name__icontains=query) |
        Q(subcategory__name__icontains=base_query) |
        Q(category__name__icontains=query) |
        Q(category__name__icontains=base_query)
        ).distinct()

    return render(request, "search.html", {
        "products": products,
        "query": query,
        
    })


def product_detail(request, id):
    product = Product.objects.get(id=id)
    quantity = 1  
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        action = request.POST.get("action")
        
    total_price = product.price * quantity

    return render(request, "product_detail.html", {
        "product": product,
        "quantity": quantity,
        "total_price": total_price,
        
    })
    
    
def subcategory_products(request, id):
    subcategory = SubCategory.objects.get(id=id)
    products = Product.objects.filter(subcategory=subcategory)

    return render(request, "search.html", {
        "subcategory": subcategory,
        "products": products
        })



@csrf_exempt
def register_view(request):
    if request.method=='POST':
        username = request.POST['username']

        email=request.POST['email']
        password=request.POST['password']
        confirmPassword=request.POST['confirmPassword']

        if password != confirmPassword:
            messages.error(request,"Passwords do not match")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"user already exist") 
            return redirect('login')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.save()
        return redirect('login')
    return render(request,'signup.html')


def login_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        # email = request.POST['email']
        password=request.POST['password']
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        
        else:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request,'signin.html')

def logout_view(request):
    logout(request)
    return redirect('/')



@login_required
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, f"Thank You {contact.name}! Your message has been sent successfully.")
            return redirect("contact")   # same page reload
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})




