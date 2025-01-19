from django.urls import path
from . import views
from .views import customer_login, customer_logout, restaurant_login, restaurant_logout, mealer_login, mealer_logout

urlpatterns = [
    # Main page and general views
    path('', views.main_page, name='main_page'),  # Main page URL
    path('customer_signup/', views.customer_signup, name='customer_signup'),  # Customer signup
    path('restaurant_signup/', views.restaurant_signup, name='restaurant_signup'),  # Restaurant signup
    path('mealer_signup/', views.mealer_signup, name='mealer_signup'),  # Mealer signup

    # Customer login/logout and home page
    path('login/', customer_login, name='login'),  # Customer login URL
    path('logout/', customer_logout, name='logout'),  # Customer logout URL
    path('home/', views.customer_home, name='customer_home'),  # Customer home URL
    path('customer_profile/', views.customer_profile, name='customer_profile'),

    # Restaurant login/logout and home page
    path('restaurant_login/', restaurant_login, name='restaurant_login'),  # Restaurant login URL
    path('restaurant_logout/', restaurant_logout, name='restaurant_logout'),  # Restaurant logout URL
    path('restaurant_home/', views.restaurant_home, name='restaurant_home'),  # Restaurant home URL
    path('restaurant/delete/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),

    # Mealer login/logout and home page
    path('mealer_login/', mealer_login, name='mealer_login'),  # Mealer login URL
    path('mealer_logout/', mealer_logout, name='mealer_logout'),  # Mealer logout URL
    path('mealer/profile/', views.mealer_profile, name='mealer_profile'),
    path('mealer_home/', views.mealer_home, name='mealer_home'),  # Mealer home URL

    # Additional pages for managing restaurant's menu and inventory (optional)
    path('restaurant_profile/', views.restaurant_profile, name='restaurant_profile'),
    path('manage_menu/', views.manage_menu, name='manage_menu'),  # Manage menu items
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),  # Add menu item
    path('manage_inventory/', views.manage_inventory, name='manage_inventory'),  # Manage inventory items
    path('add_inventory_item/', views.add_inventory_item, name='add_inventory_item'),  # Add inventory item

    # Search results
    path('search/', views.search_restaurants, name='search_restaurants'),
    path('restaurant/search-menu/', views.search_menu, name='search_menu'),

    # Cart and Checkout
    path('add-to-cart/<int:menu_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('update-cart-quantity/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-item-from-cart/<int:item_id>/', views.remove_item_from_cart, name='remove_item_from_cart'),
    path('checkout/', views.checkout_view, name='checkout_view'),

    # Checkout session and order success
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('order-success/', views.order_success_page, name='order_success'),

    # Order Status Update (for restaurant to accept/reject orders)
    path('update-order-status/<int:order_id>/', views.update_order_status, name='update_order_status'),  # Update order status URL
]
