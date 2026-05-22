from django.shortcuts import render,redirect,get_object_or_404
from .models import Stock,Categories,Products,Sales,CreditScheme
from django.contrib.auth import authenticate, login as auth_login, logout
from .forms import CustomUserForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.db.models import Sum
import random

# Create your views here.

@login_required


@login_required
def dashboard(request):

    if request.user.role not in [
        "overall_manager",
        "sales_manager",
        "stock_manager"
    ]:
        return redirect("login")

    # TOTAL PRODUCTS
    total_products = Products.objects.count()

    # TOTAL STOCK ENTRIES
    total_stock = Stock.objects.count()

    # TOTAL SALES
    total_sales = Sales.objects.count()

    # RECENT SALES
    recent_sales = Sales.objects.all().order_by("-id")[:5]

    # LOW STOCK PRODUCTS
    low_stock_products = Products.objects.filter(quantity__lt=5)

    # TOTAL REVENUE REPORT
    total_revenue = Sales.objects.aggregate(
        Sum("total_amount")
    )["total_amount__sum"] or 0

    context = {
        "total_products": total_products,
        "total_stock": total_stock,
        "total_sales": total_sales,
        "recent_sales": recent_sales,
        "low_stock_products": low_stock_products,
        "total_revenue": total_revenue,
    }

    return render(request, "dashboard.html", context)

# VIEW STOCK + ADD PRODUCT
@login_required
@login_required
def viewstock(request):

    if request.user.role not in ["stock_manager", "overall_manager"]:
        return redirect("login")

    products = Products.objects.all()
    categories = Categories.objects.all()

    if request.method == "POST":

        product_id = request.POST.get("product_name")
        quantity = request.POST.get("quantity")

        supplier = request.POST.get("supplier")
        payment_status = request.POST.get("payment_status")

        # DEBUG
        print(product_id)
        print(quantity)
        print(supplier)
        print(payment_status)

        if product_id and quantity:

            product = Products.objects.get(id=product_id)

            quantity = int(quantity)

            # increase product quantity
            product.quantity += quantity
            product.save()

            # SAVE STOCK
            Stock.objects.create(
                product_name=product,
                categories=product.categories,
                quantity=quantity,
                supplier=supplier,
                payment_status=payment_status
            )

        return redirect("viewstock")

    stocks = Stock.objects.all()

    return render(request, "viewstock.html", {
        'stocks': stocks,
        'products': products,
        'categories': categories
    })

##CATEGORIES
@login_required
def categories(request):
    if request.user.role not in ["stock_manager"  ,"overall_manager"]:
        return redirect("login")
    if request.method == "POST":

        payload = request.POST

        categories_name = payload.get('categories_name')

        description = payload.get('description')

        # SAVE CATEGORY
        Categories.objects.create(
            name= categories_name,
            description=description,

        )

        return redirect('viewstock')

    # VIEW CATEGORIES
    categories = Categories.objects.all()

    return render(request, 'categories.html',{"categories": categories})

# EDIT category
@login_required
def edit_category(request, pk):

    category = get_object_or_404(Categories, id=pk)

    if request.method == "POST":

        category.name = request.POST.get("name")
        category.description = request.POST.get("description")

        category.save()

        return redirect("categories")

    context = {
        "item": category,
        "type": "category"
    }

    return render(request, "edit.html", context)

#DELETE CATEGORIES
@login_required
def delete_category(request, pk):

    category = get_object_or_404(Categories, id=pk)

    if request.method == "POST":
        category.delete()
        return redirect("categories")

    context = {
        "item": category,
        "type": "category"
    }

    return render(request, "delete.html", context)


    
##PRODUCTS
@login_required
def products(request):
    if request.user.role not in ["stock_manager"  ,"overall_manager"]:
        return redirect("login")
    if request.method == "POST":

        product_name = request.POST.get('product_name')
        size = request.POST.get('size')
        unit_cost = request.POST.get('unit_cost')
        unit_price = request.POST.get('unit_price')
        quantity = request.POST.get('quantity')

        category_id = request.POST.get('categories')

        category = Categories.objects.get(id=category_id)

        Products.objects.create(
            product_name=product_name,
            size=size,
            unit_cost=unit_cost,
            unit_price=unit_price,
            categories=category,
            quantity = quantity
        )

        return redirect('viewstock')

    # VIEW PRODUCTS
    products = Products.objects.all()

    # VIEW CATEGORIES
    categories = Categories.objects.all()

    return render(request, 'products.html', {
        'products': products,
        'categories': categories
    })


# UPDATE PRODUCT
@login_required
def edit_product(request, pk):

    product = get_object_or_404(Products, id=pk)

    if request.method == "POST":

        product.product_name = request.POST.get("product_name")
        product.size = request.POST.get("size")
        product.unit_cost = request.POST.get("unit_cost")
        product.unit_price = request.POST.get("unit_price")
        product.quantity = request.POST.get("quantity")

        product.save()

        return redirect("products")

    context = {
        "item": product,
        "type": "product"
    }

    return render(request, "edit.html", context)
   
