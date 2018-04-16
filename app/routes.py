from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app
from app.forms import LoginForm
from app.models import User, Post
from werkzeug.urls import url_parse


@app.route("/")
@app.route("/index")
@login_required
def index():
	return render_template("index.html", title = "Home Page", posts = posts)

	'''
	@login_required decorator will intercept the request and respond with a redirect to /login, 
	but it will add a query string argument to this URL, making the complete redirect URL /login?next=/index.
	the request.args attribute exposes the contents of the query string in a friendly dictionary format
	'''
@app.route("/login", methods=["GET", "POST"])	
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("Invalid username or password")
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template("login.html", title = "Sign in", form= form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))
