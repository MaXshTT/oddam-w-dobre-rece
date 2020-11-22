from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from charitydonation_app.models import Donation

from .forms import LoginForm, ProfileForm, RegisterForm
from .models import User
from .tokens import account_activation_token


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            if not User.objects.filter(email=email).exists():
                messages.error(request, 'Nie możemy znaleźć takiego maila')
                return render(request, 'accounts/login.html', {'form': form})
            else:
                if not User.objects.filter(email=email, is_active=True).exists():
                    messages.error(
                        request, 'Twoje konto nie zostalo jeszcze aktywowane')
                    return render(request, 'accounts/login.html', {'form': form})
                else:
                    user = authenticate(
                        request, email=email, password=password)
                    if not user:
                        messages.error(request, 'Podano błędne hasło')
                        return render(request, 'accounts/login.html', {'form': form})
                    else:
                        login(request, user)
                        if request.GET.get('next'):
                            return redirect(request.GET['next'])
                        return redirect('index')
        return render(request, 'accounts/login.html', {'form': form})


class RegisterView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Aktywacja konta.'
            message = render_to_string('accounts/email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(
                request, 'Potwierdź swój adres e-mail, aby zakończyć rejestrację.')
            form = RegisterForm()
            return render(request, 'accounts/register.html', {'form': form})
        return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    context = {}
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        context['message'] = ('Dziękujemy za potwierdzenie adresu email.'
                              '\nTeraz możesz zalogować się na swoje konto.')
        return render(request, 'accounts/blank_page.html', context)
    else:
        context['message'] = 'Link aktywacyjny jest nieprawidłowy!'
        return render(request, 'accounts/blank_page.html', context)


class SettingsView(LoginRequiredMixin, View):

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'accounts/settings.html', {'form': form})

    def post(self, request):
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zapisano zmianę pomyślnie!')
            return render(request, 'accounts/settings.html', {'form': form})
        else:
            return render(request, 'accounts/settings.html', {'form': form})


class ChangePasswordView(LoginRequiredMixin, View):

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Udało się zmienić hasło')
            form = PasswordChangeForm()
            return render(request, 'accounts/change_password.html', {'form': form})
        else:
            return render(request, 'accounts/change_password.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        donations = Donation.objects.filter(
            user=request.user, is_taken=False).order_by('pick_up_date', 'pick_up_time')
        donations_taken = Donation.objects.filter(
            user=request.user, is_taken=True).order_by('pick_up_date', 'pick_up_time')
        return render(request, 'accounts/profile.html',
                      {'donations': donations, 'donations_taken': donations_taken})

    def post(self, request):
        donation = Donation.objects.get(id=request.POST.get('donation'))
        donation.is_taken = True
        donation.save()
        donations = Donation.objects.filter(
            user=request.user, is_taken=False).order_by('pick_up_date', 'pick_up_time')
        donations_taken = Donation.objects.filter(
            user=request.user, is_taken=True).order_by('pick_up_date', 'pick_up_time')
        return render(request, 'accounts/profile.html',
                      {'donations': donations, 'donations_taken': donations_taken})
