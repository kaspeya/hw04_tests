from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path(
        'logout/',
        # Прямо в описании обработчика укажем шаблон,
        # который должен применяться для отображения возвращаемой страницы.
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),

    path(
        'signup/',
        views.SignUp.as_view(template_name='users/signup.html'),
        name='signup'
    ),

    path(
        'login/',
        LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),

    # Смена пароля
    path(
        'password_change/',
        PasswordChangeView.as_view(
            template_name='users/password_change_form.html',
            success_url=reverse_lazy('users:password_change_done')
        ),
        name='password_change'
    ),

    # Сообщение об успешном изменении пароля
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'
        ),
        name='password_change_done'
    ),

    # Восстановление пароля
    path(
        'password_reset/',
        PasswordResetView.as_view(
            template_name='users/password_reset_form.html'
        ),
        name='password_reset'
    ),

    # Сообщение об отправке ссылки для восстановления пароля
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Вход по ссылке для восстановления пароля
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    # Сообщение об успешном восстановлении пароля
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
    path(
        'contact/',
        views.Contact.as_view(template_name='users/contact.html'),
        name='contact'
    ),
    path(
        'thankyou/',
        views.thankyou,
        name='thankyou'
    ),
]
