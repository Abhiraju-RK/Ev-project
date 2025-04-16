from django.urls import path
from . import views

urlpatterns = [
    path('staff_home',views.staff_home,name='staff_home'),
    path('staff_register',views.staff_register,name='staff_register'),
    path('staff_login',views.staff_login,name='staff_login'),
    path('staff_logout',views.staff_logout,name='staff_logout'),
    path('staff_profile',views.staff_profile,name='staff_profile'),

    path('station_list',views.station_list,name='station_list'),
    path('add_station',views.add_station,name='add_station'),
    path('edit_station/<int:station_id>/', views.edit_station, name='edit_station'),
    path('add_slot',views.add_slot,name='add_slot'),
    path('slot_list/<int:station_id>/',views.slot_list,name='slot_list'),
    path('slot_bookings',views.slot_bookings,name='slot_bookings'),
]
