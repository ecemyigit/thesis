from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task, Team, Comment, Attachment, Label

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'uniform-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'uniform-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'uniform-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'uniform-input'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'status', 'team', 'assignee']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'members']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file_name', 'file_type', 'content']

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name', 'color']