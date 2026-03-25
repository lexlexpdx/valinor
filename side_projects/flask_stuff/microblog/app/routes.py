from flask import render_template
from app import app
from app.forms import LoginForm

# Decorators: modifies the function that follows it
# association between URL given. When web browser requests either '/' or '/index'
# Flask invokes this function and passes its return value back to the browser as 
# a response
@app.route('/')
@app.route('/index')

# View function: handler for the application routes
def index():
    user = {'username': 'Lex'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beatiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title = "Home", user = user, posts = posts)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Sign In', form = form)