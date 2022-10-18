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

    # What happens if units are null?
    if (grades is None):
        # Set it to an empty list and show error message
        grades = []
        flash('Error, there are no grades')
    page['title'] = 'Transcript'
    return render_template('transcript.html', page=page, session=session, grades=grades)


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



################################################################################
# List Lectures page
################################################################################

# List all lectures
@app.route('/list-lectures')
def list_lectures():
    # Go into the database file and get the list_units() function
    lectures = database.list_lectures()

    # What happens if units are null?
    if (lectures is None):
        # Set it to an empty list and show error message
        lectures = []
        flash('Error, there are no lectures in database')
    page['title'] = 'Lectures'
    return render_template('lectures.html', page=page, session=session, lectures=lectures)



################################################################################
# Search lectures by time page
################################################################################

@app.route('/search-lectures-by-time', methods=['POST', 'GET'])
def search_lectures_by_time():
    
    if(request.method == 'POST'):
 
        valid_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        
        time_string = request.form["classtime"]
#         day = time_string[:3]
#         hour = time_string[3:]
#         if len(time_string) != 5 or day not in valid_days or not hour.isdigit() or (hour.isdigit() and (int(hour) < 0 or int(hour) > 23)):
#             flash('Error, please enter a valid class day and time')
#         ^^^^^ removed because sanitising inputs not necessary ^^^^^^


        
        lectures = database.search_lecs_by_time(time_string)
    
        # What happens if lectures are null?
        if (lectures is None):
            # Set it to an empty list and show error message
            lectures = []
            flash('Error, there are no lectures matching that time')

        page['title'] = 'Lecture Search Result'
        return render_template('lecturesearchresult.html', page=page, session=session, lectures=lectures)
                                                                                    
    else:
        page['title'] = 'Search Lectures By Time'
        return render_template('lecturesbytime.html', page=page, session=session)


    
################################################################################
# Lecture Report page
################################################################################

# List all lectures
@app.route('/lecture-report')
def lecture_report():
    lectures = database.get_lecture_report()

    # What happens if units are null?
    if (lectures is None):
        # Set it to an empty list and show error message
        lectures = []
        flash('Error, there are no lectures in database')
    page['title'] = 'Lecture Report'
    return render_template('lecturereport.html', page=page, session=session, lectures=lectures)


################################################################################
# Add Lecture page
################################################################################

@app.route('/add-lecture', methods=['POST', 'GET'])
def add_lecture():
    
    if(request.method == 'POST'):
        
        uoscode = request.form["uoscode"]
        semester = request.form["semester"]
        year = request.form["year"]
        classtime = request.form["classtime"]
        classroomid = request.form["classroomid"]
        
        attributes = [uoscode, semester, year, classtime, classroomid]
        
        try:
            database.add_lecture_to_db(uoscode, semester, year, classtime, classroomid)
            page['title'] = 'Lecture Successfully Added'
            return render_template('addlecturesuccess.html', page=page, session=session, attributes=attributes)

        except:
            flash('Error, constraints violated or invalid attribute parameters')
            page['title'] = 'Add Lecture Unsuccessful'
            return render_template('addlecturefailure.html', page=page, session=session, attributes=attributes)
                                                                                          
    else:
        page['title'] = 'Add Lecture'
        return render_template('addlecture.html', page=page, session=session)