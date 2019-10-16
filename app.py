from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Expense_Logger')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

expenses =db.expenses

app = Flask(__name__)

@app.route('/')
def expense_index():
    """Return homepage"""
    return render_template('expense_index.html', expenses=expenses.find())

@app.route('/expense/new')
def expense_new():
    """Return to the new expense log page"""
    return render_template('expense_new.html', expense={}, title='New Expense Log')

@app.route('/expense', methods=['POST'])
def expense_submit():
    """Submit a new expense log. User can add log information for purchases made"""
    expense = {
        'date_purchased': request.form.get('date purchased'),
        'product_name': request.form.get('product name'),
        'price': request.form.get('price'),
        'payment_method': request.form.get('payment method')
    }
    print(expense)
    expense_id = expenses.insert_one(expense).inserted_id
    return redirect(url_for('expense_show', expense_id=expense_id))

@app.route('/expense/<expense_id>')
def expense_show(expense_id):
    """Show a single expense log"""
    expense = expenses.find_one({'_id': ObjectId(expense_id)})
    return render_template('expense_show.html', expense=expense)

@app.route('/expense/<expense_id>/edit')
def expense_edit(expense_id):
    """Show the edit form for an expense log"""
    expense = expenses.find_one({'_id': ObjectId(expense_id)})
    return render_template('expense_edit.html', expense=expense, title='Edit Expense Log')

@app.route('/expense/<expense_id>', method=['POST'])
def expense_update(expense_id):
    """Submit an edited expense log"""
    updated_expense = {
        'date_purchased': request.form.get('date purchased'),
        'product_name': request.form.get('product name'),
        'price': request.form.get('price'),
        'payment_method': request.form.get('payment method')
    }
    expenses.update_one(
        {'_id': ObjectId(expense_id)},
        {'$set': updated_expense})
    return redirect(url_for('expense_show', expense_id=expense_id))

@app.route('/expense/<adoption_id>/delete', methods=['POST'])
def expense_delete(expense_id):
    """Delete one expense log."""
    expenses.delete_one({'_id': ObjectId(expense_id)})
    return redirect(url_for('expense_index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))