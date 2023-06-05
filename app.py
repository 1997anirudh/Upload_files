from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import secrets
import traceback
import os
from werkzeug.utils import secure_filename
import logging


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

UPLOAD_FOLDER = os.path.abspath('uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Establish a connection to the SQLite database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            session['username'] = username
            cursor.close()
            conn.close()
            return redirect('/welcome')
        else:
            error = "Invalid username or password."
            cursor.close()
            conn.close()
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        # return render_template('welcome.html')
        return render_template('welcome.html', username=session['username'], files=files)




        # f"<h1>Welcome, {username}!</h1>"
    else:
        return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Handle sign-up form submission
        username = request.form['username']
        password = request.form['password']

        # Insert the user's information into the database
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
        cursor.execute(insert_query, (username, password))
        connection.commit()
        connection.close()

        # Render a template with a button to proceed to login
        return render_template('signup_success.html')

    return render_template('signup.html')

# Route for handling form submission
@app.route('/submit_details', methods=['POST'])
def submit_details():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']

    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        # Insert personal details into the "personal_details" table
        insert_personal_details_query = '''
        INSERT INTO personal_details (user_id, name, email, address)
        VALUES (?, ?, ?, ?)
        '''
        # Get the user_id based on the currently logged-in user
        user_id = session.get('user_id')
        cursor.execute(insert_personal_details_query, (user_id, name, email, address))

        # Commit the changes and close the connection
        connection.commit()

        # Redirect to a success page or do any other desired actions
        # return "Form submitted successfully!"
        return render_template('welcome.html')
        # return redirect('/welcome')
    except Exception as e:
        # Handle any errors that may occur during the insertion process
        connection.rollback()
        traceback.print_exc()
        print(str(e))
        return "An error occurred while submitting the form."

    finally:
        connection.close()


    return "Details submitted successfully"

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if the user is logged in
    if 'username' not in session:
        return redirect('/login')

    # Check if the post request has the file part
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    # If the user does not select a file, the browser submits an empty file
    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        # Associate the uploaded file with the logged-in user
        username = session['username']

        # Save the file to the user's folder within the upload directory
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
        os.makedirs(user_folder, exist_ok=True)  # Create the user folder if it doesn't exist
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_folder, filename))
        files = os.listdir(user_folder/username)
        files = [file for files in os.listdir(user_folder) if file != '.DS_Store']
        return render_template('welcome.html', username=username, files=files)

        # return 'File uploaded successfully'

    return 'File upload failed'
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove the 'username' key from the session
    return render_template('base.html')


if __name__ == '__main__':
    app.run()
