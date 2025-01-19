from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomerSignupForm, CustomerLoginForm, RestaurantLoginForm
from .models import Customer

def main_page(request):
    return render(request, 'main_page.html')

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email is already registered
            if Customer.objects.filter(email=email).exists():
                messages.error(request, "This email address is already registered. Please login.")
                return render(request, 'customer_signup.html', {'form': form})

            # Save the customer
            form.save()
            messages.success(request, "Account successfully created. Please login.")
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, "Please fill in the form correctly.")
    else:
        form = CustomerSignupForm()

    return render(request, 'customer_signup.html', {'form': form})

def customer_login(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Authenticate user (for simplicity, match email and password directly)
                customer = Customer.objects.get(email=email, password=password)
                # Save the customer ID in the session
                request.session['customer_id'] = customer.id
                messages.success(request, "Login successful!")
                return redirect('customer_home')  # Redirect to customer home after login
            except Customer.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    else:
        form = CustomerLoginForm()

    return render(request, 'customer_login.html', {'form': form})

from django.shortcuts import render
from .models import Restaurant
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Restaurant

from django.shortcuts import render
from .models import Restaurant


def customer_home(request):
    """
    Renders the customer home page with a list of restaurants.
    Displays the first 12 restaurants from the database in rows of 3.
    """
    # Check if the customer_id exists in the session
    if 'customer_id' not in request.session:
        return redirect('customer_login')  # Redirect to the customer login page if not logged in

    # Fetch the customer ID from the session
    customer_id = request.session['customer_id']

    # Retrieve the customer details using the ID
    customer = Customer.objects.get(id=customer_id)

    # Get the customer's name
    customer_name = customer.name if hasattr(customer, 'name') and customer.name else "Customer"

    # Fetch the first 12 restaurants from the database
    restaurants = Restaurant.objects.all()[:12]

    # Pass the data to the template
    context = {
        'customer_name': customer_name,
        'restaurants': restaurants,
    }

    return render(request, 'customer_home.html', context)



from .models import Customer



def customer_profile(request):
    """
    Fetch and display the customer data from the mealzoapp_customer table using session data.
    """
    # Check if the customer_id exists in the session
    if 'customer_id' not in request.session:
        return redirect('customer_login')  # Redirect to the customer login page if not logged in

    # Fetch the customer ID from the session
    customer_id = request.session['customer_id']

    # Retrieve the customer details using the ID
    customer = Customer.objects.get(id=customer_id)

    # Prepare the context to pass customer data to the template
    context = {
        'customer': customer,
    }

    # Render the customer profile template
    return render(request, 'customer_profile.html', context)


def customer_logout(request):
    request.session.flush()  # Clears the session
    messages.success(request, "Logged out successfully.")
    return redirect('main_page')  # Redirect to the main page after logout



from .forms import RestaurantSignupForm


def restaurant_signup(request):
    if request.method == 'POST':
        form = RestaurantSignupForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email is already registered
            if Restaurant.objects.filter(email=email).exists():
                messages.error(request, "This email address is already registered. Please login.")
                return render(request, 'restaurant_signup.html', {'form': form})

            # Save the restaurant
            form.save()
            messages.success(request, "Restaurant account successfully created. Please login.")
            return redirect('restaurant_login')  # Redirect to the login page
        else:
            messages.error(request, "Please fill in the form correctly.")
    else:
        form = RestaurantSignupForm()

    return render(request, 'restaurant_signup.html', {'form': form})



def restaurant_login(request):
    if request.method == 'POST':
        form = RestaurantLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Authenticate restaurant (for simplicity, match email and password directly)
                restaurant = Restaurant.objects.get(email=email, password=password)
                # Save the restaurant ID in the session
                request.session['restaurant_id'] = restaurant.id
                messages.success(request, "Login successful!")
                return redirect('restaurant_home')  # Redirect to restaurant home after login
            except Restaurant.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    else:
        form = RestaurantLoginForm()

    return render(request, 'restaurant_login.html', {'form': form})


from django.shortcuts import redirect
from django.contrib import messages
from .models import Restaurant

def delete_restaurant(request, restaurant_id):
    if 'customer_id' not in request.session:  # Check if user is logged in
        messages.error(request, "You need to be logged in to delete a restaurant.")
        return redirect('customer_login')  # Redirect to login page

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        messages.error(request, "Restaurant not found.")
        return redirect('restaurant_profile')  # Redirect back if restaurant not found

    if request.method == "POST":
        restaurant_name = restaurant.restaurant_name  # Capture name for success message
        restaurant.delete()
        messages.success(request, f"Restaurant '{restaurant_name}' has been deleted successfully.")
        return redirect('main_page')  # Redirect to the home page
    else:
        messages.error(request, "Invalid request method.")
        return redirect('restaurant_profile')  # Redirect back to the profile page


from .models import Restaurant, MenuItem, InventoryItem, Order, OrderItem, Income
from .forms import MenuItemForm, InventoryItemForm, RestaurantProfileForm
import datetime
from django.db.models import Sum


# Restaurant dashboard view
def restaurant_home(request):
    if 'restaurant_id' not in request.session:
        return redirect('restaurant_login')

    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    # Calculate orders served and income for today
    orders_today = Order.objects.filter(restaurant=restaurant, created_at__date=datetime.date.today())
    orders_served = orders_today.count()
    total_income_today = Income.objects.filter(restaurant=restaurant, date=datetime.date.today()).aggregate(Sum('amount'))['amount__sum'] or 0

    # Get order requests
    order_requests = orders_today.filter(status='Pending')

    context = {
        'user': restaurant,
        'orders_served': orders_served,
        'total_income_today': total_income_today,
        'order_requests': order_requests,
    }

    return render(request, 'restaurant_home.html', context)




# Manage menu page view
def manage_menu(request):
    if 'restaurant_id' not in request.session:
        return redirect('restaurant_login')

    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
    }

    return render(request, 'manage_menu.html', context)

