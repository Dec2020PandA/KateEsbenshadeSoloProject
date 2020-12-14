from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(postData['first_name'])<1:
            errors['first_name'] = "First Name must be at least 1 character"
        if len(postData['last_name'])<1:
            errors['last_name'] = "Last Name must be at least 1 character"
        if not email_check.match(postData['email']):           
            errors['email'] = "Invalid email address"
        if len(postData['password'])<1:
                errors['password'] = "Password must be at least 1 character"
        if postData["password"] != postData["confirm_password"]:
            errors["confirm_password"] = "Password and confirm password must match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    description = models.TextField()
    location = models.TextField()
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ActionManager(models.Manager):
    def action_validator(self, postData):
        errors = {}

        if len(postData['title']) < 1:
            errors['title'] = "Title must not be blank."
        if len(postData['description']) < 5:
            errors['description'] = "Description must at least 5 characters long."

        return errors

class Action(models.Model):
    #def __init__(self, name):
        #self.name = name
        #self.count = self.count + 1
    title = models.TextField()
    topic = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="actions", on_delete = models.CASCADE)
    favorited_by = models.ManyToManyField(User, related_name="actions_to_do")
    objects = ActionManager()