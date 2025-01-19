from django.db import models


class Customer(models.Model):
    DoesNotExist = None
    objects = None
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, blank=True)
    house_number = models.CharField(max_length=100, blank=True)
    street_number = models.CharField(max_length=100, blank=True)
    locality = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
    landmark = models.CharField(max_length=100, blank=True)
    additional_instructions = models.TextField(blank=True)

    def __str__(self):
        return self.name





from django.db import models
import os
import re

def restaurant_photo_upload_to(instance, filename):
    restaurant_name = re.sub(r'\s+', '_', instance.restaurant_name)  # Replace spaces with underscores
    extension = os.path.splitext(filename)[1]
    return f'static/images/restaurant_photos/{restaurant_name}{extension}'


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    contact_no = models.IntegerField()
    address = models.TextField()  # Single field for the entire address
    cuisine_type = models.CharField(max_length=100)
    opening_hours = models.CharField(max_length=100)
    pan_card = models.FileField(upload_to='static/images/pan_cards/', blank=True, null=True)  # File upload for PAN card
    restaurant_photo = models.ImageField(upload_to=restaurant_photo_upload_to, blank=True, null=True)  # Image upload for restaurant photo

    # Bank details
    account_number = models.IntegerField()
    account_name = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)
    branch = models.CharField(max_length=100)

    def __str__(self):
        return self.restaurant_name



# MenuItem Model for managing food items in the menu
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/images/menu_items/', blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    raw_materials = models.TextField()  # Comma-separated list of raw materials

    def __str__(self):
        return self.name


# InventoryItem Model for managing the inventory of raw materials
class InventoryItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='inventory_items')
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready for Delivery'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    #customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.id = None

    def __str__(self):
        return f"Order {self.id} by {self.customer.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.CharField(max_length=100)  # Replace with a ForeignKey to a Menu model if needed
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.menu_item} (x{self.quantity})"

# Income Model to track daily income of the restaurant
class Income(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='incomes')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.amount} - {self.date}"






class Mealer(models.Model):
    # Personal information
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    address = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    # Identification documents
    adhar_card = models.FileField(upload_to='static/documents/adhar_cards/', blank=True, null=True)
    pan_card = models.FileField(upload_to='static/documents/pan_cards/', blank=True, null=True)

    # Vehicle documents
    driving_license = models.FileField(upload_to='static/documents/driving_licenses/', blank=True, null=True)
    registration_certificate = models.FileField(upload_to='static/documents/vehicle_registration/', blank=True, null=True)
    insurance = models.FileField(upload_to='static/documents/vehicle_insurance/', blank=True, null=True)
    license_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.customer.name}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} (x{self.quantity})"

    def get_total_price(self):
        return self.menu_item.price * self.quantity