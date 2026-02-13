from django.db import models
from django.contrib.auth.models import User


# =========================
# CUSTOMER & ADMIN MODELS
# =========================

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    email = models.EmailField(max_length=50)
    phoneNo = models.CharField(max_length=10)
    password = models.CharField(max_length=128, default='')  # Prefer Django auth password handling

    def __str__(self):
        return f"{self.name.username} (ID: {self.customer_id})"
    
    class Meta:
        verbose_name_plural = "Customers"


class Admin(models.Model):
    Admin_id = models.AutoField(primary_key=True)
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='admin_profile'
    )
    email = models.EmailField(max_length=50)
    phoneNo = models.CharField(max_length=10)
    password = models.CharField(max_length=128, default='')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = "Admins"


# =========================
# VENUE MODEL
# =========================

class Venue(models.Model):
    AVAILABILITY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    venue_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    amenities = models.TextField()
    pricing = models.CharField(max_length=100)
    availability = models.CharField(max_length=3, choices=AVAILABILITY_CHOICES)
    image = models.ImageField(upload_to='venue_images/', blank=True, null=True)
    
    # Basic catering and decoration fields
    catering_menu = models.TextField(
        blank=True,
        null=True,
        help_text="Basic catering summary"
    )
    decoration_options = models.TextField(
        blank=True,
        null=True,
        help_text="Basic decoration summary"
    )
    
    # Additional fields from second version
    description = models.TextField(blank=True)

    def __str__(self):
        return self.venue_name
    
    class Meta:
        verbose_name_plural = "Venues"


# =========================
# BOOKING MODEL
# =========================

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    date = models.DateTimeField()  # Changed to DateTimeField to match second version
    booking_price = models.IntegerField()  # Changed to IntegerField for better calculations
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    
    # Enhanced fields for catering/decoration
    selected_catering = models.CharField(max_length=200, blank=True, null=True, default='Not selected')
    selected_catering_price = models.IntegerField(default=0, blank=True, null=True)
    selected_decoration = models.CharField(max_length=200, blank=True, null=True, default='Not selected')
    selected_decoration_price = models.IntegerField(default=0, blank=True, null=True)
    event_type = models.CharField(max_length=100, blank=True, null=True, default='Not specified')
    guest_count = models.IntegerField(default=0, blank=True, null=True)
    special_requests = models.TextField(blank=True, null=True)
    booking_status = models.CharField(max_length=50, default='confirmed')
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.booking_id}: {self.customer.name.username} - {self.venue.venue_name} - {self.date.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Bookings"


# =========================
# REVIEW MODEL
# =========================

class Review(models.Model):
    reviewer_name = models.CharField(max_length=100)
    review_text = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer_name} on {self.created_at}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Reviews"


# =========================
# ADVANCED CATERING MODELS
# =========================

class CateringMenu(models.Model):
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name='catering_menus'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    is_vegetarian = models.BooleanField(default=False)
    min_guests = models.IntegerField(default=50)
    max_guests = models.IntegerField(default=500)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.venue.venue_name} (₹{self.price_per_person}/person)"
    
    class Meta:
        verbose_name_plural = "Catering Menus"
        ordering = ['venue', 'name']


class MenuItemImage(models.Model):
    catering_menu = models.ForeignKey(
        CateringMenu,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='menu_item_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.catering_menu.name}"
    
    class Meta:
        verbose_name_plural = "Menu Item Images"


# =========================
# DECORATION MODELS
# =========================

class DecorationPackage(models.Model):
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name='decoration_packages'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    theme = models.CharField(max_length=100, help_text="Wedding, Birthday, Corporate, etc.")
    includes_items = models.TextField(help_text="Comma-separated list of items included")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.theme}) - {self.venue.venue_name} (₹{self.price})"
    
    class Meta:
        verbose_name_plural = "Decoration Packages"
        ordering = ['venue', 'name']


class DecorationImage(models.Model):
    decoration_package = models.ForeignKey(
        DecorationPackage,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='decoration_images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.decoration_package.name}"
    
    class Meta:
        verbose_name_plural = "Decoration Images"