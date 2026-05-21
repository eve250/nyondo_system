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
  quantity = models.IntegerField(null=False,default=0)
  categories = models.ForeignKey(Categories ,on_delete=models.CASCADE)
  supplier = models.CharField(max_length=50,null=False)
  payment_status = models.CharField(null=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
     return str(self.quantity)

class CreditScheme(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    category = models.ForeignKey( Categories, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    total_amount = models.IntegerField()
    balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    nin_number = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        self.balance = self.total_amount - self.amount_paid
        super().save(*args, **kwargs)
    def __str__(self):
        return self.customer_name


