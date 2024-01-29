from rest_framework.decorators import api_view,renderer_classes,APIView
from rest_framework.renderers import TemplateHTMLRenderer,JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .process import render_to_pdf
import pdfkit as p # install this first
from swalook_backend.settings import BASE_DIR
from django.core.mail import send_mail
from swalook_backend import settings
from twilio.rest import Client # install this first
from django.urls import reverse
from django.contrib.auth.hashers import make_password,check_password
from .models import *
from .serializer import *

import datetime as dt
import datetime
import requests
import matplotlib.pyplot as plt
import matplotlib
from swalook.analysis import *
import pandas as pd
import os
from swalook_backend.settings import BASE_DIR
import random as r
import http.client
import jwt
import json
import os
from decimal import *
from swalook.word import number_2_word


#-----------------import end------------------------#


########################################################################################################################
'''                                           In this application swalook's views.py contain these classes(objects) ,

1. user_verify  --->  for signup
2. dashboard    --->  for dashboard and its all fuctionality
3. generatebill --->  for generate invoice section and all its functionality
4. appointment  --->  for book appointment section and all its functionality
5. change_password ---> for forgot password sections and all its functionality
6. geo_locate ---> for getting the location of the user ip[address]
7. vendor_service_add ---> for add service section
8. manage vendor staff ---> for attendance system
9. show cashback point ---> for customer service based cashback point generate


#########################################################################################################################
'''
#########################################################################################################################
'''                                           In this application swalook's views.py  contain these functions

1.signup_page ---> for render signup page
2.login_view_create ---> for login
3.forgot_backs ---> for back button
4.otp_backs ---> for back button
5.login_render ---> for redirect login
6.logout  ---> for logout


##########################################################################################################################
'''
##########################################################################################################################
'''

                                              In this application swalook's views.py mentioned classes contain these functions

1. user_verify  --->  POST
2. dashboard    --->  GET,
                        SEARCH_RESULT,
                                SHOW PAGE EDIT,
                                        SHOW SEARCH,
                                                NAVS,
                                                    DELETE APPOINTMENT ,
                                                            DELETE INVOICE
3. generatebill --->  GET,
                        POST BILL ,
                            SHOW INVOICE,
                                    SHOW FINAL INVOICE ,
                                            DOWNLOAD INVOICE ,
                                                    SHARE PDF ,
                                                            BACK ,
                                                                GENERATE POINTS
4. appointment  --->  POST, GET

5. change_password ---> GET, POST,
                                FORGOT PASSWORD,
                                            GET OTP
6. geo_locate ---> GET IP , GET LAT LONG

7. vendor_service_add --->  GET, POST, EDIT, DELETE

8. manage vendor staff ---> ADD STAFF,
                                EDIT STAFF,
                                    SHOW STAFF,
                                        ADD ATTENDANCE,
                                            SHOW ATTENDANCE,
                                                DELETE ATTENDANCE,
                                                                POST

9. show cashback point ---> GET


######################################################################################################################

'''

# create your view here
######################################################################################################################
class user_verify(APIView):
    def post(self,request):
        if request.method == 'POST':
            try:

                # import time
                # os.environ["TZ"] = "GMT+5:30"
                # time.tzset()
                a:int                     = r.randint(0,9) # random int combination for vendor_id
                b:int                     = r.randint(0,9)
                c:int                     = r.randint(0,9)
                data                      = request.POST
                m_e                       = data.get("mob") # mobile no
                signup_obj                = User_data()
                signup_obj.Name           = data.get("name")
                name_                     = str(signup_obj.Name)
                signup_obj.email          = None


                if User_data.objects.filter(MobileNo=m_e).exists():
                    messages.info(request,"User Account Already Exists")
                    return redirect("/")

                signup_obj.MobileNo       = m_e
                signup_obj.Password       = data.get("pwd")
                signup_obj.appointment_no = 0
                signup_obj.date_time      = dt.date.today()
                signup_obj.vendor_id      = name_[0:2] + str(a) + str(b) + str(c)
                get_ip                    = request.META.get('HTTP_X_FORWARDED_FOR') # ip
                if get_ip:
                    self.ip               = get_ip.split(',')[0]
                else:
                    self.ip               = request.META.get('REMOTE_ADDR')
                signup_obj.ip             = self.ip
                signup_obj.dev_limit      = 1
                signup_obj.gst_number     = 0
                signup_obj.s_gst_percent  = "0"
                signup_obj.c_gst_percent  = "0"
                signup_obj.save()
                user                      = User.objects.create(username=m_e) # creating user object
                user.set_password(data.get('pwd'))
                user.save()
                request.session['id']     = data.get('mob')
                user                      = auth.authenticate(username = data.get('mob'), password = data.get('pwd'))  # authenticating
                auth.login(request,user)
                sallon_details = SallonProfile()


                sallon_details.salon_name = data.get('name')
                sallon_details.owner_contactno = data.get('mob')
                sallon_details.save()


                request.session['id']     = data.get('mob')
                request.session['name']   = str(request.user)
                return redirect(reverse("dashboard"))

            except Exception as e:
                print(e)

        return redirect(reverse("signup"))
#######################################################################################################################

###########################################################
@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer])                 #   rendering the signup Template
def signup_page(request):                                 #
    ''' it shows the signup page get method '''           #
    if request.user.is_authenticated:                     #
        return redirect(reverse("dashboard"))             #
    return Response(template_name="signup.html")          #

###########################################################
class AdminDashboard(APIView):
    def __init__(self, **kwargs) -> None:
        pass
    def get(self,request):
        if request.user.is_authenticated:                     #
            return redirect(reverse("dashboard"))
        return render(request,"adminlogin.html")
    def post(self,request):
        data = request.POST
        username = data.get('mobile')
        password = data.get('password')
        if User.objects.filter(username=username).exists():

            users = auth.authenticate(username=username,password=password)
            if users is not None:
                auth.login(request,users)
            else:
                return redirect(reverse("admin"))



            request.session['name'] = str(request.user)
            request.session['id']   = str(request.user)
            request.session['auth']   = "abc"

            return redirect(reverse("dashboard"))



        else:
            return redirect(reverse("admin"))

def adduserstaff(request):
    if request.method == 'POST':
        data = request.POST
        staff = staff_account_details.objects.create(
            user = request.user,
            username = data.get('mobile'),
            staffname = data.get('name'),
            password = data.get('email'),


        )
        staff.save()

        return redirect(reverse('user-staff'))
    session_id = request.session.get('name')
    signin_data    = User_data.objects.get(MobileNo=session_id)
    context = {}
    context['user'] = staff_account_details.objects.filter(user=request.user)
    context['users'] = signin_data.Name
    return render(request,"adduser.html",context)
def deleteuserstaff(request):
    data = request.POST.getlist('basic[]')
    for i in staff_account_details.objects.filter(user=request.user):
        for j in data:
            if str(i.id) == j:
                i.delete()



    return redirect(reverse('user-staff'))


@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def login_view_Create(request,*_token_):  # authenticating user login page view
    ''' login view verify user and render login page
    if user is verified then redirect to index'''
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))

    if request.method == "POST":
            try:


                data = request.POST
                username:str          = data.get("mobile")
                Password:str          = data.get("password")
                user =  staff_account_details.objects.get(username=username,password=Password)

                x = User_data.objects.get(MobileNo=user.user)

                users = auth.authenticate(username=x.MobileNo,password=x.Password)

                auth.login(request,users)




                request.session['name'] = str(request.user)
                request.session['id']   = str(request.user)
                request.session['sub_user']   = username


                return redirect(reverse("dashboard"))

            except Exception as e:
                print(e)





    return Response(template_name="Login.html")


