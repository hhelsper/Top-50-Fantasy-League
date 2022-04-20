"""Main file of web app"""
# pylint: disable=maybe-no-member
# pylint: disable=consider-using-f-string
# pylint: disable=invalid-name
# pylint: disable=no-else-return
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-locals

import datetime
import random
import os
import pytz


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
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

bp = Blueprint(
    "bp",
    __name__,
    template_folder="./static/react",
)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

load_dotenv(find_dotenv())
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# three lines of code necessary for flask login
login_manager = LoginManager()
login_manager.login_view = "hello_world"
login_manager.init_app(app)

db = SQLAlchemy(app)
utc = pytz.UTC


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
    user_names = db.Column(ARRAY(db.String(120)), nullable=True)
    max_score = db.Column(db.Integer, nullable=True)
    winner = db.Column(db.String(120), nullable=True)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    end_date = db.Column(db.DateTime(timezone=True))


class LeagueUsers(db.Model):
    """This is the League Users Model"""

    __tablename__ = "league_users"
    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(120), nullable=False)
    artist_names = db.Column(db.ARRAY(db.String(120)), nullable=True)
    artist_images = db.Column(db.ARRAY(db.String(120)), nullable=True)
    total_score = db.Column(db.Integer, nullable=False)


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

    return render_template(
        "login.html",
    )


