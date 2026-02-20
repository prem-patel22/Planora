from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Customer, Venue, Booking, Review, CateringMenu, DecorationPackage, MenuItemImage, DecorationImage
from .forms import VenueForm
from django.http import JsonResponse, HttpResponseServerError
from django.utils import timezone
from datetime import datetime
from django.db.models import Count  # ADD THIS IMPORT
import json

def logout_view(request):
    logout(request)
    return redirect('home')

def amenities(request):
    return render(request, 'amenities.html')

def booking_availability(request):
    return render(request, 'booking-availability.html')

def cancellation(request):
    return render(request, 'cancellation.html')

def images(request):
    return render(request, 'images.html')

def index(request):
    venues_with_images = Venue.objects.exclude(image__isnull=True).exclude(image__exact='')
    welcome_message = f"Welcome {request.user.username} ..." if request.user.is_authenticated else ""
    return render(request, 'index.html', {'venues_with_images': venues_with_images, 'welcome_message': welcome_message})

def index1(request):
    venues_with_images = Venue.objects.exclude(image__isnull=True).exclude(image__exact='')
    welcome_message = f"Welcome {request.user.username} ..." if request.user.is_authenticated else ""
    return render(request, 'index1.html', {'venues_with_images': venues_with_images, 'welcome_message': welcome_message})

def user_login(request):
    return render(request, 'login.html')

def modifying_details(request):
    return render(request, 'modifying-details.html')

def notification(request):
    return render(request, 'notification.html')

def price(request):
    return render(request, 'price.html')

def register_process(request):
    if request.method == 'POST':
        username = request.POST.get('newUsername')
        password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        email = request.POST.get('email')
        phoneNo = request.POST.get('phoneNo')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return render(request, 'register-login.html')
            else:
                user = User.objects.create_user(username=username, password=password)
                Customer.objects.create(
                    name=user,
                    email=email,
                    phoneNo=phoneNo,
                )
                messages.success(request, f"Registration successful! Your username is: {username}")
                return redirect('register_login')
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register-login.html')

    return render(request, 'register-login.html')

def login_process(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    return render(request, 'login.html')

def register_admin(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        phoneNo = request.POST.get('MobileNumber')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username is already taken.')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=name, password=password)
                user.is_staff = True
                user.save()
                messages.success(request, "Admin registered successfully. Please log in.")
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')
    return render(request, 'register.html')

def register_login(request):
    return render(request, 'register-login.html')

def register(request):
    return render(request, 'register.html')

def reviews(request):
    if request.method == 'POST':
        reviewer_name = request.POST.get('name')
        review_text = request.POST.get('review-text')
        review = Review.objects.create(reviewer_name=reviewer_name, review_text=review_text)
        return JsonResponse({
            'name': reviewer_name,
            'review_text': review_text,
            'created_at': review.created_at.strftime('%Y-%m-%d')
        })
    else:
        reviews = Review.objects.all()
        return render(request, 'reviews.html', {'reviews': reviews})

def view_booking(request):
    bookings = Booking.objects.all()
    return render(request, 'view_booking.html', {'bookings': bookings})

def home(request):
    return render(request, 'home.html')

def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venue added successfully!')
            return redirect('all_venues')
        else:
            print(form.errors)
            messages.error(request, 'Error adding venue. Please correct the form below.')
    else:
        form = VenueForm()
    return render(request, 'add_venue.html', {'form': form})

def all_venues(request):
    venues = Venue.objects.all()
    return render(request, 'all_venues.html', {'venues': venues})

def search_results(request):
    if request.method == 'GET':
        location = request.GET.get('location')
        venues = Venue.objects.filter(location=location)
        return render(request, 'search_results.html', {'venues': venues})

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('index1')
        else:
            messages.error(request, "Invalid username or password, or you lack admin privileges.")
            return render(request, 'login.html')
    return render(request, 'login.html')

def check_availability(selected_date):
    return not Booking.objects.filter(date=selected_date).exists()

def book_venue(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        selected_date_str = request.POST.get('date')
        booking_price = request.POST.get('booking-price')
        venue_name = request.POST.get('venue-name')

        if not selected_date_str:
            messages.error(request, "Date is required.")
            return redirect('book_venue')

        try:
            selected_datetime = datetime.strptime(selected_date_str, '%Y-%m-%d')
            selected_datetime = timezone.make_aware(selected_datetime)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()})

        if selected_datetime <= timezone.now():
            messages.error(request, "Please select a future date.")
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()})

        if Booking.objects.filter(date=selected_datetime, venue__venue_name=venue_name).exists():
            messages.error(request, "Venue is already booked for the selected date. Please choose another date.")
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()})

        user = request.user

        try:
            customer = Customer.objects.get(name=user)
            venue = Venue.objects.get(venue_name=venue_name)
            Booking.objects.create(
                date=selected_datetime,
                booking_price=booking_price,
                customer=customer,
                venue=venue
            )
            messages.success(request, 'Venue booked successfully!')
            return redirect('your_booking')
        except Customer.DoesNotExist:
            messages.error(request, 'Customer does not exist.')
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()})
        except Venue.DoesNotExist:
            messages.error(request, 'Selected venue does not exist.')
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()})
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()})

    venues = Venue.objects.all()
    return render(request, 'book-venue.html', {'venues': venues})

