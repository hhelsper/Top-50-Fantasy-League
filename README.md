# Fantasy 50

## Overview

Welcome to Fantasy 50, a web app that allows you to create fantasy leagues based on brackets of music artists chosen from Spotify's Top 50 weekly charts. We allow you to create an account, choose your bracket, see your weekly scores on your profile, view the Top 10 users leaderboard, and create leagues with other users to compete through your brackets for a selected span of time. Though the web app in its current state does not support betting, we ultimately aim to encorporate gambling functionality so that users can add cash to pots that will be awarded to the winners of the league. In an attempt to generate a future revenue stream for our app, we will take a nominal amount from each leagues pot as a processing charge for our website. 

## Requirements to Run App

### Installation Requirements

Thanks for downloading our repo! I'm excited to help you deploy the site locally on your machine. 
Before we get started, let's make sure you have all the necessary components installed to run this code.
Run these commands in your terminal to get started:
1. `pip3 install python-dotenv`
2. `pip3 install requests`
3. `pip3 install flask`
4. `pip3 install flask_sqlalchemy`
5. `pip3 install flask_login`
6. `pip3 install psycopg2`
7. `pip3 install werkzeug`
8. `pip3 install APScheduler`
9. `heroku addons:create heroku-postgres:hobby-dev`

### Signing up with Spotify API

The next thing you'll need to do is get a spotify developer account. After getting an account, choose to create an app. This will create for you a `client id` and a `client secret` key. You will need to create a `.env` file now to include these two secret values. Set your `client id` equal to a variable called `client_id` and set your client secret key equal to a variable called `client_secret`. 

### Getting url for your Heroku Database

After you run the command `heroku addons:create heroku-postgres:hobby-dev` after creating a heroku app for your clone of this repository, you will need to grab the datbase url for this heroku postgres database. Once you get the url an important thing to note is that you will need to change `postgres://` in the url to `postgresql://`. Once you have done that and changed your url, you will need to add it to your `.env` file by typing this: `export DB_URL='postgresql://<your url here>'`. You're all set! You should now be able to type in `python3 app.py` in your terminal and follow the local link displayed to load our web app. 


## Link to our Webpage 

If you are interested [CLICK HERE](https://powerful-dusk-53061.herokuapp.com/) to view our site!

## Video Walkthrough

Here's a walk through of my website:

<img src='Top50.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />