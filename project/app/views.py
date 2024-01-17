from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, TaskForm, Task, TeamForm, CommentForm, AttachmentForm, LabelForm
from .models import Team, Comment, Attachment, Label
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth import logout

'''def custom_logout(request):
    if request.user.is_staff or request.user.is_superuser:
        logout(request)
        return redirect('admin-login')  # Redirect to the admin login page
    else:
        logout(request)
        return redirect('login')  # Redirect to the regular user login page'''
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import redirect

def welcome(request):
    return render(request, 'app/welcome.html')

def logout(request):
    """Logs out the user."""
    auth.logout(request)
    return redirect('app:login')

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
            return redirect('app:team_list')
    else:
        form = TeamForm()
    return render(request, 'app/team_form.html', {'form': form})

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = team.members.all()
    return render(request, 'app/team_detail.html', {'team': team, 'members': members})
def team_update(request, team_id):
    team = Team.objects.get(id=team_id)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('app:team_detail', team_id=team.id)
    else:
        form = TeamForm(instance=team)
    return render(request, 'app/team_form.html', {'form': form})

def team_delete(request, team_id):
    team = Team.objects.get(id=team_id)
    team.delete()
    return redirect('app:team_list')
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'app/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.creator = request.user
            new_task.save()
            return redirect('app:task_list')
    else:
        form = TaskForm()
    return render(request, 'app/task_form.html', {'form': form})


# views.py
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.comments.all()
    attachments = task.attachments.all()
    return render(request, 'app/task_detail.html', {
        'task': task,
        'comments': comments,
        'attachments': attachments
    })

def task_update(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('app:task_detail', task_id=task.id)  # Redirect to the task's detail view
    else:
        form = TaskForm(instance=task)
    return render(request, 'app/task_form.html', {'form': form})


def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('app:task_list')

def comment_list(request, task_id):
    comments = Comment.objects.filter(task_id=task_id)
    return render(request, 'app/comment_list.html', {'comments': comments, 'task_id': task_id})

def comment_create(request, task_id):
    task = Task.objects.get(id=task_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task  # Set the task instance
            comment.author = request.user  # Set the author to the current user
            comment.save()
            return redirect('app:task_detail', task_id=task_id)
    else:
        form = CommentForm()

    return render(request, 'app/comment_form.html', {'form': form, 'task_id': task_id})


def comment_detail(request, task_id, comment_id):
    task = get_object_or_404(Task, pk=task_id)
    comment = get_object_or_404(Comment, pk=comment_id, task=task)
    return render(request, 'app/comment_detail.html', {'task': task, 'comment': comment})


def comment_update(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('app:comment_list', task_id=comment.task_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'app/comment_form.html', {'form': form, 'comment_id': comment_id})

def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    task_id = comment.task_id
    comment.delete()
    return redirect('app:comment_list', task_id=task_id)

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
            return redirect('app:task_detail', task_id=task.id)
    else:
        form = AttachmentForm()

    return render(request, 'app/attachment_form.html', {'form': form})


def attachment_update(request, attachment_id):
    attachment = Attachment.objects.get(id=attachment_id)
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES, instance=attachment)
        if form.is_valid():
            form.save()
            return redirect('app:attachment_list', task_id=attachment.task_id)
    else:
        form = AttachmentForm(instance=attachment)
    return render(request, 'app/attachment_form.html', {'form': form, 'attachment_id': attachment_id})


def attachment_delete(request, attachment_id):
    attachment = Attachment.objects.get(id=attachment_id)
    task_id = attachment.task_id
    attachment.delete()
    return redirect('app:attachment_list', task_id=task_id)

