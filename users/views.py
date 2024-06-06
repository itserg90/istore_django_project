from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from users.forms import UserRegisterForm, UserProfileForm, UserLoginForm, UserPasswordResetForm
from users.models import User

from config.settings import EMAIL_HOST_USER

import secrets


class UserLogin(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject="Подтверждение почты",
            message=f"Здравствуйте! Пожалуйста, перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserPasswordReset(TemplateView):

    template_name = 'users/password_reset.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = UserPasswordResetForm()
        context['form'] = form

        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        email = request.POST.get('email')
        context['email'] = email

        password = secrets.token_urlsafe(8)
        message = f'Здравствуйте! Вы запрашивали новый пароль. Ваш новый пароль: {password}'

        user = User.objects.get(email=email)
        user.password = make_password(password)
        user.save()

        send_mail(
            subject="Восстановление пароля",
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return render(request, 'users/password_done.html', context)


class UserPasswordDone(TemplateView):
    template_name = 'users/password_done.html'


# def reset_password(request):
#     form = UserPasswordResetForm()
#     context = {'form': form}
#     if request.method == 'POST':
#         email = request.POST.get('email')
#
#         context = {'email': email}
#         password = secrets.token_urlsafe(8)
#         message = f'Здравствуйте! Вы запрашивали новый пароль. Ваш новый пароль: {password}'
#
#         user = User.objects.get(email=email)
#         user.password = make_password(password)
#         user.save()
#
#         send_mail(
#             subject="Восстановление пароля",
#             message=message,
#             from_email=EMAIL_HOST_USER,
#             recipient_list=[email]
#         )
#         return render(request, 'users/password_done.html', context)
#
#     return render(request, 'users/password_reset.html', context)
