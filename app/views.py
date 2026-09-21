from django.shortcuts import render,redirect
from .models import *
from .forms import UserForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache
from django.db.models import Q
import razorpay
from django.views.decorators.csrf import csrf_exempt
import random
from django.core.mail import send_mail


from django.http import HttpResponse

# def pay_amount(req):
#     return HttpResponse("PAYMENT WORKING")

# Create your views here.
def landing(req):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        category = Category.objects.all()
        product = Product.objects.filter(category__id=1).prefetch_related('productsize_set')
        # print(Product.objects.filter(category_id=1))
        return render(req,'landing.html',{'info':user_data,'category':category,'product':product})
    else:
        category = Category.objects.all()
        product = Product.objects.filter(category_id=1).prefetch_related('productsize_set')
        return render(req,'landing.html',{'category':category,'product':product})
    
    
# def shopbycategory(req):
#     product = Product.objects.all()
#     return render(req, 'shopbycategory.html', {'product': product})

from django.db.models import F

def shopbycategory(req):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        sort = req.GET.get('sort')

        product = Product.objects.all()

        if sort == "az":
            product = product.order_by("name")

        elif sort == "za":
            product = product.order_by("-name")

        elif sort == "low":
            product = product.order_by("price")

        elif sort == "high":
            product = product.order_by("-price")

        return render(req, 'shopbycategory.html', {
            'product': product,
            'selected_sort': sort,
            'info':user_data
        })
    else:
        sort = req.GET.get('sort')

        product = Product.objects.all()

        if sort == "az":
            product = product.order_by("name")

        elif sort == "za":
            product = product.order_by("-name")

        elif sort == "low":
            product = product.order_by("price")

        elif sort == "high":
            product = product.order_by("-price")

        return render(req, 'shopbycategory.html', {
            'product': product,
            'selected_sort': sort,
        })


def shopbycollection(req):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        joggers = Product.objects.filter(category__name="Joggers")
        jackets = Product.objects.filter(category__name="Jackets")
        hoodies = Product.objects.filter(category__name="Hoodies")
        oversizetshirt = Product.objects.filter(category__name="Oversized T-shirt")

        return render(req, "shopbycollection.html", {
            "joggers": joggers,
            "jackets": jackets,
            "hoodies": hoodies,
            "oversizetshirt":oversizetshirt,
            "info":user_data
        })
    else:
        joggers = Product.objects.filter(category__name="Joggers")
        jackets = Product.objects.filter(category__name="Jackets")
        hoodies = Product.objects.filter(category__name="Hoodies")
        oversizetshirt = Product.objects.filter(category__name="Oversized T-shirt")

        return render(req, "shopbycollection.html", {
            "joggers": joggers,
            "jackets": jackets,
            "hoodies": hoodies,
            "oversizetshirt":oversizetshirt,
        })


def aboutus(req):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        return render(req,'aboutus.html',{'info':user_data})
    else:
        return render(req,'aboutus.html')

def fitguide(req):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        return render(req,'fitguide.html',{'info':user_data})
    else:
        return render(req,'fitguide.html')


def policy(req):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        return render(req,'policy.html',{'info':user_data})
    else:
        return render(req,'policy.html')

def forget_password(req):
    return render(req,'forget_password.html')

@never_cache
def new_pass(req):
    if req.method == 'POST':
        e = req.POST.get('email')
        user = User.objects.filter(email=e)
        if not user:
            msg = 'please enter valid email'
            return render(req,'forget_password.html',{'msg':msg})
        else:
            otp=random.randint(111111,999999)
            req.session['otp']=otp
            req.session['email']=e
            send_mail(
            "otp from django server",
            f'your forgot password otp is {otp}',
            "from@example.com",
            [e],
            fail_silently=False,
        )
        return render(req,'new_pass.html')
    else:
        return redirect('landing')
    
