from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from app.models import Slider, banner_area, Main_category, Product, Category, Orders, OrdersItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Max, Min, Sum
from cart.cart import Cart


def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    slider = Slider.objects.all().order_by('-id')[0:3]
    banners = banner_area.objects.all().order_by('-id')[0:3]
    main_category = Main_category.objects.all().order_by('id')
    product = Product.objects.filter(section__name="Top Deals Of The Day")
    products = Product.objects.filter(section__name="Products")

    context = {
        'slider': slider,
        'banners': banners,
        'main_category': main_category,
        'product': product,
        'products': products,
    }
    return render(request, 'Main/home.html', context)


def PRODUCT_DETAIL(request, slug):
    product = Product.objects.filter(slug=slug)

    main_category = Main_category.objects.all().order_by('id')

    if product.exists():
        product = Product.objects.get(slug=slug)
    else:
        return redirect('404')

    context = {
        'product': product,
        'main_category': main_category,
    }
    return render(request, 'product/product_detail.html', context)


def Error404(request):
    main_category = Main_category.objects.all().order_by('id')
    context = {
        'main_category': main_category,
    }
    return render(request, 'errors/404.html', context)


def REGISTRATER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already exists')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exists')
            return redirect('login')
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'accounts/login')


def LOGIN(request):
    main_category = Main_category.objects.all().order_by('id')
    context = {
        'main_category': main_category,
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email and password are invalid !')
            return redirect('login')

    return render(request, 'accounts/login', context)


@login_required(login_url='login')
def PROFILE(request):
    return render(request, 'profile/profile.html')


def PROFILE_UPDATE(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'your profile is successfully updated!')

    return redirect('profile')


def LOGOUT(request):
    logout(request)
    return redirect('home')


def ABOUT(request):
    main_category = Main_category.objects.all().order_by('id')
    context = {
        'main_category': main_category,
    }
    return render(request, 'Main/about.html', context)


def CONTACT(request):
    main_category = Main_category.objects.all().order_by('id')
    context = {
        'main_category': main_category,
    }
    return render(request, 'Main/contact.html', context)


def PRODUCT(request):
    category = Category.objects.all()
    main_category = Main_category.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte=Int_FilterPrice)
    else:
        product = Product.objects.all()
    context = {
        'category': category,
        'product': product,
        'count': Product.objects.count(),  # for count the product
        'main_category': main_category,
        'min_price': min_price,
        'max_price': max_price,
        'FilterPrice': FilterPrice,
    }
    return render(request, 'product/product.html', context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    if len(brands) > 0:
        allProducts = allProducts.filter(Brand__id__in=brands).distinct()

    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})


def SEARCH(request):
    query = request.GET['query']
    all_product = Product.objects.filter(Tags__icontains=query)
    category = Category.objects.all()
    main_category = Main_category.objects.all()
    context = {
        'main_category': main_category,
        'category': category,
        'count': Product.objects.count(),  # for count the product
        'all_product': all_product,
    }
    return render(request, 'product/search_product.html', context)


def MAIN_CATEGORY(request):
    product = Product.objects.all()
    category = Category.objects.all()
    main_category = Main_category.objects.all()
    context = {
        'main_category': main_category,
        'category': category,
        'count': Product.objects.count(),  # for count the product
        'product': product,
    }
    return render(request, 'product/Product_cat.html', context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)

    coupon = None
    valid_coupon = None
    invalid_coupon = None
    if request.method == "GET":
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon_Code.objects.get(code=coupon_code)
                valid_coupon = "Are applicable are current order"
            except:
                invalid_coupon = "Invalid Coupon Code"

    context = {
        'packing_cost': packing_cost,
        'tax': tax,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url="/accounts/login/")
def CheckOut(request):
    coupon_discount = None
    if request.method == "POST":
        coupon_discount = request.POST.get('coupon_discount')
    cart = request.session.get('cart')

    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    tax_and_packing_cost = (packing_cost + tax)
    context = {
        'tax_and_packing_cost': tax_and_packing_cost,
        'coupon_discount': coupon_discount,
    }
    return render(request, 'Check_out/Check_out.html', context)


@login_required(login_url="/accounts/login/")
def PLACE_ORDER(request):
    if request.method == "POST":
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        address = request.POST.get('address')
        state = request.POST.get('state')
        postcode = request.POST.get('postcode')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        order_notes = request.POST.get('order_notes')
        total = request.POST.get('amt')

        order = Orders(
            user=user,
            firstname=firstname,
            lastname=lastname,
            address=address,
            state=state,
            postcode=postcode,
            phone=phone_number,
            email=email,
            addition_info=order_notes,
            PayableAmount=total,


        )
        order.save()
        for i in cart:
            a = (int(cart[i]['quantity']))
            b = (int(cart[i]['price']))
            total = a*b
            item = OrdersItem(
                orders=order,
                product=cart[i]['product_name'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                amount=total,
            )
            item.save()

    return render(request, 'placeorder/placeorder.html')
