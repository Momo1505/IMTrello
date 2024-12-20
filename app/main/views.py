from flask import render_template, url_for, redirect, flash
from . import main
from .forms import TaskForm, ProjectForm, UpdateTaskForm, UpdateTaskFormDev, FilterForm
from .. import db
from ..models import User, Role, Project, Task, projects_user
from flask_login import current_user


@main.route('/developer/<user_name>', methods=['GET', 'POST'])
def developer(user_name):
    task = current_user.assigned_tasks
    total_tasks = len(task)
    total_tasks_completed = 0

    for t in task:
        if t.completed == True:
            total_tasks_completed += 1
        if t.is_new == True:
            flash('New Task(s) Available')
            t.is_new = False
            db.session.add(t)
            db.session.commit()
    total_tasks_uncompleted = total_tasks - total_tasks_completed

    filter_form = FilterForm()
    filter = None
    if filter_form.validate_on_submit():
        filter= filter_form_handler(filter_form)
        return render_template("main/developer.html", template_tasks=task, username=current_user.username,
                           total_tasks=total_tasks, total_tasks_completed=total_tasks_completed,
                           total_tasks_uncompleted=total_tasks_uncompleted,
                           filter=filter,
                           filter_form=filter_form)


    return render_template("main/developer.html", template_tasks=task, username=current_user.username,
                           total_tasks=total_tasks, total_tasks_completed=total_tasks_completed,
                           total_tasks_uncompleted=total_tasks_uncompleted,
                           filter=filter,
                           filter_form=filter_form)


@main.route('/manager/<user_name>')
def manager(user_name):
    projects = current_user.projects
    if projects:
        return render_template('main/home.html', projects=projects, username=user_name)
    else:
        return redirect(url_for('main.create_project', user_name=current_user.username))


@main.route('/manager/<user_name>/<project_name>', methods=['GET', 'POST'])
def home(user_name, project_name):
    task_form = TaskForm()

    update_task_form = UpdateTaskForm()

    project = Project.query.filter_by(project_name=project_name).first()
    tasks = project.tasks

    total_tasks = Task.query.filter_by(project=project).count()
    total_tasks_completed = Task.query.filter_by(project=project, completed=True).count()
    total_tasks_uncompleted = total_tasks - total_tasks_completed

    if task_form.validate_on_submit():
        task_form_handler(task_form, project_name)
        return redirect(
            url_for('main.home', user_name=current_user.username, project_name=project.project_name))
    return render_template("main/manager_project_page.html", project_name=project_name, form=task_form,
                           template_tasks=tasks, total_tasks=total_tasks, total_tasks_completed=total_tasks_completed,
                           total_tasks_uncompleted=total_tasks_uncompleted, update_task_form=update_task_form)


@main.route('/create_project/<user_name>', methods=['GET', 'POST'])
def create_project(user_name):
    project_form = ProjectForm()
    if project_form.validate_on_submit():
        project_name, project_description, project_deadline = create_project_form_handler(project_form)
        return redirect(url_for('main.home', user_name=current_user.username, project_name=project_name))
    return render_template("main/new_project.html", form=project_form)


@main.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()  # get the task from the id
    project_name = task.project.project_name  # get the project name from project attribute Task class
    if task is not None:
        assigned_users = task.assigned_users
        for user in assigned_users:
            # Vérifier si l'utilisateur n'a plus aucune autre tâche attribuée
            if len(user.assigned_tasks) == 1 and task in user.assigned_tasks:
                # Supprimer le projet associé à cet utilisateur s'il en a un
                if user.projects:
                    user.projects.remove(task.project)
                    db.session.add(user)
                    db.session.commit()
        db.session.delete(task)
        db.session.commit()
        flash(f"Task {task.task_name} has been deleted")
    return redirect(url_for('main.home', user_name=current_user.username, project_name=project_name))


@main.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()  # get the task from the id
    project_name = task.project.project_name
    tasks = Task.query.filter_by(task_name=task.task_name).all()
    for task in tasks:
        if task.completed is False :
            task.completed = True
            db.session.add(task)
            db.session.commit()
    flash(f"Task {task.task_name} has been completed")
    return redirect(url_for('main.developer', user_name=current_user.username, project_name=project_name))



@main.route('/delete_project/<project_name>')
def delete_project(project_name):
    project = Project.query.filter_by(project_name=project_name).first()
    for task in project.tasks:
        db.session.delete(task)

    db.session.delete(project)
    db.session.commit()
    flash(f"Project {project_name} has been deleted")
    return redirect(url_for('main.manager', user_name=current_user.username))


