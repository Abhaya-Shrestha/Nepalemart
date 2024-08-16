
# Nepalemart
This is the repository for an e-commerce project.
## Getting Started
Follow these steps to set up the project on your local machine.
#
**Step 1: Clone the Repository**
Open your terminal and run the following command to clone the repository:

```bash
git clone https://github.com/Abhaya-Shrestha/Nepalemart
```

**Step 2: Navigate to the Project Directory**
Move into the e-commerce folder with the following command:
```bash
cd Nepalemart/ecommerce/
```
**Step 3: Install Required Packages**
Install all the required Python packages using pip:
```bash
pip install -r requirements.txt
```
**Step 4: Update Code in `cart.py`**

Make the necessary changes to the `C:\Users\[UserName]\AppData\Local\Programs\Python\Python312\Lib\site-packages\cart\cart.py` file. Replace the code with:

```python
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

**Step 5: Run the Development Server**
Start the development server with the following command:
```bash
python manage.py runserver
```
You should now be able to access the application locally at `http://127.0.0.1:8000/`. `username: Abhay / password: admin`

