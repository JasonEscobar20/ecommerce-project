from django import forms

from account.models import UserBase


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