def task_form_handler(task_form, project_name):
    new_task_name = task_form.task.data
    member_username = task_form.memberUserName.data
    task_description = task_form.taskDescription.data
    task_priority = task_form.priority.data
    task_deadline = task_form.deadline.data
    # clean the form
    task_form.task.data = ''
    task_form.memberUserName.data = ''
    task_form.taskDescription.data = ''
    task_form.priority.data = ''
    task_form.deadline.data = ''

    # Split the members string into a list of the members
    memberList = member_username.split(',')
    for user in memberList:

        # load the developer and the project from the database
        member = User.query.filter_by(username=user).first()
        project = Project.query.filter_by(project_name=project_name).first()

        # test if there is already a task by this name in the project
        existing_task = Task.query.filter_by(project_id=project.id, task_name=new_task_name).first()
        if existing_task:
            flash("There is already a task by this name in the project")
            return

        # if the developer is free
        if member:
            if member.role_id == 1:  # test if the member is a developer
                if len(member.projects) == 0:  # the developer is free
                    # add the task to the member and project
                    new_task = Task(task_name=new_task_name, description=task_description, comment="comment",
                                    priority=task_priority, deadline=task_deadline)
                    member.assigned_tasks.append(new_task)
                    member.projects.append(project)
                    project.tasks.append(new_task)
                    db.session.add_all([new_task, member, project])
                    db.session.commit()
                    flash("The task has been successfully added.")

                elif len(member.projects) == 1 and member.projects[0].id == project.id:
                    new_task = Task(task_name=new_task_name, description=task_description, comment="comment",
                                    priority=task_priority, deadline=task_deadline)
                    member.assigned_tasks.append(new_task)
                    project.tasks.append(new_task)
                    db.session.add_all([new_task, member, project])
                    db.session.commit()
                    flash("The task has been successfully added.")

                else:
                    flash("the developer is busy")
            else:
                flash("This user is a project manager.")
        else:
            flash("There is no user with this username.")


def create_project_form_handler(project_form):
    new_project = project_form.project.data
    project_description = project_form.projectDescription.data
    deadline = project_form.deadline.data
    # clean the project_form
    project_form.project.data = ''
    project_form.projectDescription.data = ''
    project_form.deadline.data = ''

    project = Project(project_name=new_project, description=project_description, deadline=deadline)
    current_user.projects.append(project)
    db.session.add_all([current_user, project])
    db.session.commit()
    return project.project_name, project_description, deadline


@main.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if current_user.role_id == 2:
        update_task_form = UpdateTaskForm()
        if update_task_form.validate_on_submit():
            project_name, username = edit_task_form_handler(update_task_form, task_id)
            return redirect(url_for('main.home', user_name=username, project_name=project_name))
        return render_template("main/edit_task.html", update_task_form=update_task_form)
    else:
        update_task_form = UpdateTaskFormDev()
        if update_task_form.validate_on_submit():
            project_name, username = edit_task_form_handler(update_task_form, task_id)
            return redirect(url_for('main.developer', user_name=username, project_name=project_name))
        return render_template("main/edit_task.html", update_task_form=update_task_form)



def edit_task_form_handler(update_task_form,task_id):
    if current_user.role_id == 2:
        description = update_task_form.description.data
        dev = update_task_form.developer.data

        update_task_form.description.data = ''
        update_task_form.developer.data = ''

        task = Task.query.filter_by(id=task_id).first()
        if description != "":
            task.description = description

        user = User.query.filter_by(username=dev).first()
        if user is not None :
            add_task(user, task)
        db.session.add(task)
        db.session.commit()
        return task.project.project_name, current_user.username
    else:
        comment = update_task_form.comment.data
        update_task_form.comment.data = ''

        task = Task.query.filter_by(id=task_id).first()
        task.comment = comment
        db.session.add(task)
        db.session.commit()
        return task.project.project_name, current_user.username


def add_task(member, task):
    if task in member.assigned_tasks:
        flash("This developer has already this task")
        return
    if member:
        if member.role_id == 1:  # test if the member is a developer
            if len(member.projects) == 0:  # the developer is free
                # add the task to the member and project
                new_task = Task(task_name=task.task_name, description=task.description, comment="comment",
                                priority=task.priority, deadline=task.deadline, completed=task.completed)
                member.assigned_tasks.append(new_task)
                member.projects.append(task.project)
                task.project.tasks.append(new_task)
                db.session.add_all([new_task, member, task.project])
                db.session.commit()
                flash("The task has been successfully added.")

            elif len(member.projects) == 1 and member.projects[0].id == task.project.id:
                new_task = Task(task_name=task.task_name, description=task.description, comment="comment",
                                priority=task.priority, deadline=task.deadline, completed=task.completed)
                member.assigned_tasks.append(new_task)
                task.project.tasks.append(new_task)
                db.session.add_all([new_task, member, new_task.project])
                db.session.commit()
                flash("The task has been successfully added.")

            else:
                flash("the developer is busy")
        else:
            flash("This user is a project manager.")
    else:
        flash("There is no user with this username.")


def filter_form_handler(filter_form):
    filter= filter_form.filter.data
    if filter == "1":
        return '1'
    elif filter == "2":
        return "2"
    elif filter == "3":
        return "3"
    elif filter == "4":
        return True
    else:
        return None
