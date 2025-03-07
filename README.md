# 🍽️ Mealzo - AI-Powered Food Delivery Platform

![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Stripe](https://img.shields.io/badge/Stripe-Payments-purple)
![Google Maps API](https://img.shields.io/badge/Google%20Maps-API-orange)

Welcome to **Mealzo**, a full-featured AI-powered food delivery platform built with **Django**. Mealzo offers a seamless online food ordering experience with AI-based recommendations, real-time order tracking, secure payments, and dedicated dashboards for customers, restaurants, and delivery agents.

---

## 🌟 Features

### 🚀 Customer Features
- **AI-Based Food Recommendation**:
  - Personalized suggestions based on order history and preferences.
- **Secure Authentication**:
  - Supports Google login, mobile OTP verification, and email-based sign-in.
- **Real-Time Order Tracking**:
  - Track orders on a live map using **Google Maps API**.
- **Payment Integration**:
  - Pay securely using **Stripe and UPI payments**.
- **Interactive Chatbot Support**:
  - Get help with orders via a built-in chatbot.
- **Restaurant Discovery**:
  - Search and explore restaurants based on location, ratings, and cuisine type.

### 🍔 Restaurant Features
- **Restaurant Dashboard**:
  - Manage orders, update menu items, and track daily earnings.
- **Stock Management**:
  - Auto-updates stock after each order.
- **Customer Feedback & Ratings**:
  - View real-time item ratings and customer reviews.
- **Promotions & Discounts**:
  - Publish special offers for customers.

### 🚴 Delivery Partner Features
- **Delivery Dashboard**:
  - View assigned orders, earnings, and order history.
- **Live Order Requests**:
  - Accept or reject delivery requests in real-time.
- **Google Maps Integration**:
  - Navigate efficiently to pickup and delivery locations.

---

## 🔄 User Flow

1. **Registration & Login**:
   - Customers, restaurants, and delivery agents register via OTP or email authentication.
   - Each user type is redirected to their respective homepage after login.

2. **Placing an Order**:
   - Customers browse restaurants, add items to their cart, and proceed to checkout.
   - Payment is completed through Stripe/UPI, and order details are sent to the restaurant.

3. **Order Processing**:
   - Restaurants accept and prepare the order.
   - The system assigns a delivery partner based on availability.

4. **Delivery & Tracking**:
   - Customers track their order’s real-time location on a map.
   - Delivery agents complete the order and update the status.

5. **Feedback & Ratings**:
   - Customers rate the restaurant and delivery service after receiving the order.

---

## 📌 Quick Start

### Prerequisites
- Python 3.8+
- Django 4.2+
- Stripe API key
- Google Maps API key
- 2Factor API key (for OTP verification)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mealzo.git
   cd mealzo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Add your API keys to `.env`:
     ```
     STRIPE_API_KEY=your_stripe_key
     GOOGLE_MAPS_API_KEY=your_google_maps_key
     TWO_FACTOR_API_KEY=your_2factor_key
     ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://localhost:8000`.

---

## 📂 Project Structure

```
Mealzo/
│
├── mealzoapp/                # Main Django app
│   ├── templates/            # HTML templates
│   ├── static/               # CSS, JS, and images
│   ├── models.py             # Database models
│   ├── views.py              # Business logic and API endpoints
│   ├── urls.py               # URL routing
│   └── forms.py              # Form handling
│
├── authentication/           # Handles user authentication and OTP
├── payments/                 # Handles Stripe & UPI payments
├── tracking/                 # Order tracking using Google Maps API
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # Project documentation
```

---

## 🛠️ Technologies Used

- **Django**: Backend framework
- **SQLite**: Database
- **Google Maps API**: Real-time location tracking
- **Stripe API**: Secure payments
- **2Factor API**: OTP-based authentication
- **Bootstrap**: Responsive UI design
- **JavaScript & jQuery**: Client-side enhancements

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## 📧 Contact

For any questions or feedback, feel free to reach out:

- **Email**: vendotha@gmail.com
- **GitHub**: [vendotha](https://github.com/vendotha)
- **LinkedIn**: [Buvananand Vendotha](https://linkedin.com/in/vendotha)

---

## 🙏 Acknowledgments

- Thanks to **Google** for the Maps API.
- Thanks to **Stripe** for seamless payment processing.
- Thanks to the **Django** community for an amazing framework.

---

## 🌐 Live Demo

Check out the live demo of Mealzo [here](#) (coming soon).

---

Made with ❤️ by [Bhuvan Vendotha](https://github.com/vendotha).

