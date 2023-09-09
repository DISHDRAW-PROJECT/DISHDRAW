from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.food_type import Food_Type
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ---------------------------------------------------

# INDEX PAGE - USERS CAN LOGIN AND RESGISTER

@app.route("/")
def index():
    return render_template("index.html")

# ---------------------------------------------------

# DASHBOARD PAGE

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect ('/')
    data = {"id": session['user_id']}
    return render_template("dashboard.html", user = User.get_by_id(data), food_type = Food_Type.all_food_types(), recipe = Recipe.get_all())

# ---------------------------------------------------

# USER REGISTER

@app.route("/register", methods=["POST"])
def register():
    if not User.is_valid_user(request.form):
        return redirect('/')
    data={
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save_recipe(data)
    session['user_id'] = id
    return redirect("/dashboard")

# ---------------------------------------------------
# USER LOGIN

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({"email":request.form['email']})
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# ---------------------------------------------------
# USER LOGOUT

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")