##DELETE PRODUCT 
@login_required
def delete_product(request, pk):

    product = get_object_or_404(Products, id=pk)

    if request.method == "POST":
        product.delete()
        return redirect("products")

    context = {
        "item": product,
        "type": "product"
    }

    return render(request, "delete.html", context)


# ADD SALE

@login_required
def addsale(request):
    if request.user.role not in ["sales_manager" ,"cashier" ,"overall_manager"]:
        return redirect("login")


    products = Products.objects.all()
    categories = Categories.objects.all()

    if request.method == "POST":

        customer = request.POST.get('customer')
        amount_paid = int(request.POST.get('amount_paid'))

        product_ids = request.POST.getlist('product_name')
        category_ids = request.POST.getlist('categories')
        quantities = request.POST.getlist('quantity')

        # UNIQUE RECEIPT NUMBER
        while True:
            receipt_number = random.randint(10000, 99999)

            if not Sales.objects.filter(receipt_number=receipt_number).exists():
                break

        grand_total = 0

        # CALCULATE TOTAL FIRST
        for i in range(len(product_ids)):

            if product_ids[i] and quantities[i]:

                product = Products.objects.get(id=product_ids[i])

                quantity = int(quantities[i])

                total = quantity * product.unit_price

                grand_total += total

        balance = amount_paid - grand_total

        # SAVE SALES
        for i in range(len(product_ids)):

            if product_ids[i] and quantities[i]:
                product = Products.objects.get(id=product_ids[i])
                category = Categories.objects.get(id=category_ids[i])
                quantity = int(quantities[i])
                unit_price = product.unit_price
                total_amount = quantity * unit_price
                Sales.objects.create(
                    customer=customer,
                    product_name=product,
                    categories=category,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_amount=total_amount,
                    amount_paid=amount_paid,
                    balance=balance,
                    receipt=f"Receipt {receipt_number}",
                    receipt_number=receipt_number
                )

        return redirect('receipt', receipt_number=receipt_number)

    return render(request, 'addsale.html', {
        'products': products,
        'categories': categories
    })




# VIEW SALES
@login_required
def viewsales(request):

    sales = Sales.objects.all().order_by('-id')

    return render(request, 'viewsales.html', {
        'sales': sales
    })



# RECEIPT
@login_required
def receipt(request, receipt_number):

    sales = Sales.objects.filter(receipt_number=receipt_number)

    total = 0

    for sale in sales:
        total += int(sale.total_amount)

    return render(request, 'receipt.html', {
        'sales': sales,
        'total': total
    })
##CREDIT SCHEME
@login_required
def creditscheme(request):
    if request.user.role not in ["customer_manager" ,"cashier" , "overall_manager"] :
        return redirect("login")

    products = Products.objects.all()
    categories = Categories.objects.all()

    if request.method == "POST":

        customer_name = request.POST.get("customer_name")
        email = request.POST.get("email")
        nin_number = request.POST.get("nin_number")
        contact = request.POST.get("contact")
        address = request.POST.get("address")

        product_id = request.POST.get("product_name")
        category_id = request.POST.get("categories_name")

        amount_paid = int(request.POST.get("amount_paid"))
        total_amount = int(request.POST.get("total_amount"))

        product = Products.objects.get(id=product_id)
        category = Categories.objects.get(id=category_id)

        CreditScheme.objects.create(
            customer_name=customer_name,
            email=email,
            nin_number=nin_number,
            contact=contact,
            address=address,
            product=product,
            category=category,
            amount_paid=amount_paid,
            total_amount=total_amount
        )

        return redirect("creditscheme")

    customers = CreditScheme.objects.all().order_by("-id")

    context = {
        "customers": customers,
        "products": products,
        "categories": categories
    }

    return render(request, "creditscheme.html", context)

##LOGIN PAGE

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )
        print("username", username)
        print("password", password)
        print("user",user)
        print(user.role)
        if user is not None:

            auth_login(request, user)

            # REDIRECT BASED ON ROLE
            if user.role == "overall_manager":
                return redirect("dashboard")

            elif user.role == "stock_manager":
                return redirect("viewstock")

            elif user.role == "sales_manager":
                return redirect("viewsales")
            
            elif user.role == "cashier":
                return redirect("addsale")

            elif user.role == "customer_manager":
                return redirect("creditscheme")

    return render(request, "login.html")

# REGISTER USER

##REGISTER
@login_required
def register(request):
    if request.user.role not in ["overall_manager"] :
        return redirect("login")
    form = CustomUserForm()

    if request.method == "POST":

        form = CustomUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    context = {
        "form": form
    }

    return render(request, "register.html", context)

@login_required
def logoutuser(request):

    logout(request)

    return redirect("login")