class dashboard(APIView):
    ''' showing the dash board with user data'''
    def __init__(self,):
        self.context:dict = {}
        self.g_data:str   = ""
        self.session_id   = None
        self.edit_ap      = {}
        global ids
        self.ap_id        = None
        self.a            = None
        self.b            = None
        self.mon = dt.date.today()
        self.month = None

    def get(self,request):
        ''' render the dash board of requested user with data'''

        self.session_id = request.session.get('name')
        if request.user.is_authenticated:
            # try:
                if request.session.get('sub_user') != None:
                    self.context['subuser'] = request.session.get('sub_user')
                if request.session.get('auth') != None:
                    self.context['auth'] = "123"

                signin_data    = User_data.objects.get(MobileNo=self.session_id)
                signin_data.dev_limit = 1
                signin_data.save()
                # if signin_data.appointment_no > 0:
                #     self.context["customer_"] = "show all"
                # else:
                #     self.context["customer_"] = "No Appointments"
                # if signin_data.invoice_number > 0:
                #     self.context["customer_button"] = "show all"
                # else:
                #     self.context["customer_button"] = "No customer services"
                self.month = self.mon.month
                b = BusinessAnalysis.objects.filter(user=request.user,month=self.month)
                if b.exists():
                    b.delete()

                a = Analysis(user= self.session_id)
                queryset = invoice_data.objects.filter(vendorname=str(request.user),month=self.month)
                serializer = Invoice_serializers(queryset,many=True)
                path = a.monthly_analysis(data={"data":serializer.data})

            # p = os.path.abspath(path)



                b = BusinessAnalysis()
                b.user = request.user
                b.monthly_analysis = f"analysis/analysis{path}"
                b.month= self.month
                b.save()

                self.monthly_sales_query = BusinessAnalysis.objects.filter(user=request.user,month=self.month)

                self.context['analysis_obj'] = self.monthly_sales_query[0]
                user_obj       = signin_data
                self.context["users"] = user_obj.Name
                inv = Invoice.objects.filter(vendor_name=request.user)
                for i in inv:
                    i.service_catg_name = i.service_catg_name.removeprefix("[")
                    i.service_catg_name = i.service_catg_name.removesuffix("]")
                    service             = i.service_catg_name
                    stri_data           = ""

                    for j in service:
                        if j == "'":
                            pass
                        elif j == ",":
                            pass
                        else:
                            stri_data   = stri_data+j
                    i.service_catg_name = stri_data
                    i.save()


                self.context["invoice_data"] = inv[::-1]
                ap_obj = Apointment.objects.filter(user=request.user)
                for i in ap_obj:
                    i.services               = i.services.removeprefix("[")
                    i.services               = i.services.removesuffix("]")
                    serv                     = i.services
                    stri_data                = ""
                    for j in serv:
                        if j == "'":
                            pass
                        elif j == ",":
                            pass
                        else:
                            stri_data        = stri_data+j
                    i.services               = stri_data
                    i.save()

                ap_obj_len                   = len(ap_obj)
                if ap_obj_len != 0:
                    if ap_obj_len >= 5:
                        ind_ex               = ap_obj_len - 5
                        dat_a:list           = []
                        for i in range(ind_ex,ap_obj_len):
                            dat_a.append(ap_obj[i])
                        self.context["ap_data"]                 = dat_a[::-1]
                        self.context["dialouge"]                = "5 Recents Appointments"
                        return render(request,"profiledashboard.html",self.context)

                    else:
                        self.context["ap_data"]                 = ap_obj [::-1]
                        self.context["dialouge"]                = "Upcoming Appointments"
                        cookie_                                 = render(request,"profiledashboard.html",self.context)
                        return cookie_
                else:

                    self.context["ap_data"]                     = ap_obj
                    self.context["dialouge"]                    = "Upcoming Appointments"
                    cookie_                                     = render(request,"profiledashboard.html",self.context)

                    return cookie_

            # except Exception as e:
            #     print(e)

        return redirect(reverse("login"))


    def search_result(self,request):
        ''' search view for perform search in a post method and show the data in get method '''

        self.session_id = request.session.get('name')
        if request.user.is_authenticated:
            try:
                c_h                          = request.POST.get("search")
                if c_h == None:
                    data                     = self.g_data
                else:
                    data                     = c_h
                inv_data = Invoice.objects.filter(vendor_name= request.user)
                if len(data) == 10:

                    ap_obj                       =  Apointment.objects.filter(user= request.user)
                    self.ap_objs                 = ap_obj.all().filter(contact_number = data)
                    self.context["dialouge"]     = "Search Result"

                    self.context["ap_data"]      = self.ap_objs
                    self.context["invoice_data"] = inv_data
                    cookie_                      = redirect(reverse("search_data"))

                    return cookie_
                else:

                    self.context["dialouge"]     = "Mobile No 10 Digit Required"

                    self.context["invoice_data"] = inv_data
                    cookie_                      = redirect(reverse("search_data"))
                    return cookie_

            except Exception as e:
                print(e)
                #return render(request,"profiledashboard.html",self.context)
        return redirect(reverse("login"))


    def show_search(self,request):
        ''' here the search data show '''
        if request.user.is_authenticated:

            try:
                if request.session.get('sub_user') != None:
                    self.context['subuser'] = request.session.get('sub_user')
                if request.session.get('auth') != None:
                    self.context['auth'] = "123"
                self.session_id             = request.session.get('name')

                user_obj                    =  User_data.objects.get(MobileNo=self.session_id)
                self.context["users"]       = user_obj.Name
                cookie_                     =  render(request,"profiledashboard.html",self.context)
                return cookie_
            except Exception as e:
                print(e)
        return redirect(reverse("login"))


    def show_page_edit(self,request,id=None,time=None,date=None,):

        if request.user.is_authenticated:
            if date == "addservice":
                return redirect(reverse("add_service"))
            elif date == "appointment":
                return redirect(reverse("appointment"))
            elif date == "generatebill":
                return redirect(reverse("generate_bill"))
            self.a = id
            self.b = time
            self.c = date
            try:
                if request.method == 'POST':
                    data = request.POST
                    hrs                   = request.POST.get('hrs')
                    mins                  = request.POST.get('mins')
                    meridian              = request.POST.get('meridian')
                    time_                 = hrs+mins+meridian



                    data_ap = Apointment.objects.filter(user=request.user,contact_number=id,booking_date=request.POST.get("datetime"),booking_time=time_).exclude(pk=self.ap_id)

                    if data_ap.exists():
                        messages.info(request,f"Appointment of  This Customer on This Date {request.POST.get('datetime')} at This Time {time_} Already Exists")
                        id = self.a
                        time = self.b
                        date = self.ap_id
                        return redirect(f"/app/edit/{id}/{time}/{date}")

                    data_ap = Apointment.objects.get(user=request.user,pk=self.ap_id)

                    if data_ap:
                        new_service = request.POST.getlist('basic[]')
                        # prev_service = request.POST.getlist('prev_value')
                        # for i in new_service:
                        #     for j in prev_service:
                        #         if i == j:
                        #             messages.info(request,f"{i} service is already selected")


                        #             id = data_ap.contact_number
                        #             time = data_ap.booking_time
                        #             date = data_ap.id
                        #             return redirect(f"/app/edit/{id}/{time}/{date}")
                        x  = int(data_ap.service_slno)
                        y  = int(data_ap.contact_number)
                        z  = str(y)+str(x)
                        serv_obj_ap = store_app_service_data.objects.filter(slnoo=z)

                        serv_obj_ap.delete()
                        for k in new_service:
                            serv_obj          = store_app_service_data()
                            serv_obj.service  = k
                            serv_obj.slnoo    = z
                            serv_obj.save()
                        # for l in prev_service:
                        #     serv_obj          = store_app_service_data()
                        #     serv_obj.service  = l
                        #     serv_obj.slnoo    = z
                        #     serv_obj.save()
                        dst = store_app_service_data.objects.filter(slnoo=z)
                        services   = []
                        for i in dst:
                            services.append(i.service)
                        data_ap.services = services
                        data_ap.booking_date = request.POST.get("datetime")
                        data_ap.booking_time = time_
                        data_ap.email        = request.POST.get("email")
                        data_ap.save()
                        return redirect("/")

                else:

                    ap_obj      = Apointment.objects.filter(user=request.user,contact_number=id,booking_time=time,pk=date)
                    x           = int(ap_obj[0].service_slno)
                    y           = int(ap_obj[0].contact_number)
                    z           = str(y)+str(x)
                    self.ap_id = ap_obj[0].id
                    serv_obj_ap       = store_app_service_data.objects.filter(slnoo=z)
                    service_datas     = Service_data.objects.filter(user=request.user).order_by('service')
                    self.edit_ap['service_data'] = service_datas
                    self.edit_ap ["serv_obj"]    = serv_obj_ap
                    self.edit_ap ["ap_edit"]     = ap_obj[0]




                    return render(request,'ap_edit.html',self.edit_ap)


            except Exception as e:
                print(e)
                return redirect("/")
        return redirect(reverse("login"))


    def deleteappointment(self,request,id):
        if request.user.is_authenticated:
            ap_obj      = Apointment.objects.filter(user=request.user,pk=id)
            x           = int(ap_obj[0].service_slno)
            y           = int(ap_obj[0].contact_number)
            z           = str(y)+str(x)
            serv_obj_ap = store_app_service_data.objects.filter(slnoo=z)
            serv_obj_ap.delete()
            ap_obj.delete()
            user_obj = User_data.objects.get(MobileNo=request.user)
            user_obj.appointment_no = user_obj.appointment_no - 1
            user_obj.save()
            return redirect(reverse('dashboard'))
        return redirect(reverse("login"))

    def deleteinvoice(self,request):
        pass


    def nav(self,request,navs=None):
        ''' for bottom nav bar '''
        try:
            if navs             ==  "user/dashboard":
                return redirect(reverse("dashboard"))

            elif navs           == "generatebill":
                return redirect(reverse("generate_bill"))
            elif navs           == "appointment":
                return redirect(reverse("appointment"))
            elif navs           == "search":
                self.g_data      = request.POST.get("search")
                return redirect(reverse("search"))
            elif navs           == "dashboard":
                return redirect(reverse("dashboard"))
            elif navs           == "service":
                return redirect(reverse("add_service"))


            elif navs           == "back":
                return redirect("/back")


            elif navs           == "setting":
                return redirect(reverse("setting"))
            elif navs           == "staff":
                return redirect("/staff")
            elif navs           == "reports":
                return redirect("/reports")
            elif navs           == "logout/users":
                return redirect("/logout/users")
            elif navs          == "adduser":
                return redirect(reverse("user-staff"))
            # elif navs          == "add-user":
            #     return adduserstaff(request)
            # elif navs          == "delete":
            #     return deleteuserstaff(request)

            elif navs          == "monthly":
                return redirect(reverse("monthly"))
            elif navs          == "query":
                request.session['bus-query'] = request.POST.get('select')

                # return HttpResponse(request.session.get('bus-query'))
                return redirect(reverse("query"))
            elif navs           == "business-analysis":
                return redirect(reverse("business"))


            else:
                 return HttpResponse("<h1>Not Found</h1>")
        except Exception as e:
            print(e)
            return redirect(reverse("dashboard"))





''' invoice generate '''
# class generate_bill(APIView):      # invoice generator class
#     ''' render and recieve bill data and show invoice'''
#     def __init__(self):
#         self.invoice_obj            = None
#         self.context:dict           = {}
#         self.billno                 = None
#         self.count:int              = 0
#         self.inner_context:dict     = {}
#         self.context__ = {}

#     def get(self,request):   # rendering bill
#         ''' render the billing form '''
#         if request.user.is_authenticated:
#             service_datas           = Service_data.objects.all().order_by('service')

#             self.context__['service_list'] = service_datas

