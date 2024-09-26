Introduction
  The Inventory Management System API is a backend service for managing products and inventory, built using Django Rest Framework. It includes JWT-based authentication for security, PostgreSQL for data storage, Redis for caching, and a logging mechanism to track API events and errors.

Technologies
  Django - Web framework
  Django REST Framework (DRF) - API framework
  PostgreSQL - Relational database
  Redis - In-memory caching system
  JWT (JSON Web Tokens) - Secure user authentication
  Docker - Containerization (optional)
  Python 3.9+
  
Features
  JWT authentication for secure access
  CRUD operations for managing inventory items
  Redis caching for frequently accessed items
  Comprehensive error handling and logging
  Unit tests for all API endpoints
  Prerequisites
  
Ensure you have the following installed on your system:
  Python 3.9+
  PostgreSQL
  Redis
  Virtualenv (optional but recommended)

Installation
  Clone the repository:
    https://github.com/Prashant-Raghorte/inventory_system
    
cd inventory

Create a virtual environment:
  python3 -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
  
Install dependencies:
  pip install -r requirements.txt

Running the Application
  Start the Redis server:
    redis-server
    
Start the Django server:
  python manage.py runserver
  
Running Tests
  To run unit tests, use the following command:
    python manage.py test
