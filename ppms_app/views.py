from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Restore this line with all models
from .models import Customer, Venue, Booking, Review, CateringMenu, DecorationPackage, MenuItemImage, DecorationImage
from .forms import VenueForm  # Import your forms
from django.http import JsonResponse, HttpResponseServerError
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse

def logout_view(request):
    logout(request)
    return redirect('home')  # Use the name attribute of your URL pattern

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
                return render(request, 'register-login.html')  # Keep user on the same page
            else:
                user = User.objects.create_user(username=username, password=password)
                Customer.objects.create(
                    name=user,
                    email=email,
                    phoneNo=phoneNo,
                )
                messages.success(request, f"Registration successful! Your username is: {username}")
                return redirect('register_login')  # Use URL name
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register-login.html')  # Keep user on the same page

    return render(request, 'register-login.html')  # Corrected template name


def login_process(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Use URL name
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html') # Stay on login page
    return render(request, 'login.html')  # Stay on login page


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
                return render(request, 'register.html')  # Stay on register page
            else:
                user = User.objects.create_user(username=name, password=password)
                user.is_staff = True  # Set the user as staff
                user.save()
                #  Consider using get_or_create to avoid duplicates
                # Note: Admin model might not exist - you may need to create it
                # Admin.objects.create(
                #     name=user,
                #     email=email,
                #     phoneNo=phoneNo,
                # )
                messages.success(request, "Admin registered successfully. Please log in.")
                return redirect('login')  # Use URL name
        else:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')  # Stay on register page
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
            print(form.errors)  # For debugging
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
        if user is not None and user.is_staff:  # Check for staff status
            login(request, user)
            return redirect('index1')  # Use URL name
        else:
            messages.error(request, "Invalid username or password, or you lack admin privileges.")
            return render(request, 'login.html')
    return render(request, 'login.html')



def check_availability(selected_date):
    return not Booking.objects.filter(date=selected_date).exists() # Simpler check


def book_venue(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Use URL name

    if request.method == 'POST':
        selected_date_str = request.POST.get('date')
        booking_price = request.POST.get('booking-price')
        venue_name = request.POST.get('venue-name')

        if not selected_date_str:
            messages.error(request, "Date is required.")
            return redirect('book_venue')  # Use URL name

        try:
            selected_datetime = datetime.strptime(selected_date_str, '%Y-%m-%d')
            selected_datetime = timezone.make_aware(selected_datetime)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()}) #show the form again

        if selected_datetime <= timezone.now():
            messages.error(request, "Please select a future date.")
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()})  # Use URL name

        if Booking.objects.filter(date=selected_datetime, venue__venue_name=venue_name).exists():
            messages.error(request, "Venue is already booked for the selected date. Please choose another date.")
            return render(request, 'book-venue.html', {'venues': Venue.objects.all()})  # Use URL name

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
            return redirect('your_booking')  # Redirect to user's bookings
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
    return render(request, 'book-venue.html', {'venues': venues})  # Corrected template name



@login_required
def rescheduling(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)  # Simplify
    if request.method == 'POST':
        new_date_str = request.POST.get('new_date')
        try:
            new_date = datetime.strptime(new_date_str, '%Y-%m-%d')
            new_date = timezone.make_aware(new_date)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'rescheduling.html', {'booking_id': booking.pk, 'booking': booking}) #send booking

        # Check for conflicts, excluding the current booking
        if Booking.objects.filter(venue=booking.venue, date=new_date).exclude(pk=booking.pk).exists():
            messages.error(request, "Venue is already booked for the selected date.")
            return render(request, 'rescheduling.html', {'booking_id': booking.pk, 'booking': booking})

        booking.date = new_date
        booking.save()
        messages.success(request, "Booking rescheduled successfully.")
        return redirect('your_booking')  # Use URL name
    return render(request, 'rescheduling.html', {'booking_id': booking.pk, 'booking': booking}) # Pass pk, not the object



@login_required
def your_booking(request):
    try:
        user = request.user
        bookings = Booking.objects.filter(customer__name=user)
        return render(request, 'your-booking.html', {'bookings': bookings})
    except Booking.DoesNotExist:
        message = "You have not made any bookings yet."
        return render(request, 'your-booking.html', {'message': message})



def update_booking(request, booking_id):  # Added booking_id
    booking = get_object_or_404(Booking, pk=booking_id)
    if request.method == 'POST':
        new_date_str = request.POST.get('date')
        try:
            new_date = datetime.strptime(new_date_str, '%Y-%m-%d')
            new_date = timezone.make_aware(new_date)
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")
            return render(request, 'update_booking.html', {'booking_id': booking.pk, 'booking': booking})

        # Check for conflicts, excluding the current booking
        if Booking.objects.filter(venue=booking.venue, date=new_date).exclude(pk=booking.pk).exists():
            messages.error(request, "Date is not available. Please choose another date.")
            return render(request, 'update_booking.html', {'booking_id': booking.pk, 'booking': booking})

        booking.date = new_date
        booking.save()
        messages.success(request, "Booking updated successfully!")
        return redirect('your_booking')  # Use URL name
    return render(request, 'update_booking.html', {'booking_id': booking.pk, 'booking': booking})  # Pass booking


def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, pk=booking_id)
        booking.delete()
        messages.success(request, 'Booking canceled successfully!')
        return redirect('your_booking')  # Use URL name
    return render(request, 'your-booking.html')  # Corrected template name



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


def fetch_venue_location(request):
    venues = Venue.objects.all()
    return render(request, 'search_venues.html', {'venues': venues})

def search_venues(request):
    locations = Venue.objects.values_list('location', flat=True).distinct()
    return render(request, 'search-venues.html', {'locations': locations})



def all_venues(request):
    venues = Venue.objects.all()
    return render(request, 'all_venues.html', {'venues': venues})


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
            venue = Venue.objects.get(venue_name=venue_name)  # Use venue_name
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



def view_booking(request):
    bookings = Booking.objects.all()
    return render(request, 'view_booking.html', {'bookings': bookings})

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

# NEW FUNCTION: Venue Details with Catering and Decoration - UPDATED VERSION
def venue_details(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    
    # Get available catering menus for this venue
    catering_menus = CateringMenu.objects.filter(
        venue=venue,
        is_available=True
    ).prefetch_related('images')
    
    # Get available decoration packages for this venue
    decoration_packages = DecorationPackage.objects.filter(
        venue=venue,
        is_available=True
    ).prefetch_related('images')
    
    context = {
        'venue': venue,
        'catering_menus': catering_menus,
        'decoration_packages': decoration_packages,
    }
    
    # CORRECTED: Use the main venue_details.html template (not the simple one)
    return render(request, 'venue_details.html', context)