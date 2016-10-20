from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def register(self, data):
        error = []
            #index 1 of the innerlist, retrieve in views side
        if len(data["first_name"]) < 3 or any(char.isdigit() for char in data["first_name"]):
            error.append('first name must be at least 2 characters and contain no numbers')
        if len(data["last_name"]) < 3 or any(char.isdigit() for char in data["last_name"]):
            error.append('last name must be at least 2 characters and contain no numbers')
        if not EMAIL_REGEX.match(data['email']):
            error.append('incorrect email')
        if len(data["password"]) < 8:
            error.append('incorrect password length')

        user = self.filter(email = data['email']) #check if false

        if user:
            error.append('email taken')
        if data['password'] != data['password_confirm']:
            error.append('please match your passwords')
        if error:
            return (False, error)

        hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user = self.create(first_name = data["first_name"],last_name = data["last_name"],email = data["email"], password = hashed)
        return (True, user)

    def login(self, data):
        error = []
        user = self.filter(email=data['email'])
        if user:
            if bcrypt.hashpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')) == user[0].password:
                return (True, user[0])
        error.append("Invalid credentials, please try again")
        return (False, error)
# Create your models here.
class User(models.Model):
    #find error and append to list, if errors returns false
    #create user
    #if errors, return (False, errors) otherwise return (True, user)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(null=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