@never_cache    
def reset(req):
    if req.method == 'POST':
        e_otp = req.POST.get('otp')   
        n_pass = req.POST.get('password')   
        c_pass = req.POST.get('cpassword')   
        otp = req.session.get('otp')
        print(type(otp),type(e_otp))
        if int(otp) == int(e_otp):
            if n_pass == c_pass :
                e = req.session.get('email')
                userdata = User.objects.get(email=e)
                userdata.password = n_pass
                userdata.save()
                msg = 'password reset succesfully'
                return render(req,'login.html',{'msg':msg})
            else:
                msg1 = 'new_password and confirm password not matched'
                return render(req,'new_pass.html',{'msg1':msg1})
        else:
            msg = 'Invalid otp'
            return render(req,'new_pass.html',{'msg':msg})

    
def category_products(req, id):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        category = Category.objects.get(id=id)
        products = Product.objects.filter(category=category).prefetch_related('productsize_set')

        return render(req, 'category_products.html', {
            'category': category,
            'products': products,
            'info':user_data
        })
    else:
        category = Category.objects.get(id=id)
        products = Product.objects.filter(category=category).prefetch_related('productsize_set')

        return render(req, 'category_products.html', {
            'category': category,
            'products': products,
            # 'info':user_data
        })





def product_detail(req, id):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        product = Product.objects.get(id=id)
        images = ProductImage.objects.filter(product=product)
        sizes = ProductSize.objects.filter(product=product, stock__gt=0)

        if req.method == "POST":
            selected_size = req.POST.get("size")

            if not selected_size:
                return render(req,"product_detail.html", {
                    "product": product,
                    "images": images,
                    "sizes": sizes,
                    "error": "Please select size",
                    'info':user_data
                })

            cart = req.session.get("cart", [])

            # 🔥 DUPLICATE CHECK
            already_exists = False
            for item in cart:
                if item['id'] == product.id and item['size'] == selected_size:
                    already_exists = True
                    break

            # ✅ only add if not exists
            if not already_exists:
                cart.append({
                    'id': product.id,
                    "name": product.name,
                    "price": product.price,
                    "size": selected_size,
                    "image": product.main_image.url
                })

            req.session["cart"] = cart

            return redirect("cart_page")

        return render(req, 'product_detail.html', {
            'product': product,
            'images': images,
            'sizes': sizes,
            'info':user_data
        })
    else:
        return redirect('login')


def cart_page(req):
    cart = req.session.get('cart', [])

    total = 0
    for item in cart:
        total += int(item['price'])

    return render(req, 'cartpay.html', {
        'cart': cart,
        'total': total
    })

@never_cache
def remove_from_cart(req):
    if req.method == "POST":
        product_id = req.POST.get('id')
        size = req.POST.get('size')

        cart = req.session.get('cart', [])
        new_cart = []

        for item in cart:
            if 'id' in item:   # 👈 safety
                if not (str(item['id']) == str(product_id) and item['size'] == size):
                    new_cart.append(item)

        req.session['cart'] = new_cart

    return redirect('cart_page')

@never_cache
def pay_amount(req):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')
        user = User.objects.get(id=user_id)

        if req.method == 'POST':
            product_id = req.POST.get('product_id')
            product_size = req.POST.get('product_size')
            product_price = req.POST.get('product_price')
            quantity = req.POST.get('quantity', 1)

            print("Product ID:", product_id)

            if not product_id:
                return redirect('cart_page')

            try:
                product_info = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return redirect('cart_page')

            # ✅ total amount calculation (MODEL MATCHED)
            price = int(product_price)
            qty = int(quantity)
            total_amount = price * qty
            amount = total_amount * 100  # Razorpay paise

            # ✅ SIR KI API KEY (UNCHANGED)
            client = razorpay.Client(auth=("rzp_test_pr99iascS1WRtU", "UTDIzPGwICnAssu3Q3lk7zUi"))

            data = {
                "amount": amount,
                "currency": "INR",
                "receipt": "order_rcptid_11"
            }

            payment = client.order.create(data=data)
            print(payment)

            # ✅ ORDER SAVE (FULL MODEL MATCHED)
            Order.objects.create(
                user=user,
                product=product_info,
                size=product_size,
                quantity=qty,
                price=price,
                total_amount=total_amount,
                order_id=payment.get('id'),
                payment_status=False
            )

            return render(req, 'payment.html', {
                'payment': payment,
                'amount': total_amount,
                'product_info': product_info
            })

        return redirect('cart_page')

    return redirect('login')