#             if request.method == 'POST':
#                 return redirect("/invoice")
#             cookie_                 = render(request,"bill_index.html",self.context__)
#             return cookie_
#         return redirect(reverse("login"))


#     def generate_points(self,total_value=None):


#         if int(total_value) >= 1000 and int(total_value) <= 1300:
#             return 10
#         elif int(total_value) >= 500 and int(total_value) <1000:
#             return 5
#         elif int(total_value) > 1300 and int(total_value) <= 2000:
#             return 15
#         elif int(total_value) > 2000 and int(total_value) <= 3000:
#             return 20
#         else:
#             return 0

#     def post_bill(self,request,vendor_name=None):   # retrive data and save method
#         ''' taking post request and save the data to db and redirect to invoice with get method'''
#         if request.user.is_authenticated:


#                     user                         = request.session.get('name')

#                     self.user_obj                = User_data.objects.get(MobileNo=user)

#                     self.context["username"]     = self.user_obj.Name
#                     self.context["id_user"]      = self.user_obj.MobileNo
#                     seri                         = dt.datetime.now()
#                     m_                           = seri.strftime("%m")
#                     y_                           = seri.strftime("%y")
#                     data                         = request.POST
#                     self.invoice_obj                    = Invoice()
#                     self.invoice_obj.Name               = request.POST.get("f_name")
#                     self.invoice_obj.Address            = request.POST.get("address")
#                     self.invoice_obj.Mobileno           = request.POST.get("mobile")
#                     self.invoice_obj.email              = request.POST.get("email")
#                     self.invoice_obj.service_catg_name  = request.POST.getlist("select")
#                     self.invoice_obj.service_by         = request.POST.get("served_by")
#                     self.invoice_obj.date_time          = dt.datetime.today()
#                     self.invoice_obj.vendor_name        = request.user
#                     v_id                                = str(self.user_obj.vendor_id)
#                     slno                                = v_id.lower() + str(self.user_obj.invoice_number) + str(m_) + str(y_)
#                     self.invoice_obj.slno               = slno
#                     self.user_obj.current_billslno      = slno

#                     self.invoice_obj.vendorname         =  self.user_obj.Name
#                     data_list                           = request.POST.getlist("select")

#                     if data_list == []:
#                         messages.info(request,"you have not selected any services")
#                         return redirect(reverse("generatebill"))
#                     self.invoice_obj.total              = 0
#                     i                                   = 0
#                     for j in data_list:
#                         serv_obj                        = store_invoice_data_service()
#                         serv_obj.service                = j
#                         serv_obj.slnoo                  = i + 1
#                         self.serv                       = Service_data.objects.get(service=j)
#                         serv_obj.prise                  = self.serv.service_prise
#                         serv_obj.slno                   = self.invoice_obj.slno



#                         serv_obj.total                  = float(serv_obj.prise)
#                         serv_obj.quantity               = 1
#                         serv_obj.save()
#                         self.invoice_obj.total          = float(self.invoice_obj.total) + float(self.serv.service_prise)
#                         i                               = i+1

#                     print(float(self.invoice_obj.total))


#                     self.invoice_obj.Discont        = 0.00
#                     self.invoice_obj.c_gst          = 0
#                     self.invoice_obj.s_gst          = 0
#                     self.user_obj.s_gst_percent     = "0"
#                     self.user_obj.c_gst_percent     = "0"
#                     self.user_obj.save()
#                     self.invoice_obj.s_gst_percent  = "0"
#                     self.invoice_obj.c_gst_percent  = "0"


#                     if request.POST.get('discount')!= '':
#                          self.invoice_obj.total = self.invoice_obj.total - float(request.POST.get('discount'))
#                          self.invoice_obj.Discont        = float(request.POST.get('discount'))

#                     if request.POST.get("checkbox1") == "11":

#                         self.invoice_obj.check_value    = request.POST.get("checkbox1")
#                         self.invoice_obj.gst_number     = request.POST.get("gst-number")
#                         gst_value              = self.invoice_obj.total * 5 / 105

#                         self.invoice_obj.total = self.invoice_obj.total - (gst_value)
#                         mod = str(self.invoice_obj.total)
#                         store_data = ""
#                         decimal_data = ""
#                         deci = 0
#                         for i in mod:
#                             if deci >= 1:
#                                 deci = deci+1

#                             store_data = store_data + i
#                             if i == ".":


#                                 deci = deci+1
#                             if deci == 3:
#                                 break
#                         print("datasert",store_data)







#                         self.invoice_obj.c_gst = self.invoice_obj.total * 2.5 / 100

#                         gst_mod = str(self.invoice_obj.c_gst)
#                         gst_v = ""
#                         gst_d = ""
#                         deci = 0
#                         for i in gst_mod:
#                             if deci >= 1:
#                                 deci = deci+1

#                             gst_v = gst_v + i
#                             if i == ".":


#                                 deci = deci+1
#                             if deci == 3:
#                                 break


#                         print("store_data",store_data)
#                         print("decimal_data",decimal_data)
#                         self.invoice_obj.total = store_data + decimal_data
#                         self.invoice_obj.c_gst = gst_v + gst_d
#                         self.invoice_obj.s_gst = gst_v + gst_d






#                         self.user_obj.s_gst_percent     = "2.5"
#                         self.user_obj.c_gst_percent     = "2.5"
#                         self.user_obj.save()
#                         self.invoice_obj.s_gst_percent  = "2.5"
#                         self.invoice_obj.c_gst_percent  = "2.5"


#                     self.invoice_obj.subtotal           = float(self.invoice_obj.total) + float(self.invoice_obj.c_gst)+float(self.invoice_obj.s_gst)

#                     #self.invoice_obj.subtotal           = (self.invoice_obj.subtotal) + (self.invoice_obj.s_gst)
#                     print(self.invoice_obj.subtotal)
#                     self.invoice_obj.grand_total        = (self.invoice_obj.subtotal)
#                     #self.invoice_obj.Discont           = (self.invoice_obj.grand_total*self.invoice_obj.Discont)/100
#                     self.invoice_obj.prise              = self.invoice_obj.grand_total
#                     self.invoice_obj.date_field = dt.date.today()
#                     self.invoice_obj.save()

#                     cashback                            = self.generate_points(total_value=self.invoice_obj.prise)
#                     table                               = CustomerPointTable()
#                     table.user                          = request.user

#                     table.cashback_Points               = cashback
#                     table.customer_name                 = self.invoice_obj.Name
#                     table.service_cost                  = self.invoice_obj.prise
#                     table.save()
#                     self.user_obj.invoice_number        = self.user_obj.invoice_number + 1
#                     self.user_obj.save()
#                     return redirect("/invoice")

#     def show_invoice(self,request):
#         ''' showing  the created invoice '''
#         try:
#             if request.user.is_authenticated:

#                 if request.method == 'GET':



#                     self.user  = User_data.objects.get(MobileNo=request.user)
#                     self.inv_obj = Invoice.objects.get(vendor_name=request.user,slno=self.user.current_billslno)
#                     self.inv_serv_obj = store_invoice_data_service.objects.filter(slno=self.user.current_billslno)
#                     self.context_dict = {}
#                     self.context_dict [ "invoice_data"] = self.inv_obj
#                     self.context_dict [ "service_obj"] = self.inv_serv_obj
#                     self.context_dict [ "username"] = self.user.Name
#                     service_datas = Service_data.objects.all().order_by('service')
#                     self.context_dict [ "service_data"] =  service_datas
#                     cookie_ =  render(request,"invoice.html",self.context_dict)
#                     return cookie_
#                 elif request.method == 'POST':

#                     price_data = request.POST.getlist('price')
#                     quantity   = request.POST.getlist('quan')
#                     discount   = request.POST.get('discounts')

#                     self.inv_obj.total = 0
#                     i                  = 0
#                     for j in self.inv_serv_obj:
#                         j.prise    = price_data[i]
#                         j.total    = float(float(price_data[i]) * int(quantity[i]))

#                         j.quantity = int(quantity[i])
#                         j.save()
#                         self.inv_obj.total = self.inv_obj.total+j.total
#                         i=i+1
#                     if request.POST.get('discounts') != None:

#                         self.inv_obj.Discont = float(discount)
#                         self.inv_obj.total   = float(float(self.inv_obj.total) - float(self.inv_obj.Discont))





#                     if self.inv_obj.c_gst_percent == "2.5":
#                         gst_value              = self.inv_obj.total * 5 / 105
#                         print("gst",gst_value)
#                         self.inv_obj.total = self.inv_obj.total - gst_value
#                         mod = str(self.inv_obj.total)
#                         store_data = ""
#                         decimal_data = ""
#                         deci = 0
#                         for i in mod:
#                             if deci >= 1:
#                                 deci = deci+1

#                             store_data = store_data + i
#                             if i == ".":


#                                 deci = deci+1
#                             if deci == 3:
#                                 break

#                         self.inv_obj.c_gst = self.inv_obj.total * 2.5 / 100


#                         gst_mod = str(self.inv_obj.c_gst)
#                         gst_v = ""
#                         gst_d = ""
#                         deci = 0
#                         for i in gst_mod:
#                             if deci >= 1:
#                                 deci = deci+1

#                             gst_v = gst_v + i
#                             if i == ".":


#                                 deci = deci+1
#                             if deci == 3:
#                                 break
#                         self.inv_obj.total = store_data + decimal_data
#                         self.inv_obj.c_gst = gst_v + gst_d
#                         self.inv_obj.s_gst = gst_v + gst_d

#                         self.inv_obj.subtotal           = float(self.inv_obj.total)+float(self.inv_obj.c_gst)
#                         self.inv_obj.subtotal           = float(self.inv_obj.subtotal) + float(self.inv_obj.s_gst)
#                         self.inv_obj.grand_total        = self.inv_obj.subtotal

