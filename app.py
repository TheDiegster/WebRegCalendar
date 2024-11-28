from flask import Flask
from views import views
from flask_session import Session
app = Flask(__name__)
app.register_blueprint(views, url_prefix="/views")
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)
if __name__ == '__main__':
    app.run(port='8000', debug=True)