from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here
class registertable(AbstractUser,PermissionsMixin):
    full_name=models.CharField(max_length=200,null=True,blank=True)
    phone_no=models.CharField(max_length=13,null=True,blank=True)
    username = models.CharField(
        max_length=50, blank=False, null=True,verbose_name="user name")
    email = models.EmailField(_('email address'), unique=True,blank=True,null=True)
    # vend_email = models.EmailField(_('email address'), unique=True,blank=True,null=True)
    address=models.TextField(null=True,blank=True)
    pincode=models.CharField(max_length=6,null=True,blank=True)

    farmerid=models.CharField(max_length=10,null=True,blank=True)

    aggreid=models.CharField(max_length=10,null=True,blank=True)

    photo=models.FileField(upload_to='customer', null=True, blank=True)
    is_farmer=models.BooleanField(default=False)
    is_aggregator=models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username",'full_name','phone_no']
    
#     class Meta:
#         verbose_name_plural = "Customer_vendor_table"
#         verbose_name = "Customer_vendor_table"
class fertilizersmodel(models.Model):
    user=models.ForeignKey(registertable,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=300,null=True,blank=True)
    descr=models.TextField(null=True,blank=True)
    image=models.FileField(upload_to="fertilizers",null=True,blank=True)
    farmer=models.BooleanField(default=False)
    aggregator=models.BooleanField(default=True)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Fertilizers"
class machinarymodel(models.Model):
    user=models.ForeignKey(registertable,on_delete=models.CASCADE,null=True,blank=True)

    name=models.CharField(max_length=300,null=True,blank=True)
    descr=models.TextField(null=True,blank=True)
    image=models.FileField(upload_to="machinary",null=True,blank=True)
    farmer=models.BooleanField(default=False)
    aggregator=models.BooleanField(default=True)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    leaseprice=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Machinaries"
class pesticidesmodel(models.Model):
    user=models.ForeignKey(registertable,on_delete=models.CASCADE,null=True,blank=True)

    name=models.CharField(max_length=300,null=True,blank=True)
    descr=models.TextField(null=True,blank=True)
    image=models.FileField(upload_to="machinary",null=True,blank=True)
    farmer=models.BooleanField(default=False)
    aggregator=models.BooleanField(default=True)
    price=models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Pesticides"
STATUS_CHOICES = (
    ("Pending","Pending"),
    ("Shipped","Shipped"),
    ("Delivered","Delivered")
    )

class orderstable(models.Model):
    user=models.ForeignKey(registertable,on_delete=models.CASCADE,null=True,blank=True)
    orderid=models.CharField(max_length=100,null=True,blank=True)
    paymentid=models.CharField(max_length=100,null=True,blank=True)
    productname=models.CharField(max_length=300,null=True,blank=True)
    price=models.CharField(max_length=20,null=True,blank=True)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=20,
        default="Pending", null=True,blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.orderid
    class Meta:
        verbose_name_plural = "Orders"
class  querymodels(models.Model):
    name=models.CharField(max_length=256,null=True,blank=True)
    email=models.EmailField(max_length=256,null=True,blank=True)
    phone=models.CharField(max_length=20,null=True,blank=True)
    subject=models.CharField(max_length=256,null=True,blank=True)
    query=models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.subject
    class Meta:
        verbose_name_plural = "User Queries"