@csrf_exempt        
def pay_status(req):
    print(req.POST)
    rpi = req.POST.get('razorpay_payment_id')
    roi = req.POST.get('razorpay_order_id')
    rps = req.POST.get('razorpay_signature')
    old_roi = Order.objects.get(order_id=roi)
    old_roi.razorpay_payment_id = rpi
    old_roi.payment_status = True
    old_roi.razorpay_signature=rps
    old_roi.save()
    return render(req,'success.html')

     
@never_cache
def success(req):
    return render(req,'success.html')   


@never_cache    
def userprofile(req,pk):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')
        user = User.objects.get(id=user_id)

        return render(req,'userprofile.html',{'data':user})
    
    
def profile_data(req,pk):
    if 'user_id' in req.session:
        user=User.objects.get(id=pk)
        return render(req,'userprofile.html',{'data':user,'my_profile':True})
    
def my_orders(req, pk):
    if 'user_id' in req.session:
        user = User.objects.get(id=pk)

        # ✅ user ke saare orders lao
        orders = Order.objects.filter(user=user,payment_status=True)

        return render(req,'userprofile.html',{
            'data':user,
            'my_orders':True,
            'orders':orders
        })
    else:
        return redirect('login')


def account(req):
    return render(req,'landing.html',{'account':True})

def signup(req):
    form = UserForm()
    return render(req,'signup.html',{'form': form})

def signupdata(req):
    if req.method == "POST":
        form = UserForm(req.POST, req.FILES)        
        if form.is_valid():
            form.save()
            return redirect("login")     
    else:         
        form = UserForm()
    return render(req,"signup.html",{"form":form})

def login(req):
    return render(req,'login.html')


def logindata(req):
    if req.method == 'POST':
        e=req.POST.get('email')
        p=req.POST.get('password')
        if e=='admin@gmail.com' and p=='Az@12345':
            a_data = User.objects.get(email=e)
            req.session['a_data'] = a_data.id   # ✅ sirf ID store karo
            return redirect('admindashboard')
        else:
            user = User.objects.filter(email=e).first()
            if user:
                if p == user.password:
                    req.session['user_id'] = user.id
                    return redirect('landing')
                else:
                    return render(req,'login.html',{'msg':'Email and password not match'})
            else:
                messages.warning(req,'User does not exist')
                return redirect('login')         
    return render(req ,'login.html')

@never_cache
def admindashboard(req):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)

        query = req.GET.get('q')   # 👈 search input

        products = Product.objects.all()

        if query:
            products = products.filter(name__icontains=query)

        return render(req, 'admindashboard.html', {
            'data': a_data,
            'products': products,
            'query': query
        })
    else:
        return redirect('login')
    
def logout(req):
    if 'user_id' in req.session:
        req.session.flush()
        return redirect('login')
    elif 'a_data' in req.session:
        req.session.flush()
        return redirect('login')
    else:
        return redirect('login')    
    
def add_category(req):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)
        return render(req,'admindashboard.html',{'data':a_data ,'add_category':True})
    else:
        return redirect('login') 
    
def save_category(req):
    if 'a_data' in req.session:
        if req.method=='POST':
            cn = req.POST.get('category_name')
            ci = req.FILES.get('category_image')
            ctgr = Category.objects.filter(name=cn)
            if ctgr:
                messages.warning(req,'Category already exist')
                a_data = req.session.get('a_data')
                return render(req,'admindashboard.html',{'data':a_data ,'add_category':True})
            else:
                Category.objects.create(name=cn,image=ci)
                messages.success(req,'Category Created')
                a_data = req.session.get('a_data')
                return render(req,'admindashboard.html',{'data':a_data ,'add_category':True})
    else:
        return redirect('login')    
    
     
def show_category(req):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)
        all_ctgr = Category.objects.all()
        return render(req,'admindashboard.html',{'data':a_data ,'show_category':True,'all_ctgr':all_ctgr})
    else:
        return redirect('login')
    
def edit_category(req, pk):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)

        old_ctgr = Category.objects.get(id=pk)
        all_ctgr = Category.objects.all()

        return render(req,'admindashboard.html',{
            'data':a_data,
            'all_ctgr':all_ctgr,
            'old_ctgr':old_ctgr,
            'show_category':True
        })
    else:
        return redirect('login')
    
