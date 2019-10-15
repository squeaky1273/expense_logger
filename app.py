from flask import Flask, render_template, request, redirect url_for
from pymongo import MongoClient
from bson.ogjectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

expense =db.expenses

app = Flask(__name__)

@app.route('/')
def expense_index():
    """Return homepage"""
    return render_template('expense_index.html', expenses=expense.find())