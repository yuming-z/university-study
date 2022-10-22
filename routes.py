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


################################################################################
# Transcript Page
################################################################################

@app.route('/transcript')
def transcript():
    # TODO
    # Now it's your turn to add to this ;)
    # Good luck!
    #   Look at the function below
    #   Look at database.py
    #   Look at units.html and transcript.html
    grades = database.get_transcript(session['sid'])
    
    if (grades is None):
        grades = []
        flash('Error, there are no grades')
    page['title'] = 'Transcript'
    return render_template('transcript.html', page=page, session=session, grades = grades)


################################################################################
# Prerequisites Page
################################################################################

@app.route('/prerequisites')
def prerequisites():
    prereq = database.get_prerequisites()
    
    if (prereq == ()):
        flash('Error, there are no prerequisites')
    page['title'] = 'Prerequisites'
    return render_template('prerequisites.html', page=page, session=session, prereq = prereq)

@app.route('/prerequisites-by-unit', methods=['POST', 'GET'])
def prerequisites_by_unit():
    
    if (request.method == 'POST'):
        unit_string = request.form["unit"]
        
        prereq_bu = database.get_prerequisites_for_unit(unit_string)
    
        if (prereq_bu == ()):
            flash('Error, there are no prerequisites')
            return render_template('prereqbyunitsearch.html', page=page, session=session)
        else:
            page['title'] = 'Prerequisites by unit'
            return render_template('prereqbyunitresults.html', page=page, session=session, prereq_bu = prereq_bu)
    else:
            page['title'] = 'Prerequisites by unit'
            return render_template('prereqbyunitsearch.html', page=page, session=session)
        
@app.route('/add-prerequisite', methods=['POST', 'GET'])
def add_prerequisite():
    
    if(request.method == 'POST'):
        
        uoscode = request.form["uoscode"]
        prerequoscode = request.form["prerequoscode"]
        enforcedsince = request.form["enforcedsince"]
        
        attributes = [uoscode, prerequoscode, enforcedsince]
        
        condition = database.add_prereq_to_db(uoscode, prerequoscode, enforcedsince)

        if(condition == 0):
            page['title'] = 'Prerequisite Successfully Added'
            return render_template('addprereqsuccess.html', page=page, session=session, attributes=attributes)

        else:
            flash('Error, constraints violated or invalid attribute parameters')
            page['title'] = 'Add Prerequisite Unsuccessful'
            return render_template('addprereqfailure.html', page=page, session=session, attributes=attributes)
                                                                                          
    else:
        page['title'] = 'Add Prerequisite'
        return render_template('addprereq.html', page=page, session=session)
    

@app.route('/count-prerequisites')
def count_prerequisites():
    count_prereq = database.count_prerequisites()
    
    if (count_prereq == ()):
        flash('Error, there are no units')
    page['title'] = 'Count Prerequisites'
    return render_template('countprereq.html', page=page, session=session, count_prereq = count_prereq)



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