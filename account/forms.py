from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm

from account.models import UserBase


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3', 
            'placeholder': 'Username', 
            'id': 'login-username'}
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control', 
            'placeholder': 'Password', 
            'id': 'login-pwd'
        }
    ))


class RegistrationForm(forms.ModelForm):
    
    user_name = forms.CharField(
        label='Enter Username',
        min_length=4,
        max_length=50,
        help_text='Required'
    )
    email = forms.EmailField(
        max_length=100,
        help_text='Required',
        error_messages={'required': 'Sorry, you will need an email'}
    )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        user_check = UserBase.objects.filter(user_name=user_name)
        if user_check.count():
            raise forms.ValidationError("Username already exists")
        return user_name
    
    def clean_password_2(self):
        clean_data = self.cleaned_data
        password = clean_data['password']
        password_2 = clean_data['password_2']
        if password != password_2:
            raise forms.ValidationError("Passwords don't match")
        return password_2
    
    def clean_email(self):
        email = self.cleaned_data['email']
        email_exists = UserBase.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError(
                'Please use another email, that is already taken'
            )
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'}
        )
        self.fields['password_2'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Repeat Password'}
        )

    
class UserEditForm(forms.ModelForm):
    
    email = forms.EmailField(
        label='Account email (cannot be changed)',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'email',
                'id': 'form-email',
                'readonly': 'readonly' 
            }
        )
    )

    first_name = forms.CharField(
        label='Username',
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3', 
                'placeholder': 'Firstname', 
                'id': 'form-lastname'
            }
        )
    )

    class Meta:
        model = UserBase
        fields = ('email', 'first_name',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True


class PwdResetForm(PasswordResetForm):
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Email',
                'id': 'form-email'
            }
        )
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserBase.objects.filter(email=email)

        if not user:
            raise forms.ValidationError('Unfortunately we can not find that email adress')
        
        return email
    

class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'New Password',
                'id': 'form_new_password'
            }
        )
    )

    new_password2 = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'New Password',
                'id': 'form_repeat_new_password'
            }
        )
    )