# Add menu item view
def add_menu_item(request):
    if 'restaurant_id' not in request.session:
        return redirect('restaurant_login')

    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    if request.method == 'POST':
        menu_form = MenuItemForm(request.POST, request.FILES)
        if menu_form.is_valid():
            menu_item = menu_form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            messages.success(request, "Menu item added successfully!")
            return redirect('manage_menu')
        else:
            messages.error(request, "Error adding menu item. Please try again.")
            print(menu_form.errors)

    menu_form = MenuItemForm()

    context = {
        'restaurant': restaurant,
        'menu_form': menu_form,
    }

    return render(request, 'add_menu_item.html', context)


from .forms import InventoryItemForm

# Manage Inventory page
def manage_inventory(request):
    if 'restaurant_id' not in request.session:
        return redirect('restaurant_login')

    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    # Handling form submission to add a new inventory item
    if request.method == 'POST':
        inventory_form = InventoryItemForm(request.POST)
        if inventory_form.is_valid():
            inventory_item = inventory_form.save(commit=False)
            inventory_item.restaurant = restaurant
            inventory_item.save()
            messages.success(request, "Inventory item added successfully!")
            return redirect('manage_inventory')
        else:
            messages.error(request, "Error adding inventory item. Please try again.")

    inventory_items = InventoryItem.objects.filter(restaurant=restaurant)
    inventory_form = InventoryItemForm()

    context = {
        'restaurant': restaurant,
        'inventory_items': inventory_items,
        'inventory_form': inventory_form,
    }

    return render(request, 'manage_inventory.html', context)

# Add Inventory Item page
def add_inventory_item(request):
    if 'restaurant_id' not in request.session:
        return redirect('restaurant_login')

    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    # Handling form submission to add a new inventory item
    if request.method == 'POST':
        inventory_form = InventoryItemForm(request.POST)
        if inventory_form.is_valid():
            inventory_item = inventory_form.save(commit=False)
            inventory_item.restaurant = restaurant
            inventory_item.save()
            messages.success(request, "Inventory item added successfully!")
            return redirect('manage_inventory')
        else:
            messages.error(request, "Error adding inventory item. Please try again.")

    inventory_form = InventoryItemForm()

    context = {
        'inventory_form': inventory_form,
    }

    return render(request, 'add_inventory_item.html', context)