#                         self.inv_obj.prise = self.inv_obj.grand_total


#                     else:
#                         self.inv_obj.subtotal           = self.inv_obj.total
#                         self.inv_obj.grand_total        = self.inv_obj.subtotal
#                         self.inv_obj.prise = self.inv_obj.grand_total

#                     self.user.current_billslno = self.inv_obj.slno
#                     self.inv_obj.save()








#                     return redirect("/invoice")
#                 else:
#                     pass
#             return redirect("/")
#         except Exception as e:
#             print(e)



#     def add_extra_services(self,request):
#         data = request.POST.getlist("select")
#         self.inv_obj = Invoice.objects.get(vendor_name=request.user,slno=self.user.current_billslno)
#         data12 = store_invoice_data_service.objects.filter(slno=self.user.current_billslno)
#         lenght = data12.count()
#         i=int(lenght)
#         for j in data:
#             serv_obj                        = store_invoice_data_service()
#             serv_obj.service                = j
#             serv_obj.slnoo                  = i + 1
#             self.serv                       = Service_data.objects.get(service=j)
#             serv_obj.modified_prise         = self.serv.service_prise
#             serv_obj.prise                  = self.serv.service_prise
#             serv_obj.slno                   = self.user.current_billslno

#             serv_obj.total = serv_obj.prise
#             serv_obj.quantity               = 1
#             serv_obj.save()
#             #self.inv_obj.total = float(self.inv_obj.total) + float(self.serv.service_prise)


#             i                               = i+1

#         # if self.inv_obj.Discont != '':


#         #     self.inv_obj.total          = float(self.inv_obj.total) - float(self.inv_obj.Discont)
#         #     self.inv_obj.subtotal           = self.inv_obj.total
#         #     self.inv_obj.grand_total        = self.inv_obj.subtotal
#         #     self.inv_obj.prise = self.inv_obj.grand_total

#         # elif self.inv_obj.check_value == "11":



#         #     gst_value              = self.inv_obj.total * 5 / 105
#         #     self.inv_obj.total = self.inv_obj.total - gst_value
#         #     self.inv_obj.c_gst = self.inv_obj.total * 2.5 / 100
#         #     self.inv_obj.s_gst = self.inv_obj.total * 2.5 / 100


#         #     self.inv_obj.subtotal           = float(self.inv_obj.total)+float(self.inv_obj.c_gst)
#         #     self.inv_obj.subtotal           = self.inv_obj.subtotal + float(self.inv_obj.s_gst)
#         #     self.inv_obj.grand_total        = self.inv_obj.subtotal
#         #     #self.invoice_obj.Discont           = (self.invoice_obj.grand_total*self.invoice_obj.Discont)/100
#         #     self.inv_obj.prise              = self.inv_obj.grand_total
#         # else:
#         #     self.inv_obj.subtotal           = self.inv_obj.total
#         #     self.inv_obj.grand_total        = self.inv_obj.subtotal
#         #     self.inv_obj.prise = self.inv_obj.grand_total

#         # self.inv_obj.save()

#         return redirect(reverse("invoic"))
#     def download_invoice(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             try:
#                 # getting the template
#                 user                         =  User_data.objects.get(MobileNo=str(request.user))
#                 inv_obj                      =  Invoice.objects.get(vendor_name=request.user,slno=user.current_billslno)
#                 data                         = inv_obj.service_catg_name
#                 data                         = inv_obj.service_catg_name.removeprefix("[")
#                 data                         = inv_obj.service_catg_name.removesuffix("]")
#                 service                      = data
#                 stri_data                    = ""

#                 for j in service:
#                     if j == "'":
#                         pass
#                     elif j == ",":
#                         pass
#                     else:
#                         stri_data            = stri_data+j
#                 data                         = stri_data
#                 inv_obj.service_catg_name    = data
#                 inv_obj.save()
#                 context_dict                 = {}
#                 s_obj                        = store_invoice_data_service.objects.filter(slno=inv_obj.slno)
#                 print(inv_obj.Name)
#                 context_dict["service_obj"]  =  s_obj
#                 context_dict["invoice_data"] =  inv_obj
#                 context_dict["username"]     = user.Name
#                 pdf                          = render_to_pdf('invoice_pdf.html',context_dict)

#                     # rendering the template
#                 return HttpResponse(pdf, content_type='application/pdf')
#             except Exception as e:
#                 print(e)

#         return redirect(reverse("login"))


#     def back(self,request):
#         return redirect("/generatebill")


#     def share_pdf(self,request):
#         ''' sharing the pdf '''

#         # inv_obj                      = Invoice.objects.last()
#         # data                         = inv_obj.service_catg_name
#         # data                         = inv_obj.service_catg_name.removeprefix("[")
#         # data                         = inv_obj.service_catg_name.removesuffix("]")
#         # service                      = data
#         # stri_data                    = ""

#         # for j in service:
#         #     if j == "'":
#         #         pass
#         #     elif j == ",":
#         #         pass
#         #     else:
#         #         stri_data            = stri_data+j
#         # data                         = stri_data
#         # inv_obj.service_catg_name    = data
#         # inv_obj.save()
#         # try:
#         #     wkhtml_path                  = p.configuration(wkhtmltopdf=settings.WKHTML2PDF_PATH)   # wkhtml path
#         #     p_df                         = p.from_url('https://{}/invoice/'.format(settings.URL),output_path= BASE_DIR / 'media/pdf/invoice{}.pdf'.format(inv_obj.slno),configuration=wkhtml_path)
#         # except Exception as e:
#         #     return HttpResponse("<h1>NET ERROR</h1>")
#         # number                       = self.context.get('mobile')
#         # slno                         = self.context.get('slno')
#         # conn                         = http.client.HTTPSConnection("api.ultramsg.com")
#         # payload                      = "token={}&to=+91{}&filename=invoice.pdf&body=Hi {},This is your swalook invoice,now you eligible to chat with us".format(settings.WHATSAPP_AUTH_TOKEN,number,self.context.get('name'))
#         # headers                      = { 'content-type': "application/x-www-form-urlencoded" }
#         # conn.request("POST", "/{}/messages/chat".format(settings.WHATSAPP_INSTANCE), payload, headers)
#         # res = conn.getresponse()
#         # data = res.read()
#         # print(data.decode("utf-8"))
#         # # pdf sending
#         # conn                         = http.client.HTTPSConnection("api.ultramsg.com")
#         # payload                      = "token={}&to=+91{}&filename=invoice.pdf&document=https://{}/media/pdf/invoice{}.pdf".format(settings.WHATSAPP_AUTH_TOKEN,number,settings.URL,slno)
#         # headers                      = { 'content-type': "application/x-www-form-urlencoded" }
#         # conn.request("POST", "/{}/messages/document".format(settings.WHATSAPP_INSTANCE), payload, headers)
#         # res = conn.getresponse()
#         # data = res.read()
#         # print(data.decode("utf-8"))
#         # try:
#         #     os.remove(path="{}/media/pdf/invoice{}.pdf".format(BASE_DIR,slno))
#         # except Exception as e:
#         #     print(e)
#         # return redirect("/")
#         return HttpResponse("under construction")

#     def show_final_invoice(self,request):
#         self.user  = User_data.objects.get(MobileNo=request.user)
#         self.inv_obj = Invoice.objects.get(vendor_name=request.user,slno=self.user.current_billslno)
#         self.inv_serv_obj = store_invoice_data_service.objects.filter(slno=self.user.current_billslno)
#         self.context_dict = {}
#         self.context_dict [ "invoice_data"] = self.inv_obj
#         self.context_dict [ "service_obj"] = self.inv_serv_obj
#         self.context_dict [ "username"] = self.user.Name
#         cookie_ =  render(request,"final_invoice.html",self.context_dict)
#         return cookie_

#     def add_extra_service(self,request):
#         pass

