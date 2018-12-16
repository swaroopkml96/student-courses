from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, InputRequired, NumberRange, ValidationError


class StudentCourseForm(FlaskForm):
    from models import db, Course
    semester = SelectField(
        'Semester',
        choices=[
            (1, '1'), (2, '2'), (3, '3'),
            (4, '4'), (5, '5'), (6, '6')
        ],
        coerce=int
    )
    c = SelectField(
        'Course',
        choices=[(course.id, course.name)
                 for course in db.session.query(Course).all()],
        coerce=int
    )
    c1 = DecimalField(validators=[InputRequired(), NumberRange(min=0, max=20)])
    c2 = DecimalField(validators=[InputRequired(), NumberRange(min=0, max=20)])
    c3 = DecimalField(validators=[InputRequired(), NumberRange(min=0, max=20)])
    c4 = DecimalField(validators=[InputRequired(), NumberRange(min=0, max=40)])
    attendance = DecimalField(
        validators=[InputRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Add')


class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    course = SelectField(
        'Course',
        choices=[
            ('MSc', 'MSc'), ('MCA', 'MCA'),
            ('MTech', 'MTech'), ('MPhil', 'MPhil')
        ]
    )
    submit = SubmitField('Add')


class CourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    desc = StringField('Description', validators=[DataRequired()])
    course_type = SelectField(
        'Type',
        choices=[('HC', 'HC'), ('SC', 'SC'), ('OE', 'OE')]
    )
    credit = IntegerField('Credit', validators=[
                          InputRequired(), NumberRange(min=0)])
    has_practical = BooleanField('Has practical')
    submit = SubmitField('Add')


class CoursesFilters(FlaskForm):
    orderby = SelectField(
        'Sort by',
        choices=[
            ('id', 'Id'),
            ('name', 'Name'),
            ('course_type', 'Type'),
        ]
    )
    rev = BooleanField('Descending')
    hp = BooleanField('Has practical')
    apply = SubmitField('Apply')


class CourseStudentFilters(FlaskForm):
    orderby = SelectField(
        'Sort by',
        choices=[
            ('student_id', 'Roll no.'),
            ('semester', 'Semester'),
            ('grade', 'Grade')
        ]
    )
    rev = BooleanField('Descending')
    attn = BooleanField('Attendance < 75%')
    apply = SubmitField('Apply')


class StudentsFilters(FlaskForm):
    from models import Course
    from app import db
    orderby = SelectField(
        'Sort by',
        choices=[
            ('id', 'Roll no.'),
            ('name', 'Name'),
            ('course', 'Course'),
            ('cum_credits', 'Credits'),
            ('cum_grade_point', 'Grade point'),
            ('cgpa', 'CGPA')
        ]
    )
    rev = BooleanField('Descending')
    cgpa9 = BooleanField('CGPA > 9')
    course1 = SelectField(
        'Course',
        choices=[(0, 'Any')] + [(course.id, course.name)
                                for course in Course.query.all()],
        coerce=int
    )
    course2 = SelectField(
        'Course',
        choices=[(0, 'Any')] + [(course.id, course.name)
                                for course in Course.query.all()],
        coerce=int
    )
    sem = SelectField(
        'Semester',
        choices=[
            ('1', 1), ('2', 2), ('3', 3),
            ('4', 4), ('5', 5), ('6', 6)
        ]
    )
    apply = SubmitField('Apply')
