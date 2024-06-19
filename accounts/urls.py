from django.urls import path
from .import views

urlpatterns=[
     path('',views.index, name='index'),
     path('register/',views.register, name='register'),
     path('student_register/',views.student_register.as_view(), name='student_register'),
     path('warden_register/',views.warden_register.as_view(), name='warden_register'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('student_land/',views.student_land, name='student_land'),
     path('warden_land/',views.warden_land, name='warden_land'),
     # -----------------other link--------------------
     #the line below I added to make warden login work for some views like add dues - error message below:
     #Reverse for 'warden_login' not found. 'warden_login' is not a valid view function or pattern name
     path('login/',views.login_request, name='warden_login'),
     #end of line added for warden_login
     path('warden_dues/', views.warden_dues, name='warden_dues'),
     path('warden_add_due/', views.warden_add_due, name='warden_add_due'),
     path('warden_remove_due/', views.warden_remove_due, name='warden_remove_due'),
     path('warden_student_list/', views.warden_student_list, name='warden_student_list'),
     path('warden_student_list/change_student_details/<slug:enrollment_no>', views.change_student_details, name='change_student_details'),
     path('warden_student_list/clear_room_details/<slug:enrollment_no>', views.clear_room_details, name='clear_room_details'),
     path('hostels/<slug:hostel_name>/', views.hostel_detail_view, name='hostel'),
     path('login/edit/', views.edit, name='edit'),
     path('login/select/', views.select, name='select'),
     path('register/login/edit/', views.edit, name='update'),
     path('login/edit/', views.edit, name='profile'),
]