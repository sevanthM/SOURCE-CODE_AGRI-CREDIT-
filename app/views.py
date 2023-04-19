from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from .models import *
import random
import threading
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
import shortuuid
from django.db.models import Count
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
class customerEmailThread(threading.Thread): #This thread class is used to send email to the customers, call this thread class wherever you want to send the email
    def __init__(self, subject, message, recipient_list):
        self.subject = subject
        self.message = message
        self.emailfrom=settings.EMAIL_HOST_USER
        self.recipient_list = recipient_list
        # self.html_content = html_content
        threading.Thread.__init__(self)
    def run (self):
        try:
            msg=EmailMultiAlternatives(
                    self.subject,
                    self.message,
                    self.emailfrom,
                    self.recipient_list,
                    )
            msg.attach_alternative( self.message, "text/html")
            a=msg.send()
            print("------------------",a)
        except Exception as e:
            pass
class registerview(View):
    template="register.html"
    def get(self,request):
        return render(request,self.template)
    def post(self,request):
        fullname=request.POST.get("fullname")   #getting fullname.email,password1 and password2 from frontend registration form
        # latname=request.POST.get("lname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        password1=request.POST.get("password")
        password2=request.POST.get("rpassword")
        role=request.POST.get("exampleRadios")


        user=registertable.objects.filter(email=email) 
        # user1=registertable.objects.filter(email=email)
        if user.exists():#checking if email is exists or not, if its exists returning message 
            messages.info(request,"Email already Registered, Please login")
        # elif user1.exists():#checking if email is registered as vendor, if yes returning message
        #     messages.info(request,"Email already Registered as vendor, Please use another Email Id")
        else:
            if password1==password2:
                if role=="farmer":
                    s = shortuuid.ShortUUID(alphabet="0123456789")
                    bid = s.random(length=5)
                    farmid="FARM"+str(bid)
                    registertable.objects.create(full_name=fullname,email=email,password=make_password(password2),is_farmer=True,phone_no=phone,farmerid=farmid)#creating the customer using fullname,email,password and is_vendor false because registering as customer
                else:
                    s = shortuuid.ShortUUID(alphabet="0123456789")
                    bid = s.random(length=5)
                    aggreid="AGGR"+str(bid)
                    registertable.objects.create(full_name=fullname,email=email,password=make_password(password2),is_aggregator=True,phone_no=phone,aggreid=aggreid)#creating the customer using fullname,email,password and is_vendor false because registering as customer


                messages.success(request,"Registered Successfully")
                return redirect("login")
            else:
                messages.error(request,"Password didn't match")
        return redirect("register") 
class loginview(View):
    template="login.html"
    def get(self,request):
        return render(request,self.template)
    def post(self,request,*args,**kwargs):
        email=request.POST.get("email")
        password=request.POST.get("password")
        print(email,password)
        try:
            user=registertable.objects.filter(email=email)
            print(user)
            if user.exists():
                authuser=authenticate(request,username=email,password=password)
        
                if authuser is not None:
                    login(request,authuser)
                    messages.success(request,"Logged in Successfully")
                    return redirect("home")
                else:
                    messages.error(request,"Invalid Credentials")
                    return redirect("login")
            else:
                messages.error(request,"Invalid Credentials")
                return redirect("login")


        except Exception as e:
            print(e)
            messages.error(request,"Invalid Credentials")
            return redirect("login")
class profileview(LoginRequiredMixin,View):
    template_name="profile.html"
    login_url="/login"


    def get(self,request):
        return render(request,self.template_name)
    def post(self, request):
        print(request.POST)
        fullname=request.POST.get("name",request.user.full_name)
        email=request.POST.get("email",request.user.email)
        phone=request.POST.get("phone",request.user.phone_no)
        address=request.POST.get("address",request.user.address)
        pincode=request.POST.get("pincode",request.user.pincode)
        registertable.objects.filter(email=request.user.email).update(full_name=fullname,email=email,phone_no=phone,address=address,pincode=pincode)
        messages.success(request,"Profile Updated Successfully")
        return redirect("profile")