def len_bool_helper(user_name_len, email_len, password_len):
    """Tests if any field of signup left empty"""
    return bool(user_name_len == 0 or email_len == 0 or password_len == 0)


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Adds user to database if not already in it and returns main page"""
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")

    if len_bool_helper(len(user_name), len(email), len(password)):
        flash("Please enter a username, email, and password")
        return render_template("signup.html")

    if password != confirm_password:
        flash("Please make sure passwords match")
        return render_template("signup.html")

    user = User.query.filter_by(email=email).first()
    user_n = User.query.filter_by(user_name=user_name).first()

    if user_n:
        flash("Username already exists. Try choosing another one")
        return render_template("signup.html")

    if user:
        flash("Email address already exists. Try logging in.")
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


def login_helper(email):
    """Login Helper Email Checker Method"""
    return bool(email == "")


@app.route("/login", methods=["POST"])
def login_post():
    """Method with logic for logging user in"""

    if request.form.get("signup") == "signup":
        return render_template("signup.html")

    email = request.form.get("email")
    password = request.form.get("password")
    remember = bool(request.form.get("remember"))
    if login_helper(email):
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
    """Function to render user profile"""
    user = User.query.filter_by(user_name=current_user.user_name).first()
    leagues_len = 0
    league_list = []
    if (
        League.query.filter(League.user_names.contains([user.user_name])).all()
        is not None
    ):
        leagues = League.query.filter(
            League.user_names.contains([user.user_name])
        ).all()
        leagues_len = len(leagues)

        for i in range(leagues_len):
            league_list.append({"name": leagues[i].league_name})

    return render_template(
        "profile.html",
        artist_names=user.artist_names,
        artist_images=user.artist_images,
        username=current_user.user_name,
        weekly_sc=user.weekly_score,
        leagues=league_list,
        leagues_len=leagues_len,
    )


# route for serving React page
@bp.route("/selection", methods=["GET"])
@bp.route("/create_a_league", methods=["GET"])
@login_required
def index():
    """Renders selection react page"""
    return render_template("index.html")


@app.route("/leader_board")
@login_required
def leader_board():
    """Renders the leaderboard screen"""
    users = User.query.filter().order_by(User.weekly_score.desc())
    users_len = len(User.query.all())
    cur_user = User.query.filter_by(user_name=current_user.user_name).first()
    cur_user_rank = 0
    for i in range(users_len):
        if users[i].user_name == cur_user.user_name:
            cur_user_rank = i
            break

    return render_template(
        "leader_board.html",
        users=users,
        users_len=users_len,
        cur_user=cur_user,
        rank=cur_user_rank,
    )


@app.route("/artists")
@login_required
def artists():
    """Renders the top artists page"""
    top_artists = TopArtists.query.filter().order_by(TopArtists.ranking.desc())
    artist_len = len(TopArtists.query.all())

    return render_template("artists.html", artists=top_artists, artist_len=artist_len)


@app.route("/my_leagues", methods=["POST", "GET"])
@login_required
def my_leagues():
    """Renders the my leagues page"""

    all_leagues = League.query.all()
    ongoing_leagues = []
    ended_leagues = []
    winner = LeagueUsers()

    for league_names in all_leagues:
        user = User.query.filter_by(user_name=current_user.user_name).first()
        if user.user_name in league_names.user_names:

            if (
                datetime.datetime.now(league_names.end_date.tzinfo)
                < league_names.end_date
            ):
                league_users = LeagueUsers.query.filter_by(
                    league_id=league_names.id
                ).all()
                max_score = 0
                for user in league_users:

                    if user.total_score > max_score:
                        winner = user
                        max_score = user.total_score

                ongoing_leagues.append(
                    {
                        "league_name": league_names.league_name,
                        "league_id": league_names.id,
                        "members": league_names.user_names,
                        "members_len": len(league_names.user_names),
                        "top_scorer": winner.user_name,
                        "top_score": winner.total_score,
                        "duration": league_names.end_date.strftime("%m/%d/%Y"),
                    }
                )

            else:
                league_users = LeagueUsers.query.filter_by(
                    league_id=league_names.id
                ).all()
                for user in league_users:

                    max_score = 0
                    if user.total_score > max_score:
                        winner = user
                        max_score = user.total_score

                ended_leagues.append(
                    {
                        "league_name": league_names.league_name,
                        "league_id": league_names.id,
                        "members": league_names.user_names,
                        "members_len": len(league_names.user_names),
                        "top_scorer": winner.user_name,
                        "top_score": winner.total_score,
                        "duration": league_names.end_date.strftime("%m/%d/%Y"),
                    }
                )
    if request.method == "POST":
        league_id = request.form.get("btn-league-name")
        ind_league = League.query.filter_by(id=league_id).first()
        end_date = ind_league.end_date
        end_date = end_date.strftime("%m/%d/%Y")
        users_list = ind_league.user_names
        users = LeagueUsers.query.filter_by(league_id=league_id).order_by(
            LeagueUsers.total_score.desc()
        )

        users_len = len(users_list)
        curr_league = ind_league.league_name

        return render_template(
            "my_leagues_page.html",
            users=users,
            users_len=users_len,
            curr_league=curr_league,
            end_date=end_date,
        )

    return render_template(
        "my_leagues.html",
        ongoing_leagues=ongoing_leagues,
        ended_leagues=ended_leagues,
        ongoing_length_league=len(ongoing_leagues),
        ended_length_league=len(ended_leagues),
    )


@app.route("/logout")
@login_required
def logout():
    """Function to log user  out and redirect to login page"""
    logout_user()
    return render_template("login.html", modal="Thanks for playing! See you next time.")


@app.route("/paypal")
@login_required
def paypal():
    """Path to paypal portal that may be used"""
    return render_template("paypal.html")


def get_artists_helper(artist_info):
    """Helper function to create and return list of artist info"""
    info_len = len(artist_info)
    artist_list = []
    for i in range(info_len):
        artist_list.append(
            {
                "id": artist_info[i].id,
                "artist_name": artist_info[i].artist_name,
                "artist_img": artist_info[i].artist_image,
                "artist_rank": artist_info[i].ranking,
            }
        )
    return artist_list


@bp.route("/get_users", methods=["GET"])
def get_users():
    """Search users based on search"""
    search = request.args.get("search")

    all_users = User.query.all()

    len_users = len(all_users)
    list_of_results = []
    for i in range(len_users):
        if (
            search in all_users[i].user_name
            and all_users[i].user_name != current_user.user_name
        ):
            list_of_results.append(
                {
                    "id": all_users[i].user_id,
                    "user_name": all_users[i].user_name,
                }
            )
    print(list_of_results)

    return jsonify(list_of_results)


@app.route("/about_us")
@login_required
def about_us():
    """Renders about us page"""
    return render_template("about_us.html")


@app.route("/create_league", methods=["POST", "GET"])
def create_league():
    """Function to create a league"""
    if request.method == "POST":
        user_ids = request.form.get("users")
        id_list = [int(s) for s in user_ids.split(",")]
        id_list_len = len(id_list)
        duration = request.form.get("end_date")
        duration_int = int(duration)
        league_name = request.form.get("name")

        user_names_array = []
        user = User.query.filter_by(user_name=current_user.user_name).first()
        user_names_array.append(user.user_name)
        scores = []
        for i in range(id_list_len):
            user = User.query.filter_by(user_id=id_list[i]).first()
            user_names_array.append(user.user_name)
            scores.append(user.weekly_score)

        new_league = League(
            league_name=league_name,
            end_date=datetime.datetime.now() + datetime.timedelta(weeks=duration_int),
            user_names=user_names_array,
            max_score=max(scores),
        )
        db.session.add(new_league)
        db.session.commit()

        league = League.query.filter_by(league_name=league_name).first()

        for n in range(id_list_len):
            user_to_add = User.query.filter_by(user_id=id_list[n]).first()
            new_league_user = LeagueUsers(
                league_id=league.id,
                user_name=user_to_add.user_name,
                artist_names=user_to_add.artist_names,
                artist_images=user_to_add.artist_images,
                total_score=user_to_add.weekly_score,
            )
            db.session.add(new_league_user)
            db.session.commit()
        cur_user = User.query.filter_by(user_name=current_user.user_name).first()
        cur_user_league_user = LeagueUsers(
            league_id=league.id,
            user_name=cur_user.user_name,
            artist_names=cur_user.artist_names,
            artist_images=cur_user.artist_images,
            total_score=cur_user.weekly_score,
        )
        db.session.add(cur_user_league_user)
        db.session.commit()

    return redirect("/my_leagues")


@bp.route("/get_artists", methods=["GET"])
def get_artists():
    """Function to pass all artists to react page in a json"""
    artists_info = TopArtists.query.all()
    artist_list = get_artists_helper(artists_info)

    random.shuffle(artist_list)
    return jsonify(artist_list)


@bp.route("/save_artists", methods=["POST"])
def deleted_comments():
    """Function takes in list of deleted comments IDs and deletes them from DB"""
    if request.method == "POST":
        artists_list = request.form.get("artists_list")

        # creates list of ints out of string of IDs seperated by commas passed back from react page
        a_list = [int(s) for s in artists_list.split(",")]
        a_list_len = len(a_list)
        user = User.query.filter_by(user_name=current_user.user_name).first()
        list_of_imgs = []
        list_of_names = []
        weekly_score = 0

        for i in range(a_list_len):
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

    leagues_len = 0
    league_list = []
    if (
        League.query.filter(League.user_names.contains([user.user_name])).all()
        is not None
    ):
        leagues = League.query.filter(
            League.user_names.contains([user.user_name])
        ).all()
        leagues_len = len(leagues)

        for i in range(leagues_len):
            league_list.append({"name": leagues[i].league_name})

    return render_template(
        "profile.html",
        artist_names=user.artist_names,
        artist_images=user.artist_images,
        username=current_user.user_name,
        weekly_sc=user.weekly_score,
        leagues_len=leagues_len,
        leagues=league_list,
    )


def weekly_database_update():
    """This is the weekly database update"""

    names_lists, img_lists = spotify_api()
    names_lists_len = len(names_lists)

    TopArtists.query.delete()
    db.session.commit()
    for i in range(names_lists_len):
        if TopArtists.query.filter_by(artist_name=names_lists[i]).first() is None:
            artist_entry = TopArtists(
                ranking=len(names_lists) - i,
                artist_name=names_lists[i],
                artist_image=img_lists[i],
            )
            db.session.add(artist_entry)
            db.session.commit()

    user = User.query.all()
    user_len = len(user)
    for x in range(user_len):
        new_weekly_score = 0
        if user[x].artist_names is not None:
            user_art_names = user[x].artist_names
            user_art_names_len = len(user_art_names)
            for y in range(user_art_names_len):
                if (
                    TopArtists.query.filter_by(artist_name=user_art_names[y]).first()
                    is not None
                ):
                    artist = TopArtists.query.filter_by(
                        artist_name=user_art_names[y]
                    ).first()
                    new_weekly_score = new_weekly_score + artist.ranking

        user[x].weekly_score = new_weekly_score
        db.session.commit()

    league_users = LeagueUsers.query.all()
    for league_user in league_users:
        leag = League.query.filter_by(id=league_user.league_id).first()

        if leag.end_date.replace(tzinfo=utc) > datetime.datetime.now().replace(
            tzinfo=utc
        ):

            new_total_score = league_user.total_score
            for art in league_user.artist_names:
                if TopArtists.query.filter_by(artist_name=art).first() is not None:
                    new_art = TopArtists.query.filter_by(artist_name=art).first()
                    new_total_score = new_total_score + new_art.ranking
            league_user.total_score = new_total_score

            db.session.commit()


sched = BackgroundScheduler()
sched.add_job(weekly_database_update, "cron", day_of_week="mon", hour=23, minute="59")
sched.start()


app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
