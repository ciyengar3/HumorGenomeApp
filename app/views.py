from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
from .forms import LoginForm
from .user import User
from populateDB import addUser
from jokeHandler import populateList, addRating, getRandomJoke
import jokes

current_joke = jokes.Joke(None, None, None)
current_user = User(None)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    global current_user
    if request.method == 'POST' and form.validate_on_submit():
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            current_user = user_obj
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("write"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/registered', methods=['GET', 'POST'])
def registered():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    internal = request.form['internal']
    addUser(username, password, first_name, last_name, internal)
    return redirect(url_for('write'))


@app.route('/logout')
def logout():
    logout_user()
    global current_user
    current_user = User(None)
    return redirect(url_for('login'))


@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    return render_template('write.html')


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    return render_template('settings.html')


@app.route('/generator', methods=['GET', 'POST'])
@login_required
def generator():
    populateList()
    return redirect(url_for('generated'))


@app.route('/generated', methods=['GET', 'POST'])
@login_required
def generated():
    global current_joke
    joke1 = getRandomJoke()
    current_joke = joke1
    joke1.content = unicode(joke1.content)
    return render_template('jokeForm.html', joke=joke1)


@app.route('/save_form', methods=['GET', 'POST'])
@login_required
def save_form():
    qual = unicode(request.form["funny"])
    quan = unicode(request.form["rating"])
    addRating(current_joke.jokeId, quan)
    return redirect(url_for('generated'))



@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