def update_category(req, pk):
    if 'a_data' in req.session:
        if req.method == "POST":
            ctgr = Category.objects.get(id=pk)

            ctgr.name = req.POST.get('name')

            if 'image' in req.FILES:
                ctgr.image = req.FILES['image']

            ctgr.save()

            return redirect('show_category')
    else:
        return redirect('login')    

def delete_category(req, pk):
    if 'a_data' in req.session:
        ctgr = Category.objects.get(id=pk)
        ctgr.delete()
        return redirect('show_category')
    else:
        return redirect('login')

def show_users(req):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)
        all_users = User.objects.all()
        return render(req,'admindashboard.html',{'data':a_data ,'show_users':True,'all_users':all_users})
    else:
        return redirect('login')

def show_orders(req):

    if 'a_data' in req.session:

        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)

        all_orders = Order.objects.select_related('user', 'product').all().order_by('-created_at')

        return render(
            req,
            'admindashboard.html',
            {
                'data': a_data,
                'show_orders': True,
                'all_orders': all_orders
            }
        )

    else:
        return redirect('login')    


def add_product(req):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)
        all_ctgr = Category.objects.all()
        return render(req,'admindashboard.html',{'data':a_data ,'add_product':True,'all_ctgr':all_ctgr})
    else:
        return redirect('login')
    
    
def save_product(req):
     if 'a_data' in req.session:
        if req.method=='POST':
            pn = req.POST.get('product_name')
            pp = req.POST.get('product_price')
            op = req.POST.get('old_price')
            pd = req.POST.get('product_description')
            pi = req.FILES.get('main_image')
            pc = req.POST.get('category')
            category_obj = Category.objects.get(id=pc)
            p_name = Product.objects.filter(name=pn)
            if p_name:
                messages.warning(req,'Product already exist')
                a_data = req.session.get('a_data')
                all_ctgr=Category.objects.all()
                return render(req,'admindashboard.html',{'data':a_data ,'add_product':True,'all_ctgr':all_ctgr})
            else:
                Product.objects.create(name=pn,price=pp,old_price=op,description=pd,category=category_obj,main_image=pi)
                messages.success(req,'Product Created')
                a_data = req.session.get('a_data')
                all_ctgr=Category.objects.all()
                return render(req,'admindashboard.html',{'data':a_data ,'add_product':True,'all_ctgr':all_ctgr})
        else:
            return redirect('login')    

def show_product(req):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)

        all_prdct = Product.objects.all()

        return render(req,'admindashboard.html',{
            'data':a_data,
            'show_product':True,
            'all_prdct':all_prdct
        })
    else:
        return redirect('login')
    
def edit_product(req, pk):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)

        old_product = Product.objects.get(id=pk)
        all_prdct = Product.objects.all()
        all_ctgr = Category.objects.all()

        return render(req,'admindashboard.html',{
            'data':a_data,
            'show_product':True,
            'all_prdct':all_prdct,
            'old_product':old_product,
            'all_ctgr':all_ctgr
        })
    else:
        return redirect('login')

def update_product(req, pk):
    if 'a_data' in req.session:
        if req.method == "POST":
            prd = Product.objects.get(id=pk)

            prd.name = req.POST.get('name')
            prd.price = req.POST.get('price')

            cat_id = req.POST.get('category')
            prd.category = Category.objects.get(id=cat_id)

            if 'main_image' in req.FILES:
                prd.main_image = req.FILES['main_image']

            prd.save()

            # ✅ NEW CODE (yaha paste kar)
            sizes = req.POST.getlist('sizes')
            prd.productsize_set.all().delete()

            for s in sizes:
                stock = req.POST.get(f'stock_{s}')
                
                ProductSize.objects.create(
                    product=prd,
                    size=s,
                    stock=stock if stock else 0
                )

            return redirect('show_product')

def delete_product(req, pk):
    if 'a_data' in req.session:
        prd = Product.objects.get(id=pk)
        prd.delete()
        return redirect('show_product')
    else:
        return redirect('login')



