from crypt import methods
from distutils.log import error
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
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False, default=1)
    
    def __repr__(self):
     return f'<Todo ID: {self.id}, description: {self.description} completed: {self.completed}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)

@app.route('/todos/create', methods=['POST'])
def create_todo():
    body={}
    error = False
    try:
        description=request.get_json()['description']
        list_id = request.get_json()['list_id']
        todo = Todo(description=description, completed=False, list_id=list_id)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
        body['description'] = todo.description
        body['completed'] = todo.completed
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(500)
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
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(500)
        else:
            return redirect(url_for('index'))

@app.route('/todos/<todo_id>/delete', methods=['DELETE'])
def delete_todo(todo_id):
    error=False
    try:
        # Todo.query.filter_by(id=todo_id).delete()
        todo=Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback
        error=True
    finally:
        db.session.close()
        if(error):
            abort(500)
        else:
           return jsonify({'success': True})


@app.route('/')
def index():
  return redirect(url_for('get_list_todos', list_id=1))

@app.route('/lists/<list_id>')
def get_list_todos(list_id):

  lists=TodoList.query.all(),
  active_list=TodoList.query.get(list_id),
  todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
    
  return render_template('index.html', todos=todos, lists=lists, active_list=active_list)

if __name__ == '__main__':
        app.debug = True
        app.run(host='0.0.0.0', port=4000)