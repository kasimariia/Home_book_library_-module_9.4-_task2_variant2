from flask import Flask, request, render_template, redirect, url_for
from collections import namedtuple
from forms import EmailPasswordForm, TodoForm 
from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, BooleanField
from models import todos

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

User = namedtuple("User", field_names=["email", "password"])
user = User(email="john@black.com", password="black")

@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("todos_list"))

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = EmailPasswordForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            if form.email.data == user.email and form.password.data == user.password:
                return "You are logged in"
            else:
                return "Wrong credentials!!"
        else:
            error = form.errors
    return render_template("login.html", form=form, error=error)


@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""

    if request.method == "POST":
        if form.validate_on_submit():
            todos.create({
                "title": form.title.data,
                "author": form.author.data,
                "year": form.year.data,
                "pages": form.pages.data
            })
            todos.save_all()
            return redirect(url_for("todos_list"))

    if request.method == "GET" and "delete" in request.args:
        todo_id = int(request.args["delete"])
        success = todos.delete(todo_id)
        if success:
            todos.save_all()

    return render_template("todos.html", form=form, todos=todos.all(), error=error)




@app.route("/todos/<int:todo_id>/", methods=["GET", "POST", "DELETE"])
def todo_details(todo_id):
    todo = todos.get(todo_id)
    form = TodoForm(data=todo)

    if request.method == "POST":
        if form.validate_on_submit():
            todos.update(todo_id, form.data)
            return redirect(url_for("todos_list"))
    elif request.method == "DELETE":
        todos.delete(todo_id)
        return redirect(url_for("todos_list"))
    
    return render_template("todo.html", form=form, todo_id=todo_id)


@app.route("/todos/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    success = todos.delete(todo_id)
    if success:
        todos.save_all()
    return redirect(url_for("todos_list"))

if __name__ == "__main__":
    app.run(debug=True)





