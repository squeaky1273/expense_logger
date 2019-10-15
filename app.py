from flask import Flask, render_template, request, redirect url_for
from pymongo import MongoClient
from bson.ogjectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Contractor')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

app = Flask(__name__)

@app.route('/')