import math
import os
from flask import Flask, render_template, url_for, request, flash
from flask_bootstrap import Bootstrap
from models import db, Student, Course, StudentCourse

app = Flask(__name__)
app.config['SECRET_KEY'] = '210ec2b2d4555bb07cdf2b704070d321'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

with app.app_context():
    db.init_app(app)

bootstrap = Bootstrap(app)


@app.route("/", methods=['GET', 'POST'])
def home():
    return students()


@app.route("/students", methods=['GET', 'POST'])
def students():
    from forms import StudentsFilters
    form = StudentsFilters(request.form)
    students = Student.query
    if request.method == 'POST' and form.validate():
        orderby = form.orderby.data
        course1 = form.course1.data
        course2 = form.course2.data
        sem = form.sem.data

        if (not course1 == 0) and (not course2 == 0):
            students = students.join(Student.courses).filter(
                StudentCourse.course_id == course1,
                StudentCourse.semester == sem
            ).intersect(
                students.join(Student.courses).filter(
                    StudentCourse.course_id == course2,
                    StudentCourse.semester == sem
                )
            )

        elif not course1 == 0:
            students = students.join(Student.courses).filter(
                StudentCourse.course_id == course1,
                StudentCourse.semester == sem
            )

        elif not course2 == 0:
            students = students.join(Student.courses).filter(
                StudentCourse.course_id == course2,
                StudentCourse.semester == sem
            )

        if form.cgpa9.data:
            students = students.filter(Student.cgpa > 9)
        if form.rev.data:
            students = students.order_by(getattr(Student, orderby).desc())
        else:
            students = students.order_by(getattr(Student, orderby))
    return render_template('students.html', students=students.all(), form=form)


@app.route("/student/<id>")
def getStudent(id):
    return render_template('student.html', Student=Student, StudentCourse=StudentCourse, student=Student.query.get(id))


@app.route("/addstudent", methods=['GET', 'POST'])
def addStudent():
    from forms import StudentForm
    form = StudentForm(request.form)
    if request.method == "POST" and form.validate():
        s = Student(
            name=form.name.data,
            course=form.course.data
        )
        db.session.add(s)
        db.session.commit()
    return render_template('addstudent.html', form=form)


@app.route("/delstudent/<id>", methods=['GET', 'POST'])
def delStudent(id):
    StudentCourse.query.filter_by(student_id=id).delete()
    Student.query.filter_by(id=id).delete()
    db.session.commit()
    return students()


@app.route("/courses", methods=['GET', 'POST'])
def courses():
    from forms import CoursesFilters
    form = CoursesFilters(request.form)
    courses = Course.query
    if request.method == 'POST' and form.validate():
        orderby = form.orderby.data
        if form.hp.data:
            courses = courses.filter_by(has_practical=True)
        if form.rev.data:
            courses = courses.order_by(getattr(Course, orderby).desc())
        else:
            courses = courses.order_by(getattr(Course, orderby))
    return render_template('courses.html', courses=courses.all(), form=form)


@app.route("/course/<id>", methods=['GET', 'POST'])
def getCourse(id):
    from forms import CourseStudentFilters
    form = CourseStudentFilters(request.form)
    course = Course.query.get(id)
    enrollments = StudentCourse.query.filter_by(course_id=id)
    if request.method == 'POST' and form.validate():
        orderby = form.orderby.data
        if form.attn.data:
            enrollments = enrollments.filter(StudentCourse.attendance < 75)
        if form.rev.data:
            enrollments = enrollments.order_by(
                getattr(StudentCourse, orderby).desc())
        else:
            enrollments = enrollments.order_by(getattr(StudentCourse, orderby))
    return render_template('course.html', course=course, enrollments=enrollments.all(), form=form)


@app.route("/addcourse", methods=['GET', 'POST'])
def addCourse():
    from forms import CourseForm
    form = CourseForm(request.form)
    if request.method == 'POST':
        if not form.validate():
            print(form.errors)
        c = Course(
            name=form.name.data,
            course_type=form.course_type.data,
            has_practical=form.has_practical.data,
            desc=form.desc.data,
            credit=form.credit.data
        )
        db.session.add(c)
        db.session.commit()
    return render_template('addcourse.html', form=form)


@app.route("/delcourse/<id>", methods=['GET', 'POST'])
def delCourse(id):
    StudentCourse.query.filter_by(course_id=id).delete()
    Course.query.filter_by(id=id).delete()
    db.session.commit()
    updateStudents()
    db.session.commit()
    return courses()


@app.route("/addenrollment/<student_id>", methods=['GET', 'POST'])
def addEnrollment(student_id):
    from forms import StudentCourseForm
    form = StudentCourseForm(request.form)
    if request.method == "POST" and form.validate():
        sc = getStudentCourseObject(form, student_id)
        db.session.add(sc)
        db.session.commit()
        updateStudents()
        db.session.commit()
    return render_template('addenrollment.html', form=form, student=Student.query.get(student_id))


# Convenience functions
def getStudentCourseObject(form, student_id):
    course_id = form.c.data
    c1 = form.c1.data
    c2 = form.c2.data
    c3 = form.c3.data
    c4 = form.c4.data

    course = Course.query.get(course_id)
    credit = course.credit
    grade = math.ceil((c1 + c2 + c3 + c4) / 10)
    grade_point = credit * grade

    sc = StudentCourse(
        course_id=course_id,
        student_id=student_id,
        c1=c1,
        c2=c2,
        c3=c3,
        c4=c4,
        attendance=form.attendance.data,
        grade=grade,
        grade_point=grade_point,
        semester=form.semester.data,
    )
    return sc


def updateStudents():
    for s in Student.query.all():
        courses = s.courses
        cum_credits = 0
        cum_grade_point = 0
        for c in courses:
            cum_credits += c.course.credit
            cum_grade_point += c.grade_point
        if cum_credits > 0:
            cgpa = cum_grade_point / cum_credits
        else:
            cgpa = 0
        s.cum_credits = cum_credits
        s.cum_grade_point = cum_grade_point
        s.cgpa = cgpa


if __name__ == '__main__':
    app.run(debug=True)
