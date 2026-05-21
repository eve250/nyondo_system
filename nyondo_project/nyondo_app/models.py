from django.db import models

# Create your models here.

class Categories (models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(null=True , max_length=50)
  def __str__(self):
    return self.name
  

class Products (models.Model):
  product_name = models.CharField(max_length=50 ,default=0 )
  size = models.CharField(max_length= 20)
  unit_cost = models.IntegerField()
  unit_price = models.IntegerField()
  quantity = models.IntegerField()
  categories = models.ForeignKey(Categories, on_delete= models.CASCADE, )
  def __str__(self):
    return self.product_name

class Sales (models.Model):
  customer = models.CharField(max_length=50,null=True)
  product_name = models.ForeignKey(Products,on_delete=models.CASCADE)
  categories = models.ForeignKey(Categories ,on_delete=models.CASCADE)
  quantity = models.IntegerField()
  unit_price = models.IntegerField()
  total_amount = models.CharField(max_length=50)
  date = models.DateField(auto_now_add=True)
  amount_paid = models.IntegerField()
  balance = models.DecimalField(max_digits=10 , decimal_places=3)
  receipt =models.CharField(max_length= 100)
  receipt_number = models.IntegerField(unique=True)
  def __str__(self):
    return self.customer
 


class Stock (models.Model):
  product_name= models.ForeignKey(Products , max_length=50,on_delete=models.CASCADE)
  quantity = models.IntegerField(null=False)
  categories = models.ForeignKey(Categories ,on_delete=models.CASCADE)
  supplier = models.CharField(max_length=50,null=False)
  payment_status = models.CharField(null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.quantity




