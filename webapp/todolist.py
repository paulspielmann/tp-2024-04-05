"""webapp.todolist: a Web APP exposing a todolist"""

from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
)
from libtodolist.tasks import Task, TaskList, PriorityLevel
from typing import List
from os import getenv

app = Flask(__name__)

JSON_FILE = getenv("JSON_FILE", "web-tasks.json")


def get_task_manager():
    return TaskList.from_json(JSON_FILE)


@app.route("/")
def homepage():
    return render_template(
        "homepage.html",
        page_title="Homepage",
    )


@app.route("/tasks")
def tasks():
    return render_template(
        "tasklist.html", tasks=get_task_manager().tasks, page_title="List of all tasks"
    )

@app.route("/all_tasks")
def all_tasks():
    raise NotImplementedError()

@app.route("/create_task", methods=["POST", "GET"])
def create_task():
    if request.method == "GET":
        return render_template(
            "create-task.html", priority_list=[e.value for e in PriorityLevel]
        )
    else:
        assert all(a in request.form for a in ("name", "priority"))
        assert request.form["priority"] in [e.value for e in PriorityLevel]
        name = request.form["name"]
        priority = request.form["priority"]
        task_manager = get_task_manager()
        task_manager.tasks.append(Task(name=name, priority=priority))
        task_manager.to_json(JSON_FILE)
        return redirect(url_for("tasks"))

@app.route("/toggle_task_status", methods=["POST"])
def toggle_task_status():
    if request.method != "POST":
        raise ValueError("POST-only route")
    raise NotImplementedError()