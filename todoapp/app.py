from crypt import methods
from email.policy import default
import sys
from flask import Flask, abort, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yuhcee@127.0.0.1:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(),nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
     return f'<Todo ID: {self.id}, description: {self.description}>'

@app.route('/todos/create', methods=['POST'])
def create_todo():
    body={}
    error = False
    try:
        description=request.get_json()['description']
        todo=Todo(description=description)
        body['description'] = todo.description
        db.session.add(todo)
        db.session.commit()
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            return jsonify(body)

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed(todo_id):
    error = False
    try:
        completed=request.get_json()['completed']
        todo=Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            return redirect(url_for('index'))


@app.route('/')
def index():
    # todo = Todo.query.first()
    # return f"Your todo number {todo.id} is to {todo.description}."
    return render_template('index.html', todos=Todo.query.order_by('id').all())

if __name__ == '__main__':
        app.debug = True
        app.run(host='0.0.0.0', port=4000)