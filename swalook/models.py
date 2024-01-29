from django.db import models
from django.contrib.auth.models import User
import datetime as dt
from django.core import validators
# Create your models here.
import uuid
class img(models.Model):
    img = models.ImageField(upload_to="logo")

class staff_account_details(models.Model):
    user     =  models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    username =  models.CharField(max_length=1000)
    staffname =  models.CharField(max_length=1000)
    password =  models.CharField(max_length=1000)
    # billing_permission = models.BooleanField()
    # appointment_permission = models.BooleanField()
    # inventory_permission = models.BooleanField()
    # business_permission = models.BooleanField()

    def __str__(self) -> str:
        return str(self.user)


class User_data(models.Model):   # model instance for store signup objects
    id                 = models.UUIDField    (    default=uuid.uuid4,           primary_key=True,  editable=False)
    Name               = models.CharField    (    max_length=1000)
    MobileNo           = models.CharField    (    max_length=10,                null=True,         blank=True)
    email              = models.EmailField   (    null=True,                    blank=True,)
    Password           = models.CharField    (    max_length=1000,)
    invoice_number     = models.IntegerField (    default=0,       null=True,   editable=True) # generated invoice count of each user
    date_time          = models.DateTimeField(    auto_now_add=False,           null=True)
    vendor_id          = models.CharField    (    null=False,                   max_length=6) # id of vendor [note that vendor name and id are not same]
    ip                 = models.CharField    (    max_length=200,               null=True,         blank=True)
    dev_limit          = models.IntegerField () # device limit
    gst_number         = models.CharField    (    max_length=20,                null=True,         blank=True) # device limit
    number_of_staff    = models.IntegerField (    default=0)
    s_gst_percent      = models.CharField    (    max_length=30)
    c_gst_percent      = models.CharField    (    max_length=30)
    current_billslno   = models.CharField    (    max_length=50)
    appointment_no     = models.IntegerField ( default=0,       null=True,   editable=True) # generated invoice count of each user


    def __str__(self):
        return str(self.Name)

class Client_service_data(models.Model):
    vendor_name        = models.ForeignKey   (   User,on_delete=models.CASCADE, null=True)
    Name               = models.CharField    (    max_length=50,)
    Address            = models.CharField    (    max_length=200,null=True,         blank=True)
    Mobileno           = models.CharField    (    max_length=10,null=True,               blank=True)
    email              = models.CharField    (    max_length=50,null=True,                      blank=True)
    service_catg_name  = models.CharField    (    max_length=100,)
    date_time          = models.DateTimeField(    auto_now_add=False ,          null=True)
    prise              = models.DecimalField (    max_digits=100,       decimal_places=2,  null=True,  blank=True)
    service_by         = models.CharField    (    max_length=40,)

    def __str__(self):
        return str(self.Name)


