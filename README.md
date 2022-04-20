# Fantasy 50

## Link to our Webpage 

If you are interested [CLICK HERE](https://powerful-dusk-53061.herokuapp.com/) to view our Sprint 1 site!

If you are interested [CLICK HERE](https://whispering-garden-45374.herokuapp.com/) to view our Sprint 2 site!


## Video Walkthrough

Here's a walk through of our Sprint 1 website:

<img src='Top50.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

Here's a walk through of our Sprint 2 website:

<img src='Top50-Sprint-2.gif' title='Video Walkthrough2' width='' alt='Video Walkthrough2' />

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


## Linting

We have made the choice to disable some linting errors and warnings, and with these disabled our pylint rating is a 10/10. 

### Disabled Warnings and Errors

1. `pylint: disable=maybe-no-member`
    This disable was an easy one to rationalize. This warning comes due to our use of sqlalchemy and all of the `db.session` lines. These lines are neccessary to interact with our database, but for some reason, pylint takes issue with them. That is why it only makes sense to disable this pylint error. 
2. `pylint: disable=consider-using-f-string`
    This pylint warning came in one of the boiler plate functions needed in our User model to successfully implement Flask login. So we disabled this warning because, as mentioned, this is just neccessary code needed and it came straight from the source of the flask login documentation. 
3. `pylint: disable=no-else-return`
    This was a strange pylint warning. It came about when we used an if else statement to check whether a user had a bracket of artists saved in the database. Upon logging in, if a user had not yet set their bracket of 5 artists, the are redirected to the selection screen to choose there artists, but if they already have a bracket of artists saved in the database, they are redirected to the profile page. We disabled this because this was a necessary if/else statement, even if pylint doesn't like it.
4. `pylint: disable=too-few-public-methods`
    This pylint warning comes up on our classes that we created for our database. I think that python wants these classes to have methods instead of just being the creation of a table in our database. This, however, is the nature of how we must create tables in our database which is why we disabled this pylint warning. 
5. `pylint: disable=pointless-string-statement`
    We disabled pointless-string-statement in our README.md because we needed to write comments as to why we commented out two of our unmocked tests. The reason we commented them out is because although they pass locally, these two tests fail on github due to our `.env` file not being accessible on github. I tried using Github secret variables and loading a env into our testing but this did not work so we decided to comment out these two tests. However, if you clone our code, and make your own `.env` file with the necessary variables you can uncomment out these two tests and see that they both pass.
6. `pylint: disable=invalid-name`
    We disabled this warning becuase we use nested for loops in our app.py file, where we loop through all users and then loop through each users selected artists. In the for loop we used `for x in range(user_len)` for example, and pylint complained that x was an invalid name. However, we chose to not changed our variables for the two for loop from `x` and `y` to something different because we already have variables with names that would make sense to use in place of x and y so we stuck with x and y and disabled this warning

