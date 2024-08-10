# Nepalemart

**Nepalemart** is a comprehensive e-commerce platform developed as a college project for the Bachelor of Information Technology (BIT) course. This project aims to provide a robust and user-friendly online shopping experience tailored for users in Nepal. It integrates various features to enhance user engagement and streamline the purchasing process.

## Key Features

1. **Product Catalog:** A dynamic catalog of products with detailed descriptions, images, and prices.
2. **Shopping Cart:** An intuitive shopping cart system that allows users to add, remove, and modify items.
3. **Checkout Process:** A secure and straightforward checkout process with multiple payment options.
4. **User Accounts:** User account management with registration, login, and profile management features.
5. **Order Tracking:** Real-time order tracking and status updates for users.
6. **Search and Filters:** Advanced search functionality and filters to help users find products easily.
7. **Responsive Design:** A mobile-friendly design ensuring a consistent experience across different devices.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/DeadPool0087/Nepalemart.git
    cd Nepalemart
    ```

2. **Set Up a Virtual Environment:**

    ```bash
    python -m venv venv
    # On macOS and Linux: source venv/bin/activate
    # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    cd ecommerce
    ```

4. **Start the Development Server:**

    ```bash
    python manage.py runserver
    ```
5. **Update cart.py**
    `goto to : C:\Users\[YourUserName(eg:Abhay)]\AppData\Local\Programs\Python\Python312\Lib\site-packages\cart `
    ```bash
    from decimal import Decimal
    from django.conf import settings
    from django.http import HttpResponse
    from django.shortcuts import render, redirect
    class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    def add(self, product, quantity=1, action=None):
        """
        Add a product to the cart or update its quantity.
        """
        id = product.id
        newItem = True
        if str(product.id) not in self.cart.keys():
            discount_price = product.price - (product.price * product.Discount / 100)
            self.cart[product.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'product_name': product.product_name,
                'quantity': 1,
                'price': int(discount_price),
                'featured_image': product.featured_image.url,
                'tax':product.tax,
                'packing_cost': product.packing_cost,
            }
        else:
            newItem = True
            for key, value in self.cart.items():
                if key == str(product.id):
                    value['quantity'] = value['quantity'] + 1
                    newItem = False
                    self.save()
                    break
            if newItem == True:
                self.cart[product.id] = {
                    'userid': self.request,
                    'product_id': product.id,
                    'name': product.name,
                    'quantity': 1,
                    'price': str(product.price),
                    'image': product.image.url,
                }
        self.save()
    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):

                value['quantity'] = value['quantity'] - 1
                if(value['quantity'] < 1):
                    return redirect('cart:cart_detail')
                self.save()
                break
            else:
                print("Something Wrong")

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
    ```
Open your browser and navigate to `http://127.0.0.1:8000/` to see the application in action. `user:Abhay / password: admin`
email used for forgot password: 

## Acknowledgements

Special thanks to the open-source community and the libraries used in this project and my friends to help me build this project.

## About the Project

This project was developed as part of the Bachelor of Information Technology (BIT) course at Mahendra Multiple Campus, Nepalgunj. It demonstrates practical skills in web development, including backend development with Django, asynchronous task handling with Celery, and integration of third-party services.
