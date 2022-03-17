from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from forms.taskCreateForm import TaskCreateForm
from forms.taskUpdateForm import TaskUpdateForm
from utils.db import db
from models.user import User
from models.task import Task

todolist = Blueprint("todolist", __name__, url_prefix="/todolist")


@todolist.route("/")
@login_required
def home():
    userList = None
    if "admin" in current_user.rank:
        # es un admin
        userList = User.query.all()
    else:
        # es un user
        userList = list((User.query.filter_by(id=current_user.id).first(),))
    return render_template("todolist/home.html", user=current_user, userList=userList)


# http://127.0.0.1:5000/todolist/tasklist/2
@todolist.route("/tasklist/<int:userId>")
@login_required
def tasklist(userId):
    currentTaskList = Task.query.filter_by(userId=userId).all()
    return render_template("todolist/tasklist.html", user=current_user, userId=userId, tasks=currentTaskList)


# http://127.0.0.1:5000/todolist/tasklist/create/2
@todolist.route("/tasklist/create/<int:userId>", methods=["GET", "POST"])
@login_required
def create(userId):
    form = TaskCreateForm()
    if form.validate_on_submit():
        description = form.description.data
        newTask = Task(userId, description)
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for("todolist.tasklist", userId=userId))
    return render_template("todolist/create.html", form=form, user=current_user, userId=userId)


@todolist.route("/tasklist/update/<int:userId>/<int:taskId>", methods=["GET", "POST"])
@login_required
def update(userId, taskId):
    currentTask = Task.query.filter_by(id=taskId).first()
    form = TaskUpdateForm(status=currentTask.status)
    if form.validate_on_submit():
        description = form.description.data
        status = form.status.data
        currentTask.description = description
        currentTask.status = status
        db.session.add(currentTask)
        db.session.commit()
        return redirect(url_for("todolist.tasklist", userId=userId))
    return render_template("todolist/update.html", form=form, userId=userId, task=currentTask)


@todolist.route("/tasklist/delete/<int:userId>/<int:taskId>")
@login_required
def delete(userId, taskId):
    # que pasos tengo hacer para eliminar el task id
    if current_user.id == userId or "admin" in current_user.rank:
        currentTask = Task.query.filter_by(id=taskId).first()
        db.session.delete(currentTask)
        db.session.commit()
    return redirect(url_for("todolist.tasklist", userId=userId))
