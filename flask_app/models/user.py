from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    DB = 'users_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def show_users(cls):
        users = []
        query = '''
                SELECT *
                FROM users;
        '''
        results = connectToMySQL(cls.DB).query_db(query)
        for user in results:
            users.append(cls(user))
        
        return users

    @classmethod
    def show_one_user(cls, user_id):
        query = '''
                SELECT *
                FROM users
                WHERE id = %(id)s;
        '''
        result = connectToMySQL(cls.DB).query_db(query, user_id)
        return cls(result[0])

    @classmethod
    def add_user(cls, data):
        query = '''
                INSERT INTO users(first_name, last_name, email) 
                VALUES (%(fname)s, %(lname)s, %(email)s);
        '''
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def delete_user(cls, user_id):
        query = '''
                DELETE
                FROM users 
                WHERE id=( %(id)s );
        '''
        return connectToMySQL(cls.DB).query_db(query, user_id)
    
    @classmethod
    def edit_one_user(cls, data):
        query = '''
                UPDATE users
                SET first_name =%(fname)s,  last_name =%(lname)s, email =%(email)s
                WHERE id=%(id)s;
        '''
        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['fname']) == 0 or len(user['lname']) == 0 or len(user['email']) == 0:
            flash('All fields are required!')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash('Invalid email address!')
            is_valid = False
        all_users = User.show_users()
        for row in all_users:
            if row.email.lower() == user['email'].lower():
                flash('Email is already registered')
                is_valid = False
        return is_valid
    