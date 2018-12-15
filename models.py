from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    course_type = db.Column(db.String(2), nullable=False)
    has_practical = db.Column(db.Boolean, default=False, nullable=False)
    desc = db.Column(db.String(200))
    credit = db.Column(db.Integer, nullable=False)
    enrollments = db.relationship('StudentCourse', backref='course')

    def __repr__(self):
        return f'Course({self.id},{self.name},{self.semester},{self.course_type},{self.has_practical})'


class StudentCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    c1 = db.Column(db.Numeric)
    c2 = db.Column(db.Numeric)
    c3 = db.Column(db.Numeric)
    c4 = db.Column(db.Numeric)
    attendance = db.Column(db.Numeric)
    grade = db.Column(db.Integer)
    grade_point = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    semester = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'StudentCourse({self.id},{self.student_id},{self.course_id},{self.c1},{self.c2},{self.c3},{self.c4})'


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(20), nullable=False)
    courses = db.relationship('StudentCourse', backref='student')
    cum_credits = db.Column(db.Integer, default=0)
    cum_grade_point = db.Column(db.Integer, default=0)
    cgpa = db.Column(db.Numeric, default=0)

    def __repr__(self):
        return f'Student({self.id},{self.name},{self.course})'
