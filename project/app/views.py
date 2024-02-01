
from .forms import UserRegisterForm, TaskForm, TeamForm, CommentForm, AttachmentForm
from .models import Team, Comment, Attachment
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import auth
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Task, TaskStatus
from django.contrib import messages
import json
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.models import User, Group

def is_team_leader(user):
    team_leader_group = 'Team Leader'
    is_leader = user.groups.filter(name=team_leader_group).exists()
    print(f"{user.username} is a team leader: {is_leader}")
    return is_leader

def is_team_member(user):
    team_member_group = 'Team Member'
    is_member = user.groups.filter(name=team_member_group).exists()
    print(f"{user.username} is a team member: {is_member}")
    return is_member

def get_task_events(request):
    task_events = []

    tasks = Task.objects.all()

    for task in tasks:
        task_url = reverse('app:task_detail', args=[task.id])

        task_events.append({
            'id': task.id,
            'title': task.title,
            'start': task.due_date.strftime('%Y-%m-%d'),
            'url': task_url,
        })

    return JsonResponse(task_events, safe=False)


def get_kanban_tasks(request):
    kanban_data = {
        'todo': [],
        'in_progress': [],
        'done': [],
    }

    tasks = Task.objects.all()

    for task in tasks:
        status = task.status

        if status == TaskStatus.TODO:
            kanban_data['todo'].append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
            })
        elif status == TaskStatus.IN_PROGRESS:
            kanban_data['in_progress'].append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
            })
        elif status == TaskStatus.DONE:
            kanban_data['done'].append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
            })

    return JsonResponse(kanban_data)


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
            user = form.save()

            team_member_group = Group.objects.get(name='Team Member')
            user.groups.add(team_member_group)

            return redirect('app:login')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})


@login_required
def dashboard(request):
    done_tasks = Task.objects.filter(assignee=request.user, status=TaskStatus.DONE)
    teams = request.user.teams.all()
    return render(request, 'app/dashboard.html', {'tasks': done_tasks, 'teams': teams})


def team_list(request):
    teams = Team.objects.all()
    return render(request, 'app/team_list.html', {'teams': teams})

@login_required
def team_create(request):
    # Check if the user is a team leader
    if request.user.groups.filter(name='Team Leader').exists():
        if request.method == 'POST':
            form = TeamForm(request.POST)
            if form.is_valid():
                team = form.save(commit=False)
                team.team_leader = request.user
                team.save()
                messages.success(request, 'Team created successfully!')
                return redirect('app:team_detail', team_id=team.id)
            else:
                messages.error(request, 'Error creating the team. Please check the form data.')

        else:
            form = TeamForm()

        return render(request, 'app/team_form.html', {'form': form})
    else:
        # User is not authorized, return a custom error message or redirect
        return HttpResponseForbidden("You are not authorized to access this page.")

def team_detail(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    members = team.members.all()
    return render(request, 'app/team_detail.html', {'team': team, 'members': members})


@login_required
def team_update(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    # Check if the user is the team leader or has the necessary permissions
    if request.user == team.team_leader or request.user.groups.filter(name='Team Leader').exists():
        # User has permission, allow them to access the view
        if request.method == 'POST':
            form = TeamForm(request.POST, instance=team)
            if form.is_valid():
                form.save()
                messages.success(request, 'Team updated successfully!')
                return redirect('app:team_detail', team_id=team.id)
            else:
                messages.error(request, 'Error updating the team. Please check the form data.')
        else:
            form = TeamForm(instance=team)

        return render(request, 'app/team_form.html', {'form': form, 'team': team})

    else:
        # User is not authorized, return a custom error message or redirect
        return HttpResponseForbidden("You are not authorized to access this page.")


@login_required
def team_delete(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    # Check if the user is the team leader
    if request.user == team.team_leader:
        if request.method == 'POST':
            team.delete()
            messages.success(request, 'Team deleted successfully!')
            return redirect('app:team_list')
        else:
            messages.error(request, 'Error deleting the team.')
            return redirect('app:team_list')

    else:
        # User is not authorized, return a custom error message or redirect
        return HttpResponseForbidden("You are not authorized to access this page.")


@login_required
def task_list(request):
    sort_by = request.GET.get('sort')
    if sort_by == 'priority':
        tasks = Task.objects.order_by('-priority')
    else:
        tasks = Task.objects.all()  # Default ordering
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
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        if request.content_type == 'application/json':
            # Handle JSON data for drag-and-drop updates
            data = json.loads(request.body)
            new_status = data.get('status')

            if new_status not in [status[0] for status in TaskStatus.choices]:
                return JsonResponse({'error': 'Invalid status value'}, status=400)

            task.status = new_status
            task.save()

            # Return a JSON response
            return JsonResponse({'status': task.status})

        else:
            # Parse form data from the request for form-based updates
            title = request.POST.get('title')
            description = request.POST.get('description')
            priority = request.POST.get('priority')
            due_date = request.POST.get('due_date')
            status = request.POST.get('status')
            team = request.POST.get('team')
            assignee = request.POST.get('assignee')

            task.title = title
            task.description = description
            task.priority = priority
            task.due_date = due_date
            task.status = status
            task.team_id = team
            task.assignee_id = assignee
            task.save()

            # Redirect to the task list page (app/tasks) after updating the task
            return redirect('app:task_list')

    elif request.method == 'GET':
        form = TaskForm(instance=task)
        context = {
            'form': form,
            'form_title': 'Update Task',
        }
        return render(request, 'app/task_update_form.html', context)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

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
            comment.task = task
            comment.author = request.user
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
