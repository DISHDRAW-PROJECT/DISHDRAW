from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_app.models.food_type import Food_Type
from flask_app.models.note import Note
from werkzeug.utils import secure_filename
import os

# ---------------------------------------------------
# SHOW EACH RECIPE

@app.route('/foodtype/<int:food_type_id>')
def each_recipe(food_type_id):
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {"id": session['user_id']}
    food_type_data = {"id": food_type_id}
    print(food_type_data)
    return render_template('foodtype_display.html', user = User.get_by_id(data), food_type = Food_Type.get_one_food_type(food_type_data), recipes = Recipe.get_recipes_by_id_and_foodtypes(food_type_data))

# ---------------------------------------------------

# SHOW RECIPES BY FOOD TYPE - FOOD TYPE DISPLAY PAGE

@app.route('/food_type/recipes/<int:recipe_id>/<int:food_type_id>')
def food_type_display(recipe_id,food_type_id):
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {"id": session['user_id']}
    food_type_data = {"id": food_type_id}
    return render_template('show.html', user= User.get_by_id(data), reports = Recipe.get_recipe_by_id(food_type_data))

#----------------------------------------------------

# SHOW ONE RECIPE - SHOW.HTML

@app.route('/foodtype/show/<int:recipe_id>/<int:food_type_id>')
def show_recipe(recipe_id,food_type_id):
    if 'user_id' not in session:
        return redirect ('/logout')
    data = {"id":recipe_id}
    user_data = {"id":session['user_id']}
    food_type_data = {"id": food_type_id}
    return render_template('/show.html', recipe = Recipe.get_recipes_by_id_and_foodtypes(data), user = User.get_by_id(user_data), notes = Note.notes_with_recipe_id(data), food_type = Food_Type.get_one_food_type(food_type_data))

# ---------------------------------------------------

# CREATE RECIPE

@app.route('/create')
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('create.html', user = user, food_type = Food_Type.all_food_types())


@app.route('/create/process', methods=['POST'])
def process_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.valid_report(request.form):
        return redirect('/create')
    image = request.files['image']
    if image.filename == "":
        flash("Please select a file")
        return redirect('/create')
    image.save(os.path.join(app.config['IMAGE_UPLOADS'], image.filename))
    data = {
        'name': request.form['name'],
        'ingredients': request.form['ingredients'],
        'directions': request.form['directions'],
        'servings': request.form['servings'],
        'prep_time': request.form['prep_time'],
        'cooking_time': request.form['cooking_time'],
        'user_id': session['user_id'],
        'image': image.filename
    }
    Recipe.save_recipe(data)
    return redirect('/foodtype')

# ---------------------------------------------------

# EDIT AND UPDATE RECIPE - USERS CAN EDIT AND UPDATE THEIR RECIPES

@app.route('/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_by_id({"id":session['user_id']})
    Data = {"id": id}
    return render_template('edit.html', user = user, recipe = Recipe.get_recipes_by_id_and_foodtypes(Data), food_type = Food_Type.all_food_types())

@app.route('/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'id': id,
        'name': request.form['name'],
        'ingredients': request.form['ingredients'],
        'directions': request.form['directions'],
        'servings': request.form['servings'],
        'prep_time': request.form['prep_time'],
        'cooking_time': request.form['cooking_time'],
        'user_id': session['user_id'],
        'image': request.form['image']
    }
    Recipe.update_recipe(data)
    return redirect('/city')

# ---------------------------------------------------

# DELETE - USERS CAN DELETE THEIR RECIPES

@app.route('/delete/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id":id}
    Recipe.delete_recipe(data)
    return redirect('/food_type')