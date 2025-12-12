# 🛒 E-Commerce Backend (Django + DRF)

A simple, modular e-commerce backend built with **Django** and **Django REST Framework**.
This project includes core features like user accounts, product management, cart handling, orders, and a basic payment workflow.

---

## 🚀 Features

### **🧑‍💻 Authentication & Users**

* Custom user model
* Login, Register, Token authentication
* Address management

### **📦 Products**

* Categories
* Product
* Product Variants (size, color, stock)
* Admin-friendly CRUD

### **🛍️ Cart System**

* Cart per user
* Cart items
* Quantity updates
* Automatic total calculation

### **📑 Orders**

* Order + Order Items
* Coupon support
* Status workflow

  * Pending → Paid → Shipped → Delivered

### **💳 Payment (Sandbox Mode)**

* Fake payment API
* One-to-one Order → Payment
* Transaction record
* Marks order as **PAID**
* Stock deduction on checkout

---

## 📁 Project Structure

```
/cart
/orders
/products
/users
/payments
```

Each app is fully isolated with its own models, serializers, and views.

---

## 🔧 Tech Stack

* **Python 3**
* **Django 5/6**
* **Django REST Framework**
* SQLite / PostgreSQL (optional)
* Token authentication

---

## ▶️ Running the Project

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## 📬 API Overview

### Products

* `GET /api/products/`
* `POST /api/products/` (admin only)

### Cart

* `GET /carts/`
* `POST /carts/`
* `POST /carts/checkout/`

### Orders

* `GET /orders/`
* `POST /orders/`

### Payment

* `POST /payments/pay/<order_id>/`

---

## 🧪 Testing

You can test all endpoints using:

* **DRF browsable API**
* **Postman**
* **cURL**

---

## 📄 License

This project is free to use for learning and experimentation.