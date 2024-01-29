from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(User_data)
class User_data(admin.ModelAdmin):
    list_display = ['Name','vendor_id','MobileNo',"email"]

@admin.register(Apointment)
class appointment_data(admin.ModelAdmin):
    list_display = ['customer_name','user',]


admin.site.register(Invoice)
admin.site.register(invoice_data)
admin.site.register(SallonProfile)
admin.site.register(img)
admin.site.register(staff_account_details)

admin.site.register(BusinessAnalysis)



# @admin.register(Service_data)
# class service_data(admin.ModelAdmin):
#     list_display = ["service","service_prise",]

# @admin.register(StaffAttendence)
# class StaffAttendence(admin.ModelAdmin):
#     list_display = ["user"]

# @admin.register(StaffDetails)
# class StaffDetails(admin.ModelAdmin):
#     list_display = ['user','staffname','mobileno']

# @admin.register(CustomerPointTable)
# class CustomerPointTable(admin.ModelAdmin):
#     list_display = ['customer_name','user','service_cost',"cashback_Points"]

# admin.site.register(store_app_service_data)
# admin.site.register(store_invoice_data_service)