class generate_bill(APIView):      # invoice generator class
    ''' render and recieve bill data and show invoice'''
    def __init__(self):
        self.invoice_obj            = None
        self.context:dict           = {}
        self.billno                 = None
        self.count:int              = 0
        self.inner_context:dict     = {}
        self.context__ = {}

    def get(self,request):   # rendering bill
        ''' render the billing form '''
        if request.user.is_authenticated:
            if request.session.get('sub_user') != None:
                    self.context__['subuser'] = request.session.get('sub_user')
            if request.session.get('auth') != None:
                    self.context__['auth'] = "123"
            service_datas           = Service_data.objects.filter(user=request.user).order_by('service')
            gst_number              = SallonProfile.objects.get(owner_contactno=str(request.user))
            staff                   = StaffDetails.objects.filter(user=request.user)
            self.session_id = request.session.get('name')
            signin_data    = User_data.objects.get(MobileNo=self.session_id)

            self.context__['users'] = signin_data.Name
            self.context__['service_list'] = service_datas
            self.context__['gst'] = gst_number.owner_cgst_no
            self.context__['staff'] = staff

            if request.method == 'POST':
                return redirect("/invoice")
            cookie_                 = render(request,"bill_index.html",self.context__)
            return cookie_
        return redirect(reverse("login"))


    def generate_points(self,total_value=None):


        if int(total_value) >= 1000 and int(total_value) <= 1300:
            return 10
        elif int(total_value) >= 500 and int(total_value) <1000:
            return 5
        elif int(total_value) > 1300 and int(total_value) <= 2000:
            return 15
        elif int(total_value) > 2000 and int(total_value) <= 3000:
            return 20
        else:
            return 0

    def post_bill(self,request,vendor_name=None):   # retrive data and save method
        ''' taking post request and save the data to db and redirect to invoice with get method'''
        if request.user.is_authenticated:

                    # import time


                    # os.environ["TZ"] = "GMT+5:30"
                    # time.tzset()

                    user                         = request.session.get('name')

                    self.user_obj                = User_data.objects.get(MobileNo=user)

                    self.context["username"]     = self.user_obj.Name
                    self.context["id_user"]      = self.user_obj.MobileNo
                    seri                         = dt.datetime.now()
                    m_                           = seri.strftime("%m")
                    y_                           = seri.strftime("%y")
                    data                         = request.POST
                    self.invoice_obj                    = Invoice()
                    self.invoice_obj.Name               = request.POST.get("f_name")
                    self.invoice_obj.Address            = request.POST.get("address")
                    self.invoice_obj.Mobileno           = request.POST.get("mobile")
                    self.invoice_obj.email              = request.POST.get("email")
                    self.invoice_obj.service_catg_name  = request.POST.getlist("basic[]")
                    self.invoice_obj.service_by         = request.POST.get("served_by")
                    self.invoice_obj.date_time          = dt.date.today()
                    self.invoice_obj.vendor_name        = request.user
                    v_id                                = str(self.user_obj.vendor_id)
                    slno                                = v_id.lower() + str(self.user_obj.invoice_number) + str(m_) + str(y_)
                    self.invoice_obj.slno               = slno
                    self.user_obj.current_billslno      = slno

                    self.invoice_obj.vendorname         =  self.user_obj.Name
                    data_list                           = request.POST.getlist("basic[]")

                    if data_list == []:
                        messages.info(request,"you have not selected any services")
                        return redirect(reverse("generatebill"))

                    i                                   = 0
                    for j in data_list:
                        serv_obj                        = store_invoice_data_service()
                        serv_obj.service                = j
                        serv_obj.slnoo                  = i + 1
                        self.serv                       = Service_data.objects.get(user=request.user,service=j)
                        serv_obj.prise                  = int(self.serv.service_prise)

                        self.invoice_obj.total_prise = self.invoice_obj.total_prise + serv_obj.prise

                        serv_obj.slno                   = self.invoice_obj.slno
                        if request.POST.get('discount')!= '':
                            current_price = serv_obj.prise - float(request.POST.get('discount'))
                            serv_obj.dicount        = float(request.POST.get('discount'))

                            self.invoice_obj.total_discount = self.invoice_obj.total_discount + serv_obj.dicount

                        else:
                            serv_obj.dicount        = 0.00
                            current_price = serv_obj.prise
                        if request.POST.get("checkbox1") == "11":

                            self.invoice_obj.check_value    = request.POST.get("checkbox1")
                            self.invoice_obj.gst_number     = request.POST.get("gst-number")
                            gst_value              =  current_price * 5 / 105

                            serv_obj.taxableamt = current_price - (gst_value)

                            mod = str(serv_obj.taxableamt)
                            store_data = ""
                            decimal_data = ""
                            deci = 0
                            for k in mod:
                                if deci >= 1:
                                    deci = deci+1

                                store_data = store_data + k
                                if k == ".":


                                    deci = deci+1
                                if deci == 3:
                                    break








                            serv_obj.cgst = float(serv_obj.taxableamt) * 2.5 / 100

                            gst_mod = str(serv_obj.cgst)
                            gst_v = ""
                            gst_d = ""
                            deci = 0
                            for l in gst_mod:
                                if deci >= 1:
                                    deci = deci+1

                                gst_v = gst_v + l
                                if l == ".":


                                    deci = deci+1
                                if deci == 3:
                                    break




                            serv_obj.taxableamt = store_data + decimal_data
                            self.invoice_obj.total_tax = float(self.invoice_obj.total_tax) + float(serv_obj.taxableamt)

                            serv_obj.cgst = gst_v + gst_d

                            self.invoice_obj.total_cgst = float(self.invoice_obj.total_cgst) + float(serv_obj.cgst)
                            serv_obj.sgst = gst_v + gst_d

                            self.invoice_obj.total_sgst = float(self.invoice_obj.total_sgst) + float(serv_obj.sgst)

                            serv_obj.total = float(serv_obj.taxableamt)+float(serv_obj.cgst) + float(serv_obj.sgst)


                            self.invoice_obj.grand_total = self.invoice_obj.grand_total+float(serv_obj.total)
                            self.invoice_obj.c_gst_percent = "2.5"
                            self.invoice_obj.s_gst_percent = "2.5"

                        else:
                            serv_obj.total = current_price
                            self.invoice_obj.grand_total = self.invoice_obj.grand_total+float(serv_obj.total)
                            serv_obj.taxableamt = 0.00

                            self.invoice_obj.total_tax = 0.00
                            serv_obj.cgst = 0.00

                            self.invoice_obj.total_cgst = 0.00
                            serv_obj.sgst = 0.00

                            self.invoice_obj.total_sgst = 0.00




                            self.invoice_obj.c_gst_percent = "0.00"
                            self.invoice_obj.s_gst_percent = "0.00"
                        serv_obj.quantity               = 1

                        self.invoice_obj.total_quantity = self.invoice_obj.total_quantity + serv_obj.quantity
                        serv_obj.save()

                        i                               = i+1













                    self.invoice_obj.date_field = dt.date.today()
                    self.invoice_obj.save()

                    # data--invoice
                    d = invoice_data()
                    d.Name = self.invoice_obj.Name
                    d.Address = self.invoice_obj.Address
                    d.Mobileno = self.invoice_obj.Mobileno
                    d.email = self.invoice_obj.email
                    d.service_catg_name = self.invoice_obj.service_catg_name

                    d.total_prise = self.invoice_obj.total_prise
                    d.service_by = self.invoice_obj.service_by
                    d.slno = self.invoice_obj.slno
                    d.total_tax = self.invoice_obj.total_tax
                    d.total_discount = self.invoice_obj.total_discount
                    d.gst_number = self.invoice_obj.gst_number
                    d.total_quantity = self.invoice_obj.total_quantity
                    d.total_cgst = self.invoice_obj.total_cgst
                    d.total_sgst = self.invoice_obj.total_sgst
                    d.grand_total = self.invoice_obj.grand_total
                    d.s_gst_percent = self.invoice_obj.s_gst_percent
                    d.c_gst_percent = self.invoice_obj.c_gst_percent
                    d.vendorname    = str(request.user)
                    d.date_field    = dt.date.today()
                    mon = dt.date.today()
                    if int(mon.day) >=1 and int(mon.day) <=7:

                        d.week          = "1"
                    if int(mon.day) >=8 and int(mon.day) <=15:
                        d.week          = "2"
                    if int(mon.day) >=16 and int(mon.day) <=23:
                        d.week          = "3"
                    if int(mon.day) >=24 and int(mon.day) <=31:
                        d.week          = "4"

                    d.month         = mon.month
                    d.save()

                    self.user_obj.invoice_number        = self.user_obj.invoice_number + 1
                    self.user_obj.save()
                    return redirect("/invoice")

    def show_invoice(self,request):
            ''' showing  the created invoice '''

            if request.user.is_authenticated:

                if request.method == 'GET':



                    self.user  = User_data.objects.get(MobileNo=str(request.user))
                    self.inv_obj = Invoice.objects.get(vendor_name=request.user,slno=self.user.current_billslno)
                    self.inv_serv_obj = store_invoice_data_service.objects.filter(slno=self.user.current_billslno)
                    data_word = number_2_word(int(self.inv_obj.grand_total))
                    word = ""
                    i=0
                    for j in data_word:
                        if i == 0:
                            word = word + j.capitalize()

                        else:
                            word = word + j
                        i = i+1

                    data_word = word


                    self.context_dict = {}
                    self.context_dict [ "invoice_data"] = self.inv_obj
                    self.context_dict [ "service_obj"] = self.inv_serv_obj
                    self.context_dict [ "username"] = self.user.Name
                    self.context_dict [ "dict"] = self.user.Name
                    service_datas = Service_data.objects.filter(user=request.user).order_by('service')
                    self.context_dict [ "service_data"] =  service_datas
                    self.context_dict [ "data_word"] =  data_word
                    cookie_ =  render(request,"invoice.html",self.context_dict)
                    return cookie_
                if request.method == 'POST':


                    price_data = request.POST.getlist('price')
                    quantity   = request.POST.getlist('quan')
                    discount   = request.POST.getlist('discounts')

                    self.inv_obj.total_prise = 0
                    self.inv_obj.total_discount = 0
                    self.inv_obj.grand_total = 0
                    self.inv_obj.total_sgst = 0
                    self.inv_obj.total_cgst = 0
                    self.inv_obj.total_tax = 0
                    self.inv_obj.total_quantity = 0

                    i                  = 0
                    for j in self.inv_serv_obj:
                        j.prise   = price_data[i]
                        self.inv_obj.total_prise = self.inv_obj.total_prise+float(j.prise)
                        j.quantity = int(quantity[i])
                        self.inv_obj.total_quantity = self.inv_obj.total_quantity + j.quantity




                        self.curent_prise = None
                        if discount[i] != '0.00':
                            total_price = float(j.prise) * j.quantity
                            total_price = total_price - float(discount[i])
                            j.dicount = float(discount[i])
                            j.total   = total_price

                            self.inv_obj.total_discount = self.inv_obj.total_discount + j.dicount

                        else:
                            total_price = float(j.prise) * j.quantity
                            j.total = total_price





                        if self.inv_obj.c_gst_percent == "2.5":
                            gst_value              =  total_price * 5 / 105

                            j.taxableamt = total_price - (gst_value)
                            mod = str(j.taxableamt)
                            store_data = ""
                            decimal_data = ""
                            deci = 0
                            for k in mod:
                                if deci >= 1:
                                    deci = deci+1

                                store_data = store_data + k
                                if k == ".":


                                    deci = deci+1
                                if deci == 3:
                                    break


                            j.taxableamt = store_data + decimal_data




                            j.cgst = float(j.taxableamt) * 2.5 / 100

                            gst_mod = str(j.cgst)
                            gst_v = ""
                            gst_d = ""
                            deci = 0
                            for l in gst_mod:
                                if deci >= 1:
                                    deci = deci+1

                                gst_v = gst_v + l
                                if l == ".":


                                    deci = deci+1
                                if deci == 3:
                                    break






                            self.inv_obj.total_tax = self.inv_obj.total_tax + float(j.taxableamt)

                            j.cgst = gst_v + gst_d
                            self.inv_obj.total_cgst = self.inv_obj.total_cgst +float(j.cgst)


                            j.sgst = gst_v + gst_d
                            self.inv_obj.total_sgst = self.inv_obj.total_sgst + float(j.sgst)


                            j.total = float(j.taxableamt)+float(j.cgst) + float(j.sgst)
                            self.inv_obj.grand_total = self.inv_obj.grand_total + j.total

                        else:


                            self.inv_obj.grand_total = self.inv_obj.grand_total + j.total


                        j.save()
                        i = i+1








                    self.user.current_billslno = self.inv_obj.slno
                    self.inv_obj.save()


                    d = invoice_data.objects.get(slno=self.inv_obj.slno)

                    d.service_catg_name = self.inv_obj.service_catg_name

                    d.total_prise = self.inv_obj.total_prise


                    d.total_tax = self.inv_obj.total_tax
                    d.total_discount = self.inv_obj.total_discount

                    d.total_quantity = self.inv_obj.total_quantity
                    d.total_cgst = self.inv_obj.total_cgst
                    d.total_sgst = self.inv_obj.total_sgst
                    d.grand_total = self.inv_obj.grand_total


                    d.save()
                    return redirect(reverse("invoic"))

            return redirect("/")



    def add_extra_services(self,request):
        data = request.POST.getlist("basic[]")
        self.inv_obj = Invoice.objects.get(vendor_name=request.user,slno=self.user.current_billslno)
        data12 = store_invoice_data_service.objects.filter(slno=self.user.current_billslno)
        lenght = data12.count()
        i=int(lenght)
        for j in data:
            serv_obj                        = store_invoice_data_service()
            serv_obj.service                = j
            serv_obj.slnoo                  = i + 1
            self.serv                       = Service_data.objects.get(user=request.user,service=j)

            serv_obj.prise                  = self.serv.service_prise
            serv_obj.slno                   = self.user.current_billslno
            serv_obj.quantity               = 1
            serv_obj.dicount               = 0.00
            serv_obj.taxableamt = 0.00
            serv_obj.cgst = 0.00
            serv_obj.sgst = 0.00
            serv_obj.total = serv_obj.prise
            serv_obj.save()





            i                               = i+1




        return redirect(reverse("invoic"))
    def download_invoice(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                # getting the template
                user                         =  User_data.objects.get(MobileNo=str(request.user))
                inv_obj                      =  Invoice.objects.get(vendor_name=request.user,slno=user.current_billslno)
                data                         = inv_obj.service_catg_name
                data                         = inv_obj.service_catg_name.removeprefix("[")
                data                         = inv_obj.service_catg_name.removesuffix("]")
                service                      = data
                stri_data                    = ""

                for j in service:
                    if j == "'":
                        pass
                    elif j == ",":
                        pass
                    else:
                        stri_data            = stri_data+j
                data                         = stri_data
                inv_obj.service_catg_name    = data
                inv_obj.save()
                context_dict                 = {}
                s_obj                        = store_invoice_data_service.objects.filter(slno=inv_obj.slno)
                data_word = number_2_word(int(self.inv_obj.grand_total))
                word = ""
                i=0
                for j in data_word:
                    if i == 0:
                        word = word + j.capitalize()

                    else:
                        word = word + j
                    i = i+1

                data_word = word

                context_dict["service_obj"]  =  s_obj
                context_dict["invoice_data"] =  inv_obj
                context_dict["username"]     = user.Name
                context_dict["data_word"]     = data_word
                imgs =  img.objects.get(pk=1)
                context_dict["img"]     = imgs
                pdf                          = render_to_pdf('invoice_pdf.html',context_dict)

                    # rendering the template
                return HttpResponse(pdf, content_type='application/pdf')
            except Exception as e:
                print(e)

        return redirect(reverse("login"))


    def back(self,request):
        return redirect("/generatebill")


    def share_pdf(self,request):
        ''' sharing the pdf '''

        # inv_obj                      = Invoice.objects.last()
        # data                         = inv_obj.service_catg_name
        # data                         = inv_obj.service_catg_name.removeprefix("[")
        # data                         = inv_obj.service_catg_name.removesuffix("]")
        # service                      = data
        # stri_data                    = ""

        # for j in service:
        #     if j == "'":
        #         pass
        #     elif j == ",":
        #         pass
        #     else:
        #         stri_data            = stri_data+j
        # data                         = stri_data
        # inv_obj.service_catg_name    = data
        # inv_obj.save()
        # try:
        #     wkhtml_path                  = p.configuration(wkhtmltopdf=settings.WKHTML2PDF_PATH)   # wkhtml path
        #     p_df                         = p.from_url('https://{}/invoice/'.format(settings.URL),output_path= BASE_DIR / 'media/pdf/invoice{}.pdf'.format(inv_obj.slno),configuration=wkhtml_path)
        # except Exception as e:
        #     return HttpResponse("<h1>NET ERROR</h1>")
        # number                       = self.context.get('mobile')
        # slno                         = self.context.get('slno')
        # conn                         = http.client.HTTPSConnection("api.ultramsg.com")
        # payload                      = "token={}&to=+91{}&filename=invoice.pdf&body=Hi {},This is your swalook invoice,now you eligible to chat with us".format(settings.WHATSAPP_AUTH_TOKEN,number,self.context.get('name'))
        # headers                      = { 'content-type': "application/x-www-form-urlencoded" }
        # conn.request("POST", "/{}/messages/chat".format(settings.WHATSAPP_INSTANCE), payload, headers)
        # res = conn.getresponse()
        # data = res.read()
        # print(data.decode("utf-8"))
        # # pdf sending
        # conn                         = http.client.HTTPSConnection("api.ultramsg.com")
        # payload                      = "token={}&to=+91{}&filename=invoice.pdf&document=https://{}/media/pdf/invoice{}.pdf".format(settings.WHATSAPP_AUTH_TOKEN,number,settings.URL,slno)
        # headers                      = { 'content-type': "application/x-www-form-urlencoded" }
        # conn.request("POST", "/{}/messages/document".format(settings.WHATSAPP_INSTANCE), payload, headers)
        # res = conn.getresponse()
        # data = res.read()
        # print(data.decode("utf-8"))
        # try:
        #     os.remove(path="{}/media/pdf/invoice{}.pdf".format(BASE_DIR,slno))
        # except Exception as e:
        #     print(e)
        # return redirect("/")
        return HttpResponse("under construction")

    def show_final_invoice(self,request):
        self.user  = User_data.objects.get(MobileNo=request.user)
        self.inv_obj = Invoice.objects.get(vendor_name=request.user,slno=self.user.current_billslno)
        self.inv_serv_obj = store_invoice_data_service.objects.filter(slno=self.user.current_billslno)

        data_word = number_2_word(int(self.inv_obj.grand_total))
        word = ""
        i=0
        for j in data_word:
            if i == 0:
                word = word + j.capitalize()

            else:
                word = word + j
            i = i+1

        data_word = word
        self.context_dict = {}
        self.context_dict [ "invoice_data"] = self.inv_obj
        self.context_dict [ "service_obj"] = self.inv_serv_obj
        self.context_dict [ "username"] = self.user.Name
        self.context_dict [ "data_word"] =  data_word

        cookie_ =  render(request,"final_invoice.html",self.context_dict)
        return cookie_









''' appointment '''
class appointmnet():
    ''' Appointment class render and featch data '''
    def __init__(self):
        pass

    def post(self,request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                data = request.POST
                def validate(data=data):
                    if len(data.get("l_name")) < 10:
                            messages.info(request,"MobileNo: 10digit Required")
                            return True
                    if len(data.get("l_name")) > 10:
                            messages.info(request,"MobileNo: 10digit Required")
                            return True
                    else:
                        return False
                v = validate()
                if v:

                    return redirect(reverse("appointment"))
                else:
                    try:
                        hrs                      = request.POST.get('hrs')
                        mins                     = request.POST.get('mins')
                        meridian                 = request.POST.get('meridian')
                        time_                    = hrs+mins+meridian
                        if Apointment.objects.filter(user=request.user,contact_number=request.POST.get('l_name'),booking_date=request.POST.get('datetime'),booking_time=time_).exists():
                            messages.info(request,"This coustomer already has an appointment on{} at {}".format(request.POST.get('datetime'),time_))
                            return redirect(reverse("appointment"))
                        else:
                            ap_obj                = Apointment()
                            ap_obj.user           = request.user
                            ap_obj.customer_name  = request.POST.get('f_name')
                            ap_obj.contact_number = request.POST.get('l_name')
                            ap_obj.booking_date   = request.POST.get('datetime')
                            hrs                   = request.POST.get('hrs')
                            mins                  = request.POST.get('mins')
                            meridian              = request.POST.get('meridian')
                            time_                 = hrs+mins+meridian
                            ap_obj.booking_time   = time_
                            a                     = r.randint(0,9) # generating random int for users
                            b                     = r.randint(0,9)
                            c                     = r.randint(0,9)
                            uniquee               = str(a) + str(b) + str(c)
                            ap_obj.service_slno   = uniquee
                            data_list             = request.POST.getlist('basic[]')
                            if data_list == []:
                                messages.info(request,"you have not selected any services")
                                return redirect(reverse("appointment"))

                            for j in data_list:
                                serv_obj          = store_app_service_data()
                                serv_obj.service  = j
                                serv_obj.slnoo    = ap_obj.contact_number + uniquee
                                serv_obj.save()

                            ap_obj.email          = request.POST.get('email')
                            dst                   = store_app_service_data.objects.filter(slnoo=ap_obj.contact_number+uniquee)
                            ap_obj.services       = []
                            for i in dst:
                                ap_obj.services.append(i.service)

                            ap_obj.save()
                            user = User_data.objects.get(MobileNo=str(request.user))
                            user.appointment_no = user.appointment_no + 1
                            user.save()
                            return redirect(reverse("dashboard"))
                    except Exception as e:
                        print(e)
            else:
                return redirect("/appointment")

        return redirect(reverse("login"))
    def get(self,request):
        if request.user.is_authenticated:
            service_datas = Service_data.objects.filter(user=request.user).order_by('service')
            self.session_id = request.session.get('name')
            signin_data    = User_data.objects.get(MobileNo=self.session_id)


            context = {}
            if request.session.get('sub_user') != None:
                    context['subuser'] = request.session.get('sub_user')
            if request.session.get('auth') != None:
                    context['auth'] = "123"
            context['service_data'] = service_datas
            context['users'] = signin_data.Name
            cookie_ =  render(request,"appointment.html",context)
            cookie_.set_cookie("device_id",value=request.COOKIES.get("device_id"),max_age=315360000 * 5)
            return cookie_

        return redirect(reverse("signup"))




''' pdf '''



# class set_session_admin:
#     # it is a view from where admin can handle the user login devcie limit
#     def show_session_page(self,request):
#         if request.user.is_authenticated:
#             user_obj             = User.objects.get(username=str(request.user))
#             if user_obj.is_staff:
#                 sess_ion_obj     = User_data.objects.all()
#                 return render(request,"user_manager.html",{'data':sess_ion_obj})
#         return HttpResponse("<h1> You Are Not Authorized for this page</h1>")


#     def save_device_limit(self,request,user):
#         try:
#             if "@" in user:
#                 token_obj                   = User_data.objects.get(email=user)
#                 if int(request.POST.get('devicelimit')) < int(token_obj.dev_limit):
#                     if int(token_obj.dev_limit) - int(request.POST.get('devicelimit')) == 1:
#                         token_obj.dev_limit = int(request.POST.get('devicelimit'))
#                         dev_id            = token_obj.reg_dev_id
#                         dev               = json.decoder.JSONDecoder()
#                         device_id         = dev.decode(dev_id)
#                         device_id.pop()
#                         token_obj.reg_dev_id = json.dumps(device_id)

#                         messages.info(request,"{} Device Limit is Updated To {}".format(token_obj.email,token_obj.dev_limit))
#                     else:
#                         messages.info(request,"only one device can be remove at a time")
#                         return redirect(reverse("user"))

#                 else:
#                     if int(request.POST.get('devicelimit'))-int(token_obj.dev_limit) == 1:
#                         token_obj.dev_limit = request.POST.get('devicelimit')
#                         messages.info(request,"{} Device Limit is Updated To {}".format(token_obj.email,token_obj.dev_limit))

#                     else:
#                         messages.info(request,"only one device can be add at a time")
#                         return redirect(reverse("user"))

#                 token_obj.save()
#                 return redirect(reverse("user"))
#             else:
#                 token_obj                   = User_data.objects.get(MobileNo=user)
#                 if int(request.POST.get('devicelimit')) < int(token_obj.dev_limit):
#                     if int(token_obj.dev_limit) - int(request.POST.get('devicelimit')) == 1:
#                         token_obj.dev_limit = int(request.POST.get('devicelimit'))
#                         dev_id            = token_obj.reg_dev_id
#                         dev               = json.decoder.JSONDecoder()
#                         device_id         = dev.decode(dev_id)
#                         device_id.pop()
#                         token_obj.reg_dev_id = json.dumps(device_id)
#                         messages.info(request,"{} Device Limit is Updated To {}".format(user,token_obj.dev_limit))

#                     else:
#                         messages.info(request,"only one device can be remove at a time")
#                         return redirect(reverse("user"))

#                 else:
#                     if int(request.POST.get('devicelimit'))-int(token_obj.dev_limit) == 1:
#                         token_obj.dev_limit = request.POST.get('devicelimit')
#                         messages.info(request,"{} Device Limit is Updated To {}".format(token_obj.MobileNo,token_obj.dev_limit))

#                     else:

#                         messages.info(request,"only one device can be add at a time")
#                         return redirect(reverse("user"))

#                 token_obj.save()
#                 return redirect(reverse("user"))
#         except Exception as e:
#             print(e)

#     def ResetUserDevice(self,request,user):
#         try:
#             if "@" in user:
#                 token_obj            = User_data.objects.get(email=user)
#                 dev_id               = token_obj.reg_dev_id
#                 dev                  = json.decoder.JSONDecoder()
#                 device_id            = dev.decode(dev_id)
#                 token_obj.dev_limit  = len(device_id)
#                 token_obj.reg_dev_id = json.dumps([])
#                 token_obj.save()

#                 messages.info(request,"{} Device Limit is Updated To {}".format(token_obj.email,token_obj.dev_limit))
#                 return redirect(reverse("user"))
#             else:
#                 token_obj            = User_data.objects.get(MobileNo=user)
#                 dev_id               = token_obj.reg_dev_id
#                 dev                  = json.decoder.JSONDecoder()
#                 device_id            = dev.decode(dev_id)
#                 token_obj.dev_limit  = len(device_id)
#                 token_obj.reg_dev_id = json.dumps([])
#                 token_obj.save()
#                 messages.info(request,"{} Device Limit is Updated To {}".format(token_obj.email,token_obj.dev_limit))
#                 return redirect(reverse("user"))
#         except Exception as e:
#             print(e)





''' password change '''
class change_password:
    def __init__(self):
        self.otp  = None
        self.name = None


    def forgot_password(self,request):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))
        if request.method == 'POST':
            try:
                data                          = request.POST

                if "@" in data.get('f_pass'):
                    messages.info(request,"Email Service Currently Not Available")
                    return redirect(reverse("forgot"))
                else:
                    if User_data.objects.filter(MobileNo = data.get('f_pass')).exists():
                        self.otp              = data.get('f_pass')
                        self.name             = self.otp
                        url                   = "https://verificationapi-v1.sinch.com/verification/v1/verifications"
                        payload               ="{\n  \"identity\": {\n  \"type\": \"number\",\n  \"endpoint\": \"+91%s\"\n  },\n  \"method\": \"sms\"\n}" % data.get('f_pass')
                        headers               = {
                            'Content-Type': 'application/json',
                            'Authorization': settings.API_SINCH_KEY,
                        }
                        response              = requests.request("POST", url, headers=headers, data=payload)
                        return redirect(reverse("otp_get"))
                    else:
                        messages.info(request,"Account Does Not Exists")
                        return redirect(reverse("forgot"))
            except Exception as e:
                print(e)
                messages.info(request,"No Internet Connection Available")
                return redirect(reverse("forgot"))

        return render(request,"forgot_password.html")


    def get_otp(self,request):
        if request.method == 'POST':
            try:
                data     = request.POST
                url      = "https://verificationapi-v1.sinch.com/verification/v1/verifications/number/+91%s" % self.otp
                payload  ="{ \"method\": \"sms\", \"sms\":{ \"code\": \"%s\" }}" % str(data.get('otp'))
                headers  = {
                'Content-Type': 'application/json',
                'Authorization': settings.API_SINCH_KEY,
                }
                response = requests.request("PUT", url, headers=headers, data=payload)
                datas    = response.json()
                if datas.get('status') == 'SUCCESSFUL':
                    return redirect(reverse("reset_password"))
                else:
                    messages.info(request,"you entered a invalid otp")
                    return redirect(reverse("otp_get"))
            except Exception as e:
                print(e)
        messages.info(request,"otp valid for 15 mins")
        return render(request,"token.html")

    def get(self,request):
        if request.user.is_authenticated:
            return redirect(reverse("dashboard"))
        return render(request,"new_password.html")


    def post(self,request):
        try:
            if request.user.is_authenticated:
                return redirect(reverse("dashboard"))

            data  = request.POST
            pwd   = data.get("pwd")
            c_pwd = data.get("pwd2")

            if pwd == c_pwd:

                if "@" in self.name:
                    sign_up = User_data.objects.get(email=self.name)

                else:
                    sign_up = User_data.objects.get(MobileNo=self.name)

                sign_up.Password = make_password(c_pwd)
                sign_up.save()
                user_obj         = User.objects.get(username=self.name)
                user_obj.set_password(c_pwd)
                user_obj.save()
                messages.info(request,"password change succesfully")
                return redirect(reverse("login"))

            else:
                return redirect(reverse("reset_password"))
        except Exception as e:
            print(e)



