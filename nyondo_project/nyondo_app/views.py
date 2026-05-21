from django.shortcuts import render,redirect,get_object_or_404
from .models import Stock,Categories,Products,Sales,CreditScheme
import random
# Create your views here.
# LOGIN
def login(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

# VIEW STOCK + ADD PRODUCT

def viewstock(request):

    products = Products.objects.all()
    categories = Categories.objects.all()

    if request.method == "POST":

        product_id = request.POST.get("product_name")
        quantity = int(request.POST.get("quantity"))

        product = Products.objects.get(id=product_id)

        # increase product quantity
        product.quantity += quantity
        product.save()

        Stock.objects.create(
            product_name=product,
            categories=product.categories,
            quantity=quantity,
            supplier=request.POST.get("supplier"),
            payment_status=request.POST.get("payment_status")
        )

        return redirect("viewstock")

    stocks = Stock.objects.all()

    return render(request, "viewstock.html", {
        'stocks': stocks,
        'products': products,
        'categories': categories
    })

def categories(request):
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
    

def products(request):

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
def updatestock(request, pk):
        # GET PRODUCT
    product = get_object_or_404(Products, id=pk)

    # UPDATE PRODUCT
    if request.method == "POST":
        product.product_name = request.POST.get('name')
        product.size = request.POST.get('size')
        product.unit_cost = request.POST.get('unit_cost')
        product.unit_price = request.POST.get('unit_price')
        product.save()
        return redirect('viewstock')
    return render(request, 'updateproduct.html', {
        'product': product
    })
   


# EDIT CREDIT CUSTOMER
def editscheme(request):
    return render(request, 'editscheme.html', )

# ADD SALE



def addsale(request):

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

def viewsales(request):

    sales = Sales.objects.all().order_by('-id')

    return render(request, 'viewsales.html', {
        'sales': sales
    })



# RECEIPT
def receipt(request, receipt_number):

    sales = Sales.objects.filter(receipt_number=receipt_number)

    total = 0

    for sale in sales:
        total += int(sale.total_amount)

    return render(request, 'receipt.html', {
        'sales': sales,
        'total': total
    })
   
def creditscheme(request):

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




