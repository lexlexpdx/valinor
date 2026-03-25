from flask import Flask
from config import Config

# Creates application object as an instance of class Flask
app = Flask(__name__)
app.config.from_object(Config)

# importing at the bottom of the script prevents circular imports, which is a 
# common problem with Flask applications
from app import routes