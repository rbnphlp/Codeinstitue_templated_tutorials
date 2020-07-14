import os
from flask import Flask,render_template
from flask_pymongo import PyMongo

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


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

