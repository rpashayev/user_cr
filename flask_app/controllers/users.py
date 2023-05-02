from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User


@app.route('/')
def index():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.show_users()
    return render_template('read.html', all_users=users)

@app.route('/users/new')
def add_form():
    return render_template('create.html')

@app.route('/add', methods=['POST'])
def add_new_user():
    data = {
        'fname': request.form['fname'], 
        'lname': request.form['lname'],
        'email': request.form['email'],
    }
    if not User.validate_user(request.form):
        first_name = request.form['fname']
        lname =request.form['lname']
        email =request.form['email']
        return render_template('create.html', fname=first_name, lname=lname, email=email)
    User.add_user(data)
    return redirect('/users')

@app.route('/delete', methods=['POST'])
def delete_user():
    user_id = {
        'id': request.form['u_id']
    }
    print(user_id)
    User.delete_user(user_id)
    return redirect('/users')

@app.route('/users/delete/<int:user_id>')
def delete_selected_user(user_id):
    id = {
        'id': user_id
    }
    print(id)
    User.delete_user(id)
    return redirect('/users')

@app.route('/users/show/<int:user_id>')
def show_user(user_id):
    id = {
        'id': user_id
    }
    one_user=User.show_one_user(id)
    return render_template('show.html', user=one_user)

@app.route('/users/edit/<int:user_id>')
def edit_page(user_id):
    id = {
        'id': user_id
    }
    one_user=User.show_one_user(id)
    return render_template('edit.html', user=one_user)

@app.route('/users/edit', methods=['POST'])
def edit_user():
    User.edit_one_user(request.form)
    return redirect('/users')