import psycopg2

# open a connection to database
connection = psycopg2.connect("dbname=example")

# open cursor to perform database operations
cursor = connection.cursor()

# drop any existing todos table
cursor.execute('DROP TABLE IF EXISTS todos');

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cursor.execute('''
CREATE TABLE todos (
    id INTEGER PRIMARY KEY,
    description VARCHAR NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT False
);
''')

cursor.execute('''INSERT INTO todos (id, description, completed) VALUES (1, 'Learn Python', true);''')
cursor.execute('''INSERT INTO todos (id, description, completed) VALUES (2, 'Go to bed', false);''')

# string interpolation first example
cursor.execute('INSERT INTO todos (id, description, completed) VALUES (%s, %s, %s)', (3, 'Eat Break fast', False));

# string interpolation second example
SQLQUERY = 'INSERT INTO todos (id, description, completed) VALUES (%(id)s, %(description)s, %(completed)s);'
data = {
    'id': 4,
    'description': 'Publish article',
    'completed': True
}

cursor.execute(SQLQUERY, data)
cursor.execute('SELECT * FROM todos');

# commit, so it does the executions on the db and persists in the db
connection.commit()
cursor.close()
connection.close()