from flask import render_template, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.food_type import Food_Type


# ---------------------------------------------------

# SHOW ALL FOOD TYPES

@app.route('/foodtypes')
def food_types():
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {"id": session['user_id']}
    return render_template('foodtypes.html', user = User.get_by_id(data), food_type = Food_Type.all_food_types())