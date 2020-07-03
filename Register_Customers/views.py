from django.shortcuts import render, redirect
from django.http import HttpResponse,request,JsonResponse
from .models import Products,Orders,Payment,CustomerDetails
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
import random
from .forms import   AddProducts, MyCarts,PickProducts
from django.db.models import Sum
from datetime import date
from io import BytesIO
from xhtml2pdf import pisa   
from django.template.loader import get_template
from django.views import View
from django.utils.decorators import method_decorator
import requests 
from django.db.models import Q 
from django.core.mail import send_mail


def  error_404_view(request, exception):
     return render(request, '404.html')

# Create your views here.
def HomePage(request):
    return render(request, 'index.html')

def Customer(request):
     return render(request, 'MyCustomers.html')

def Time(request):
    return render(request, 'Orders.html')



def UserRegister(request):       
    if request.method == 'POST':

        Firstname = request.POST.get("firstname")
        Lastname = request.POST.get("lastname")
        Location = request.POST.get("location")
        Telephone = request.POST.get("telephone")
        Email = request.POST.get("email")
        Password = request.POST.get("password")
        confirm = request.POST.get("confirm")
        SaveMessage ="Record Saved Successfully"
        PassCheck = "SIGNUP ERROR  (Password Already Exist )"
        ConfirmCheck = " SIGNUP ERROR  (Password differ from Confirm Password)"
        Usercheck = "SIGNUP ERROR  (Username Already Exist )"
        ErrorMessage =""
        Myname=Firstname+" "+Lastname

        if Password != confirm:
           messages.info(request, ConfirmCheck)
           return redirect('/customer')
        else:    
            if User.objects.filter(username=Email).exists():
              messages.info(request, Usercheck)
              return redirect('/customer')
            elif User.objects.filter(password=Password).exists():
              messages.info(request, PassCheck)
              return redirect('/customer')
            else:
                
                SaveCustomer = CustomerDetails(Location=Location, Telephone=Telephone, Username=Email, password=Password, Name=Myname, Mobile=Telephone,Firstname=Firstname,Lastname=Lastname,Email=Email)
                SaveCustomer.save()
                
                user = User.objects.create_user(first_name=Firstname, last_name=Lastname,  email=Email, username=Email, password=Password)
                user.save()
                return redirect('/insert')
               

    else:
          return redirect('/customer')
          
def UserLogIn(request):
    if request.method =='POST':
       
        Username = request.POST['username']
        Password = request.POST['password']

        User = auth.authenticate(username=Username,password=Password)
        if User is not None:
               login(request, User)
               if request.user.is_superuser:
                  return redirect('/Dashboard')
               else:
                  Email= request.POST.get('username')
                  password = request.POST.get('password')
                  Details = CustomerDetails.objects.get(Username=Email)  
                  return render(request, 'profile.html', {"user":Details})
                
        else:
             messages.info(request,'Wrong Username or Password Please Check')
             return redirect('/Login')
    else:
     
        return render(request,'Login.html')

def LogOut(request):
    logout(request)

    return redirect('/Login')

def ViewCustomer(request):
    if request.method =='POST':
     Username = request.POST['search']
     user = CustomerDetails.objects.filter(Username=Username)  
     return render(request, 'ViewCustomer.html', {"User":user})
    else:
        return render(request, 'ViewCustomer.html', {})


@login_required(login_url='Login')
def GetProducts(request):
     if request.method == 'POST':
         Search = request.POST['search'] 
         products = Products.objects.filter(Product__icontains=Search)
         return render(request, 'AllProducts.html', {'products':products})
     else:
          products = Products.objects.all().order_by('pk')  
          return render(request, 'AllProducts.html', {'products':products})

@login_required(login_url='Login')
def  AddProductData(request,  id=0):
     if request.method == 'GET':
          if id  == 0:
            data = AddProducts()
          else:
              pro= Products.objects.get(pk=id)
              data = AddProducts(instance=pro)
          return render(request, 'AddProducts.html', {'Products':data})  
     else:
          if id == 0:
             data = AddProducts(request.POST) 
             data = AddProducts(request.POST, request.FILES)
             if data.is_valid():      
                      data.save() 
                  
          else:
               pro= Products.objects.get(pk=id)
               data = AddProducts(request.POST, request.FILES, instance=pro)
          if data.is_valid():      
              data.save()  
          return redirect('/Products/')

@login_required(login_url='Login')
def DeleteProduct(request, id):
    Delete = Products.objects.get(pk=id) 
    if request.method == 'POST':
       Delete.delete()
       return redirect('/Products/')
    return render(request, 'DeleteProduct.html', {'Products':Delete})

