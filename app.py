"""Flask app for devotion app"""
from flask import Flask, request, redirect, render_template, flash, jsonify, session, current_app
from user import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LogInUserForm
import requests
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'pickrpsecrectkey')
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL','postgresql:///PickrrUp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True 
app.config['TESTING'] = True 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)

@app.route("/")
def home_page():
    """Renders the home/landing page"""

    return render_template("homepage.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.commit()
        session['username'] = user.username
        flash("You have Sucessfully Created Your Account")
        return redirect(f"/users/{user.username}")
    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def logIn_user():
    """Show a form that when submitted will log in an existing user"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LogInUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate user
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome back {user.username}!")
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid name/password"]
            return render_template("login.html", form=form)
            
    return render_template("login.html", form=form)



@app.route("/users/<username>")
def user_detail_page(username):
    """Shows user detail page"""
    if "username" not in session:
        flash("Please login first!")
        return redirect("/login")
    else:
        user = User.query.get(username)
    return render_template("dashboard.html", user=user)





@app.route("/daily-devotion")
def get_daily_devotion():
    """Make API requests to return daily devotion"""
    resp = requests.get("https://devotionalium.com/api/v2?lang=en")
    
    data = resp.json()
    text = data['1']['text']

    ref = data['1']['referenceLong']
    # readUrl = data['1']['readingUrl']
    photoUrl = data['photo']['url']
    # date = data['date']

    return render_template("devotion.html", text=text, ref=ref, photoUrl=photoUrl )



@app.route("/meditate")
def meditation_page():
    """directs to /meditate"""

    return render_template("meditate.html")


@app.route("/breathe")
def breathe_page():
    """directs to /meditate"""

    return render_template("breathe.html")




@app.route("/youtube")
def youtube_page():
        
    return render_template('youtube.html')


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("username")
    flash("You are now logged out!")
    return redirect("/")