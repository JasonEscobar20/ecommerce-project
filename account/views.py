from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from account.forms import RegistrationForm, UserEditForm, PwdResetForm, PwdResetConfirmForm
from account.token import account_activation_token
from account.models import UserBase


@login_required
def dashboard(request):
    # orders = user_orders(request)
    return render(request,
                  'account/user/dashboard.html',
                  )

@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    
    return render(request, 'account/user/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')

def account_register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)

        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered successfully and activation sent')

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')
    

class PwdResetView(auth_views.PasswordResetView):
    template_name = 'account/user/password_reset_form.html'
    success_url = 'password_reset_email_confirm'
    email_template_name = 'account/user/password_reset_email.html'
    form_class = PwdResetForm


class PwdResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/user/password_reset_confirm.html'
    success_url = '/account/password_reset_complete/'
    form_class = PwdResetConfirmForm


class PwdResetStatusView(TemplateView):
    template_name = 'account/user/reset_password_status.html'


class PwdResetCompleteView(TemplateView):
    template_name = 'account/user/reset_password_status.html'

