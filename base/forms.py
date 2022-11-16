from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from .models import Submission, User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'bio']

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        
        fields = ['details']

class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']