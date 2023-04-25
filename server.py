from flask import Flask, render_template, redirect, request, session
from classes.users import User

app = Flask(__name__)
app.secret_key = '123456'

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
    User.add_user(data)
    return redirect('/users')

@app.route('/delete', methods=['POST'])
def delete_user():
    user_id = request.form['u_id']
    User.delete_user(user_id)
    return redirect('/users')


if __name__ == '__main__':
    app.run(debug=True)
