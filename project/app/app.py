from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
def get_db():
    client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://mongodb:27017/'))
    return client.taskdb

# Simple health check endpoint
@app.route('/health')
def health_check():
    try:
        # Try to connect to the database
        db = get_db()
        db.admin.command('ping')
        return {'status': 'healthy'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
 
@app.route('/')
def index():
    tasks = get_db().tasks.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task = {
            'title': request.form['title'],
            'description': request.form['description']
        }
        get_db().tasks.insert_one(task)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_db().tasks.find_one({'_id': ObjectId(task_id)})
    if request.method == 'POST':
        updated_task = {
            'title': request.form['title'],
            'description': request.form['description']
        }
        get_db().tasks.update_one({'_id': ObjectId(task_id)}, {'$set': updated_task})
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/delete/<task_id>')
def delete_task(task_id):
    get_db().tasks.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
