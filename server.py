"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db, db

import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """View homepage."""
    return render_template("Homepage.html")

@app.route('/users')
def users():
    users = crud.ret_all_users()
    
    return render_template('all_users.html', users = users)

@app.route('/users', methods=['POST'])
def new_user():
    
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Email already exists. Try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("User created.")
    
    return redirect('/')

@app.route('/login',methods=['POST'])
def login():
     
    email = request.form.get("email")
    password = request.form.get("password") 

    user = crud.get_user_by_email(email)
    # 
    if user:
        if password == user.password:
            session['user_email']= user.email
            flash(f"{user.email}, you're logged in.")
        else:
            flash('Incorrect password. Try again.')
    else:
        flash('Email not found. Try again')

    return redirect('/')



# if email in database
#   if password == user.passsword
        # session[user.email] = current email
        # flash(logged in)
        
    #if password != user.passsword
        # flash('Incorrect password')
# else if email not in database raiseValueError



@app.route('/users/<user_id>')
def user_details(user_id):
    
    user=crud.get_user_by_id(user_id)
    return render_template("user_details.html", user=user)

@app.route('/movies')
def movies():

    movies = crud.ret_all_movies()
    
    return render_template("all_movies.html", movies = movies)


@app.route('/movies/<movie_id>')
def movie_details(movie_id):

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie = movie)

@app.route('/movies/<movie_id>/rating', methods=['POST'])
def rating(movie_id):

    logged_in_email= session.get('user_email')
    rating = int(request.form.get('rating'))

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    else:
        movie = crud.get_movie_by_id(movie_id)
        user = crud.get_user_by_email(logged_in_email)
        
        user_rating = crud.create_rating(user, movie, rating)
        
        db.session.add(user_rating)
        db.session.commit()

        flash(f"You rated {movie.title} {rating} out of 5.")

    return redirect(f"/movies/{movie_id}")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
