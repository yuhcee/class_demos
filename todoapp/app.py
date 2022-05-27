from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yuhcee@127.0.0.1:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(),nullable=False)
    # completed = db.Column(db.Boolean, nullable=False)
    
    def __repr__(self):
     return f'<Todo ID: {self.id}, description: {self.name}>'

db.create_all()

@app.route('/')
def index():
    todo = Todo.query.first()
    return "Your todo number" + todo.id + " is "  + todo.description

if __name__ == '__main__':
        app.debug = True
        app.run(host='0.0.0.0', port=5000)