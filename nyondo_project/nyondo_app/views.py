from django.shortcuts import render

# Create your views here.
def viewstock(request):
    return render(request , "viewstock.html")

def updatestock(request):
    return render(request , "updatestock.html")

def creditscheme(request):
    return render(request , "creditscheme.html")

def editscheme(request):
    return render(request , "editscheme.html")

def viewsale(request):
    return render(request , "viewsale.html")

def addsale(request):
    return render(request , "addsale.html")

def reciept(request):
    return render(request , "reciept.html")