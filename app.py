"""Flask app for devotion app"""
from flask import Flask, request, redirect, render_template, flash, jsonify, session, current_app
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterUserForm, LogInUserForm
import requests
from secret import YOUTUBE_API_KEY
# from isodate import parse_duration
# Run in terminal --- pip install isodate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///PickrrUp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True 

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    """Redirects to /register"""

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

@app.route("/login", methods=["GET", "POST"])
def logIn_user():
    """Show a form that when submitted will log in an existing user."""
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


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("username")
    flash("You are now logged out!")
    return redirect("/")






@app.route('/youtube', methods=['GET', 'POST'])
def youtube_search():
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    if request.method == 'POST':
        search_params = {
            'key' : 'YOUTUBE_API_KEY',
            'q' : request.form.get('query'),
            'part' : 'snippet',
            'maxResults' : 9,
            'type' : 'video'
        }
        print(r)
        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.form.get('submit') == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={ video_ids[0] }')

        video_params = {
            'key' : 'YOUTUBE_API_KEY',
            'id' : ','.join(video_ids),
            'part' : 'snippet,contentDetails',
            'maxResults' : 9
        }

        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'duration' : int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'title' : result['snippet']['title'],
            }
            videos.append(video_data)
        
    return render_template('youtube.html', videos=videos)