def add_product_image(req):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)

        all_prdct = Product.objects.all()

        return render(req,'admindashboard.html',{
            'data':a_data,
            'add_product_image':True,
            'all_prdct':all_prdct
        })
    else:
        return redirect('login')


def save_product_image(req):
    if 'a_data' in req.session:
        if req.method == 'POST':

            pn = req.POST.get('product_name')
            image = req.FILES.get('product_image')   # ✅ single file

            if not image:
                messages.warning(req, "Please select an image")
                return redirect('add_product_image')

            product_obj = get_object_or_404(Product, id=pn)

            ProductImage.objects.create(
                product=product_obj,
                image=image
            )

            messages.success(req, "Image Uploaded Successfully")

            return redirect('add_product_image')   # ✅ refresh form

    return redirect('login')
    

def show_product_image(req):
    pass

def add_product_size(req):
    if 'a_data' in req.session:
        user_id = req.session.get('a_data')
        a_data = User.objects.get(id=user_id)

        all_prdct = Product.objects.all()

        return render(req,'admindashboard.html',{
            'data':a_data,
            'add_product_size':True,
            'all_prdct':all_prdct
        })
    else:
        return redirect('login')

def save_product_size(req):
    if 'a_data' in req.session:
        if req.method == 'POST':

            product_id = req.POST.get('product')
            size = req.POST.get('size')
            stock = req.POST.get('stock')

            product_obj = get_object_or_404(Product, id=product_id)

            # 🔥 check duplicate (same product + size)
            if ProductSize.objects.filter(product=product_obj, size=size).exists():
                messages.warning(req, "This size already exists for this product")
            else:
                ProductSize.objects.create(
                    product=product_obj,
                    size=size,
                    stock=stock
                )
                messages.success(req, "Size Added Successfully")

        return redirect('add_product_size')

    return redirect('login')

def search(req):
    if 'user_id' in req.session:
        user_id = req.session.get('user_id')   # ✔ already id hai
        user_data = User.objects.get(id=user_id)
        # return render(req,'aboutus.html',)
        query = req.GET.get("q")

        products = Product.objects.all()

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(category__name__icontains=query)
            )

        return render(req, "search.html", {
            "product": products,
            "query": query,
            'info':user_data
        })
    else:
        query = req.GET.get("q")

        products = Product.objects.all()

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(category__name__icontains=query)
            )

        return render(req, "search.html", {
            "product": products,
            "query": query,
        })


# def search_data(req):
#     if 'user_id' in req.session:
#         u_id=req.session.get('user_id')
#         emp_data = User.objects.get(id=u_id)
#         if req.method == 'POST':
#             s = req.POST.get('search')
#             # all_query = Query.objects.filter(Email=emp_data.Email,Query=s)
#             # all_query = Query.objects.filter(Email=emp_data.Email,Query = s,Departments=s)
#             # all_query = Query.objects.filter(Email__icontains=emp_data.Email,Query__icontains = s)
#             # all_query = Query.objects.filter(Email=emp_data.Email,Query__icontains = s)
#             # all_query = Query.objects.filter(Email=emp_data.Email,Query__icontains = s,Dept__icontains = s)
#             # return render(req,'empdashboard.html',{'data':emp_data,'all_query':all_query,'s':s,'all_q':True})
#             # all_query = Query.objects.filter(Email=emp_data.Email and (Q(Query__icontains = s) | Q(Dept__icontains = s)))
#             all_query = Query.objects.filter(Email=emp_data.Email).filter(Q(Query__icontains=s) | Q(Dept__icontains=s))
#             print(all_query)
#             return render(req,'empdashboard.html',{'data':emp_data,'all_query':all_query,'s':s,'all_q':True})
#         else:
#             e_id = req.session.get('emp_id')
#             emp_data = Employee.objects.get(id=e_id)
#             all_query = Query.objects.filter(Email=emp_data.Email)
#             return render(req,'empdashboard.html',{'data':emp_data,'all_q':True,'all_query':all_query})
#     else:
#         return redirect('login')

def bag(req):
    return render(req,'landing.html',{'bag':True})

def otc(req):
    return render(req,'otc.html')

