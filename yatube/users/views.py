from django.core.mail import send_mail
from django.shortcuts import redirect, render
# Функция reverse_lazy позволяет получить URL по параметрам функции path()
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import ContactForm, CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class Contact(CreateView):
    form_class = ContactForm
    success_url = reverse_lazy('users:thankyou')
    template_name = 'users/contact.html'


def send_msg(email, name, title, body):
    subject = f"Письмо от {name}"
    body = f"""Cообщение администратору

    Имя: {name}
    Тема: {title}
    Cообщение: {body}

    """
    send_mail(
        subject, body, email, ["kaspeya@yandex,com"],
    )


def user_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']
            send_msg(name, email, title, body)
            print('123')
            return redirect('users:thankyou')
        return render(request, 'contact.html', {'form': form})
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def thankyou(request):
    template = 'users/thankyou.html'
    return render(request, template)
