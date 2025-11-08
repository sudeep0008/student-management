from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# ********   Database Configuration ******

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ***** Model Definition *****

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(100), nullable=False)
    student_class = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)



@app.route('/')
def home():
    students = Student.query.all()
    return render_template('index.html',std = students) 


# Add Student Page
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        student_class = request.form['class']
        email = request.form['email']

        new_student = Student(
            name=name,
              roll=roll, 
              student_class=student_class,
                email=email)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('add.html')


# 🗑️ DELETE STUDENT
@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    global students
    students = [s for s in students if s['id'] != student_id]
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



# ✏️ UPDATE STUDENT
@app.route('/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    for student in students:
        if student['id'] == student_id:
            if request.method == 'POST':
                student['name'] = request.form['name']
                student['roll'] = request.form['roll']
                student['class'] = request.form['class']
                student['email'] = request.form['email']
                return redirect(url_for('home'))
            return render_template('update.html', student=student)
    return "Student not found", 404



@app.route('/services')
def services():
    return render_template('services.html')



if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)