from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms

#importing default django user model
from django.contrib.auth.models import User



class Signup_form(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(Signup_form, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model =User
        fields = ['username' , 'email' , 'password1' , 'password2']