def logout_request(request):
    logout(request)
    return redirect("/")
class homeview(View):
    template="home.html"
    def get(self,request):
        # product = get_object_or_404(fertilizersmodel, id=1)
        # print(product)
        return render(request,self.template)
    def post(self, request):
        # print(request.POST)
        # name=request.POST.get("name",request.user.full_name)
        # email=request.POST.get("email",request.user.email)
        # phone=request.POST.get("phone",request.user.phone_no)
        if request.user.is_authenticated:
            name=request.user.full_name
            email=request.user.email
            phone=request.user.phone_no
        else:
            name=request.POST.get("name")
            email=request.POST.get("email")
            phone=request.POST.get("phone")
        subject=request.POST.get("subject")
        query=request.POST.get("query")
        querymodels.objects.create(name=name,email=email,phone=phone,subject=subject,query=query)
        subject1="Query Sumbitted"
        message1=f"Hello {name}, Our Expert will get back to you soon with suitable suggestion for your query \n Thank You"
        customerEmailThread(subject1, message1, [email]).start()


        messages.success(request,"Thank you, your query recorded successfully, our expert will get back to you soon with suggestion")
        return redirect("home")
class sellproduce(LoginRequiredMixin,View):
    template_name="sell.html"   
    login_url="/login"


    def get(self,request):
        return render(request,self.template_name)
    def post(self, request):
        print(request.POST)
        print(request.FILES)
        name=request.POST.get("name")
        description=request.POST.get("description")
        category=request.POST.get("category")
        price=request.POST.get("price")
        lprice=request.POST.get("lprice")
        image=request.FILES["image"]
        
        if category=="fertilizer":
            if request.user.is_farmer:
                fertilizersmodel.objects.create(user=request.user,name=name,descr=description,image=image,farmer=True,price=price)
            else:
                fertilizersmodel.objects.create(user=request.user,name=name,descr=description,image=image,aggregator=True,price=price)


        elif category=="machinary":
            if request.user.is_farmer:
                machinarymodel.objects.create(user=request.user,leaseprice=lprice,name=name,descr=description,image=image,farmer=True,price=price)
            else:
                machinarymodel.objects.create(user=request.user,leaseprice=lprice,name=name,descr=description,image=image,aggregator=True,price=price)


        elif category=="pesticides":
            if request.user.is_farmer:
                pesticidesmodel.objects.create(user=request.user,name=name,descr=description,image=image,farmer=True,price=price)
            else:
                pesticidesmodel.objects.create(user=request.user,name=name,descr=description,image=image,aggregator=True,price=price)
        elif category=="pesticides":
            if request.user.is_farmer:
                pesticidesmodel.objects.create(user=request.user,name=name,descr=description,image=image,farmer=True,price=price)
            else:
                pesticidesmodel.objects.create(user=request.user,name=name,descr=description,image=image,aggregator=True,price=price)
        messages.success(request,"Your Product added successfully")
        return redirect("sell")
class aggrefertileview(View):
    template="aggrfertile.html"
    def get(self,request):
        products=fertilizersmodel.objects.filter(aggregator=True)
        context={
            "products":products,
            "id":True
        }
        return render(request,self.template,context)
class farmfertileview(View):
    template="aggrfertile.html"
    def get(self,request):
        products=fertilizersmodel.objects.filter(farmer=True)
        context={
            "products":products,
            "id1":True
        }
        return render(request,self.template,context)
class aggremachinaryview(View):
    template="aggremachinary.html"
    def get(self,request):
        products=machinarymodel.objects.filter(aggregator=True)
        context={
            "products":products,
            "id":True
        }
        return render(request,self.template,context)
    
class farmmachinaryview(View):
    template="aggremachinary.html"
    def get(self,request):
        products=machinarymodel.objects.filter(farmer=True)
        context={
            "products":products,
            "id1":True
        }
        return render(request,self.template,context)


