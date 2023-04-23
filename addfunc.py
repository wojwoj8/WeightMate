from flask import redirect, render_template, request, session
from functools import wraps
import secrets
import string

#Ensures that user is logged, otherwise redirect to login page
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/notlogged")
        return f(*args, **kwargs)
    return decorated_function

def startform_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") != None and session.get("age") is None:
            return redirect("/getstarted")
        return f(*args, **kwargs)
    return decorated_function

def premium_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") != None and session.get("premium") != 1:
            return redirect("/premium")
        return f(*args, **kwargs)
    return decorated_function

def password_gen():
    alphabet = string.ascii_letters + string.digits
    password_length = 12
    password = ''.join(secrets.choice(alphabet) for i in range(password_length))
    
    return(password)