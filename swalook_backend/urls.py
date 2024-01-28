"""swalook_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path
from django.contrib import admin
from django.urls import path
from swalook.views import *
from django.conf import settings
from django.conf.urls.static import static
security        = Security()
bill_invoice    = generate_bill()
user_ver        = user_verify()
dashboards      = dashboard()
appointments    = appointmnet()
v_service       = vendor_service_add()
#token = generate_token()
#token_verify = verify_token()
#session_admin   = set_session_admin()
change_pwd      = change_password()
geo_loc         = geo_locate()
setting         = UserSettings()
staff           = ManageVendorStaff()
api = businessdata()
rep = Reports()
admins = AdminDashboard()
# admins = AdminDashboard()

bus = BusinessAnalyis()
urlpatterns     = [
    # api urls
   #path("api/",Route.as_view()),
   #path("api/user/signup/",user_verify.as_view()),
   #path("api/user/login/",api_login.as_view()),

   #path("api/user/login/<_token_>/",api_login.as_view()),
   #path("api/user/user_data/<vendor_id>/<device_ids>",dashboards.as_view()),

   #path("api/user/add/appointment/<vendor_name>/",appointments.as_view()),
   #path("api/user/add/invoice/<vendor_name>/",bill_invoice.post_bill),

   #path("api/user/appointment/search/<contact_number>",search_appointment.as_view()),
   path('admin_swa_look/', admin.site.urls),
   path('api/user/invoice_data/',api.as_view()),
   path('api/user/invoice_data/past_month/',get_past_month),
   path('api/user/invoice_data/present_month/',get_present_month),
   # application urls

   # signup & login urls
   path("user/dashboard",   dashboard.as_view(),   name= "dashboard"),
   path("user/<navs>/",     dashboards.nav,        name= ""),
   path("signup/login/",    login_render,          name= "signup-login"),
   path("",           login_view_Create,     name= "login"),
   path("authenticate",           login_view_Create,     name= "login-verify-url"),
   path("createnew/",       user_verify.as_view(), name= "create_account"), # private_url
   #path("createnew/",user_verify.as_view(), name= "signup/create-new"), # private_url
   path("user/logout/user",logout,name="logout"),

   # dashboard & serviceadd urls
   path("login/",                           signup_page   ,                  name= "signup"),
   path("admin/",                           admins.as_view(),  name= "admin"),
   path("invoice/add/",                  bill_invoice.add_extra_services,                  name= ""),
   path("service/",             vendor_service_add.as_view(), name= "add_service"),
   path("service/logout/users", logout),
   path("service/service_data/",v_service.post,               name= "add_data"), # private url
   path("service/delete/",v_service.delete,               name= ""), # private url
   path("service/<navs>/",      dashboards.nav,               name= "add_service_nav"), # private url

   # login verification & forgot password urls & otp sent urls
   path("login/verify/password",       change_pwd.forgot_password, name= "for_got_password"),
   #path("signup/login/verify/password",change_pwd.forgot_password, name="signup_forgot_password"),
   path("forgot_password",             change_pwd.forgot_password, name="forgot"),
   path("reset_password",              change_pwd.get,             name= "reset_password"),
   path("set_password/",               change_pwd.post,            name= "set_password"), # private url
   path("otp-sent/",                   change_pwd.forgot_password, name= "otp_password"), # private url
   path("enter_otp/",                  change_pwd.get_otp,         name= "otp_get"),
   path("verify/",                     change_pwd.get_otp,         name= "otp_verify"), # private url

   # appointments and search urls and add service urls
   path("appointment/",                     appointments.get,             name= "appointment"),
   path("appointment/logout/users",         logout,),
   path("appointment/save/",                appointments.post,            name= "ap_save"), # private_url
   path("appointment/<navs>/",              dashboards.nav,               name= "appointment_nav"), # private url
   path("search/",                          dashboards.search_result,     name= "search"), # private_url
   path("data/",                            dashboards.show_search,       name= "search_data") ,
   path("data/logout/users",                logout,) ,
   path("data/add/service/",                vendor_service_add.as_view(), name= "search_data_page_nav") ,
   path("data/<navs>/",                     dashboards.nav,               name= "search_nav"), # private_url
   path("user/app/edit/<id>/<time>/<date>", dashboards.show_page_edit,    name= "ap_edit"), # private_url
   path("user/app/edit/<id>/<time>/<date>/logout/users", logout), # private_url
   path("data/user/app/edit/<id>/<time>/<date>", dashboards.show_page_edit,    ), # private_url
   path("data/user/app/edit/<id>/<time>/<date>/logout/users",logout), # private_url
   path("app/edit/<id>/<time>/<date>",      dashboards.show_page_edit,    name= "ap____edit"), # private_url
   path("app/edit/<id>/<time>/<date>/logout/users",logout), # private_url
   path("data/app/edit/<id>/<time>/<date>",      dashboards.show_page_edit,    ), # private_url
   path("data/app/edit/<id>/<time>/<date>/logout/users",logout), # private_url
   path("app/edit/<id>/<time>/update/",     dashboards.show_page_edit,    name= "edit_app"), # private_url # private_url
   path("data/app/edit/<id>/<time>/update/",     dashboards.show_page_edit,    ), # private_url # private_url
   path("user/app/delete/<id>/",            dashboards.deleteappointment, name= "del_ap"), # private_url # private_url
   path("data/user/app/delete/<id>/",            dashboards.deleteappointment, ), # private_url # private_url
   path("app/edit/<id>/<time>/<date>/<navs>",dashboards.nav,              name= ""), # private_url # private_url
   path("data/app/edit/<id>/<time>/<date>/<navs>",dashboards.nav,              ), # private_url # private_url


   # bill generate & invoice & pdf urls
   path("generatebill/create/invoice/",bill_invoice.post_bill,       name= "invoice"), # private url
   path("invoice/",                    bill_invoice.show_invoice,    name= "invoic"),
   path("invoice/finalinvoice",        bill_invoice.show_final_invoice,    name= "invoice_"),
   path("invoice/invoice/update",      bill_invoice.show_invoice,    name= "invoice_update"),
   path("invoice/<navs>/",             dashboards.nav,               name= "invoice_nav"),
   path("back",                        bill_invoice.back,            name= "back"),
   path("enter_otp/_back/",            otp_backs,                    name= "otp_back"),
   path("_back/",                      forgot_backs,                 name= "forgot_back"),

   path("login/verify/_back/",         forgot_backs,                 name= "login_back"),
   path("generatebill/",               bill_invoice.as_view(),       name= "generate_bill"),
   path("generatebill/logout/users",    logout,),
   path("generate_bill/",              bill_invoice.as_view(),       name= "generatebill"),
   path("generate_bill/logout/users",   logout,),
   path("generatebill/<navs>/",        dashboards.nav,               name= "generate_bill_nav"), # private url
   path("generate_bill/<navs>/",       dashboards.nav,               name= "generatebill_nav"), # private url
   path("invoice/invoice_/<slno>/",    bill_invoice.download_invoice,name= "pdf"),  # private url
   #path("invoice/send_msg/",          bill_invoice.share_pdf,       name= "share_pdf"), # private url

   # index & device manage & ip geo location urls

   #path("generate_token/",token.get), # private url
   #path("token/",token_verify.show_token),
   #path("index/",                      show_landing_page,               name= "index"),
   #path("index/<navs>",                dashboards.nav,                  name= "index_nav"), # private url
#    path("user_manager/",               session_admin.show_session_page,  name= "user"), # user device limit setting url
#    path("user_manager/update/<user>/", session_admin.save_device_limit,  name= "update_user"), # private url
#    path("user_manager/reset/<user>/", session_admin.ResetUserDevice,     name= "reset_user"), # private url
#    #path("ip/",                         geo_loc.get_lat_long,            name= "ip"), # private url

    # settings

    path("setting",setting.showsettings,name="setting",),
    path("setting/logout/users",logout,),
    path("reports/",rep.get,name="",),
    path("reports/logout/users",logout),

    path("reports/showall/",rep.post,name="",),
    path("reports/showall/logout/users",logout),
    path("reports/<navs>/",dashboards.nav,name="",),
    path("reports/showall/<navs>/",dashboards.nav,name="",),
    path("security/",security.show,),
    path("security/logout/users",logout),
    path("security/<navs>/",dashboards.nav,),
    path("information/",setting.showuserinformation),
    path("information/logout/users",logout),
    path("information/<navs>/",dashboards.nav),
    path("staff/",staff.addstaff),
    path("staff/logout/users",logout),
    path("staff/<navs>/",dashboards.nav),
    path("staff/add/staff/",staff.post),
    path("staff/delete/staff/",staff.delete),
    path("information/update/user/",setting.sallonprofile),
    path("adduser/",adduserstaff,name="user-staff"),
    path("adduser/logout/users",logout),
    path("adduser/user/add",adduserstaff,),
    path("adduser/user/delete",deleteuserstaff,),

    path("adduser/<navs>/",dashboards.nav,name=""),


     #business analysis
    path("business-analysis/",bus.get,name="business"),
    path("business-analysis/logout/users",logout,name=""),
    path("monthly-analysis/",bus.month_ana,name="monthly"),
    path("monthly-analysis/logout/users",logout,name=""),
    path("business-query/",bus.query,name="query"),
    path("business-query/logout/users",logout,name=""),

    path("monthly-analysis/<navs>/",dashboards.nav,name=""),
    path("business-analysis/<navs>/",dashboards.nav,name=""),
    path("business-query/<navs>/",dashboards.nav,name=""),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)