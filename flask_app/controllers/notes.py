from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_app.models.food_type import Food_Type
from flask_app.models.note import Note

# ---------------------------------------------------

# CREATE NOTES

@app.route('/create/note/<int:recipe_id>/<int:user_id>/<int:food_type_id>')
def create_note(recipe_id,user_id,food_type_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id":recipe_id}
    user = {"id":session['user_id']}
    food_type_data = {"id": food_type_id}
    return render_template('update.html', user = User.get_by_id(user), recipe = Recipe.get_recipes_by_id_and_foodtypes(data), food_type = Food_Type.get_one_food_type(food_type_data))

@app.route('/create/note/<int:recipe_id>/<int:user_id>/<int:food_type_id>', methods=['POST'])
def process_note(recipe_id,user_id,food_type_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Note.is_valid_note(request.form):
        flash("Please enter a valid note", "note")
        return redirect(f'/create/note/{recipe_id}/{user_id}/{food_type_id}')
    data = {
        "notes": request.form['notes'],
        "user_id": session['user_id'],
        "recipe_id": request.form['recipe_id'],
        "food_type_id": request.form['food_type_id']
    }
    Note.save_note(data)
    return redirect(f'/food_type/show/{recipe_id}/{food_type_id}')

# ---------------------------------------------------

# DELETE - USERS CAN DELETE THEIR NOTES

@app.route('/delete/note/<int:id>/<int:idd>/<int:iddd>')
def delete_note(id,idd,iddd):
    if 'user_id' not in session:
        return redirect('/logout')
    Note.delete_note({'id':id})
    recipe_id = idd
    food_type_id = iddd
    return redirect(f'/food_type/show/{recipe_id}/{food_type_id}')

# ---------------------------------------------------

# EDIT AND UPDATE NOTES

@app.route('/edit/note/<int:id>/<int:idd>/<int:iddd>')
def edit_note(id,idd,iddd):
    if 'user_id' not in session:
        return redirect('/logout')
    data = ({'id':id})
    recipe_data = {"id":idd}
    user_data = {"id": session['user_id']}
    food_type_data = {"id": iddd}
    return render_template('edit_update_note.html', note = Note.get_one_by_id(data), user = User.get_by_id(user_data), food_types = Food_Type.all_food_types(), recipe = Recipe.get_recipes_by_id_and_foodtypes(recipe_data), food_type = Food_Type.get_one_food_type(food_type_data))


@app.route('/update/note/<int:id>/<int:food_type_id>/<int:user_id>/<int:recipe_id>',methods=['POST'] )
def update_note(id,food_type_id, user_id, recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Note.is_valid_note(request.form):
        flash("Please enter a valid note", "note")
        return redirect(f'/create/note/{recipe_id}/{user_id}/{food_type_id}')
    data = {"id": id,"notes": request.form['notes']}
    Note.note(data)
    user_data= {"id":session['user_id']}
    recipe_id = recipe_id
    return redirect(f'/food_type/show/{recipe_id}/{food_type_id}')
