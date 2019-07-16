### forms contains the details of all forms that we will import
## while rendering our web page
# django forms are cleaned for sql injections and passwords are hashed


from django.contrib.auth.models import User
from django import forms

from .models import Candidate


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','email','password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('photo',)

        
class ResumeUpdate(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('resume',)


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', )


class CvForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['resume']