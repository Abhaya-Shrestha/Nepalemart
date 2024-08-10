# Nepalemart
Nepalemart is a comprehensive e-commerce platform developed as a college project for the Bachelor of Information Technology (BIT) course. This project aims to provide a robust and user-friendly online shopping experience tailored for users in Nepal. It integrates various features to enhance user engagement and streamline the purchasing process.
Key Features
1.	Product Catalog: A dynamic catalog of products with detailed descriptions, images, and prices.
2.	Shopping Cart: An intuitive shopping cart system that allows users to add, remove, and modify items.
3.	Checkout Process: A secure and straightforward checkout process with multiple payment options.
4.	User Accounts: User account management with registration, login, and profile management features.
1.	Order Tracking: Real-time order tracking and status updates for users.
2.	Search and Filters: Advanced search functionality and filters to help users find products easily.
3.	Responsive Design: A mobile-friendly design ensuring a consistent experience across different devices.
4.	Technologies Used
5.	Django: The core framework for building the backend, handling the application logic and data management.
6.	Celery: For asynchronous task management and background processing.
7.	Cloudinary: For managing and optimizing media files.
8.	Stripe: For secure payment processing.

**Installation**
1.	**Clone the Repository:**
    git clone https://github.com/DeadPool0087/Nepalemart.git
    cd Nepalemart/ecommerce/
2.	**Set Up a Virtual Environment:**
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3.	**Install Dependencies:**
      pip install -r requirements.txt
4.	**Run Migrations:**
	    python manage.py migrate
5.	**Start the Development Server:**
      python manage.py runserver
