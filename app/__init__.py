from flask import Flask, request
from backend.backend_manager import backend_manager

app = Flask(__name__, template_folder="templates")

app.config['SECRET_KEY'] = 'the random string' 
app.config["backend"] = backend_manager()

from app import index
