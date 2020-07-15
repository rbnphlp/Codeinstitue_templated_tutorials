import os
from flask import Flask,render_template,request,redirect,url_for
from flask_pymongo import PyMongo 
import requests
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_DBNAME"]='TaskManager'
app.config["MONGO_URI"]="mongodb+srv://rbnphlp:Hebrew13011990@cluster0.rxhwu.mongodb.net/TaskManager?retryWrites=true&w=majority"

mongo=PyMongo(app)


@app.route('/')

@app.route("/get_tasks")
def get_tasks():
    return render_template("tasks.html",tasks=mongo.db.tasks.find())


@app.route("/add_tasks")
def add_tasks():

    return render_template("add_tasks.html",categories=mongo.db.categories.find())

@app.route('/insert_task', methods=['POST'])
def insert_task():
    tasks = mongo.db.tasks
    tasks.insert_one(request.form.to_dict())
    return redirect(url_for('get_tasks'))

@app.route('/edit_tasks/<task_id>')
def edit_tasks(task_id):
    the_task =  mongo.db.tasks.find_one({"_id": ObjectId(task_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('edit_tasks.html', task=the_task,
                           categories=all_categories)

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

