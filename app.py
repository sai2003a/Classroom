

from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "batch2SecretKey"
app.permanent_session_lifetime = timedelta(days=365)


@app.route("/")
def home():
    if 'username' in session and session['role'] == 'student':
        return render_template('student_dashboard.html')
    elif  'username' in session and session['role'] == 'teacher':
        return render_template('teacher_dashboard.html')
    else:
        return redirect("/select_role")

@app.route("/logout")
def logout():
    session.pop("username") and session.pop("role")
    return redirect("/select_role")

@app.route('/select_role')
def select_role():
    return render_template('select_role.html')

@app.route('/register_student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db=sqlite3.connect('database.db')
        existing_user = db.execute('SELECT * FROM register_student WHERE name = ? OR email = ?', (username, email)).fetchone()
        db.execute('INSERT INTO register_student (name, email, password) VALUES (?, ?, ?)', (username, email, password))
        db.commit()
        db.close()
        return redirect(url_for('login_student'))
        
    return render_template('register_student.html')

@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db=sqlite3.connect('database.db')
        existing_user = db.execute('SELECT * FROM register_teacher WHERE name = ? OR email = ?', (username, email)).fetchone()
        
        db.execute('INSERT INTO register_teacher (name, email, password) VALUES (?, ?, ?)', (username, email, password))
        db.commit()
        db.close()
        return redirect(url_for('login_teacher'))
       
    return render_template('register_teacher.html')

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db=sqlite3.connect('database.db')
        student = db.execute('SELECT * FROM register_student WHERE name = ?', (username,)).fetchone()
        if student and student[3] == password:  
            session['username'] = username
            session['role'] = 'student'
            return redirect(url_for('student_dashboard'))
        db.commit()
        db.close()
    return render_template('login_student.html')

@app.route('/login_teacher', methods=['GET', 'POST'])
def login_teacher():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db=sqlite3.connect('database.db')
        teacher = db.execute('SELECT * FROM register_teacher WHERE name = ?', (username,)).fetchone()
        if teacher and teacher[3] == password: 
            session['username'] = username
            session['role'] = 'teacher'
            return redirect(url_for('teacher_dashboard'))
        db.commit()
        db.close()
    return render_template('login_teacher.html')


@app.route('/student_dashboard')
def student_dashboard():
    if 'username' in session and session['role'] == 'student':
        return render_template('student_dashboard.html')
    else:
        return redirect(url_for('login_student'))
    
@app.route('/student_classes')
def student_classes():
    return render_template('student_classes.html')

@app.route('/student_assignment')
def student_assignment():
    return render_template('student_assignment.html')

@app.route('/student_announcement')
def student_announcement():
    return render_template('student_announcement.html')

@app.route('/student_attendance')
def student_attendance():
    return render_template('student_attendance.html')

@app.route('/teacher_dashboard')
def teacher_dashboard():
    if 'username' in session and session['role'] == 'teacher':
        return render_template('teacher_dashboard.html')
    else:
        return redirect(url_for('login_teacher'))
    
@app.route('/teacher_classes')
def teacher_classes():
    return render_template('teacher_classes.html')

@app.route('/teacher_assignment')
def teacher_assignment():
    return render_template('teacher_assignment.html')


@app.route('/teacher_announcement')
def teacher_announcement():
    return render_template('teacher_announcement.html')

@app.route('/teacher_attendance')
def teacher_attendance():
    return render_template('teacher_attendance.html')

if __name__ == "__main__":
    app.run(debug=True)