def OrderPicker(request, id): 
    firstname =  Products.objects.get(pk=id)
    # ListItems = MyCarts(instance=firstname)
    if request.method == 'POST':
        #   ListItems = MyCarts()
          Search = request.POST.get('search', False)
          products = Products.objects.filter(Product__icontains=Search)
          return render(request, 'GetCart.html', {"products":products, "name":firstname})
          

    return render(request, 'Display.html', {"name":firstname})

def SaveOrders(request) :
    if request.method == 'POST':
        Telephone=request.POST.get("id_Telephone")
        Product=request.POST.get("item")
        Price=request.POST.get("id_Price")
        Quantity=request.POST.get("id_quantity")
        Total=request.POST.get("tprice") 
        if CustomerDetails.objects.filter(Telephone=Telephone).exists():
           SaveCartItems = Orders(Telephone=Telephone,  Product=Product, Price=Price,quantity=Quantity, Total=Total)
           SaveCartItems.save() 
           return redirect('/choose/') 
        else:
            SignUpError= "Please SignUp and use Your Telephone Number as Order ID" 
            return render(request, 'SignUpErrors.html', {"Errors":SignUpError})
    else:
          return render(request, 'Display.html')  

def Options(request):
    return render(request, 'CartOption.html')


def Cart(request):
    products = Products.objects.all()
    if request.method == 'POST':
          ListItems = MyCarts()
          Search = request.POST.get('search', False)
          products = Products.objects.filter(Product__icontains=Search)
          return render(request, 'Display.html', {"products":products, "List":ListItems})
          
    else:
          products = Products.objects.all()
          ListItems = MyCarts() 
          return render(request, 'Display.html', {"products":products, "List":ListItems})
    return render(request, 'Display.html', {"products":products})

def CartViewer(request): 
    if request.method == 'POST':
      ID = request.POST.get('Unique')
      dates = request.POST.get('date')    
      Carts = Orders.objects.filter(Telephone=ID, Date=dates, Onsubmitted="Pending") 
      Amount = Orders.objects.filter(Telephone=ID, Date=dates, Onsubmitted="Pending").aggregate(total=Sum('Total')) 
      customerdetails = CustomerDetails.objects.get(Telephone=ID)
      Pay = {
      "Recipient_Number":"0241209304",
      "Momo_Pay_Code":"273312",
      "Reg_Name":"Frank Gina Company Limited",
      }
      
    return render(request, 'OriginalCart.html', {"Carts":Carts, "Amount":Amount['total'], "ID":ID, "Date":dates,  "Customer":customerdetails, "Momo":Pay})


def Sales(request):
    return render(request, 'Display.html')

def GetCustomerInfo(request):
    return render(request, 'OriginalCart.html')




def DeleteCart(request, id):
    Fetch= Orders.objects.get(pk=id)
    if request.method == 'POST':
       Fetch= Orders.objects.get(pk=id)
       Fetch.delete()  
       return redirect('/delete/') 
       ID = request.POST.get('order')  
       Carts = Orders.objects.filter(Telephone=ID)
       Amount = Orders.objects.filter(Telephone=ID).aggregate(total=Sum('Total'))
       return render(request, 'OriginalCart.html', {"Carts":Carts, "Amount":Amount['total'], "ID":ID})
    return render(request, 'DeleteOrders.html', {"Carts":Fetch})

def DeleteView(request):
    messages.info(request,"Item Removed From Orders")

    return render(request, 'DeleteOrders.html')


def  OrderUpdate(request):
     if request.method =='POST':
        ID = request.POST.get('telephone')
        Invoice = request.POST.get('Invoice')
        dates = request.POST.get('date')
        Customer = request.POST.get('firstname')
        Telephone = request.POST.get('telephone')   
        Location = request.POST.get('location')
        Final_Amount= request.POST.get('Paid')
        Mobile_Number = request.POST.get('reg_telephone')
        Reg_Name = "Frank Gina Company Limited"

        Orders.objects.filter(Telephone=ID, Date=dates, Onsubmitted="Pending").update(Invoice=Invoice)
        Orders.objects.filter(Telephone=ID, Date=dates, Onsubmitted="Pending").update(Onsubmitted="Submitted")

        Orders.objects.filter(Invoice=Invoice).update(Final_Amount=Final_Amount, Customer=Customer, Location=Location, Mobile_Number=Mobile_Number, Reg_Name=Reg_Name)
        messages.info(request,"Orders submitted successfully please wait for payment confirmation")
        dashboard = Payment(Customer=Customer,  Location= Location, Telephone=Telephone, Amount_Paid=Final_Amount, Invoice=Invoice, Onsubmitted="Submitted")
        dashboard.save() 
        Sender = "Frank Gina(NEW ORDERS)"
        Sender_Email = request.POST['email']
        Message = "New Orders submitted please check for Payment confirmation and Delivery"          
        send_mail(
         Sender,
          Message,
         Sender_Email,
         ['afiamoah90@gmail.com','manieadudonkor@gmail.com'],
         fail_silently=False
            )      
     return render(request, 'OrderPrinter.html', {"Invoice":Invoice,"Telephone":ID})

