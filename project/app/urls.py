# taskmanager/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'app'

urlpatterns = [
    path('register/', views.register, name='register'),  # URL for user registration
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),
    # Team URLs
    # Team URLs
    path('teams/', views.team_list, name='team-list'),
    path('teams/create/', views.team_create, name='team-create'),
    path('teams/<int:team_id>/', views.team_detail, name='team-detail'),
    path('teams/<int:team_id>/update/', views.team_update, name='team-update'),
    path('teams/<int:team_id>/delete/', views.team_delete, name='team-delete'),

    # Task URLs
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/create/', views.task_create, name='task-create'),
    path('tasks/<int:task_id>/', views.task_detail, name='task-detail'),
    path('tasks/<int:task_id>/update/', views.task_update, name='task-update'),
    path('tasks/<int:task_id>/delete/', views.task_delete, name='task-delete'),

    # Comment URLs
    path('tasks/<int:task_id>/comments/', views.comment_list, name='comment-list'),
    path('tasks/<int:task_id>/comments/create/', views.comment_create, name='comment-create'),
    path('comments/<int:comment_id>/update/', views.comment_update, name='comment-update'),
    path('comments/<int:comment_id>/delete/', views.comment_delete, name='comment-delete'),

    # Attachment URLs
    path('tasks/<int:task_id>/attachments/', views.attachment_list, name='attachment-list'),
    path('tasks/<int:task_id>/attachments/create/', views.attachment_create, name='attachment-create'),
    path('attachments/<int:attachment_id>/update/', views.attachment_update, name='attachment-update'),
    path('attachments/<int:attachment_id>/delete/', views.attachment_delete, name='attachment-delete'),

    # Label URLs
    path('labels/', views.label_list, name='label-list'),
    path('labels/create/', views.label_create, name='label-create'),
    path('labels/<int:label_id>/', views.label_detail, name='label-detail'),
    path('labels/<int:label_id>/update/', views.label_update, name='label-update'),
    path('labels/<int:label_id>/delete/', views.label_delete, name='label-delete'),
]
