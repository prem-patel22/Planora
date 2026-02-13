from django.urls import path, re_path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('index1/', views.index1, name='index1'),
    
    # Authentication
    path('login/', views.user_login, name='user_login'),
    path('login_process/', views.login_process, name='login_process'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_login/', views.admin_login, name='admin_login'),
    
    # Registration
    path('register/', views.register, name='register'),
    path('register-login/', views.register_login, name='register_login'),
    path('register_process/', views.register_process, name='register_process'),
    path('register_admin/', views.register_admin, name='register_admin'),
    
    # Venue search and management
    path('search-venues/', views.search_venues, name='search_venues'),
    path('search_results/', views.search_results, name='search_results'),
    path('all-venues/', views.all_venues, name='all_venues'),
    path('add_venue/', views.add_venue, name='add_venue'),
    path('edit_venue/', views.edit_venue, name='edit_venue'),
    path('update_venue/', views.update_venue, name='update_venue'),
    path('delete_venue/', views.delete_venue, name='delete_venue'),
    path('fetch_venue_location/', views.fetch_venue_location, name='fetch_venue_location'),
    path('fetch_venue_details/', views.fetch_venue_details, name='fetch_venue_details'),
    
    # Booking system
    path('book-venue/', views.book_venue, name='book_venue'),
    path('your-booking/', views.your_booking, name='your_booking'),
    path('view_booking/', views.view_booking, name='view_booking'),
    path('cancel-booking/', views.cancel_booking, name='cancel_booking'),
    path('update_booking/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('rescheduling/<int:booking_id>/', views.rescheduling, name='rescheduling'),
    path('check-availability/', views.check_availability, name='check-availability'),
    path('booking-availability/', views.booking_availability, name='booking_availability'),
    
    # NEW: Enhanced booking system with catering/decoration
    # Add BOTH names for backward compatibility
    path('venue/<int:venue_id>/', views.venue_details, name='venue_details'),           # With underscore (preferred)
    path('venue-details/<int:venue_id>/', views.venue_details, name='venue-details'),   # With hyphen (for backward compatibility)
    path('create-booking/', views.create_booking, name='create_booking'),
    path('booking-confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('get-user-bookings/', views.get_user_bookings, name='get_user_bookings'),
    
    # Information pages
    path('cancellation/', views.cancellation, name='cancellation'),
    path('images/', views.images, name='images'),
    path('price/', views.price, name='price'),
    path('amenities/', views.amenities, name='amenities'),
    path('notification/', views.notification, name='notification'),
    path('modifying-details/', views.modifying_details, name='modifying_details'),
    
    # Reviews
    path('reviews/', views.reviews, name='reviews'),
    path('get_reviews/', views.get_reviews, name='get_reviews'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)