@login_required(login_url='Login')
def  Dashboard(request):
      if request.user.is_authenticated:
         SubmitOrders =  Payment.objects.filter(Date=date.today())  
         if request.method =='POST':
            dates =  request.POST.get('getdate')
            ID =  request.POST.get('search')
         
            if ID == "":
                 SubmitOrders = Payment.objects.filter(Date=dates)
            else:
                SubmitOrders = Payment.objects.filter(Telephone=ID, Date=dates)
            return render(request, 'table.html', {"SubmitOrders":SubmitOrders}) 

         else:

             SubmitOrders = Payment.objects.filter(Date=date.today())
       
       
         return render(request, 'table.html', {"SubmitOrders":SubmitOrders})
      return render(request, 'table.html', {"SubmitOrders":SubmitOrders})



def  ConfirmOrders(request, id):
     Confirm = Payment.objects.get(pk=id)
     if request.method == 'POST':
        return render(request, 'Confirm.html',  {"Confirm":Confirm})
        

     return render(request, 'Confirm.html',  {"Confirm":Confirm})


def  Confirmation(request):
     if request.method == 'POST':
        ID = request.POST.get('id')
        Amount = request.POST.get('paid')
        payment = request.POST.get('payment')
        delivery = request.POST.get('delivery')  
        
        Payment.objects.filter(pk=ID).update(Payments=payment, Delivery=delivery, Amount_Paid=Amount) 
        return render(request, 'Success.html')



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None  
    

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'GET':
          ID= request.GET['telephone']          
          Pmkey= request.GET['id']  
          Invoice = request.GET['Invoice']  
          data = Orders.objects.filter(Invoice=Invoice) 
          paymentdetails = Payment.objects.get(pk=Pmkey)
          customerdetails = CustomerDetails.objects.get(Telephone=ID)
          Amount = Orders.objects.filter(Invoice=Invoice).aggregate(total=Sum('Total'))
          pdf = render_to_pdf('invoice.html', {"data":data, "Paymentdetails":paymentdetails, "Customer":customerdetails,"Amount":Amount['total']})
        return HttpResponse(pdf, content_type='application/pdf')


class OrdersPdf(View):
      def get(self, request, *args, **kwargs):
        if request.method == 'GET':
          ID= request.GET['telephone']           
          Invoice = request.GET['Invoice']  
          data = Orders.objects.filter(Invoice=Invoice) 
          paymentdetails = Payment.objects.get(Invoice=Invoice)
          customerdetails = CustomerDetails.objects.get(Telephone=ID)
          Amount = Orders.objects.filter(Invoice=Invoice).aggregate(total=Sum('Total'))
          pdf = render_to_pdf('invoice.html', {"data":data, "Paymentdetails":paymentdetails, "Customer":customerdetails,"Amount":Amount['total']})
        return HttpResponse(pdf, content_type='application/pdf')


def OrderPrinter(requests):
     
    return render(request, 'OrderPrinter.html')

def Success(request):

    return render(request, 'Success.html')

    
def Print(request):
    if request.method == 'GET':
       Pmkey= request.GET['ids']  
       paymentdetails = Payment.objects.get(pk=Pmkey)                                     

       return render(request, 'Print.html', {"Confirm": paymentdetails})
    return render(request, 'Print.html')


def SMS(request):
    if request.method == 'GET':
       Pmkey= request.GET['ids']  
       paymentdetails = Payment.objects.get(pk=Pmkey)  
       return render(request, 'SMS.html', {"Confirm": paymentdetails})
    else:        
         return render(request, 'SMS.html')

def SendSMS(request):
    if request.method == 'POST':
       Telephone=request.POST.get('telephone')
       SenderID=request.POST.get('sender')
       Message=request.POST.get('message')
       Amount=request.POST.get('paid')
       Invoice=request.POST.get('Invoice')

       AvailableMessage="Payment Confirmed for  Orders with Invoice Number"
       UnavailableMessage="Payment Confirmed for  Orders with Invoice Number"

       Endpoint="https://apps.mnotify.net/smsapi?key=Xjqdjwn9RyM0wmWtLE3iBJyk1&to=%s&msg=%s&sender_id=%s" % (Telephone,Message,SenderID)
           
       return render(request, 'smsrecieved.html', {"data":Endpoint})
    return render(request, 'smsrecieved.html')
     

