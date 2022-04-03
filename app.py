import random
import os
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator
from sqlalchemy.sql import func
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Blueprint,
)
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import find_dotenv, load_dotenv
from spotify import spotify_api

app = Flask(__name__)

# set up a separate route to serve the index.html file generated
# by create-react-app/npm run build.
# By doing this, we make it so you can paste in all your old app routes
# from Milestone 2 without interfering with the functionality here.
bp = Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

load_dotenv(find_dotenv())
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# three lines of code necessary for flask login
login_manager = LoginManager()
login_manager.login_view = "hello_world"
login_manager.init_app(app)

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    """This is the User Model"""

    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    artist_names = db.Column(db.ARRAY(db.String(120)), nullable=True)
    artist_images = db.Column(db.ARRAY(db.String(120)), nullable=True)
    weekly_score = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Neccessary function for Flask Login"""
        return "<User %r" % self.user_name

    def get_username(self):
        """Neccessary function for Flask Login"""
        return self.user_name

    def get_id(self):
        """Neccessary function for Flask Login"""
        return self.user_id


@login_manager.user_loader
def load_user(user_id):
    """Neccessary function for Flask Login"""
    return User.query.get(int(user_id))


class League(db.Model):
    """This is the League model"""

    __tablename__ = "league"
    id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String(120), nullable=False)
    # users_and_scores = db.Column(UsersScoresType())
    # users of type string
    # scores of type int

    # users in array
    user_names = db.Column(db.ARRAY(db.String(120)), nullable=True)
    max_score = db.Column(db.Integer, nullable=True)
    winner = db.Column(db.String(120), nullable=True)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    end_date = db.Column(db.DateTime(timezone=True))

    # foreign key of users so you can pull their artists and picks
    # maybe query users based on users in users scores and then do another query for


# create a
# when creating league also create league users
# create league
# query league just created by name
#
#
#

# def
#  creates league with data given
# it queries that league based on its name to retreive id of league
# then it does a loop through users and creates league users with league id as league id
# queries users table for users artist picks and pick images and sets those for each league user
#


class LeagueUsers(db.Model):
    """This is the League Users Model"""

    __tablename__ = "league_users"
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(120), nullable=False)
    artist_names = db.Column(db.ARRAY(db.String(120)), nullable=True)
    artist_images = db.Column(db.ARRAY(db.String(120)), nullable=True)
    total_score = db.Column(db.Integer, nullable=False)

    # foreign key is league id
    # total score (dependent on specified league)
    # username
    # user artists
    # user artist pics


# scores for each user per league
# id for league (foreign key)
# primary key id
# foreign key user id
# from that you pull the arrays of pics and artist names
# and score
# and user name


class TopArtists(db.Model):
    """This is the Top Artists model"""

    __tablename__ = "top_artists"
    id = db.Column(db.Integer, primary_key=True)
    ranking = db.Column(db.Integer, nullable=False)
    artist_name = db.Column(db.String(120), nullable=True)
    artist_image = db.Column(db.String(120), nullable=True)


# creates all db models
db.create_all()

# base route of web app that starts user at the login page
@app.route("/", methods=["POST", "GET"])
def hello_world():
    """Returns root endpoint HTML"""
    # names_lists, img_lists = spotify_api()
    # TopArtists.query.delete()
    # db.session.commit()
    # for i in range(len(names_lists)):
    #     artist_entry = TopArtists(
    #         ranking=len(names_lists) - i,
    #         artist_name=names_lists[i],
    #         artist_image=img_lists[i],
    #     )
    #     db.session.add(artist_entry)
    #     db.session.commit()

    return render_template(
        "login.html",
    )


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Adds user to database if not already in it and returns main page"""
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        email = request.form.get("email")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email address already exists. Try logging in")
        return redirect(url_for("login"))

    new_user = User(
        user_name=user_name,
        email=email,
        password=generate_password_hash(password, method="sha256"),
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/login")


@app.route("/login")
def login():
    """Return main page after successful login"""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    """Method with logic for logging user in"""

    if request.form.get("signup") == "signup":
        return render_template("signup.html")

    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    if email == "":
        flash("Please check your login details and try again.")
        return redirect(url_for("login"))

    user = User.query.filter_by(email=email).first()
    # if statement checks if username is in db and password for that user matches
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("login"))

    login_user(user, remember=remember)
    if user.artist_names is None:
        return redirect("/selection")
    else:
        return redirect("/profile")


