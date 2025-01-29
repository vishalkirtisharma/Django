# E-commerce Application Documentation

## Introduction
This documentation provides an overview of the e-commerce application built using Django. The application allows users to browse products, add them to a cart, and complete purchases through a checkout process.

## Project Structure
The project is organized into several key directories and files:
- **ecomsite/**: The main project directory containing settings and configuration files.
- **shop/**: The application directory containing models, views, templates, and static files related to the shop functionality.
- **manage.py**: A command-line utility for administrative tasks.
- **db.sqlite3**: The SQLite database file used to store application data.

## Models
### ProductsModel
- **title**: CharField - The name of the product.
- **price**: FloatField - The original price of the product.
- **discount_price**: FloatField - The discounted price of the product.
- **category**: CharField - The category of the product.
- **description**: TextField - A detailed description of the product.
- **image**: CharField - URL of the product image.

### OrderModel
- **item**: CharField - The items included in the order.
- **name**: CharField - The customer's name.
- **address**: TextField - The customer's address.
- **phone**: IntegerField - The customer's phone number.
- **city**: CharField - The customer's city.

## Views
### index
- Displays a list of all products with filtering and pagination.
- Renders the `index.html` template.

### detail
- Displays detailed information about a specific product.
- Renders the `details.html` template.

### checkout
- Handles the checkout process, including saving order details.
- Renders the `checkout.html` template.

## Templates
### index.html
- Displays the main shop page with product listings and pagination.

### checkout.html
- Provides a form for users to enter their details and complete the order.

## Admin Interface
- Custom configuration for managing products and orders through the Django admin interface.
- Allows for easy addition, modification, and deletion of products.

## How to Run the Application
1. Ensure you have Python and Django installed.
2. Navigate to the project directory.
3. Run the command: `python manage.py runserver` to start the development server.
4. Access the application at `http://127.0.0.1:8000/`.
