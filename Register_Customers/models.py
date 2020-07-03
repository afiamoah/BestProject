from django.db import models
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.http import HttpResponse,request,JsonResponse
# Create your models here.
class CustomerDetails(models.Model):
    Name = models.CharField(max_length=200,   null=True)
    Firstname = models.CharField(max_length=200, null=True)
    Lastname = models.CharField(max_length=200, null=True)
    Location = models.CharField(max_length=510, null=True)
    Telephone = models.CharField(max_length=200, null=True)
    Username = models.EmailField(max_length=200, null=True)
    password = models.CharField(max_length=200,  null=True)
    Mobile = models.CharField(max_length=200, null=True)
    Mobile = models.CharField(max_length=200, null=True)
    Email = models.CharField(max_length=200, null=True)




class  Products (models.Model):
        Product = models.CharField(max_length=200, null=True)
        Desc = models.CharField(max_length=300, null=True)
        Quantity = models.IntegerField(null=True)
        Price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
        Image = models.ImageField(upload_to='Images', null=True)
        Brand = models.CharField(max_length=200,   null=True)
        Availability= models.CharField(max_length=200, default="Available", null=True)



class   Orders(models.Model):
        Payments= "Pending"                                                  
        Delivery  = "Pending"

        Customer_Id =  models.CharField(max_length=200, null=True, default="ID")
        Customer =  models.CharField(max_length=200, null=True, default="Customer")
        Location =  models.CharField(max_length=200, null=True, default="location")
        Telephone = models.CharField(max_length=200, null=True) 
        Product =   models.CharField(max_length=200, null=True)
        quantity =  models.IntegerField(null=True)  
        Price   =  models.DecimalField(max_digits=10, decimal_places=2, null=True)
        Total= models.DecimalField(max_digits=10, decimal_places=2, null=True) 
        Final_Amount= models.DecimalField(max_digits=10, decimal_places=2, null=True)
        Invoice = models.CharField(max_length=200, null=True)
        Onsubmitted =   models.CharField(max_length=200, null=True,  default="Pending")
        Payment = models.CharField(max_length=200, default=Payments )
        Delivery = models.CharField(max_length=200, default=Delivery)
        Date =   models.DateField(auto_now_add=True, null=True)
        Mobile_Number = models.CharField(max_length=50, null=True, default="0241209304")
        Reg_Name = models.CharField(max_length=50, null=True, default="name")
        Momo_CODE = models.CharField(max_length=50, null=True, default="273312")
        DateTimeField=models.DateTimeField(auto_now_add=True, null=True)

class   OrderItems(models.Model):
        Payments= "Pending"
        Delivery  = "pending"

        Customer_Id =  models.CharField(max_length=50, null=True, default="ID")
        Customer =  models.CharField(max_length=50, null=True, default="Customer")
        Location =  models.CharField(max_length=50, null=True, default="location")
        Telephone = models.CharField(max_length=50, null=True, default="+233") 
        Product=   models.CharField(max_length=50, null=True)
        quantity =  models.IntegerField(null=True)  
        Price   =  models.DecimalField(max_digits=10, decimal_places=2, null=True)
        Total= models.DecimalField(max_digits=10, decimal_places=2, null=True) 
        Final_Amount= models.DecimalField(max_digits=10, decimal_places=5, null=True)
        Invoice =   models.CharField(max_length=50, null=True)
        Onsubmitted =   models.CharField(max_length=50, null=True)
        Payment = models.CharField(max_length=200, default=Payments )
        Delivery = models.CharField(max_length=200, default=Delivery)
        Date =   models.DateField(auto_now_add=True, null=True)
        Mobile_Number = models.CharField(max_length=200, null=True, default="+233")
        Reg_Name = models.CharField(max_length=200, null=True, default="Agent Name")

class   Payment(models.Model):
        Customer =  models.CharField(max_length=200, null=True )
        Location =  models.CharField(max_length=200, null=True)
        Telephone = models.CharField(max_length=200, null=True) 
        Amount_Paid = models.CharField(max_length=200, null=True) 
        Payments = models.CharField(max_length=200, null=True,  default="Pending")
        Delivery = models.CharField(max_length=200, null=True,  default="Pending")
        Date =   models.DateField(auto_now_add=True, null=True) 
        DateTimeField=models.DateTimeField(auto_now_add=True, null=True)
        Invoice = models.CharField(max_length=200, null=True)
        Onsubmitted =   models.CharField(max_length=200, null=True)

# def SendSignal(request, sender, instance, **kwargs):
#         signs ="new order available"
        
             

# post_save.connect(SendSignal,sender=Payment) 