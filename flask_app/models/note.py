from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user, recipe


# ---------------------------------------------------

# "Note" CLASS

class Note:
    def __init__(self, data):
        self.id = data['id']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.recipe_id = data['recipe_id']

# ---------------------------------------------------

# VALIDATION

    @staticmethod
    def is_valid_note(data):
        is_valid = True
        if len(data['notes']) < 3:
            flash("Notes must be at least 3 characters.","notes")
            is_valid = False
        return is_valid
    
# ---------------------------------------------------

# SAVE NOTES WITH USER ID AND RECIPE ID

    @classmethod
    def save_note(cls, data):
        query = "INSERT INTO notes (notes, user_id, recipe_id, food_type_id) VALUES (%(notes)s, %(user_id)s, %(recipe_id)s, %(food_type_id)s);"
        return connectToMySQL('dish_draw').query_db(query, data)
    
# ---------------------------------------------------

# GET ALL NOTES

    @classmethod
    def all_notes(cls):
        query = "SELECT * FROM notes;"
        results = connectToMySQL('dish_draw').query_db(query)
        notes = []
        for note in results:
            notes.append(cls(note))
        return notes
    
# ---------------------------------------------------

# GET ONE NOTES

    @classmethod
    def get_one_by_id(cls, data):
        query = "SELECT * FROM notes WHERE id = %(id)s;"
        result = connectToMySQL('dish_draw').query_db(query, data)
        if result:
            note = cls(result[0])
            return note
        else:
            return False
        
# ---------------------------------------------------

# UPDATE NOTES

    @classmethod
    def update_note(cls, data):
        query = "UPDATE notes SET notes = %(notes)s, updated_at = NOW() WHERE id = %(id)s;"
        result = connectToMySQL('dish_draw').query_db(query, data)
        return result

# ---------------------------------------------------

# DELETE NOTES

    @classmethod
    def delete_note(cls, data):
        query = "DELETE FROM notes WHERE id = %(id)s;"
        result = connectToMySQL('dish_draw').query_db(query, data)
        return result

# ---------------------------------------------------

# GET NOTES WITH RECIPE ID
    
    @classmethod
    def notes_with_recipe_id(cls,data):
        query = "SELECT * FROM notes LEFT JOIN users ON notes.user_id = users.id WHERE notes.recipe_id = %(id)s;"
        results = connectToMySQL('dish_draw').query_db(query,data)
        notes = []
        for note in results:
            note_obj = cls(note)
            note_obj.users_first_name = note['first_name']
            notes.append(note_obj)
        return notes
    
# ------------------------