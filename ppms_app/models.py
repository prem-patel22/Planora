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
        return f"Customer ID: {self.customer_id}"


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

    def __str__(self):
        return self.venue_name


# =========================
# BOOKING MODEL
# =========================

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    date = models.DateField()
    booking_price = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return f"Booking on {self.date}"


# =========================
# REVIEW MODEL
# =========================

class Review(models.Model):
    reviewer_name = models.CharField(max_length=100)
    review_text = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.reviewer_name


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
        return f"{self.name} - {self.venue.venue_name}"


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
    theme = models.CharField(max_length=100)  # Wedding, Birthday, Corporate
    includes_items = models.TextField()  # comma-separated or JSON-like
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.theme}) - {self.venue.venue_name}"


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
