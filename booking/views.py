from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import MaidRegistrationForm, CustomerRegistrationForm
from .models import Maid, Customer, Booking  # Added Booking to the import
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Maid related views
def maid_register(request):
    if request.method == 'POST':
        form = MaidRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the user first
            user = form.save()
            
            # Now create the maid profile
            Maid.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone'),
                address=form.cleaned_data.get('address'),
                profile_pic=form.cleaned_data.get('profile_pic'),
                services=form.cleaned_data.get('services'),
                experience=form.cleaned_data.get('experience')
            )
            
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('maid_login')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = MaidRegistrationForm()
    
    return render(request, 'booking/maid_register.html', {'form': form})

def maid_login(request):
    """Handle maid login authentication and redirection"""
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        print(f"Login attempt for username: {username}")
        
        if not username or not password:
            context['error'] = 'Please enter both username and password.'
            return render(request, 'booking/maid_login.html', context)
            
        # Check if username exists
        try:
            user_exists = User.objects.filter(username=username).exists()
            if not user_exists:
                context['error'] = 'Username does not exist. Please register first.'
                context['register_link'] = True
                return render(request, 'booking/maid_login.html', context)
            
            # Attempt authentication
            user = authenticate(request, username=username, password=password)
            print(f"Authentication result for {username}: {'Success' if user else 'Failed'}")
            
            if user is not None:
                # Check if user is a maid
                try:
                    maid = Maid.objects.get(user=user)
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    print(f"Maid {username} logged in successfully")
                    return redirect('maid_dashboard')
                except Maid.DoesNotExist as e:
                    print(f"Maid not found error: {str(e)}")
                    context['error'] = 'This account is not registered as a maid.'
                    context['register_link'] = True
            else:
                context['error'] = 'Invalid password. Please try again.'
        except Exception as e:
            print(f"Login error: {str(e)}")
            context['error'] = f'Login error: {str(e)}'
        
        # Keep the username in the form for convenience
        context['username'] = username
    
    return render(request, 'booking/maid_login.html', context)

def maid_dashboard(request):
    """Display the maid dashboard if user is authenticated as a maid"""
    if request.user.is_authenticated:
        try:
            maid = Maid.objects.get(user=request.user)
            # Get all bookings for this maid
            bookings = Booking.objects.filter(maid=maid).order_by('-booking_date')
            return render(request, 'booking/maid_dashboard.html', {'maid': maid, 'bookings': bookings})
        except Maid.DoesNotExist:
            messages.error(request, 'You are not registered as a maid.')
            logout(request)  # Log them out if they're not a maid
            return redirect('maid_login')
    else:
        return redirect('maid_login')

