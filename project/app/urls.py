# taskmanager/urls.py

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .views import logout


app_name = 'app'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),  # URL for user registration
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('app:login')), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Team URLs
    path('teams/', views.team_list, name='team_list'),
    path('teams/create/', views.team_create, name='team_create'),
    path('teams/<int:team_id>/', views.team_detail, name='team_detail'),
    path('teams/<int:team_id>/update/', views.team_update, name='team_update'),
    path('teams/<int:team_id>/delete/', views.team_delete, name='team_delete'),

    # Task URLs
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/update/', views.task_update, name='task_update'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task_delete'),

    # Comment URLs
    path('tasks/<int:task_id>/comments/', views.comment_list, name='comment_list'),
    path('tasks/<int:task_id>/comments/create/', views.comment_create, name='comment_create'),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', views.comment_detail, name='comment_detail'),
    path('comments/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    # Attachment URLs
    path('tasks/<int:task_id>/attachments/', views.attachment_list, name='attachment_list'),
    path('tasks/<int:task_id>/attachments/create/', views.attachment_create, name='attachment_create'),
    path('attachments/<int:attachment_id>/update/', views.attachment_update, name='attachment_update'),
    path('attachments/<int:attachment_id>/delete/', views.attachment_delete, name='attachment_delete'),

    path('get_task_events/', views.get_task_events, name='get_task_events'),
    path('get_kanban_tasks/', views.get_kanban_tasks, name='get_kanban_tasks'),

]