class geo_locate:
    def __init__(self):
        self.lati             = None
        self.longi            = None
        self.ip               = None


    def get_ip(self,request):
        get_ip                = request.META.get('HTTP_X_FORWARDED_FOR')
        if get_ip:
            self.ip           = get_ip.split(',')[0]
        else:
            self.ip           = request.META.get('REMOTE_ADDR')
        return self.ip


    def get_lat_long(self,request,ip=get_ip):
        get_ip                 = ip(self,request)
        api_key                = settings.GEO_LOCATION_KEY
        response               = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key="+api_key+"&ip_address="+get_ip)
        return redirect(reverse("dashboard"))



class vendor_service_add(APIView):
    def post(self,request,vendor_id=None):

        data                   =  request.POST
        if Service_data.objects.filter(user=request.user,service=data.get("service")).exists():
            messages.info(request,"service already exists")
            return redirect(reverse("add_service"))
        else:

            serv_ice               = Service_data()
            serv_ice.user           = request.user
            serv_ice.service       = data.get("service")
            serv_ice.service_prise = data.get("price")
            serv_ice.service_duration = data.get("duration")
            serv_ice.save()
            messages.info(request,"service added to your service list")
            return redirect(reverse("add_service"))

    def get(self,request):
        self.context = {}
        data = Service_data.objects.filter(user=request.user)
        self.session_id = request.session.get('name')
        signin_data    = User_data.objects.get(MobileNo=self.session_id)
        self.context['data'] = data
        self.context['users'] = signin_data.Name
        return render(request,"addService.html",self.context)



    def delete(self,request):
        data = request.POST.getlist('basic[]')
        serv = Service_data.objects.filter(user=request.user)
        for i in range(len(data)):
            value = serv.get(service=data[int(i)])
            value.delete()
        return redirect(reverse("add_service"))






