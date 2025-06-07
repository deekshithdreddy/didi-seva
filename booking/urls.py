from django.urls import path
from . import views

urlpatterns = [
    # Root URL pattern
    path('', views.landing_page, name='landing'),
    
    # User related URLs
    path('user/register/', views.user_register, name='user_register'),
    path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user/bookings/', views.user_bookings, name='user_bookings'),
    
    # Maid related URLs
    path('maid/register/', views.maid_register, name='maid_register'),
    path('maid/login/', views.maid_login, name='maid_login'),
    path('maid/logout/', views.maid_logout, name='maid_logout'),
    path('maid/dashboard/', views.maid_dashboard, name='maid_dashboard'),
    
    # Booking related URLs
    path('maid-listings/', views.maid_listings, name='maid_listings'),
    path('maid-details/<int:maid_id>/', views.maid_details, name='maid_details'),
    path('book-maid/<int:maid_id>/', views.book_maid, name='book_maid'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('accept-booking/<int:booking_id>/', views.accept_booking, name='accept_booking'),
    path('reject-booking/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    
    # Manager related URLs
    path('manager/login/', views.manager_login, name='manager_login'),
    path('manager/register/', views.manager_register, name='manager_register'),
]
