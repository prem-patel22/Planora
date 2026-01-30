from django.urls import path, re_path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('register-login/', views.register_login, name='register_login'),
    path('search-venues/', views.search_venues, name='search_venues'),
    path('book-venue/', views.book_venue, name='book_venue'),
    path('booking-availability/', views.booking_availability, name='booking_availability'),
    path('cancellation/', views.cancellation, name='cancellation'),
    path('images/', views.images, name='images'),
    path('price/', views.price, name='price'),
    path('reviews/', views.reviews, name='reviews'),
    path('amenities/', views.amenities, name='amenities'),
    path('edit_venue/', views.edit_venue, name='edit_venue'),
    path('notification/', views.notification, name='notification'),
    path('view_booking/', views.view_booking, name='view_booking'),
    path('modifying-details/', views.modifying_details, name='modifying_details'),
    path('register_process/', views.register_process, name='register_process'),
    path('login_process/', views.login_process, name='login_process'),
    path('add_venue.html/', views.add_venue, name='add_venue'),
    path('search_results/', views.search_results, name='search_results'),
    path('register_admin/', views.register_admin, name='register_admin'),
    path('check-availability/', views.check_availability, name='check-availability'),
    path('book-venue/', views.book_venue, name='book-venue'),
    path('rescheduling/', views.rescheduling, name='rescheduling'),
    path('your-booking/', views.your_booking, name='your_booking'),
    path('cancel-booking/', views.cancel_booking, name='cancel_booking'),
    path('update_booking/', views.update_booking, name='update_booking'),
    path('search-venues/', views.fetch_venue_location, name='fetch_venue_location'),
    path('edit_venue/', views.edit_venue, name='edit_venue'),
    path('update_venue/', views.update_venue, name='update_venue'),
    path('all-venues/', views.all_venues, name='all_venues'),
    path('view_booking.html/', views.view_booking, name='view_booking'),
    path('get_reviews.html/', views.get_reviews, name='get_reviews'),
    path('index1/', views.index1, name='index1'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('delete_venue/', views.delete_venue, name='delete_venue'),
    
    # NEW URL: Venue Details with Catering and Decoration
    path('venue/<int:venue_id>/', views.venue_details, name='venue-details'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)