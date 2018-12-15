import math
import os
from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from models import db, Student, Course, StudentCourse

app = Flask(__name__)
app.config['SECRET_KEY'] = '210ec2b2d4555bb07cdf2b704070d321'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:bprop42@localhost/student_courses'
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
    form = StudentsFilters()
    students = Student.query
    if request.method == 'POST':
        r = request.form
        orderby = r['orderby']
        course1 = int(r['course1'])
        course2 = int(r['course2'])
        sem = int(r['sem'])

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

        if 'cgpa9' in r.keys():
            students = students.filter(Student.cgpa > 9)
        if 'rev' in r.keys():
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
    form = StudentForm()
    if request.method == "POST":
        r = request.form
        s = getStudentObject(r)
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
    form = CoursesFilters()
    courses = Course.query
    if request.method == 'POST':
        r = request.form
        orderby = r['orderby']
        if 'hp' in r.keys():
            courses = courses.filter_by(has_practical=True)
        if 'rev' in r.keys():
            courses = courses.order_by(getattr(Course, orderby).desc())
        else:
            courses = courses.order_by(getattr(Course, orderby))
    return render_template('courses.html', courses=courses.all(), form=form)


@app.route("/course/<id>", methods=['GET', 'POST'])
def getCourse(id):
    from forms import CourseStudentFilters
    form = CourseStudentFilters()
    course = Course.query.get(id)
    enrollments = StudentCourse.query.filter_by(course_id=id)
    if request.method == 'POST':
        r = request.form
        orderby = r['orderby']
        if 'attn' in r.keys():
            enrollments = enrollments.filter(StudentCourse.attendance < 75)
        if 'rev' in r.keys():
            enrollments = enrollments.order_by(
                getattr(StudentCourse, orderby).desc())
        else:
            enrollments = enrollments.order_by(getattr(StudentCourse, orderby))
    return render_template('course.html', course=course, enrollments=enrollments.all(), form=form)


@app.route("/addcourse", methods=['GET', 'POST'])
def addCourse():
    from forms import CourseForm
    form = CourseForm()
    if request.method == "POST":
        r = request.form
        c = getCourseObject(r)
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
    form = StudentCourseForm()
    if request.method == "POST":
        r = request.form
        sc = getStudentCourseObject(r, student_id)
        db.session.add(sc)
        db.session.commit()
        updateStudents()
        db.session.commit()
    return render_template('addenrollment.html', form=form, student=Student.query.get(student_id))


# Convenience functions
def getStudentObject(formData):
    s = Student(
        name=formData['name'],
        course=formData['course'],
    )
    return s


def getCourseObject(formData):
    has_practical = False
    if 'has_practical' in formData.keys():
        has_practical = True
    c = Course(
        name=formData['name'],
        course_type=formData['course_type'],
        has_practical=has_practical,
        desc=formData['desc'],
        credit=formData['credit']
    )
    return c


def getStudentCourseObject(formData, student_id):
    course_id = formData['c']
    c1 = float(formData['c1'])
    c2 = float(formData['c2'])
    c3 = float(formData['c3'])
    c4 = float(formData['c4'])

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
        attendance=formData['attendance'],
        grade=grade,
        grade_point=grade_point,
        semester=formData['semester'],
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
