from django import forms
from .models import Customer


class CustomerSignupForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'password', 'mobile_number',
                  'house_number', 'street_number', 'locality', 'city',
                  'state', 'pin_code', 'landmark', 'additional_instructions']
        widgets = {
            'password': forms.PasswordInput(),
            'additional_instructions': forms.Textarea(attrs={'rows': 4}),
        }

class CustomerLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")



from .models import Restaurant

class RestaurantSignupForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name', 'address', 'contact_no', 'email', 'password', 'cuisine_type', 'opening_hours', 'pan_card', 'restaurant_photo',
                  'account_number','account_name', 'ifsc_code', 'branch']
        widgets = {
            'password': forms.PasswordInput(),
            'opening_hours': forms.Textarea(attrs={'rows': 2}),
        }

class RestaurantLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")



from .models import Mealer  # Ensure this model is defined in your models.py

class MealerSignupForm(forms.ModelForm):
    class Meta:
        model = Mealer
        fields = [
            'name', 'date_of_birth', 'gender', 'address', 'email', 'password', 'mobile_number',
            'adhar_card', 'pan_card', 'driving_license',
            'registration_certificate', 'insurance', 'license_number'
        ]
        widgets = {
            'password': forms.PasswordInput(),  # To render as a password field
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date picker
            'gender': forms.RadioSelect(choices=['Male','Female']),  # Gender options
        }


class MealerLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")



from .models import Restaurant, MenuItem, InventoryItem

# Form for restaurant profile update
class RestaurantProfileForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'owner_name', 'email', 'mobile_number', 'address', 'image']

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Restaurant Name'}))
    owner_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    mobile_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}))
    address = forms.CharField(max_length=255, required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Restaurant Address'}))
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if not mobile_number.isdigit():
            raise forms.ValidationError('Please enter a valid mobile number.')
        return mobile_number

# Form for adding/updating menu items
class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'image', 'price', 'quantity', 'raw_materials']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        'raw_materials': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),}

    def clean_raw_materials(self):
        raw_materials = self.cleaned_data.get('raw_materials')
        # Ensuring raw materials are separated by commas
        if ',' not in raw_materials:
            raise forms.ValidationError('Please separate raw materials with commas.')
        return raw_materials

# Form for adding/updating inventory items
class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'unit_price']

    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inventory Item Name'}))
    quantity = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}))
    unit_price = forms.DecimalField(max_digits=5, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Unit Price'}))

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be a positive number.')
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data.get('unit_price')
        if unit_price <= 0:
            raise forms.ValidationError('Unit price must be a positive number.')
        return unit_price