class ManageVendorStaff(APIView):
    def __init__(self) -> None:
        self.context = {}
    def addstaff(self,request):
        queryset              = StaffDetails.objects.filter(user=request.user)
        self.session_id = request.session.get('name')
        signin_data    = User_data.objects.get(MobileNo=self.session_id)
        self.context["staff"] = queryset
        self.context["users"] = signin_data.Name
        return render(request,"staff.html",self.context)
    def post(self,request):
        data                        = request.POST
        staff_object                = StaffDetails()
        staff_object.user           = request.user
        staff_object.staffname          = data.get('name')
        staff_object.mobileno      = data.get('mobile')
        staff_object.email          = data.get('email')

        staff_object.save()
        return redirect("/staff")


    def showattendence(self,request):
        data                  = request.POST
        queryset              = StaffAttendence.objects.filter(date=dt.date.today(),user=request.user)
        self.context["staff_attendence"] = queryset
        return render(request,"showattendence.html",self.context)
    def add_attendence(self,request):
        data = request.POST
        attendence = StaffAttendence()
        attendence.user = request.user
        attendence.present_staff_Names = None
        attendence.absent_staff_names  = None
        attendence.date                = dt.date.today()
        attendence.save()

    def delete(self,request):
        data                  = request.POST.getlist('basic[]')
        stf = StaffDetails.objects.filter(user=request.user)
        for i in range(len(data)):
            value = stf.get(id=int(data[int(i)]))
            value.delete()
        return redirect("/staff")


    def edit_staff(self,request):
        pass

