from flask_app import app
from flask_app.controllers import users
from flask_app.controllers import food_types
from flask_app.controllers import recipes
from flask_app.controllers import notes

if __name__=="__main__":
    app.run(debug=True)
