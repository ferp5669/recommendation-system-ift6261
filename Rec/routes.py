import requests
from flask import redirect, request, url_for, render_template, flash, abort
from flask_login import login_user, logout_user, current_user, login_required
from flask_paginate import Pagination, get_page_args
from Rec import app, db, bcrypt
from Rec.forms import LoginForm, RegisterForm
from Rec.models import User

api_key = 'api_key=7c2b193215341693c006975935406e1c'
genre_colors = {
    'Action': 'is-danger',
    'Adventure': 'is-primary',
    'Animation': 'is-link',
    'Comedy': 'is-warning',
    'Crime': 'is-black',
    'Documentary': 'is-info',
    'Drama': 'is-success',
    'Family': 'is-info',
    'Fantasy': 'is-purple',
    'History': 'is-link',
    'Horror': 'is-danger',
    'Music': 'is-link',
    'Mystery': 'is-info',
    'Romance': 'is-danger',
    'Science Fiction': 'is-primary',
    'Thriller': 'is-warning',
    'TV Movie': 'is-info',
    'War': 'is-black',
    'Western': 'is-link'
}


@app.route('/')
def index():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    per_page = 15
    movies = []
    for i in range(2, 80):
        response = requests.get(f'https://api.themoviedb.org/3/movie/{i}?{api_key}')
        if response.status_code == 200:
            movie_data = response.json()
            if not movie_data['poster_path'] is None:
                movies.append(movie_data)
                #providers_response = requests.get(f'https://api.themoviedb.org/3/movie/{i}/watch/providers?{api_key}')
                #if providers_response.status_code == 200:
                    #providers_results = providers_response.json().get('results')
                    #flatrate_providers = providers_results.get('CA', {}).get('flatrate', [])
                #else:
                    #flatrate_providers = []

    pagination = Pagination(page=page, total=len(movies), per_page=per_page, css_framework='bulma')
    paginated_movies = movies[offset: offset + per_page - (per_page % 5)]
    # Render template with movie data
    return render_template('layouts/default.html',
                           title="HomePage",
                           content=render_template('pages/index.html', movies_list=paginated_movies, page=page,
                                                   per_page=per_page, pagination=pagination))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Send to homepage if already logged in and trying to access this page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(request.form)
    page_title = 'Login - Recommender System'
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return "nice"
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('layouts/default.html',
                           title="Login",
                           content=render_template('pages/login.html', form=form))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Default salt value of 12 is used since I'm not specifying it
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully! Welcome {form.username.data}! You can now login', 'success')
        return redirect(url_for('login'))
    return render_template('layouts/default.html',
                           title="register",
                           content=render_template('pages/register.html', form=form))


@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?{api_key}')
    if response.status_code == 200:
        movie_data = response.json()
        related_response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/similar?{api_key}')
        if related_response.status_code == 200:
            related_movies = related_response.json()['results'][:3]
        else:
            related_movies = []

        if not movie_data['poster_path'] is None:
            return render_template('layouts/default.html',
                                   title=movie_data['title'],
                                   content=render_template('pages/movie_detail.html', movie=movie_data,
                                                           genre_colors=genre_colors, related_movies=related_movies))
    else:
        return "Error fetching movie details"

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))