def SMSGet(request):

    return render(request, 'smsrecieved.html')


def Profile(request):
    if request.method == 'POST':
        ID=request.POST.get('id') 
        Firstname = request.POST.get('firstname') 
        Lastname=request.POST.get('lastname') 
        Location=request.POST.get('location') 
        Email=request.POST.get('email') 
        Mobile=request.POST.get('mobile') 
        Name=Firstname+""+Lastname
        CustomerDetails.objects.filter(pk=ID).update(Location=Location, Mobile=Mobile, Firstname=Firstname, Lastname=Lastname, Name=Name,Email=Email)
        messages.info(request,"Profile Updated Successfully")  
        Context={
            'id':ID,
            'Firstname':Firstname,
            'Lastname': Lastname,
            'Location':Location,
            'Email':Email,
            'Mobile':Mobile,
        }
        return render(request, 'profile.html', {"user":Context})
    return render(request, 'profile.html')

def ViewMyOrders(request):
    if request.method == 'GET':
       Pmkey= request.GET['telephone'] 
       Myorders =  Payment.objects.filter(Telephone=Pmkey) 
       MyCustomer = CustomerDetails.objects.get(Telephone=Pmkey)
       return render(request, 'CustomerOrders.html', {"Confirm":Myorders, "Customer":MyCustomer})
    else:
         if request.method == 'POST':      
          dates =  request.POST.get('getdate')
          ID =  request.POST.get('search')
          List =  Payment.objects.filter(Telephone=ID,Date=dates) 
          return render(request, 'CustomerOrders.html', {"Confirm":List})    
    return render(request, 'CustomerOrders.html', {"Confirm":Myorders, "Customer":MyCustomer})                              

def ReprintOrders(request, id):
    Confirm = Payment.objects.get(pk=id)
    if request.method == 'POST':
        return render(request, 'RePrint.html',  {"Confirm":Confirm})

    return render(request, 'RePrint.html',  {"Confirm":Confirm})

@login_required(login_url='Login')
def ManageCustomers(request):
    MyCustomers = CustomerDetails.objects.all()
    if request.method == 'POST':
        Myname = request.POST['search']
        MyCustomers = CustomerDetails.objects.filter(Name__icontains=Myname)
        return render(request, 'ManageCustomer.html',  {"MyCustomers":MyCustomers})

    return render(request, 'ManageCustomer.html',  {"MyCustomers":MyCustomers})

def EditCustomer(request, id):
    MyCustomers = CustomerDetails.objects.get(pk=id)
    if request.method == 'POST':
        return render(request, 'RePrint.html',  {"user": MyCustomers})

    return render(request, 'Profiles.html',  {"user": MyCustomers})



def EditProfile(request):
    if request.method == 'POST':
        ID=request.POST.get('id') 
        Firstname = request.POST.get('firstname') 
        Lastname=request.POST.get('lastname') 
        Location=request.POST.get('location') 
        Email=request.POST.get('email') 
        Mobile=request.POST.get('mobile') 
        Username=request.POST.get('username') 
        Password=request.POST.get('password') 
        Name=Firstname+"  "+Lastname
        CustomerDetails.objects.filter(pk=ID).update(Location=Location, Mobile=Mobile, Firstname=Firstname, Lastname=Lastname, Name=Name,Email=Email)
        messages.info(request,"Profile Updated Successfully")  
        Context={
            'id':ID,
            'Firstname':Firstname,
            'Lastname': Lastname,
            'Location':Location,
            'Email':Email,
            'Mobile':Mobile,
            'Username':Username,
            'password':Password,
        }
        return render(request, 'Profiles.html', {"user":Context})
    return render(request, 'Profiles.html')


def ContactUS(request):
    if request.method == 'POST':
        Sender = request.POST['name']
        Sender_Email = request.POST['email']
        Message = request.POST['message']     
        Sent = "message sent  Successfully"
        send_mail(
         Sender,
          Message,
         Sender_Email,
         ['afiamoah90@gmail.com'],
         fail_silently=False
            )
        return render(request, 'contactus.html', {"Sent":Sent})
    else:
         return render(request, 'contactus.html')

def GetCart(request,id):
    firstname =  Products.objects.get(pk=id)

    return render(request, 'GetCart.html', {"name":firstname})
