from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, food_type
from flask import flash
from werkzeug.utils import secure_filename
import os

# ---------------------------------------------------

# "Recipe" CLASS

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.image = data['image']
        self.ingredients = data['ingredients']
        self.directions = data['directions']
        self.servings = data['servings']
        self.prep_time = data['prep_time']
        self.cooking_time = data['cooking_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']        
        self.user_id = data['user_id']
        self.food_type = data['food_type_id']
        self.recipe_poster = None
        self.notes = []
        
# ---------------------------------------------------

# GET RECIPES BY FOOD TYPE AND ID

    @classmethod
    def get_recipes_by_id_and_foodtypes(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN food_types ON food_type_id = food_types.id LEFT JOIN users ON user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('dish_draw').query_db(query, data)
        recipes = []
        print(results)
        for recipe in results:
            this_recipe = cls(recipe)
            user_data = {
                "id": recipe['users.id'],
                "first_name": recipe['first_name'],
                "last_name": recipe['last_name'],
                "email": recipe['email'],
                "password": "",
                "created_at": recipe['users.created_at'],
                "updated_at": recipe['users.updated_at']
            }
            this_recipe.recipe_poster = user.User(user_data)
            recipes.append(recipe)

        for recipe in results:
            this_recipe = cls(recipe)
            food_type_data = {
                "id": recipe['food_type.id'],
                "name_of_food": recipe['name_of_food'],
                "created_at": recipe['food_type.created_at'],
                "updated_at": recipe['food_type.updated_at']
            }
            this_recipe.recipe_poster = food_type.Food_Type(food_type_data)
            recipes.append(recipe)
        
        return recipes[0]
            
# ---------------------------------------------------

# VALIDATIONS

    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['name']) < 5:
            flash("Name must be at least 5 characters long","recipes")
            is_valid = False
        if len(data['ingredients']) < 20:
            flash("Ingredients must be at least 20 characters long","recipes")
            is_valid = False
        if len(data['directions']) < 20:
            flash("Directions must be at least 20 characters long","recipes")
            is_valid = False
        if len(data['servings']) < 1:
            flash("Servings can not be blank","recipes")
            is_valid = False
        if len(data['prep_time']) < 1:
            flash("Prepping Time can not be blank","recipes")
            is_valid = False
        if len(data['cooking_time']) < 1:
            flash("Cooking Time can not be blank","recipes")
            is_valid = False
            
        return is_valid
    
# ---------------------------------------------------

# GET RECIPES BY RECIPE ID AND FOOD TYPE

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('dish_draw').query_db(query, data)
        recipes = []
        print(results)
        for recipe in results:
            this_recipe = cls(recipe)
            user_data = {
                "id": recipe['users.id'],
                "first_name": recipe['first_name'],
                "last_name": recipe['last_name'],
                "email": recipe['email'],
                "password": "",
                "created_at": recipe['users.created_at'],
                "updated_at": recipe['users.updated_at']
            }
            this_recipe.recipeer = user.User(user_data)
            recipes.append(recipe)
        print(recipes)
        return recipes
    
# ---------------------------------------------------

# GET ALL RECIPES JOINS WITH USERS AND FOOD TYPE

    @classmethod
    def recipes_with_users(cls):
        query = "SELECT * FROM recipes LEFT JOIN users on recipes.user_id = users.id LEFT JOIN food_types on recipes.food_type_id = food_types.id;"        
        results = connectToMySQL('dish_draw').query_db(query)
        recipes = []
        for row in results:
            this_recipe = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],    
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            food_type_data = {
                "id": row['food_types.id'],
                "name_of_food":row['name_of_food'],
                "created_at": row['food_types.created_at'],
                "updated_at": row['food_types.updated_at'],
                "recipes": None
            }
            this_recipe.user_id = user.User(user_data)
            this_recipe.food_type_id = food_type.Food_Type(food_type_data)
            recipes.append(this_recipe)
        return recipes

# ---------------------------------------------------

# GET RECIPE BY ID

    @classmethod
    def get_recipe_by_id(cls, id):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('dish_draw').query_db(query,id)
        return cls(results[0])

# ---------------------------------------------------

# SAVE A RECIPE

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name,image,ingredients,directions,notes,servings,prep_time,cooking_time,created_at,updated_at) VALUES (%(name)s,%(image)s,%(ingredients)s,%(directions)s,%(notes)s,%(servings)s,%(prep_time)s,%(cooking_time)s,%(created_at)s,%(updated_at)s;"
        return connectToMySQL('dish_draw').query_db(query,data)

# ---------------------------------------------------
# UPDATE A RECIPE

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, image = %(image)s, ingredients = %(ingredients)s, directions = %(directions)s, notes = %(notes)s, servings = %(servings)s, prep_time = %(prep_time)s, cooking_time = %(cooking_time)s, created_at = %(created_at)s, updated_at = %(updated_at)s, user_id = %(user_id)s, food_type_id = %(food_type_id)s WHERE id = %(id)s;"
        result = connectToMySQL('dish_draw').query_db(query,data)
        return result

# ---------------------------------------------------
# DELETE A RECIPE

    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL('dish_draw').query_db(query,data)
        return result

