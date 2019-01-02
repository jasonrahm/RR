from config import Configuration
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object(Configuration)
mysql = MySQL(app)