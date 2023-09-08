from flask import Flask

app = Flask(__name__)

app.secret_key = "dish_draw_by_tt"

app.config['IMAGE_UPLOADS'] = '/Users/IK-Q/ObeDrive/Desktop/DISHDRAW/DISHDRAW/flask_app/static'