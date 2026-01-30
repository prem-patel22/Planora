# Front-End vs Back-End File Breakdown

## 🎨 FRONT-END FILES (Client-Side)

### **HTML Templates** (`templates/` directory)
These files define the structure and layout of web pages:
- `index.html` - Main user homepage
- `index1.html` - Admin homepage
- `home.html` - Landing page
- `login.html` - User login page
- `register.html` - Admin registration page
- `register-login.html` - User registration/login page
- `book-venue.html` - Venue booking page
- `search-venues.html` - Venue search page
- `search_results.html` - Search results display
- `all_venues.html` - Display all venues (admin)
- `add_venue.html` - Add new venue form (admin)
- `edit_venue.html` - Edit venue form (admin)
- `view_booking.html` - View all bookings (admin)
- `your-booking.html` - User's bookings page
- `reviews.html` - Reviews page
- `get_reviews.html` - Display all reviews (admin)
- `images.html` - Images gallery
- `amenities.html` - Amenities page
- `price.html` - Pricing page
- `cancellation.html` - Cancellation page
- `notification.html` - Notifications page
- `modifying-details.html` - Modify details page
- `booking-availability.html` - Booking availability page

### **CSS Stylesheets** (`static/` directory)
Styling files that control the appearance:
- `static/style.css` - Main stylesheet
- `static/style1.css` - Additional stylesheet (likely for admin pages)

### **Static Images** (`ppms_app/static/images/`)
- `ppms_app/static/images/wedding-bg.png` - Background image

### **Media Files** (`media/` directory)
User-uploaded content:
- `media/venue_images/` - Uploaded venue images (46 files: .jpg, .jpeg, .webp)

### **Inline CSS & JavaScript**
- Embedded `<style>` tags in HTML templates
- Embedded `<script>` tags in HTML templates (for client-side interactivity)

---

## ⚙️ BACK-END FILES (Server-Side)

### **Django Application Core** (`ppms_app/` directory)

#### **Models** - Database Structure
- `ppms_app/models.py` - Defines database models:
  - `Customer` - Customer/user data model
  - `Admin` - Admin user model
  - `Venue` - Venue information model
  - `Booking` - Booking records model
  - `Review` - Review/feedback model

#### **Views** - Business Logic & Request Handling
- `ppms_app/views.py` - Contains all view functions that:
  - Handle HTTP requests
  - Process form submissions
  - Query database
  - Render templates with data
  - Manage authentication
  - Handle booking logic
  - Process search queries

#### **URL Routing** - URL Configuration
- `ppms_app/urls.py` - Maps URLs to view functions
- Defines all application routes/endpoints

#### **Forms** - Form Handling
- `ppms_app/forms.py` - Django form definitions:
  - `VenueForm` - Form for adding/editing venues

#### **Admin Configuration**
- `ppms_app/admin.py` - Django admin interface configuration

#### **App Configuration**
- `ppms_app/apps.py` - Application configuration
- `ppms_app/__init__.py` - Package initialization

#### **Database Migrations** (`ppms_app/migrations/`)
- `migrations/0001_initial.py` - Database schema migrations
- `migrations/__init__.py` - Migrations package

### **Django Project Settings** (`ppms/` directory)

#### **Project Configuration**
- `ppms/settings.py` - Main Django settings:
  - Database configuration
  - Installed apps
  - Middleware
  - Static/media file settings
  - Security settings
  - Template configuration

#### **URL Configuration**
- `ppms/urls.py` - Main project URL routing
  - Includes admin URLs
  - Includes app URLs

#### **WSGI/ASGI Configuration**
- `ppms/wsgi.py` - Web Server Gateway Interface (for production)
- `ppms/asgi.py` - Asynchronous Server Gateway Interface (for async)

#### **Package Initialization**
- `ppms/__init__.py` - Project package initialization

### **Django Management**
- `manage.py` - Django's command-line utility for:
  - Running migrations
  - Starting development server
  - Creating superusers
  - Running management commands

### **Database**
- `db.sqlite3` - SQLite database file (contains all data)

### **Configuration Files**
- `requirements.txt` - Python package dependencies
- `README.md` - Project documentation

---

## 📊 Summary

### Front-End Components:
- **HTML Templates** (19 files) - User interface structure
- **CSS Files** (2 files) - Styling
- **Static Images** - Visual assets
- **Media Files** - User-uploaded content
- **Inline JavaScript/CSS** - Client-side interactivity

### Back-End Components:
- **Python Files** - Server-side logic
  - Models (database structure)
  - Views (request handling & business logic)
  - URLs (routing)
  - Forms (form processing)
  - Settings (configuration)
- **Database** - Data storage (SQLite)
- **Migrations** - Database schema changes

---

## 🔄 How They Work Together

1. **User Request** → Browser sends HTTP request
2. **URL Routing** (`urls.py`) → Determines which view to call
3. **View Function** (`views.py`) → Processes request, queries database (`models.py`)
4. **Template Rendering** → View renders HTML template with data
5. **Response** → HTML + CSS + JavaScript sent to browser
6. **Display** → Browser renders the front-end for user

---

## 📝 Notes

- **Front-end** = What users see and interact with (HTML, CSS, JavaScript)
- **Back-end** = Server-side logic that processes requests, manages data, and generates responses (Python/Django)
- Django uses the **MVT (Model-View-Template)** pattern:
  - **Model** = Database structure (back-end)
  - **View** = Business logic (back-end)
  - **Template** = HTML presentation (front-end)
