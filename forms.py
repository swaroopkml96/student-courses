from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SelectField, DecimalField, IntegerField, FormField, FieldList, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from models import Course


class StudentCourseForm(FlaskForm):
    semester = SelectField(
        'Semester',
        validators=[DataRequired()],
        choices=[
            ('1', 1), ('2', 2), ('3', 3),
            ('4', 4), ('5', 5), ('6', 6)
        ]
    )
    c = SelectField(
        'Course',
        choices=[(course.id, course.name)
                 for course in Course.query.all()]
    )
    c1 = DecimalField('C1', validators=[NumberRange(min=0, max=20)], places=2)
    c2 = DecimalField('C2', validators=[NumberRange(min=0, max=20)], places=2)
    c3 = DecimalField('C3', validators=[NumberRange(min=0, max=20)], places=2)
    c4 = DecimalField('C4', validators=[NumberRange(min=0, max=40)], places=2)
    attendance = DecimalField(
        'Attendance', validators=[NumberRange(min=0, max=100)], places=2)
    submit = SubmitField('Add')


class StudentForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=1)])
    course = SelectField(
        'Course',
        validators=[DataRequired()],
        choices=[
            ('MSc', 'MSc'), ('MCA', 'MCA'),
            ('MTech', 'MTech'), ('MPhil', 'MPhil')
        ]
    )
    submit = SubmitField('Add')


class CourseForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(), Length(min=1)])
    desc = StringField('Description', validators=[
        DataRequired(), Length(min=1)])
    course_type = SelectField(
        'Type',
        validators=[DataRequired()],
        choices=[('HC', 'HC'), ('SC', 'SC'), ('OE', 'OE')]
    )
    credit = IntegerField('Credit', validators=[DataRequired()])
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
            ('grade', 'Grade')
        ]
    )
    rev = BooleanField('Descending')
    attn = BooleanField('Attendance < 75%')
    apply = SubmitField('Apply')


class StudentsFilters(FlaskForm):
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
                                for course in Course.query.all()]
    )
    course2 = SelectField(
        'Course',
        choices=[(0, 'Any')] + [(course.id, course.name)
                                for course in Course.query.all()]
    )
    sem = SelectField(
        'Semester',
        choices=[
            ('1', 1), ('2', 2), ('3', 3),
            ('4', 4), ('5', 5), ('6', 6)
        ]
    )
    apply = SubmitField('Apply')
