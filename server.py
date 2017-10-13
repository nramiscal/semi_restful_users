from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'users')
app.secret_key = 'ThisIsSecret'

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def index():
    users = mysql.query_db("SELECT * FROM users")
    return render_template('index.html', users=users)

@app.route('/users/new')
def new():

    return render_template('new.html')

@app.route('/users/<id>/edit')
def edit(id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM users WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': id}
    # Run query with inserted data.
    users = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('edit.html', user=users[0])




@app.route('/users/<id>')
def show(id):
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM users WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': id}
    # Run query with inserted data.
    users = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('show.html', user=users[0])


@app.route('/users/create', methods=['POST'])
def create():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
            }
    mysql.query_db(query, data)
    return redirect('/users')


@app.route('/users/<id>/destroy')
def destroy(id):
    query = "DELETE FROM users WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)

    return redirect('/users')


@app.route('/users/<id>', methods=['POST'])
def update(id):
    print request.form
    query = "UPDATE users SET first_name = :first_name, last_name = :last_name, email = :email WHERE id = :id"

    data = {
                'first_name':request.form['first_name'],
                'last_name':request.form['last_name'],
                'email':request.form['email'],
                'id':id
            }
    print data
    mysql.query_db(query, data)
    return redirect('/users')

app.run(debug=True)