class aggrepestiview(View):
    template="pestiaggre.html"
    def get(self,request):
        products=pesticidesmodel.objects.filter(aggregator=True)
        context={
            "products":products,
            "id":True
        }
        return render(request,self.template,context)
    
class farmpestiview(View):
    template="pestiaggre.html"
    def get(self,request):
        products=pesticidesmodel.objects.filter(farmer=True)
        context={
            "products":products,
            "id1":True
        }
        return render(request,self.template,context)
    
class aggreseedview(View):
    template="aggreseeds.html"
    def get(self,request):
        products=seedsmodel.objects.filter(aggregator=True)
        context={
            "products":products,
            "id":True
        }
        return render(request,self.template,context)
    
class farmseedview(View):
    template="aggreseeds.html"
    def get(self,request):
        products=seedsmodel.objects.filter(farmer=True)
        context={
            "products":products,
            "id1":True
        }
        return render(request,self.template,context)   


class detailedfertview(LoginRequiredMixin,View):
    login_url="/login"
    template="detailedpro.html"
    def get(self, request, str):
        product=fertilizersmodel.objects.get(id=int(str))
        products=fertilizersmodel.objects.all()
      
        context={
            "product":product,
"products":products,
"id1": True
        }
       
        return render(request,self.template,context)
class detailedmachview(LoginRequiredMixin,View):
    login_url="/login"
    template="machinarydetail.html"
    def get(self, request, str):
        product=machinarymodel.objects.get(id=int(str))
        products=machinarymodel.objects.all()
        context={
            "product":product,
"products":products,
"id2": True
        }
        return render(request,self.template,context)
class detailedpestview(LoginRequiredMixin,View):
    login_url="/login"
    template="detailedpro.html"
    def get(self, request, str):
        product=pesticidesmodel.objects.get(id=int(str))
        products=pesticidesmodel.objects.all()
        context={
            "product":product,
"products":products,
"id3": True
        }
        return render(request,self.template,context)
class detailedseedview(LoginRequiredMixin,View):
    login_url="/login"
    template="detailedpro.html"
    def get(self, request, str):
        product=seedsmodel.objects.get(id=int(str))
        products=seedsmodel.objects.all()
        context={
            "product":product,
"products":products,
"id3": True
        }
        return render(request,self.template,context)    
    
    
class ordersview(LoginRequiredMixin,View):
    template_name="orders.html"
    login_url="/login"
    def get(self, request):
        orders=orderstable.objects.filter(user=request.user)
        context={
            "orders":orders
        }
        return render(request,self.template_name,context)
    
class productsview(LoginRequiredMixin,View):
    template_name="products.html"
    login_url="/login"
    def get(self, request):
        productss=[]
        # products={}
        products1=fertilizersmodel.objects.filter(user=request.user)
        products2=machinarymodel.objects.filter(user=request.user)
        products3=pesticidesmodel.objects.filter(user=request.user)
        products4=seedsmodel.objects.filter(user=request.user)
       
        from itertools import chain
        result_list = list(chain(products1, products2, products3,products4))
        print("------------",result_list)
        for i in result_list:
            print(i.price)
        for product in products1:
            products={}
            products["name"]=product.name
            products["image"]=product.image.url
            products["price"]=product.price
            products["category"]="Fertilizer"
            products["date"]=product.created_at


            productss.append(products)
        for product in products2:
            products={}
            products["name"]=product.name
            products["image"]=product.image.url
            products["price"]=product.price
            products["lease"]=product.leaseprice
            products["date"]=product.created_at
            products["category"]="Machinary"
            productss.append(products)
        for product in products3:
            products={}
            products["name"]=product.name
            products["image"]=product.image.url
            products["price"]=product.price
            products["date"]=product.created_at
            products["category"]="Pesticide"
            productss.append(products)
        for product in products4:
            products={}
            products["name"]=product.name
            products["image"]=product.image.url
            products["price"]=product.price
            products["date"]=product.created_at
            products["category"]="Seed"
            productss.append(products)    
        # print(productss)
        context={
            "products":productss
        }
     
        return render(request,self.template_name,context)
