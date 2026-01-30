from django.contrib import admin
from .models import Admin, Customer, Venue, Booking, Review

# Register Customer model
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'email', 'phoneNo', 'password')

# Register Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'date', 'booking_price', 'customer_id', 'get_venue_name')

    def get_venue_name(self, obj):
        return obj.venue.venue_name

    get_venue_name.short_description = 'Venue Name'

# Register Venue model
@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('venue_name', 'location', 'capacity', 'amenities', 'pricing', 'availability')

# Register Admin model
@admin.register(Admin)
class AdminuserAdmin(admin.ModelAdmin):
    list_display = ('Admin_id', 'name', 'email', 'phoneNo', 'password')

    def Admin_id(self, obj):
        return obj.Admin_id

# Register Review model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'review_text', 'created_at')


from .models import CateringMenu, DecorationPackage, MenuItemImage, DecorationImage

# Add these admin classes
class MenuItemImageInline(admin.TabularInline):
    model = MenuItemImage
    extra = 1

class DecorationImageInline(admin.TabularInline):
    model = DecorationImage
    extra = 1

@admin.register(CateringMenu)
class CateringMenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'price_per_person', 'is_vegetarian', 'is_available']
    list_filter = ['is_vegetarian', 'is_available', 'venue']
    search_fields = ['name', 'description']
    inlines = [MenuItemImageInline]

@admin.register(DecorationPackage)
class DecorationPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'venue', 'theme', 'price', 'is_available']
    list_filter = ['theme', 'is_available', 'venue']
    search_fields = ['name', 'theme', 'description']
    inlines = [DecorationImageInline]

@admin.register(MenuItemImage)
class MenuItemImageAdmin(admin.ModelAdmin):
    list_display = ['catering_menu', 'caption', 'is_primary']

@admin.register(DecorationImage)
class DecorationImageAdmin(admin.ModelAdmin):
    list_display = ['decoration_package', 'caption', 'is_primary']