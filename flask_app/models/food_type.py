from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe, user, food_type , note
from flask import flash

# ---------------------------------------------------

# "Food Type" CLASS

class Food_Type:
    def __init__( self , data ):
        self.id = data['id']
        self.name_of_food = data['name_of_food']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.note_poster = []

# ---------------------------------------------------

# SAVE FOOD TYPE

    @classmethod
    def save_food_type(cls, data):
        query = "INSERT INTO food_types (name_of_food) VALUES(%(name_of_food)s);"
        return connectToMySQL('dish_draw').query_db(query, data)
    

# ---------------------------------------------------

# GET ALL FOOD TYPES

    @classmethod
    def all_food_types(cls):
        query = "SELECT * FROM food_types;"
        results = connectToMySQL('dish_draw').query_db(query)
        food_types = []
        for food_type in results:
            food_types.append(cls(food_type))
        return food_types

# ---------------------------------------------------

# GET FOOD TYPES BY ID

    @classmethod
    def get_one_food_type(cls, data):
        query = "SELECT * FROM food_types WHERE id = %(id)s;"
        results = connectToMySQL('dish_draw').query_db(query, data)
        print(results)
        return cls(results[0])