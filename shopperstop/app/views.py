from django.shortcuts import render,redirect, get_object_or_404
from .models import Product,Customer,Cart,OrderPlaced,Payment,Wishlist
from django.views import View
from django.db.models import Count,Q
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
import razorpay
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.utils.decorators import method_decorator
# Create your views here.
@login_required
# def home(request):
#     totalitem = 0
#     wishitem=0
#     if request.user.is_authenticated:
#         totalitem = len(Cart.objects.filter(user = request.user))
#         wishitem = len(Wishlist.objects.filter(user = request.user))
#     # return render(request,"app/home.html",locals())
#     images = [
#             "app/images/banner/b1.jpg",
#             "app/images/banner/b2.jpg",
#             "app/images/banner/b3.jpg",
#             "app/images/banner/b4.jpg",
#             "app/images/banner/b5.jpg",
#         ]
#     return render(request, "app/home.html", {"totalitem": totalitem, "wishitem": wishitem, "images": images})
def home(request):
    totalitem = 0
    wishitem = 0
    
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))

    # Image Data with Captions
    images = [
        {"image": "app/images/banner/b1.jpg", "title": "New Arrivals!", "subtitle": "Get the latest trends now.", "link": "/shop"},
        {"image": "app/images/banner/b2.jpg", "title": "Winter Collection", "subtitle": "Stay warm & stylish!", "link": "/winter"},
        {"image": "app/images/banner/b3.jpg", "title": "Mega Sale 50% Off!", "subtitle": "Don’t miss out.", "link": "/sale"},
        {"image": "app/images/banner/b4.jpg", "title": "Exclusive Footwear", "subtitle": "Step into style!", "link": "/footwear"},
        {"image": "app/images/banner/b5.jpg", "title": "Elegant Accessories", "subtitle": "Complete your look.", "link": "/accessories"},
    ]

    return render(request, "app/home.html", {"totalitem": totalitem, "wishitem": wishitem, "images": images})


@login_required
def about(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    return render(request,"app/about.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    return render(request,"app/contact.html",locals())

@method_decorator(login_required,name="dispatch")
class CategoryView(View):
    def get(self, request,val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            wishitem = len(Wishlist.objects.filter(user = request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name="dispatch")    
class CategoryTitle(View):
    def get(self, request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            wishitem = len(Wishlist.objects.filter(user = request.user))
        return render(request,"app/category.html",locals())    

@method_decorator(login_required,name="dispatch")    
class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        wishlist = None  # Default value if user is anonymous
        totalitem = 0  # Default cart item count
        wishitem  = 0
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user)).exists()
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = len(Wishlist.objects.filter(user = request.user))
        context = {
            "product": product,
            "wishlist": wishlist,
            "totalitem": totalitem
        }
        return render(request, "app/productdetail.html", context)


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            wishitem = len(Wishlist.objects.filter(user = request.user))
        return render(request,"app/customerregistration.html",locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! You have successfully registered")
        else:
            messages.warning(request,"Invalid Input Data")    
        return render(request,"app/customerregistration.html",locals())

@method_decorator(login_required,name="dispatch")
class ProfileView(View):
        def get(self, request):
            form = CustomerProfileForm()
            totalitem = 0
            wishitem=0
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user = request.user))
                wishitem = len(Wishlist.objects.filter(user = request.user))
            return render(request,"app/profile.html",locals())
        def post(self, request):
            form = CustomerProfileForm(request.POST)
            if form.is_valid():
                user = request.user
                name = form.cleaned_data['name']
                locality = form.cleaned_data['locality']
                city = form.cleaned_data['city']
                mobile = form.cleaned_data['mobile']
                state = form.cleaned_data['state']
                zipcode = form.cleaned_data['zipcode']

                reg = Customer(user = user, name = name, locality = locality, city = city,state = state, zipcode = zipcode)
                reg.save()
                messages.success(request,"Congratulations! Profile Save Successfully")
            else:
                messages.warning(request,"Invalid Input Data")    
            return render(request,"app/profile.html",locals())
@login_required       
def address(request):
    add = Customer.objects.filter(user=request.user)     
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))  
        wishitem = len(Wishlist.objects.filter(user = request.user)) 
    return render(request,"app/address.html",locals())

@method_decorator(login_required,name="dispatch")
class updateAddress(View):
    def get(self, request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            wishitem = len(Wishlist.objects.filter(user = request.user))
        return render(request,"app/updateAddress.html",locals())
    def post(self, request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data["name"]
            add.locality = form.cleaned_data["locality"]
            add.city = form.cleaned_data["city"]
            add.mobile = form.cleaned_data["mobile"]
            add.state =  form.cleaned_data["state"]
            add.zipcode = form.cleaned_data["zipcode"]
            add.save()
            messages.success(request,"Congratulations! Profile updated Sucessfully  ")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")        
    
@login_required
def add_to_cart(request):
        user = request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40    
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    return render(request,'app/addtocart.html',locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    product = Wishlist.objects.filter(user = request.user)

    return render(request, 'app/wishlist.html',locals())    

@method_decorator(login_required,name="dispatch")
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user = request.user))
            wishitem = len(Wishlist.objects.filter(user = request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        if not add.exists():
            return redirect("profile") 
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return redirect("cart") 
        famount = sum(p.quantity * p.product.discounted_price for p in cart_items)
        totalamount = int(famount + 40)  # Adding fixed shipping charge
        razoramount = totalamount * 100  # Convert to smallest currency unit
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}

        try:
            payment_response = client.order.create(data=data)
            order_id = payment_response['id']
            order_status = payment_response['status']
        except razorpay.errors.BadRequestError as e:
            print(f"Razorpay Error: {e}")
            return redirect("checkout") 
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        context = {
            "add": add,
            "cart_items": cart_items,
            "totalamount": totalamount,
            "razoramount": razoramount,
            "order_id": order_id
        }
        return render(request, 'app/checkout.html', context)
     
@login_required  
def payment_done(request):
    if not request.user.is_authenticated:
        raise PermissionDenied("You must be logged in to complete the payment.")
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    if not order_id or not payment_id or not cust_id:
        raise PermissionDenied("Required parameters missing.")
    user = request.user
    try:
        customer = Customer.objects.get(id=cust_id)
        payment = Payment.objects.get(razorpay_order_id=order_id)
    except Customer.DoesNotExist:
        raise PermissionDenied("Customer does not exist.")
    except Payment.DoesNotExist:
        raise PermissionDenied("Payment details not found.")
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart_items = Cart.objects.filter(user=user)
    for c in cart_items:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect("orders")

@login_required
def orders(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, "app/orders.html", locals())

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()  

        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40  
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()  

        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40  
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()  

        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40  
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
   

@login_required
def plus_wishlist(request):
    prod_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=prod_id)

    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    return JsonResponse({'action': 'added' if created else 'exists'})

@login_required
def minus_wishlist(request):
    prod_id = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=prod_id)

    deleted, _ = Wishlist.objects.filter(user=request.user, product=product).delete()

    return JsonResponse({'action': 'removed' if deleted else 'not_found'})

@login_required
def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user = request.user))
        wishitem = len(Wishlist.objects.filter(user = request.user))
    product = Product.objects.filter(Q(title__icontains=query))

    return render(request, 'app/search.html',locals())    
