from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Expense_Logger')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()

expense_log = db.expenses

app = Flask(__name__)

@app.route('/')
def expenses_index():
    """Return homepage"""
    return render_template('expenses_index.html', expenses=expense_log.find())

@app.route('/expenses/new')
def expenses_new():
    """Return to the new expense log page"""
    return render_template('expenses_new.html', expense={}, title='New Expense Log')

@app.route('/expenses', methods=['POST'])
def expenses_submit():
    """Submit a new expense log. User can add log information for purchases made"""
    expense = {
        'date_purchased': request.form.get('date_purchased'),
        'product_name': request.form.get('product_name'),
        'price': request.form.get('price'),
        'payment_method': request.form.get('payment_method')
    }
    print(expense)
    expense_id = expense_log.insert_one(expense).inserted_id
    return redirect(url_for('expenses_show', expense_id=expense_id))

@app.route('/expenses/<expense_id>')
def expenses_show(expense_id):
    """Show a single expense log"""
    expense = expense_log.find_one({'_id': ObjectId(expense_id)})
    return render_template('expenses_show.html', expense=expense)

@app.route('/expenses/<expense_id>/edit')
def expenses_edit(expense_id):
    """Show the edit form for an expense log"""
    expense = expense_log.find_one({'_id': ObjectId(expense_id)})
    return render_template('expenses_edit.html', expense=expense, title='Edit Expense Log')

@app.route('/expenses/<expense_id>', methods=['POST'])
def expenses_update(expense_id):
    """Submit an edited expense log"""
    updated_expense = {
        'date_purchased': request.form.get('date_purchased'),
        'product_name': request.form.get('product_name'),
        'price': request.form.get('price'),
        'payment_method': request.form.get('payment_method')
    }
    expense_log.update_one(
        {'_id': ObjectId(expense_id)},
        {'$set': updated_expense})
    return redirect(url_for('expenses_show', expense_id=expense_id))

@app.route('/expenses/<expense_id>/delete', methods=['POST'])
def expenses_delete(expense_id):
    """Delete one expense log."""
    expense_log.delete_one({'_id': ObjectId(expense_id)})
    return redirect(url_for('expenses_index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))