@login_required
def rescheduling(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        new_date_str = request.POST.get('new_date')
        try:
            new_date = datetime.strptime(new_date_str, '%Y-%m-%d')
            new_date = timezone.make_aware(new_date)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'rescheduling.html', {'booking_id': booking.pk, 'booking': booking})

        if Booking.objects.filter(venue=booking.venue, date=new_date).exclude(pk=booking.pk).exists():
            messages.error(request, "Venue is already booked for the selected date.")
            return render(request, 'rescheduling.html', {'booking_id': booking.pk, 'booking': booking})

        booking.date = new_date
        booking.save()
        messages.success(request, "Booking rescheduled successfully.")
        return redirect('your_booking')
    return render(request, 'rescheduling.html', {'booking_id': booking.pk, 'booking': booking})

@login_required
def your_booking(request):
    try:
        user = request.user
        customer = Customer.objects.get(name=user)
        bookings = Booking.objects.filter(customer=customer).order_by('-date')
        
        for booking in bookings:
            booking.formatted_date = booking.date.strftime('%B %d, %Y')
            booking.formatted_price = f"₹{int(booking.booking_price):,}"
            if hasattr(booking, 'selected_catering_price') and booking.selected_catering_price:
                booking.formatted_catering_price = f"₹{int(booking.selected_catering_price):,}"
            if hasattr(booking, 'selected_decoration_price') and booking.selected_decoration_price:
                booking.formatted_decoration_price = f"₹{int(booking.selected_decoration_price):,}"
        
        context = {
            'bookings': bookings,
            'has_bookings': bookings.exists()
        }
        return render(request, 'your-booking.html', context)
        
    except Customer.DoesNotExist:
        context = {
            'message': 'You have not made any bookings yet.',
            'has_bookings': False
        }
        return render(request, 'your-booking.html', context)
    except Exception as e:
        print(f"Error in your_booking: {e}")
        context = {
            'message': 'An error occurred while fetching your bookings.',
            'has_bookings': False
        }
        return render(request, 'your-booking.html', context)

def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        new_date_str = request.POST.get('date')
        try:
            new_date = datetime.strptime(new_date_str, '%Y-%m-%d')
            new_date = timezone.make_aware(new_date)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'update_booking.html', {'booking_id': booking.pk, 'booking': booking})

        if Booking.objects.filter(venue=booking.venue, date=new_date).exclude(pk=booking.pk).exists():
            messages.error(request, "Date is not available. Please choose another date.")
            return render(request, 'update_booking.html', {'booking_id': booking.pk, 'booking': booking})

        booking.date = new_date
        booking.save()
        messages.success(request, "Booking updated successfully!")
        return redirect('your_booking')
    return render(request, 'update_booking.html', {'booking_id': booking.pk, 'booking': booking})

@login_required
def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = Booking.objects.get(booking_id=booking_id)
            if booking.customer.name == request.user:
                booking.delete()
                return JsonResponse({
                    'success': True,
                    'message': 'Booking canceled successfully!'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'You do not have permission to cancel this booking.'
                })
        except Booking.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Booking not found.'
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def fetch_venue_location(request):
    venues = Venue.objects.all()
    return render(request, 'search_venues.html', {'venues': venues})

# ===== UPDATED SEARCH_VENUES FUNCTION =====
def search_venues(request):
    """View for the search venues page with most booked venues section"""
    locations = Venue.objects.values_list('location', flat=True).distinct()
    
    # Get most booked venues (top 6)
    most_booked_venues = Venue.objects.annotate(
        booking_count=Count('booking')
    ).order_by('-booking_count')[:6]
    
    context = {
        'locations': locations,
        'most_booked_venues': most_booked_venues,
    }
    return render(request, 'search-venues.html', context)