def maid_logout(request):
    """Log out the current user and redirect to login page"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('maid_login')

# Customer related views
def user_register(request):
    """Handle customer registration"""
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the user first
            user = form.save()
            
            # Now create the customer profile
            Customer.objects.create(
                user=user,
                phone=form.cleaned_data.get('phone'),
                address=form.cleaned_data.get('address'),
                profile_pic=form.cleaned_data.get('profile_pic')
            )
            
            messages.success(request, 'Registration successful! You can now login.')
            return redirect('user_login')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'booking/user_register.html', {'form': form})

def user_login(request):
    """Handle user login authentication and redirection"""
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        print(f"Login attempt for username: {username}")
        
        if not username or not password:
            context['error'] = 'Please enter both username and password.'
            return render(request, 'booking/user_login.html', context)
            
        # Check if username exists
        try:
            user_exists = User.objects.filter(username=username).exists()
            if not user_exists:
                context['error'] = 'Username does not exist. Please register first.'
                context['register_link'] = True
                return render(request, 'booking/user_login.html', context)
            
            # Attempt authentication
            user = authenticate(request, username=username, password=password)
            print(f"Authentication result for {username}: {'Success' if user else 'Failed'}")
            
            if user is not None:
                # Check if user is a customer
                try:
                    customer = Customer.objects.get(user=user)
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    print(f"Customer {username} logged in successfully")
                    # In your user_login view, make sure this line is correct
                    return redirect('maid_listings')  # This should match the name in urls.py
                except Customer.DoesNotExist:
                    context['error'] = 'This account is not registered as a customer.'
                    context['register_link'] = True
            else:
                context['error'] = 'Invalid password. Please try again.'
        except Exception as e:
            print(f"Login error: {str(e)}")
            context['error'] = f'Login error: {str(e)}'
        
        # Keep the username in the form for convenience
        context['username'] = username
    
    return render(request, 'booking/user_login.html', context)

def dashboard(request):
    """Display the dashboard for authenticated users"""
    print("Dashboard view called")  # Add this for debugging
    if request.user.is_authenticated:
        try:
            # Try to get customer profile
            customer = Customer.objects.get(user=request.user)
            return render(request, 'booking/dashboard.html', {'customer': customer})
        except Customer.DoesNotExist:
            # If not a customer, check if they're a maid
            try:
                maid = Maid.objects.get(user=request.user)
                return redirect('maid_dashboard')
            except Maid.DoesNotExist:
                # If neither customer nor maid, show an error
                messages.error(request, 'Account type not recognized.')
                return redirect('landing')
    else:
        # If not authenticated, redirect to login
        return redirect('user_login')
def user_bookings(request):
    """Display user bookings"""
    print("User bookings view called")
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            # Get all bookings for this customer
            bookings = Booking.objects.filter(customer=customer).order_by('-booking_date')
            return render(request, 'booking/user_bookings.html', {'bookings': bookings})
        except Customer.DoesNotExist:
            messages.error(request, 'You are not registered as a customer.')
            return redirect('landing')
    else:
        # If not authenticated, redirect to login
        return redirect('user_login')
def user_logout(request):
    """Log out the current user and redirect to login page"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('user_login')

# Manager related views
def manager_login(request):
    """Placeholder for manager login"""
    return render(request, 'booking/manager_login.html')

def manager_register(request):
    """Placeholder for manager registration"""
    return render(request, 'booking/manager_register.html')

# General views
def landing_page(request):
    """Display the landing page"""
    return render(request, 'booking/landing.html')


# Add these new view functions to your views.py file

def maid_listings(request):
    """Display all available maids with filtering options"""
    # Get filter parameters from request
    state = request.GET.get('state', '')
    city = request.GET.get('city', '')
    area = request.GET.get('area', '')
    
    # Start with all maids
    maids = Maid.objects.all()
    
    # Define state-city mapping (in a real app, this would come from a database)
    state_city_mapping = {
        'Andhra Pradesh': ['Vijayawada', 'Visakhapatnam', 'Tirupati', 'Guntur', 'Nellore'],
        'Karnataka': ['Bangalore', 'Mysore', 'Hubli', 'Mangalore', 'Belgaum'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Trichy'],
        'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Thrissur', 'Kollam'],
        'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Karimnagar', 'Khammam']
    }
    
    # Define city-area mapping (in a real app, this would come from a database)
    city_area_mapping = {
        'Hyderabad': ['Banjara Hills', 'Jubilee Hills', 'Gachibowli', 'Madhapur', 'Kukatpally'],
        'Bangalore': ['Koramangala', 'Indiranagar', 'Whitefield', 'Electronic City', 'Jayanagar'],
        'Chennai': ['T Nagar', 'Adyar', 'Anna Nagar', 'Velachery', 'Mylapore'],
        'Vijayawada': ['Benz Circle', 'Bandar Road', 'MG Road', 'Governorpet', 'Gunadala'],
        'Visakhapatnam': ['Beach Road', 'MVP Colony', 'Dwaraka Nagar', 'Gajuwaka', 'Madhurawada']
        # Add more cities and areas as needed
    }
    
    # Get available cities based on selected state
    cities = []
    if state:
        cities = state_city_mapping.get(state, [])
        maids = maids.filter(address__icontains=state)
    else:
        # If no state selected, show all cities from all states
        for city_list in state_city_mapping.values():
            cities.extend(city_list)
    
    # Get available areas based on selected city
    areas = []
    if city:
        areas = city_area_mapping.get(city, [])
        maids = maids.filter(address__icontains=city)
    
    # Apply area filter if provided
    if area:
        maids = maids.filter(address__icontains=area)
    
    context = {
        'maids': maids,
        'cities': sorted(cities),
        'areas': sorted(areas)
    }
    
    return render(request, 'booking/maid_listings.html', context)

