from flask import Blueprint, render_template, request, jsonify

views = Blueprint(__name__, "views")

@views.route("/home")
def home():
    return render_template("homepage.html")


@views.route("/profile")
def profile():
    args = request.args
    name = args.get('name')
    return render_template("index.html", name=name)

@views.route("/login")
def login():
    return render_template("login.html")

@views.route("/json")
def get_json():
    return jsonify({'name': 'Dara', 'coolness': 100})