class Invoice(Client_service_data): # model instance for store invoice objects


    slno          = models.CharField      (max_length=50,     null=True,      blank=True)
    s_gst         = models.DecimalField   (null=True,      blank=True,     decimal_places=2, max_digits=100)
    c_gst         = models.DecimalField   (null=True,      blank=True,     decimal_places=2, max_digits=100)
    gst_number    = models.CharField      (max_length=20,  blank=True,     null=True) # device limit
    Discont       = models.DecimalField   (null=True,      blank=True,     decimal_places=2, max_digits=100)
    total         = models.DecimalField   (null=True,      blank=True,     decimal_places=2, max_digits=100)
    subtotal      = models.DecimalField   (null=True,      blank=True,     decimal_places=2, max_digits=100)
    total_prise              = models.DecimalField (default=0,    max_digits=100,       decimal_places=2,  null=True,  blank=True)
    total_tax         = models.DecimalField   (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    total_discount        = models.DecimalField   (null=True,      blank=True,     decimal_places=2, max_digits=100,default=0)

    total_quantity       = models.IntegerField(default=0)
    total_cgst       = models.DecimalField   (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    total_sgst      = models.DecimalField   (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)


    grand_total   = models.DecimalField   (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    s_gst_percent = models.CharField      (                 max_length=30)
    c_gst_percent = models.CharField      (             max_length=30)
    vendorname    = models.CharField      (        max_length=30)
    check_value   = models.CharField      (max_length=30,null=True,blank=True)
    date_field   = models.DateField()

    def __str__(self):
        return str(self.vendor_name)


class invoice_data(models.Model):

    Name               = models.CharField    (    max_length=50,)
    Address            = models.CharField    (    max_length=200,null=True,         blank=True)
    Mobileno           = models.CharField    (    max_length=10,null=True,               blank=True)
    email              = models.CharField    (    max_length=50,null=True,                      blank=True)
    service_catg_name  = models.CharField    (    max_length=100,)

    total_prise              = models.DecimalField (default=0,    max_digits=100,       decimal_places=2,  null=True,  blank=True)
    service_by         = models.CharField    (    max_length=40,)
    slno          = models.CharField      (max_length=50,     null=True,      blank=True)
    total_tax         = models.DecimalField   (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    total_discount        = models.DecimalField   (null=True,      blank=True,     decimal_places=2, max_digits=100,default=0)
    gst_number    = models.CharField      (max_length=20,  blank=True,     null=True) # device limit
    total_quantity       = models.IntegerField(default=0)
    total_cgst       = models.DecimalField   (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    total_sgst      = models.DecimalField   (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)



    grand_total   = models.DecimalField   (default=0,null=True,      blank=True,     decimal_places=2, max_digits=100)
    s_gst_percent = models.CharField      (                 max_length=30)
    c_gst_percent = models.CharField      (             max_length=30)
    vendorname    = models.CharField      (        max_length=30)
    check_value   = models.CharField      (max_length=30,null=True,blank=True)
    date_field   = models.DateField()
    month        = models.CharField(max_length=30,null=True,blank=True)
    week         = models.CharField(max_length=30,null=True,blank=True)
    def __str__(self):
        return str(self.vendorname)

class Apointment(models.Model):  # model objects for store appointments

    user           = models.ForeignKey  (User,               on_delete=models.CASCADE, null=True)
    customer_name  = models.CharField   (max_length=100,     null=True, blank=True)
    contact_number = models.CharField   (max_length=10,        null=True, blank=True)
    email          = models.CharField   (max_length=100,         null=True, blank=True)
    services       = models.CharField   (max_length=1000,          null=True, blank=True)
    price          = models.DecimalField(max_digits=100,             decimal_places=2,   null=True, blank=True)
    booking_date   = models.DateField   (auto_now_add=False,            null=True)
    booking_time   = models.CharField   (max_length=100,                  null=True, blank=True)
    service_slno   = models.CharField   (max_length=30)


    def __str__(self):
        return str(self.customer_name)

class Service_data(models.Model): # model object for store available services of indivisual user

    user          = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    service        = models.CharField(max_length=30)
    service_prise  = models.CharField(max_length=30)
    service_duration  = models.CharField(max_length=30)



    def __str__(self):
        return str(self.service)


class store_invoice_data_service(models.Model): # model object for store invoice selected services

    service  = models.CharField      (max_length=30)
    slnoo    = models.IntegerField   (null=True,   blank=True) # indexing the selected service of each user
    prise    = models.DecimalField   (null=True, blank=True, decimal_places=2, max_digits=100)
    slno     = models.CharField      (max_length=30) # slno of invoice
    total    = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=100)
    quantity = models.IntegerField   ()
    dicount  = models.DecimalField   (null=True, blank=True, decimal_places=2, max_digits=100)
    taxableamt  = models.DecimalField   (null=True, blank=True, decimal_places=2, max_digits=100)
    cgst  = models.DecimalField   (null=True, blank=True, decimal_places=2, max_digits=100)
    sgst  = models.DecimalField   (null=True, blank=True, decimal_places=2, max_digits=100)
    total  = models.DecimalField   (null=True, blank=True, decimal_places=2, max_digits=100)
    value  = models.DecimalField   (null=True, blank=True, decimal_places=2, max_digits=100)



    def __str__(self):
        return str(self.slno)

class store_app_service_data(models.Model): # model object for store appointment selected services

    service  = models.CharField   (max_length=30)
    slnoo    = models.IntegerField(null=True, blank=True) # indexing the selected service of each user


    def __str__(self):
        return str(self.slnoo)


class CustomerPointTable(models.Model):

    user               = models.ForeignKey  (User,               on_delete=models.CASCADE)
    customer_name      = models.CharField   (max_length=50,      blank=True,       null=True)
    cashback_Points    = models.IntegerField()
    service_cost       = models.IntegerField()
class StaffDetails(models.Model):

    user               = models.ForeignKey  (User,               on_delete=models.CASCADE, null=True)
    staffname           = models.CharField   (max_length=1000,)
    mobileno           = models.CharField   (max_length=13,      null=True ,blank=True)
    email              = models.EmailField  (null=True,          blank=True           )
    # address            = models.CharField   (max_length=1000,    blank=True,null=True)
    # aadhar_id          = models.CharField   (max_length=12)
    # aadhar_id_img      = models.ImageField  (upload_to='media/staff/aadhar', height_field=None, width_field=None, max_length=None)
    # pan_id             = models.CharField   (max_length=12)
    # pan_id_img         = models.ImageField  (upload_to='media/staff/pan', height_field=None, width_field=None, max_length=None)
    # date_of_joined     = models.DateField   (max_length=300)
    # days_of_attend     = models.IntegerField(default=0)
    # date_of_birth      = models.DateField()


    def __str__(self) -> str:
        return str(self.staffname)

class StaffAttendence(models.Model):

    user                     = models.ForeignKey  (User,on_delete=models.CASCADE,null=True)
    staff_name               = models.CharField   (max_length=30)
    present_staff_attendence = models.TextField   ()


    def __str__(self) -> str:
        return str(self.user)


class SallonProfile(models.Model):
    id              = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    salon_name      = models.CharField(max_length=1000,null=True,blank=True)
    owner_name      = models.CharField(max_length=1000,null=True,blank=True)
    owner_address   = models.CharField(max_length=1000,null=True,blank=True)
    owner_contactno = models.CharField(max_length=1000,null=True,blank=True)
    owner_Panno     = models.CharField(max_length=1000,null=True,blank=True)
    owner_cgst_no   = models.CharField(max_length=1000,null=True,blank=True)
    owner_email   = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.salon_name)

class security(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    time = models.CharField(max_length=1000,null=True,blank=True)

    def __str__(self) -> str:
        return str(self.user)

class BusinessAnalysis(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    monthly_analysis = models.ImageField(upload_to="analysis",null=True)
    month = models.CharField(max_length=1000)
    def __str__(self) -> str:
        return str(self.user)




