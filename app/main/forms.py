from flask_wtf import FlaskForm
from wtforms import TextAreaField, BooleanField, SubmitField, StringField
from wtforms.fields import DateField
from wtforms.fields import RadioField
from wtforms.validators import DataRequired, Optional
from ..models import User


class FilterForm(FlaskForm):
    filter = RadioField('Priority', choices=[('1', 'Top Priority'), ('2', 'Not Urgent'), ('3', 'Low Priority'),
                                             ('4', 'Completed'), (None, 'Delete Filter')], validators=[Optional()])
    apply = SubmitField('Apply')



class TaskForm(FlaskForm):
    task = TextAreaField('Task', validators=[DataRequired()], render_kw={"placeholder": "Add to do"})
    memberUserName = StringField('MemberUserName', validators=[Optional(), ],
                                 render_kw={"placeholder": "user1,user2,user3"})
    taskDescription = TextAreaField('TaskDescription', validators=[DataRequired()],
                                    render_kw={"placeholder": "Task Description"})
    priority = RadioField('Priority', choices=[('1', 'Top Priority'), ('2', 'Not Urgent'), ('3', 'Low Priority')],
                          validators=[DataRequired()])
    deadline = DateField('Deadline', render_kw={"placeholder": "YYYY-MM-DD"})

    add = SubmitField('Add')


class ProjectForm(FlaskForm):
    project = StringField('Project Name', validators=[DataRequired()], render_kw={"placeholder": "Name of the project"})
    projectDescription = TextAreaField('Project Description', validators=[DataRequired()],
                                       render_kw={"placeholder": "Project description"})
    deadline = DateField('Deadline', render_kw={"placeholder": "YYYY-MM-DD"})
    create = SubmitField('Create')


class UpdateTaskForm(FlaskForm):
    description = TextAreaField('Task Description', validators=[Optional()],
                                render_kw={"placeholder": "new task description"})
    developer = TextAreaField('Developer Name', validators=[Optional()],
                              render_kw={"placeholder": "place here the developer username"})
    update = SubmitField('Update')


class UpdateTaskFormDev(FlaskForm):
    comment = TextAreaField('Developer Comment', validators=[Optional()])
    update = SubmitField('Update')