class ShowCashBackPoints(APIView):
    def __init__(self,) -> None:
        self.context = {}
    def get(self,request):
        queryset = CustomerPointTable.objects.filter(user=request.user)
        self.context['data'] = queryset
        return render(request,"cashback.html")

class UserSettings(APIView):
    def __init__(self) -> None:
        self.context = {}

    def showsettings(self,request):
        self.session_id = request.session.get('name')
        signin_data    = User_data.objects.get(MobileNo=self.session_id)
        self.context['users'] = signin_data.Name
        return render(request,"setting.html",self.context)

    def showuserinformation(self,request):
        user = User_data.objects.get(MobileNo=str(request.user))


        sallon_details = SallonProfile.objects.get(salon_name=user.Name)
        self.context['personal'] = sallon_details
        self.session_id = request.session.get('name')
        signin_data    = User_data.objects.get(MobileNo=self.session_id)
        self.context['users'] = signin_data.Name


        return render(request,"personal-information.html",self.context)

    def sallonprofile(self,request):
        user = User_data.objects.get(MobileNo=str(request.user))


        sallon_details = SallonProfile.objects.get(salon_name=user.Name)
        data = request.POST

        sallon_details.owner_name = data.get('owner-name')
        sallon_details.owner_email = data.get('email')
        sallon_details.owner_cgst_no = data.get('gst')
        sallon_details.owner_Panno = data.get('pan')
        sallon_details.owner_address = data.get('pincode')


        sallon_details.save()
        return redirect(reverse('setting'))


class Security(APIView):

    def show(self,request):
        self.context = {}
        self.session_id = request.session.get('name')
        signin_data    = User_data.objects.get(MobileNo=self.session_id)
        self.context['users'] = signin_data.Name
        return render(request,"security.html",self.context)

    def post(self,request):
        data = request.POST

        settings.SESSION_COOKIE_AGE = int(data.get('time'))

        return redirect("/security")

class businessdata(APIView):
    def __init__(self):
        self.queryset = invoice_data

    def get(self,request):
        #user_obj  =  User_data.objects.get(MobileNo=str(request.user))
        self.queryset = invoice_data.objects.all()
        serializer = Invoice_serializers(self.queryset,many=True)

        return Response({
            "data":serializer.data
        })
@api_view(['GET'])
def get_past_month(request):
    #user_obj  =  User_data.objects.get(MobileNo=str(request.user))
    queryset = invoice_data.objects.filter(month="02")
    serializer = Invoice_serializers(queryset,many=True)

    return Response({
        "data":serializer.data
    })
@api_view(['GET'])
def get_present_month(request):
    #user_obj  =  User_data.objects.get(MobileNo=str(request.user))
    queryset = invoice_data.objects.filter(month="03")
    serializer = Invoice_serializers(queryset,many=True)

    return Response({
        "data":serializer.data
    })





class Reports(APIView):
    def __init__(self) -> None:
        self.context = {}
    def get(self,request):
        inv_ = Invoice.objects.filter(vendor_name=request.user, date_field=dt.date.today())
        app_ = Apointment.objects.filter(user=request.user, booking_date=dt.date.today())
        total = 0
        for i in inv_:
          total = total + int(i.grand_total)
        self.context['inv'] = len(inv_)
        self.context['app_'] = len(app_)
        self.context['total_billing'] = total
        self.session_id = request.session.get('name')
        signin_data    = User_data.objects.get(MobileNo=self.session_id)
        self.context['users'] = signin_data.Name


        return render(request,"report.html",self.context)
    def post(self,request):
        inv_ = Invoice.objects.filter(vendor_name=request.user, date_field=request.POST.get('datetime'))

        self.context['inv'] = inv_
        self.context['date'] = request.POST.get('datetime')
        return render(request,"report_table.html",self.context)





class BusinessAnalyis(APIView):
    def __init__(self):
        self.context             = {}
        self.monthly_sales_query = None
        self.service_query       = None
        self.yearly_sales_query  = None
        self.month = None
        self.mon = dt.date.today()
        self.status = False
        self.context['status'] = self.status

    def month_ana(self,request):
        if request.user.is_authenticated:
            if request.session.get('sub_user') != None:
                    self.context['subuser'] = request.session.get('sub_user')
            if request.session.get('auth') != None:
                    self.context['auth'] = "123"
            self.session_id = request.session.get('name')
            signin_data    = User_data.objects.get(MobileNo=self.session_id)

            self.context['users'] = signin_data.Name



            self.month =  self.mon.month
            self.status = True
            self.context['status'] = self.status


            b = BusinessAnalysis.objects.filter(user=request.user,month=self.month)
            if b.exists():
                b.delete()

            a = Analysis(user= self.session_id)
            queryset = invoice_data.objects.filter(vendorname=str(request.user),month=self.month)
            serializer = Invoice_serializers(queryset,many=True)
            path = a.monthly_analysis(data={"data":serializer.data})

            # p = os.path.abspath(path)



            b = BusinessAnalysis()
            b.user = request.user
            b.monthly_analysis = f"analysis/analysis{path}"
            b.month= self.month
            b.save()

            self.monthly_sales_query = BusinessAnalysis.objects.filter(user=request.user,month=self.month)

            self.context['analysis_obj'] = self.monthly_sales_query[0]
            self.context['Dialoug'] = "Analysis month-"+str(b.month)
            return render(request,"business-lys.html",self.context)



    def query(self,request):
                if request.session.get('sub_user') != None:
                    self.context['subuser'] = request.session.get('sub_user')
                if request.session.get('auth') != None:
                    self.context['auth'] = "123"
                self.session_id = request.session.get('name')
                signin_data    = User_data.objects.get(MobileNo=self.session_id)

                self.context['users'] = signin_data.Name
                self.month =  request.session.get('bus-query')

                self.status = True
                self.context['status'] = self.status
                self.context['users'] = signin_data.Name



                self.monthly_sales_query = BusinessAnalysis.objects.filter(user=request.user,month=self.month)
                try:
                    self.context['analysis_obj'] = self.monthly_sales_query[0]
                except Exception as e:
                     print(e)


                self.context['Dialoug'] =  "Analysis month-"+str(self.month)




                return render(request,"business-lys.html",self.context)


    def get(self,request):
            if request.session.get('sub_user') != None:
                    self.context['subuser'] = request.session.get('sub_user')
            if request.session.get('auth') != None:
                    self.context['auth'] = "123"
            self.session_id = request.session.get('name')
            signin_data    = User_data.objects.get(MobileNo=self.session_id)

            self.context['users'] = signin_data.Name
            self.context['Dialoug'] =  "Select Analysis"




            return render(request,"business-lys.html",self.context)





def logout(request):
    user = User_data.objects.get(MobileNo=str(request.user))
    user.dev_limit = 0
    user.save()
    auth.logout(request)
    return redirect(reverse("login"))

def forgot_backs(request):
    return redirect("/login")
def otp_backs(request):
    return redirect("/forgot_password")

def login_render(request):
    return redirect("login")
def logout(request):
    user = User_data.objects.get(MobileNo=str(request.user))
    user.dev_limit = 0
    user.save()
    auth.logout(request)
    return redirect(reverse("login"))