@app.route("/profile")
@login_required
def profile():
    user = User.query.filter_by(user_name=current_user.user_name).first()

    return render_template(
        "profile.html",
        artist_names=user.artist_names,
        artist_images=user.artist_images,
        username=current_user.user_name,
        weekly_sc=user.weekly_score,
    )


# route for serving React page
@bp.route("/selection", methods=["POST", "GET"])
@login_required
def index():

    return render_template("index.html")


@app.route("/logout")
@login_required
def logout():
    """Function to log user  out and redirect to login page"""
    logout_user()
    return redirect(url_for("login"))


@bp.route("/get_artists", methods=["GET"])
def get_artists():
    """Function to pass all artists to react page in a json"""
    artists_info = TopArtists.query.all()
    info_len = len(artists_info)
    artist_list = []
    print(info_len)

    for i in range(info_len):
        artist_list.append(
            {
                "id": artists_info[i].id,
                "artist_name": artists_info[i].artist_name,
                "artist_img": artists_info[i].artist_image,
                "artist_rank": artists_info[i].ranking,
            }
        )
    random.shuffle(artist_list)
    return jsonify(artist_list)


@bp.route("/save_artists", methods=["POST"])
def deleted_comments():
    """Function takes in list of deleted comments IDs and deletes them from DB"""
    if request.method == "POST":
        artists_list = request.form.get("artists_list")

        # creates list of ints out of string of IDs seperated by commas passed back from react page
        a_list = [int(s) for s in artists_list.split(",")]
        user = User.query.filter_by(user_name=current_user.user_name).first()
        list_of_imgs = []
        list_of_names = []
        weekly_score = 0

        for i in range(len(a_list)):
            artist_info = TopArtists.query.filter_by(id=a_list[i]).first()
            list_of_names.append(artist_info.artist_name)
            list_of_imgs.append(artist_info.artist_image)
            weekly_score = weekly_score + artist_info.ranking
        user.weekly_score = weekly_score
        db.session.commit()
        user.artist_names = list_of_names
        db.session.commit()
        user.artist_images = list_of_imgs
        db.session.commit()

        user = User.query.filter_by(user_name=current_user.user_name).first()

    return render_template(
        "profile.html",
        artist_names=user.artist_names,
        artist_images=user.artist_images,
        username=current_user.user_name,
        weekly_sc=user.weekly_score,
    )


@app.route("/selections")
def selections():
    names_lists, img_lists = spotify_api()
    artist_and_img = {}
    names_list = []
    img_list = []
    for i in range(50):
        artist_and_img[names_lists[i]] = img_lists[i]
    keys = list(artist_and_img.keys())
    random.shuffle(keys)
    for key in keys:
        names_list.append(key)
        img_list.append(artist_and_img[key])

    name_len = len(names_list)
    return render_template(
        "selection_screen.html",
        name_list=names_list,
        img=img_list,
        name_len=name_len,
    )


def weekly_database_update():
    # print('This job is run every monday at 11pm.')
    names_lists, img_lists = spotify_api()
    TopArtists.query.delete()
    db.session.commit()
    for i in range(len(names_lists)):
        artist_entry = TopArtists(
            ranking=len(names_lists) - i,
            artist_name=names_lists[i],
            artist_image=img_lists[i],
        )
        db.session.add(artist_entry)
        db.session.commit()
    user = User.query.all()
    for x in range(len(user)):
        new_weekly_score = 0
        if user[x].artist_names is not None:
            user_art_names = user[x].artist_names
            for y in range(len(user_art_names)):
                if (
                    TopArtists.query.filter_by(artist_name=user_art_names[y])
                    is not None
                ):
                    artist = TopArtists.query.filter_by(artist_name=user_art_names[y])
                    new_weekly_score = new_weekly_score + artist.ranking
        user[x].weekly_score = new_weekly_score


sched = BackgroundScheduler()
sched.add_job(weekly_database_update, "cron", day_of_week="mon", hour=23)
sched.start()


app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
