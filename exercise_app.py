from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="exercise_tracker",
        user="postgres",
        password="admin"
    )
    return conn

# Initialize database table
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            description TEXT,
            photo_path VARCHAR(255),
            hashtag VARCHAR(100)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_exercise', methods=['POST'])
def add_exercise():
    name = request.form['name']
    description = request.form['description']
    hashtag = request.form['hashtag']
    
    # Handle file upload
    photo = request.files['photo']
    photo_path = None
    
    if photo and photo.filename != '':
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)
    
    # Insert into database
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO exercises (name, description, photo_path, hashtag) VALUES (%s, %s, %s, %s)",
        (name, description, photo_path, hashtag)
    )
    conn.commit()
    cur.close()
    conn.close()
    
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/exercises')
def exercises():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM exercises ORDER BY id DESC")
    exercises = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('exercises.html', exercises=exercises)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
