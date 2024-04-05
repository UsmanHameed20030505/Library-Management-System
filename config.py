import os

SECRET_KEY = os.urandom(24)  # Generate a random secret key
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.getcwd(), 'library.db') 