def maid_details(request, maid_id):
    """Display detailed information about a specific maid"""
    try:
        maid = Maid.objects.get(id=maid_id)
        return render(request, 'booking/maid_details.html', {'maid': maid})
    except Maid.DoesNotExist:
        messages.error(request, 'Maid not found.')
        return redirect('maid_listings')


def book_maid(request, maid_id):
    """Handle booking a maid"""
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to request service.')
        return redirect('user_login')
    
    # Get the maid object
    maid = get_object_or_404(Maid, id=maid_id)
    
    # Get the customer object
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        messages.error(request, 'You need a customer account to request service.')
        return redirect('maid_details', maid_id=maid_id)
    
    if request.method == 'POST':
        # Get form data
        service_type = request.POST.get('service_type', 'cleaning')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        duration_hours = int(request.POST.get('duration_hours', 2))
        notes = request.POST.get('notes', '')
        
        print(f"Service request - Type: {service_type}, Date: {booking_date}, Time: {booking_time}, Duration: {duration_hours}h")
        
        # Validate the data
        if not booking_date:
            messages.error(request, 'Please select a date for the service.')
            return redirect('maid_details', maid_id=maid_id)
        
        # Combine date and time
        if booking_date and booking_time:
            service_datetime = f"{booking_date} {booking_time}"
            try:
                # Parse the datetime string
                service_date = timezone.datetime.strptime(service_datetime, "%Y-%m-%d %H:%M")
            except ValueError:
                messages.error(request, 'Invalid date or time format.')
                return redirect('maid_details', maid_id=maid_id)
        else:
            service_date = timezone.datetime.strptime(booking_date, "%Y-%m-%d")
        
        try:
            # Create a new booking
            booking = Booking.objects.create(
                customer=customer,
                maid=maid,
                booking_date=timezone.now(),
                service_date=service_date,
                service_type=service_type,
                duration_hours=duration_hours,
                notes=notes,
                status='pending'  # Initial status is pending
            )
            
            messages.success(request, f'Service request sent to {maid.user.first_name}. You will be notified when they accept.')
            return redirect('user_bookings')
        except Exception as e:
            print(f"Error creating service request: {str(e)}")
            messages.error(request, f'Error creating service request: {str(e)}')
            return redirect('maid_details', maid_id=maid_id)
    
    return redirect('maid_details', maid_id=maid_id)

def cancel_booking(request, booking_id):
    """Cancel a booking"""
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if the booking belongs to the current user
    if booking.customer.user != request.user:
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('user_bookings')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Booking has been cancelled successfully.')
    
    return redirect('user_bookings')


def accept_booking(request, booking_id):
    """Allow maid to accept a booking"""
    if not request.user.is_authenticated:
        return redirect('maid_login')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if the booking belongs to the current maid
    try:
        maid = Maid.objects.get(user=request.user)
        if booking.maid != maid:
            messages.error(request, 'You do not have permission to accept this booking.')
            return redirect('maid_dashboard')
    except Maid.DoesNotExist:
        messages.error(request, 'You are not registered as a maid.')
        return redirect('maid_login')
    
    if request.method == 'POST':
        booking.status = 'accepted'
        booking.save()
        messages.success(request, 'Booking has been accepted successfully.')
    
    return redirect('maid_dashboard')

def reject_booking(request, booking_id):
    """Allow maid to reject a booking"""
    if not request.user.is_authenticated:
        return redirect('maid_login')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if the booking belongs to the current maid
    try:
        maid = Maid.objects.get(user=request.user)
        if booking.maid != maid:
            messages.error(request, 'You do not have permission to reject this booking.')
            return redirect('maid_dashboard')
    except Maid.DoesNotExist:
        messages.error(request, 'You are not registered as a maid.')
        return redirect('maid_login')
    
    if request.method == 'POST':
        booking.status = 'rejected'
        booking.save()
        messages.success(request, 'Booking has been rejected.')
    
    return redirect('maid_dashboard')
