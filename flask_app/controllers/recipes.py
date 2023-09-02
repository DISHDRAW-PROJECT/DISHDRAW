from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

# ---------------------------------------------------
# SHOW PAGE - SHOW ALL RECIPES

@app.route('/show')
def home():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/logout')
        
    return render_template('show.html', user=user, recipes=Recipe.get_all())

# ---------------------------------------------------
# SHOW EACH RECIPE BY ID - USERS CAN VIEW EACH RECIPE

@app.route('/show/<int:id>')
def show_each_recipe(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    data = {
        'id' : id
    }
    return render_template('view.html', recipe=Recipe.get_recipe_by_id(data))

# ---------------------------------------------------
# CREATE RECIPE - USERS CAN CREATE A RECIPE

@app.route('/create')
def create_recipe():
    if 'user_id' not in session:
        return redirect('/dashboard')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('create.html', user=user)


@app.route('/create/process', methods=['POST'])
def process_recipe():
    if 'user_id' not in session:
        return redirect('/dashboard')
    if not Recipe.validate_recipe(request.form):
        return redirect('/create')
    data = {
        'user_id': session['user_id'],
        'name': request.form['name'],
        'ingredients': request.form['ingredients'],
        'notes': request.form['notes'],
        'servings': request.form['servings'],
        'prep_time': request.form['prep_time'],
        'cooking_time': request.form['cooking_time'],
        'created_at': request.form['created_at'],
        'updated_at': request.form['updated_at']
    }
    Recipe.save_recipe(data)
    return redirect('/show')

# ---------------------------------------------------
# EDIT AND UPDATE RECIPE - USERS CAN EDIT AND UPDATE THEIR RECIPES

@app.route('/edit/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    user = User.get_by_id({"id":session['user_id']})
    return render_template('edit.html', user=user, recipe=Recipe.get_recipe_by_id({'id': id}))

@app.route('/update/<int:id>', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{id}')
    data = {
        'id': id,
        'user_id': session['user_id'],
        'name': request.form['name'],
        'ingredients': request.form['ingredients'],
        'notes': request.form['notes'],
        'servings': request.form['servings'],
        'prep_time': request.form['prep_time'],
        'cooking_time': request.form['cooking_time'],
        'created_at': request.form['created_at'],
        'updated_at': request.form['updated_at']
    }
    Recipe.update_recipe(data)
    return redirect('/show')

# ---------------------------------------------------
# DELETE - USERS CAN DELETE THEIR RECIPES

@app.route('/delete/fact/<int:id>')
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    Recipe.delete_recipe({'id':id})
    return redirect('/show')