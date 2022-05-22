from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yuhcee@127.0.0.1:5432/example'

db = SQLAlchemy(app)

class Todo():
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
        app.debug = True
        app.run(host='0.0.0.0', port=5000)