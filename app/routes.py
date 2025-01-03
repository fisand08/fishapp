from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User, WATER, WATER_COORDS, WATER_OWNERS, WATER_SEASON
import sqlalchemy as sa
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, jsonify
from urllib.parse import urlsplit
from datetime import datetime, timezone

#########################################################
#######                DECORATORS               #########
#########################################################

"""
Logic executed before every request; executed before any view function
"""
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc) # adding to db - no .add() needed here
        db.session.commit() # committing to db

#########################################################
#######                PAGE RENDERS             #########
#########################################################


@app.route('/', methods=['GET', 'POST'])  # decorator for following function
@app.route('/index', methods=['GET', 'POST'])  # 2nd decorator
#@login_required  # although it's index, we can set that here - not logged in person will be sent to login function
def index():
    return render_template('index.html')

    #return render_template('index.html',title='Starting page',user=mock_user)

@app.route('/fishing_infos')
def fishing_infos():
    return render_template('fishing_infos.html')

@app.route('/map')
def map():

    # dummy code
    query_test = WATER.query.filter(WATER.WATER_ID == 1).first()
    print(f'query_test: {query_test.WATER_NAME} {query_test.SCHONGEBIET}')
    # end of dummy code

    return render_template('map.html')


@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/catches')
def catches():
    return render_template('catches.html')

@app.route('/furniture')
def furniture():
    return render_template('furniture.html')


##########################################################
#######                LOGIC                     #########
##########################################################

@app.route('/get_coords', methods=['GET', 'POST'])
def get_coords():
    """
    description:
        - queries coordinates from database into proper format
    input: 
        - nothing
    output:
        - coord_data: list of dict; data in proper format
    """

    # Use a single query with a join to fetch all required data
    results = (
        db.session.query(
            WATER.WATER_ID,
            WATER.WATER_NAME,
            WATER.WATER_TYPE,
            WATER.WATER_OWNER_ID,
            WATER.SCHONGEBIET,
            WATER_COORDS.COORD_X,
            WATER_COORDS.COORD_Y,
            WATER_OWNERS.OWNER_PUBLIC_INT
        )
        .join(WATER_COORDS, WATER.WATER_ID == WATER_COORDS.WATER_ID)
        .join(WATER_OWNERS, WATER.WATER_OWNER_ID == WATER_OWNERS.OWNER_ID)

        .all()
    )
    
    # Organize data into the desired format
    coord_data = {}
    for water_id, water_name, water_type, water_owner_id, schongebiet, coord_x, coord_y, owner_public in results:
        if water_id not in coord_data:
            coord_data[water_id] = {
                'name': water_name,
                'description': water_type,
                'public': owner_public,
                'schongebiet':schongebiet,
                'coordinates': []
            }
            #print(water_name, water_type, owner_public, schongebiet )
        coord_data[water_id]['coordinates'].append({'lat': coord_x, 'lng': coord_y})

    # Convert the data structure to a list of dictionaries
    coord_data_list = list(coord_data.values())

    return jsonify(coord_data_list)


@app.route('/get_water', methods=['GET', 'POST'])
def get_water():
    """
    description:
        - queries water details
    """

    results_owner = db.session.query(WATER_OWNERS.OWNER_PUBLIC).all()
    print(results_owner)

    results = (
        db.session.query(
            WATER.WATER_ID,
            WATER.WATER_NAME,
            WATER.WATER_TYPE,
            WATER.SCHONGEBIET,
            WATER.WATER_SEASON_ID,
            WATER.FREIANGELEI,
            WATER_OWNERS.OWNER_ID,
            WATER_OWNERS.OWNER_PUBLIC_INT,
            WATER_SEASON.SAISON_FROM,
            WATER_SEASON.SAISON_TO
        )
        .join(WATER_OWNERS, WATER.WATER_OWNER_ID == WATER_OWNERS.OWNER_ID)
        .join(WATER_SEASON, WATER.WATER_SEASON_ID == WATER_SEASON.SAISON_ID)
        .all()
    )
    print(results)

    return jsonify({'results':'result'})


##########################################################
#######                LOGIN                     #########
##########################################################


@app.route('/login', methods=['GET','POST'])  # view function accepts "methods" (POST: browser to webserver)
def login():
    if current_user.is_authenticated:
        """
        User is sent back to index if already logged-in
        """
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data)) # query user from DB
        if user is None or not user.check_password(form.password.data): # password check
            flash('Invalid username or password') # flash field response if wrong password
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) # username and pw are correct -> login
        """
        Adding some logic to bring user to page that he wanted to access before he got
        forced to login; request variable contains information of initial request
        """
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        
        return redirect(next_page)
    return render_template('login.html',title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')  # <> brackets allow dynamic URL like youtube.com/FarioStalking
@login_required # only accessible to logged-in users
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    alt_names = ['profil_' + x for x in ['guati','schatzi','schatzus','schatzo']]
    portfolios = ['NVS.SW,APPLE,DOWJON','ROG.SW,NVS.SW']
    return render_template('user.html', user=user, alt_names=alt_names, portfolios=portfolios)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)