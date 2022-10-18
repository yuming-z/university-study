# Importing the Flask Framework

from modules import *
from flask import *
import database
import configparser


page = {}
session = {}

# Initialise the FLASK application
app = Flask(__name__)
app.secret_key = 'SoMeSeCrEtKeYhErE'


# Debug = true if you want debug output on error ; change to false if you dont
app.debug = True


# Read my unikey to show me a personalised app
config = configparser.ConfigParser()
config.read('config.ini')
unikey = config['DATABASE']['user']
portchoice = config['FLASK']['port']

#####################################################
##  INDEX
#####################################################

# What happens when we go to our website
@app.route('/')
def index():
    # If the user is not logged in, then make them go to the login page
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['unikey'] = unikey
    page['title'] = 'Welcome'
    return render_template('welcome.html', session=session, page=page)

################################################################################
# Login Page
################################################################################

# This is for the login
# Look at the methods [post, get] that corresponds with form actions etc.
@app.route('/login', methods=['POST', 'GET'])
def login():
    page = {'title' : 'Login', 'unikey' : unikey}
    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our login value
        val = database.check_login(request.form['sid'], request.form['password'])

        # If our database connection gave back an error
        if(val == None):
            flash("""Error with the database connection. Please check your terminal
            and make sure you updated your INI files.""")
            return redirect(url_for('login'))

        # If it's null, or nothing came up, flash a message saying error
        # And make them go back to the login screen
        if(val is None or len(val) < 1):
            flash('There was an error logging you in')
            return redirect(url_for('login'))
        # If it was successful, then we can log them in :)
        session['name'] = val[1]
        session['sid'] = request.form['sid']
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        # Else, they're just looking at the page :)
        if('logged_in' in session and session['logged_in'] == True):
            return redirect(url_for('index'))
        return render_template('index.html', page=page)


################################################################################
# Logout Endpoint
################################################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('index'))

# List the classrooms
@app.route('/list-classroom')
def list_classroom():
    # Go into the database file and get the list_classroom() function
    classrooms = database.list_classroom()

    # Error checking
    if (classrooms is None):
        classrooms = []
        flash("Error! There is no classroom stored")
    
    page['title'] = "Classroom"
    return render_template('classrooms.html', page=page, session=session, classrooms=classrooms)


################################################################################
# List Units page
################################################################################

# List the units of study
@app.route('/list-units')
def list_units():
    # Go into the database file and get the list_units() function
    units = database.list_units()

    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Units of Study'
    return render_template('units.html', page=page, session=session, units=units)
