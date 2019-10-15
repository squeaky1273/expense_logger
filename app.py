from flask import Flask, render_template, request, redirect url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
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

@app.route('/expense/new')
def expense_new():
    """Return to the new expense log page"""
    return render_template('expense_new.html', expense={}, title='New Expense Log')

@app.route('/expense', methods=['POST'])
def expense_submit():
    """Submit a new expense log. User can add log information for purchases made"""
    expense = {
        'product name': request.form.get('product name'),
        'price': request.form.get('price'),
        'payment method': request.form.get('payment method')
    }
    print(expense)
    expense_id = expense.insert_one(expense).inserted_id
    return redirect(url_for('expense_show', expense_id=expense_id))

@app.route('/expense/<expense_id>')
def expense_show():
    """Show a single expense log"""
    expense = expense.find_one({'_id': ObjectId(expense_id)})
    return render_template('expense_edit.html', expense=expense, title='Edit Expense Log')