# ==========================================

def edit_venue(request):
    venue_name = request.POST.get('venue_name')
    venue = get_object_or_404(Venue, venue_name=venue_name)
    return render(request, 'edit_venue.html', {'venue': venue})

def update_venue(request):
    if request.method == 'POST':
        print("In update_venue if")
        venue_name = request.POST.get('venue_name')
        try:
            venue = Venue.objects.get(venue_name=venue_name)
        except Venue.DoesNotExist:
            return HttpResponseServerError("Venue with name '{}' does not exist.".format(venue_name))

        venue.location = request.POST.get('location')
        venue.capacity = request.POST.get('capacity')
        venue.amenities = request.POST.get('amenities')
        venue.pricing = request.POST.get('pricing')
        venue.availability = request.POST.get('availability')
        venue.image = request.FILES.get('image')
        venue.save()

        messages.success(request, 'Venue updated successfully!')
        return redirect('all_venues')
    else:
        messages.error(request, 'Error updating venue. Please try again.')
        pass

def fetch_venue_details(request):
    if request.method == 'GET' and 'venue_name' in request.GET:
        venue_name = request.GET.get('venue_name')
        try:
            venue = Venue.objects.get(venue_name=venue_name)
        except Venue.DoesNotExist:
            return JsonResponse({'error': 'Venue not found'})
        data = {
            'name': venue.venue_name,
            'location': venue.location,
            'capacity': venue.capacity,
            'amenities': venue.amenities,
            'pricing': venue.pricing,
            'availability': venue.availability,
        }
        if venue.image:
           data['image_url'] = venue.image.url
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid request'})

def get_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'get_reviews.html', {'reviews': reviews})

def delete_venue(request):
    if request.method == 'POST':
        venue_name = request.POST.get('venue_name')
        try:
            venue = Venue.objects.get(venue_name=venue_name)
            venue.delete()
            messages.success(request, 'Venue deleted successfully!')
        except Venue.DoesNotExist:
            return HttpResponseServerError(f"Venue with name '{venue_name}' does not exist.")
        return redirect('all_venues')
    else:
        messages.error(request, 'Invalid request to delete venue.')
        return redirect('all_venues')

# Venue Details with Catering and Decoration
def venue_details(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    
    catering_menus = CateringMenu.objects.filter(
        venue=venue,
        is_available=True
    ).prefetch_related('images')
    
    decoration_packages = DecorationPackage.objects.filter(
        venue=venue,
        is_available=True
    ).prefetch_related('images')
    
    context = {
        'venue': venue,
        'catering_menus': catering_menus,
        'decoration_packages': decoration_packages,
    }
    
    return render(request, 'venue_details.html', context)

# Create Booking with Catering and Decoration
@login_required
def create_booking(request):
    if request.method == 'POST':
        try:
            venue_id = request.POST.get('venue_id')
            venue_name = request.POST.get('venue_name')
            venue_price_str = request.POST.get('venue_price', '0')
            selected_catering = request.POST.get('selected_catering', 'No catering selected')
            selected_catering_price_str = request.POST.get('selected_catering_price', '0')
            selected_decoration = request.POST.get('selected_decoration', 'No decoration selected')
            selected_decoration_price_str = request.POST.get('selected_decoration_price', '0')
            booking_date = request.POST.get('booking_date')
            event_type = request.POST.get('event_type', 'Not specified')
            guest_count = request.POST.get('guest_count', '0')
            special_requests = request.POST.get('special_requests', '')
            
            try:
                venue_price = int(venue_price_str.replace(',', '')) if venue_price_str else 0
                selected_catering_price = int(selected_catering_price_str.replace(',', '')) if selected_catering_price_str else 0
                selected_decoration_price = int(selected_decoration_price_str.replace(',', '')) if selected_decoration_price_str else 0
            except ValueError:
                venue_price = 0
                selected_catering_price = 0
                selected_decoration_price = 0
            
            total_price = venue_price + selected_catering_price + selected_decoration_price
            
            customer = Customer.objects.get(name=request.user)
            venue = Venue.objects.get(id=venue_id)
            
            booking_datetime = datetime.strptime(booking_date, '%Y-%m-%d')
            booking_datetime = timezone.make_aware(booking_datetime)
            
            if Booking.objects.filter(venue=venue, date=booking_datetime).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Venue is already booked for the selected date.'
                })
            
            booking = Booking.objects.create(
                date=booking_datetime,
                booking_price=total_price,
                customer=customer,
                venue=venue,
                selected_catering=selected_catering,
                selected_catering_price=selected_catering_price,
                selected_decoration=selected_decoration,
                selected_decoration_price=selected_decoration_price,
                event_type=event_type,
                guest_count=guest_count,
                special_requests=special_requests,
                booking_status='confirmed'
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Booking created successfully',
                'booking_id': booking.booking_id
            })
            
        except Customer.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Customer profile not found. Please complete your profile.'
            })
        except Venue.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Venue not found.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Get user bookings for AJAX