# Restaurant Profile page (view details)
def restaurant_profile(request):
    if 'restaurant_id' not in request.session:
        return redirect('restaurant_login')

    restaurant_id = request.session['restaurant_id']
    restaurant = Restaurant.objects.get(id=restaurant_id)

    context = {
        'restaurant': restaurant,
    }

    return render(request, 'restaurant_profile.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Order

def current_orders(request):
    restaurant = request.user.restaurant  # Assuming authenticated restaurant user
    orders = Order.objects.filter(restaurant=restaurant, status__in=['Pending', 'Preparing']).order_by('-created_at')
    return render(request, 'restaurant_current_orders.html', {'orders': orders})

def order_history(request):
    restaurant = request.user.restaurant
    orders = Order.objects.filter(restaurant=restaurant).exclude(status__in=['Pending', 'Preparing']).order_by('-created_at')
    return render(request, 'restaurant_order_history.html', {'orders': orders})

from django.http import JsonResponse

def update_order_status(request, order_id):
    if request.method == 'POST':
        restaurant = request.user.restaurant
        order = get_object_or_404(Order, id=order_id, restaurant=restaurant)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            return JsonResponse({'success': True, 'new_status': new_status})
        return JsonResponse({'success': False, 'error': 'Invalid status'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})







def restaurant_logout(request):
    request.session.flush()  # Clears the session
    messages.success(request, "Logged out successfully.")
    return redirect('main_page')  # Redirect to the main page after logout.


from .forms import MealerSignupForm
from .models import Mealer

def mealer_signup(request):
    if request.method == 'POST':
        form = MealerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email is already registered
            if Mealer.objects.filter(email=email).exists():
                messages.error(request, "This email address is already registered. Please login.")
                return render(request, 'mealer_signup.html', {'form': form})

            # Save the mealer
            form.save()
            messages.success(request, "Mealer account successfully created. Please login.")
            return redirect('mealer_login')  # Redirect to the login page
        else:
            messages.error(request, "Please fill in the form correctly.")
    else:
        form = MealerSignupForm()

    return render(request, 'mealer_signup.html', {'form': form})



from .forms import MealerLoginForm


def mealer_login(request):
    if request.method == 'POST':
        form = MealerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Authenticate Mealer (for simplicity, match email and password directly)
                mealer = Mealer.objects.get(email=email, password=password)
                # Save the Mealer ID in the session
                request.session['mealer_id'] = mealer.id
                messages.success(request, "Login successful!")
                return redirect('mealer_home')  # Redirect to Mealer home after login
            except Mealer.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    else:
        form = MealerLoginForm()

    return render(request, 'mealer_login.html', {'form': form})

def mealer_logout(request):
    request.session.flush()  # Clears the session
    messages.success(request, "Logged out successfully.")
    return redirect('main_page')  # Redirect to the main page after logout.


from django.shortcuts import render, redirect
from .models import Mealer  # Make sure to import the correct Mealer model

def mealer_profile(request):
    """
    Fetch and display the Mealer data from the mealzoapp_mealer table using session data.
    """
    # Check if the mealer_id exists in the session
    if 'mealer_id' not in request.session:
        return redirect('mealer_login')  # Redirect to the mealer login page if not logged in

    # Fetch the mealer ID from the session
    mealer_id = request.session['mealer_id']

    # Retrieve the Mealer details using the ID
    mealer = Mealer.objects.get(id=mealer_id)

    # Prepare the context to pass mealer data to the template
    context = {
        'mealer': mealer,
    }

    # Render the mealer profile template
    return render(request, 'mealer_profile.html', context)



def mealer_home(request):
    if 'mealer_id' not in request.session:
        return redirect('mealer_login')  # Redirect to login if no valid session

    mealer_id = request.session['mealer_id']
    try:
        mealer = Mealer.objects.get(id=mealer_id)
    except Mealer.DoesNotExist:
        # Handle the case where Mealer does not exist
        messages.error(request, "Session expired or invalid. Please login again.")
        return redirect('mealer_login')  # Redirect to login page

    context = {
        'user': mealer,  # Pass the Mealer object to the template
        'welcome_message': f"Welcome, {mealer.name}!" if mealer.name else "Welcome to Mealzo!",
    }

    return render(request, 'mealer_home.html', context)




from django.shortcuts import render, redirect
from .models import Restaurant

def search_restaurants(request):
    query = request.GET.get('query', '')
    restaurants = Restaurant.objects.filter(restaurant_name__icontains=query)

    context = {
        'restaurants': restaurants,
    }

    return render(request, 'search_results.html', context)



from django.shortcuts import render
from .models import Restaurant

def search_menu(request):
    restaurant_id = request.GET.get('restaurant_id')
    if restaurant_id:
        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            menu_items = restaurant.menu_items.all()
        except Restaurant.DoesNotExist:
            restaurant = None
            menu_items = []
    else:
        restaurant = None
        menu_items = []

    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
    }
    return render(request, 'search_menu.html', context)


