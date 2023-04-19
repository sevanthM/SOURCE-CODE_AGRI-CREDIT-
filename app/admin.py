from django.contrib import admin
from .models import *
from django.utils.html import format_html
class registertableadmin(admin.ModelAdmin):
    list_display=["customerid","full_name","email","phone_no","is_farmer","is_aggregator","created"]
    def customerid(self, obj):
        if obj.farmerid:
            return obj.farmerid
        else:
            return obj.aggreid
class fertilizersadmin(admin.ModelAdmin):
    list_display=["id","name","imagee","farmer","aggregator","price","created_at","updated_at"]
    def imagee(self, obj):
        if obj.image:
            return format_html('<a href="{}"><img src="{}" width="{}" height="{}"/></a>'.format(obj.image.url,obj.image.url, "100", "100"))
        
class machinaryadmin(admin.ModelAdmin):
    list_display=["id","name","imagee","farmer","aggregator","price","leaseprice","created_at","updated_at"]
    def imagee(self, obj):
        if obj.image:
            return format_html('<a href="{}"><img src="{}" width="{}" height="{}"/></a>'.format(obj.image.url,obj.image.url, "100", "100"))
        
class ordersadmin(admin.ModelAdmin):
    list_display=["id","user","orderid","paymentid","productname","price","status","created_at"]
    list_editable=["status"]
class queryadmin(admin.ModelAdmin):
    list_display=["id","name","email","phone","subject","query","created_at"]
admin.site.register(registertable,registertableadmin)
admin.site.register(fertilizersmodel,fertilizersadmin)
admin.site.register(machinarymodel,machinaryadmin)
admin.site.register(pesticidesmodel,fertilizersadmin)
admin.site.register(orderstable,ordersadmin)
admin.site.register(querymodels,queryadmin)

# Register your models here.