@login_required
def get_user_bookings(request):
    try:
        user = request.user
        customer = Customer.objects.get(name=user)
        bookings = Booking.objects.filter(customer=customer).order_by('-date')
        
        bookings_data = []
        for booking in bookings:
            booking_dict = {
                'id': booking.booking_id,
                'venue_name': booking.venue.venue_name,
                'venue_location': booking.venue.location,
                'booking_date': booking.date.strftime('%Y-%m-%d'),
                'formatted_date': booking.date.strftime('%B %d, %Y'),
                'total_price': str(booking.booking_price),
                'formatted_price': f"₹{int(booking.booking_price):,}",
                'selected_catering': booking.selected_catering if hasattr(booking, 'selected_catering') and booking.selected_catering else 'Not selected',
                'selected_catering_price': str(booking.selected_catering_price) if hasattr(booking, 'selected_catering_price') and booking.selected_catering_price else '0',
                'formatted_catering_price': f"₹{int(booking.selected_catering_price):,}" if hasattr(booking, 'selected_catering_price') and booking.selected_catering_price and int(booking.selected_catering_price) > 0 else 'Not selected',
                'selected_decoration': booking.selected_decoration if hasattr(booking, 'selected_decoration') and booking.selected_decoration else 'Not selected',
                'selected_decoration_price': str(booking.selected_decoration_price) if hasattr(booking, 'selected_decoration_price') and booking.selected_decoration_price else '0',
                'formatted_decoration_price': f"₹{int(booking.selected_decoration_price):,}" if hasattr(booking, 'selected_decoration_price') and booking.selected_decoration_price and int(booking.selected_decoration_price) > 0 else 'Not selected',
                'event_type': booking.event_type if hasattr(booking, 'event_type') and booking.event_type else 'Not specified',
                'guest_count': booking.guest_count if hasattr(booking, 'guest_count') else '0',
                'booking_status': booking.booking_status if hasattr(booking, 'booking_status') else 'confirmed',
            }
            bookings_data.append(booking_dict)
        
        return JsonResponse({
            'success': True,
            'bookings': bookings_data
        })
        
    except Customer.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Customer not found'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })

# Booking Confirmation Page
@login_required
def booking_confirmation(request):
    """Show booking confirmation page"""
    if request.method == 'GET':
        try:
            venue_id = request.GET.get('venue_id')
            if not venue_id:
                messages.error(request, 'Venue ID is required.')
                return redirect('search_venues')
                
            venue = Venue.objects.get(id=venue_id)
            
            selected_catering_price_str = request.GET.get('selected_catering_price', '0')
            selected_decoration_price_str = request.GET.get('selected_decoration_price', '0')
            
            try:
                selected_catering_price = int(selected_catering_price_str) if selected_catering_price_str else 0
                selected_decoration_price = int(selected_decoration_price_str) if selected_decoration_price_str else 0
            except ValueError:
                selected_catering_price = 0
                selected_decoration_price = 0
            
            context = {
                'venue': venue,
                'selected_catering': request.GET.get('selected_catering', 'Not selected'),
                'selected_catering_price': selected_catering_price,
                'selected_decoration': request.GET.get('selected_decoration', 'Not selected'),
                'selected_decoration_price': selected_decoration_price,
                'booking_date': request.GET.get('booking_date'),
                'event_type': request.GET.get('event_type', 'Not specified'),
                'guest_count': request.GET.get('guest_count', 0),
                'special_requests': request.GET.get('special_requests', ''),
            }
            
            try:
                venue_price = int(str(venue.pricing).replace(',', ''))
            except ValueError:
                venue_price = 0
                
            total = venue_price + context['selected_catering_price'] + context['selected_decoration_price']
            context['total_price'] = total
            
            return render(request, 'booking_confirmation.html', context)
            
        except Venue.DoesNotExist:
            messages.error(request, 'Venue not found.')
            return redirect('search_venues')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('search_venues')
    
    return redirect('search_venues')