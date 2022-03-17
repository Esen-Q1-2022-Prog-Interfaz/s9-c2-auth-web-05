from flask import Blueprint, render_template
from flask_login import current_user, login_required
from forms.taskCreateForm import TaskCreateForm
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


@todolist.route("/tasklist/<int:userId>")
@login_required
def tasklist(userId):
    currentTaskList = Task.query.filter_by(userId=userId).all()
    return render_template("todolist/tasklist.html", user=current_user, userId=userId, tasks=currentTaskList)


@todolist.route("/tasklist/create/<int:userId>", methods=["GET", "POST"])
@login_required
def create(userId):
    form = TaskCreateForm()
    if form.validate_on_submit():
        pass
    return render_template("todolist/create.html", form=form, user=current_user, userId=userId)
