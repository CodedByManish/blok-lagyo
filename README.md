
# 🍔 Blok Lagyo! (Food Delivery System)

[![Django Version](https://img.shields.io/badge/django-5.0+-092e20?style=for-the-badge&logo=django)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/python-3.11+-3776ab?style=for-the-badge&logo=python)](https://www.python.org/)
[![Payment Gateway](https://img.shields.io/badge/Payment-eSewa%20%7C%20Khalti-60bb46?style=for-the-badge)](https://esewa.com.np)

**Blok Lagyo!** is a high-performance, full-stack food delivery application built with Django. It features a modern UI, a seamless shopping cart experience, and integrated dual-payment gateways for the Nepalese market.

---

## ✨ Key Features

* 🛒 **Smart Shopping Cart:** Persistent session-based cart management.
* 💳 **Dual Payment Integration:**
    * **eSewa v2:** Integrated via HMAC-SHA256 signature for secure transactions.
    * **Khalti v2:** Server-side initiation for seamless ePayment flow.
* 📍 **Order Management:** Automated order creation and line-item tracking.
* 🎨 **Modern UI:** Crafted with Tailwind CSS for a premium look and feel.
* 🔒 **Secure Checkout:** User authentication and server-side amount verification.

---

## 🛠️ Tech Stack

| Frontend | Backend | Database | Payments |
| :--- | :--- | :--- | :--- |
| Tailwind CSS | Django | SQLite / PostgreSQL | eSewa v2 |
| JavaScript (ES6) | Python 3.11+ | Django ORM | Khalti v2 |

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/blok-lagyo.git](https://github.com/yourusername/blok-lagyo.git)
   cd blok-lagyo

 * Create and Activate Virtual Environment:
   python -m venv env
# Windows:
.\env\Scripts\activate
# Linux/Mac:
source env/bin/activate

 * Install Dependencies:
   pip install -r requirements.txt

 * Setup Environment Variables:
   Create a .env file or update settings.py with your credentials:
   KHALTI_SECRET_KEY = "test_secret_key_..."
ESEWA_SECRET_KEY = "8gBm/:&EnhH.1/q"

 * Run Migrations:
   python manage.py makemigrations
python manage.py migrate

 * Start the Engine:
   python manage.py runserver

💳 Payment Integration Logic
eSewa (v2)
Uses a client-side POST redirection. The signature is generated using HMAC-SHA256 hashing of total_amount, transaction_uuid, and product_code.
Khalti (v2)
Uses a server-to-server API call. We initiate the payment by sending a JSON payload to a.khalti.com and receiving a payment_url for user redirection.
📸 Screenshots
| Checkout Page | Payment Redirection |
|---|---|
|  |  |
🤝 Contributing
 * Fork the Project
 * Create your Feature Branch (git checkout -b feature/AmazingFeature)
 * Commit your Changes (git commit -m 'Add some AmazingFeature')
 * Push to the Branch (git push origin feature/AmazingFeature)
 * Open a Pull Request
📄 License
Distributed under the MIT License. See LICENSE for more information.
<p align="center">
Developed by Manish in Nepal 🇳🇵
</p>

