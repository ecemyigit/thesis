from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, TaskForm, Task, TeamForm, CommentForm, AttachmentForm, LabelForm
from .models import Team, Comment, Attachment, Label
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})

@login_required
def dashboard(request):
    tasks = Task.objects.filter(assignee=request.user)
    teams = request.user.teams.all()
    return render(request, 'app/dashboard.html', {'tasks': tasks, 'teams': teams})

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'app/team_list.html', {'teams': teams})

def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'app/team_form.html', {'form': form})

def team_detail(request, team_id):
    team = Team.objects.get(id=team_id)
    return render(request, 'app/team_detail.html', {'team': team})

def team_update(request, team_id):
    team = Team.objects.get(id=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team_detail', team_id=team.id)
    else:
        form = TeamForm(instance=team)
    return render(request, 'app/team_form.html', {'form': form})

def team_delete(request, team_id):
    team = Team.objects.get(id=team_id)
    team.delete()
    return redirect('team_list')
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'app/task_list.html', {'tasks': tasks})

@login_required  # Ensures that only logged-in users can create tasks
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.creator = request.user  # Set the creator to the current user
            new_task.save()
            return redirect('task_list')  # Redirect to the task list view
    else:
        form = TaskForm()
    return render(request, 'app/task_form.html', {'form': form})


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'app/task_detail.html', {'task': task})

def task_update(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)  # Redirect to the task's detail view
    else:
        form = TaskForm(instance=task)
    return render(request, 'app/task_form.html', {'form': form})


def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')

def comment_list(request, task_id):
    comments = Comment.objects.filter(task_id=task_id)
    return render(request, 'app/comment_list.html', {'comments': comments, 'task_id': task_id})

def comment_create(request, task_id):
    task = Task.objects.get(id=task_id)  # Get the Task instance

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task  # Set the task instance
            comment.author = request.user  # Set the author to the current user
            comment.save()
            return redirect('comment_list', task_id=task_id)
    else:
        form = CommentForm()

    return render(request, 'app/comment_form.html', {'form': form, 'task_id': task_id})

def comment_update(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comment_list', task_id=comment.task_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'app/comment_form.html', {'form': form, 'comment_id': comment_id})

def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    task_id = comment.task_id
    comment.delete()
    return redirect('comment_list', task_id=task_id)

def attachment_list(request, task_id):
    attachments = Attachment.objects.filter(task_id=task_id)
    return render(request, 'app/attachment_list.html', {'attachments': attachments, 'task_id': task_id})


def attachment_create(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.task = task
            attachment.author = request.user
            attachment.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = AttachmentForm()

    return render(request, 'app/attachment_form.html', {'form': form})


def attachment_update(request, attachment_id):
    attachment = Attachment.objects.get(id=attachment_id)
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES, instance=attachment)
        if form.is_valid():
            form.save()
            return redirect('attachment_list', task_id=attachment.task_id)
    else:
        form = AttachmentForm(instance=attachment)
    return render(request, 'app/attachment_form.html', {'form': form, 'attachment_id': attachment_id})

def attachment_delete(request, attachment_id):
    attachment = Attachment.objects.get(id=attachment_id)
    task_id = attachment.task_id
    attachment.delete()
    return redirect('attachment_list', task_id=task_id)

def label_list(request):
    labels = Label.objects.all()
    return render(request, 'app/label_list.html', {'labels': labels})

"""
def label_create(request):
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('label_list')
    else:
        form = LabelForm()
    return render(request, 'app/label_form.html', {'form': form})

def label_update(request, label_id):
    label = Label.objects.get(id=label_id)
    if request.method == 'POST':
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return redirect('label_list')
    else:
        form = LabelForm(instance=label)
    return render(request, 'app/label_form.html', {'form': form, 'label_id': label_id})
def label_detail(request, label_id):
    label = Label.objects.get(id=label_id)
    return render(request, 'app/label_detail.html', {'label': label})
def label_delete(request, label_id):
    label = Label.objects.get(id=label_id)
    label.delete()
    return redirect('label_list')
"""