# views.py
from django.shortcuts import render, redirect
from .models import MenuItem, Cart, CartItem
from django.http import Http404

def add_to_cart(request, menu_item_id):
    # Fetch the menu item based on the provided ID
    try:
        menu_item = MenuItem.objects.get(id=menu_item_id)
    except MenuItem.DoesNotExist:
        raise Http404("Menu item does not exist.")

    # Ensure the customer is logged in (you can also handle session-based login for now)
    if 'customer_id' not in request.session:
        return redirect('customer_login')  # Redirect to login if not logged in

    customer_id = request.session['customer_id']

    # Get or create a cart for the logged-in customer
    cart, created = Cart.objects.get_or_create(customer_id=customer_id)

    # Check if the item already exists in the cart, otherwise create a new CartItem
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)

    if not created:
        # If the item already exists in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')  # Redirect to cart view after adding the item


# views.py (continued)
def cart_view(request):
    # Get customer ID from session
    customer_id = request.session.get('customer_id')

    if not customer_id:
        return redirect('customer_login')  # Redirect to login if not logged in

    try:
        # Retrieve the customer's cart and associated cart items
        cart = Cart.objects.get(customer_id=customer_id)
        cart_items = cart.items.all()
        total_price = sum(item.get_total_price() for item in cart_items)
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
        total_price = 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'cart.html', context)


from django.shortcuts import redirect
from django.http import HttpResponse
from .models import CartItem

def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = CartItem.objects.get(id=item_id)

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1

        cart_item.save()

    return redirect('cart_view')  # Redirect back to the cart page after updating quantity


from django.shortcuts import redirect
from .models import CartItem

def remove_item_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()

    return redirect('cart_view')  # Redirect back to the cart page after removal



from django.shortcuts import render

from django.shortcuts import render
from django.conf import settings

def checkout_view(request):
    context = {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, "checkout.html", context)



#payment

import stripe
from django.http import JsonResponse
from django.conf import settings

stripe.api_key = 'sk_test_51QX1xOFK4MRXJxiQVzUfBHZPcKCFbo4a1G4oj2y1BDPp1x9jAgOeT4NxmoRSy00A11c1mlHE9BMrQXMo2xrRQRBh00THzuMrIV'  # Replace with your secret key

def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Create Stripe Checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Mealzo Food Order',
                        },
                        'unit_amount': 55000,  # ₹550 in paisa
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/order-success/'),
                cancel_url=request.build_absolute_uri('/checkout/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


#order success
from django.shortcuts import render

def order_success_page(request):
    return render(request, 'order_success.html')


from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Sum
from .models import Order, MenuItem, InventoryItem, Income
import datetime

# Update order status to "Preparing" and handle inventory, income, and orders served
def update_order_status(request, order_id):
    if request.method == 'POST':
        restaurant = request.user.restaurant
        order = get_object_or_404(Order, id=order_id, restaurant=restaurant)

        new_status = request.POST.get('status')

        if new_status == 'Preparing':  # If restaurant accepts the order
            order.status = 'Preparing'

            # Update inventory by reducing raw materials by 5% for each order item
            for order_item in order.items.all():
                menu_item = get_object_or_404(MenuItem, id=order_item.menu_item.id)
                raw_materials = menu_item.raw_materials.split(',')

                # Reduce 5% from each raw material in inventory
                for raw_material in raw_materials:
                    inventory_item = get_object_or_404(InventoryItem, restaurant=restaurant, name=raw_material.strip())
                    inventory_item.quantity = int(inventory_item.quantity * 0.95)  # Decrease by 5%
                    inventory_item.save()

                # Decrease the menu item quantity by the ordered amount
                menu_item.quantity -= order_item.quantity
                menu_item.save()

            # Update the orders served count and today's income
            Income.objects.create(
                restaurant=restaurant,
                amount=order.total_amount,
                date=datetime.date.today()
            )

            # Increment the orders served count
            orders_today = Order.objects.filter(restaurant=restaurant, status='Completed', created_at__date=datetime.date.today())
            orders_served = orders_today.count()

            # Update the income for today
            total_income_today = Income.objects.filter(restaurant=restaurant, date=datetime.date.today()).aggregate(Sum('amount'))['amount__sum'] or 0

            order.save()

        elif new_status == 'Canceled':  # If the restaurant rejects the order
            order.status = 'Canceled'
            order.save()

        return JsonResponse({'success': True, 'new_status': new_status})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


