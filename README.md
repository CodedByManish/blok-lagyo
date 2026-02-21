<div align="center">

# 🍔 Bhok-Lagyo  
### Django-Powered Food Delivery System  

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2+-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-blue?logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> A secure, server-side rendered food delivery system built using Django’s MVT architecture with multi-gateway payment integration.

</div>

---

## 📌 Table of Contents

- [📖 Introduction](#-introduction)
- [⚙️ System Architecture](#️-system-architecture)
- [🚀 Key Features](#-key-features)
- [💳 Payment Integration](#-payment-integration)
- [🛠️ Technology Stack](#️-technology-stack)
- [🖥️ Installation & Setup](#️-installation--setup)
- [🛡️ Security Measures](#️-security-measures)
- [📂 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📸 Screenshots (Optional)](#-screenshots-optional)

---

## 📖 Introduction

**Bhok-Lagyo** is a robust food delivery application built using **Django (MVT architecture)**.  
It focuses on **security, financial accuracy, and scalable design** while maintaining a clean and responsive UI.

### Users Can:

- 🛒 Browse a dynamic food catalog  
- 🧺 Add items to a session-based persistent cart  
- 💳 Pay securely using:
  - eSewa  
  - Khalti  
  - PayPal  

---

## ⚙️ System Architecture

The system follows Django’s **Model-View-Template (MVT)** pattern.

### 🔐 Authentication & User Management
- Powered by Django’s built-in `auth` system
- Secure login & session-based user tracking

### 🍽️ Product Catalog
- Managed inside the `Products` app
- `models.py` defines schema
- Full CRUD from Django Admin
- Real-time menu updates

### 🛒 Stateful Cart System
- Uses Django **Sessions**
- Prevents database clutter from abandoned carts
- Cart persists even after page refresh

### 🧾 Checkout & Order Persistence
- Server-side validation prevents price tampering
- Cart revalidated against database prices
- Permanent storage in:
  - `Order`
  - `OrderLineItem`

---

## 💳 Payment Integration

| Gateway  | Integration Method |
|-----------|-------------------|
| **eSewa** | Server-side signature + HTML form redirect |
| **Khalti** | Secure Server-to-Server API handshake |
| **PayPal** | JavaScript SDK |

All payment flows ensure:
- Server-side verification
- Accurate Decimal-based calculations
- Secure key handling via environment variables

---

## 🚀 Key Features

- ✅ Persistent Cart via Sessions  
- ✅ Multi-Gateway Payments (eSewa, Khalti, PayPal)  
- ✅ Django Admin Dashboard  
- ✅ Tailwind CSS Responsive UI  
- ✅ Server-Side Checkout Validation  
- ✅ Financial Accuracy using Python `Decimal`  
- ✅ Clean MVT Architecture  

---

## 🛠️ Technology Stack

| Layer        | Technology |
|--------------|------------|
| Backend      | Python 3.10+, Django 4.2+ |
| Database     | SQLite (Development), PostgreSQL (Production) |
| Payments     | eSewa API v2, Khalti ePayment v2, PayPal SDK |
| Frontend     | Django Templates, Tailwind CSS |
| Server Logic | 99.5% Python, 0.5% JavaScript |

---

## 🖥️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/CodedByManish/blok-lagyo.git
cd blok-lagyo
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Mac/Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file:

```env
KHALTI_SECRET_KEY=your_test_key
ESEWA_SECRET_KEY=8gBm/:&EnhH.1/q
PAYPAL_TEST=True
```

---

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Start Development Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

## 🛡️ Security Measures

- 🔐 CSRF Protection enabled on all POST requests  
- 🧮 Server-side price recalculation during checkout  
- 🔑 API keys stored in environment variables  
- 🛑 Prevention of client-side price manipulation  
- 💰 Decimal-based currency calculations  

---

## 📂 Project Structure

```bash
blok-lagyo/
│
├── products/          # Product catalog app
├── orders/            # Order & checkout logic
├── payments/          # Payment gateway integrations
├── templates/         # Django Templates
├── static/            # CSS, JS, Images
├── docs/              # Screenshots & demo assets
├── manage.py
└── requirements.txt
```

---

## 📸 Screenshots (Optional)

Create a `docs/` folder and add:

```markdown
![Homepage](docs/homepage.png)
![Checkout](docs/checkout.png)
![Payment Redirect](docs/paypal_redirect.png)
```

You may also include:
- Admin dashboard screenshot
- Cart page
- Payment success page
- Demo GIF of checkout flow

---

## 🤝 Contributing

1. Fork the project  
2. Create your feature branch  

```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes  
>>>>>>> 1c98f8f (Add PayPal integration and update README.md)

```bash
git commit -m "Add AmazingFeature"
```

4. Push to branch  

```bash
git push origin feature/AmazingFeature"
```

5. Open a Pull Request  

---

## 📄 License

Distributed under the **MIT License**.  
See `LICENSE` for more information.

---

<div align="center">

### ⭐ If you like this project, give it a star!

Built by **CodedByManish** using Django

</div>