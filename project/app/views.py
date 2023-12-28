from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})

# Placeholder for team views
def team_list(request):
    return HttpResponse("Placeholder for team list view")

def team_create(request):
    return HttpResponse("Placeholder for team create view")

def team_detail(request, team_id):
    return HttpResponse(f"Placeholder for team detail view with team_id: {team_id}")

def team_update(request, team_id):
    return HttpResponse(f"Placeholder for team update view with team_id: {team_id}")

def team_delete(request, team_id):
    return HttpResponse(f"Placeholder for team delete view with team_id: {team_id}")

# Placeholder for task views
def task_list(request):
    return HttpResponse("Placeholder for task list view")

def task_create(request):
    return HttpResponse("Placeholder for task create view")

def task_detail(request, task_id):
    return HttpResponse(f"Placeholder for task detail view with task_id: {task_id}")

def task_update(request, task_id):
    return HttpResponse(f"Placeholder for task update view with task_id: {task_id}")

def task_delete(request, task_id):
    return HttpResponse(f"Placeholder for task delete view with task_id: {task_id}")

# Placeholder for comment views
def comment_list(request, task_id):
    return HttpResponse(f"Placeholder for comment list view with task_id: {task_id}")

def comment_create(request, task_id):
    return HttpResponse(f"Placeholder for comment create view with task_id: {task_id}")

def comment_update(request, comment_id):
    return HttpResponse(f"Placeholder for comment update view with comment_id: {comment_id}")

def comment_delete(request, comment_id):
    return HttpResponse(f"Placeholder for comment delete view with comment_id: {comment_id}")

# Placeholder for attachment views
def attachment_list(request, task_id):
    return HttpResponse(f"Placeholder for attachment list view with task_id: {task_id}")

def attachment_create(request, task_id):
    return HttpResponse(f"Placeholder for attachment create view with task_id: {task_id}")

def attachment_update(request, attachment_id):
    return HttpResponse(f"Placeholder for attachment update view with attachment_id: {attachment_id}")

def attachment_delete(request, attachment_id):
    return HttpResponse(f"Placeholder for attachment delete view with attachment_id: {attachment_id}")

# Placeholder for label views
def label_list(request):
    return HttpResponse("Placeholder for label list view")

def label_create(request):
    return HttpResponse("Placeholder for label create view")

def label_detail(request, label_id):
    return HttpResponse(f"Placeholder for label detail view with label_id: {label_id}")

def label_update(request, label_id):
    return HttpResponse(f"Placeholder for label update view with label_id: {label_id}")

def label_delete(request, label_id):
    return HttpResponse(f"Placeholder for label delete view with label_id: {label_id}")
