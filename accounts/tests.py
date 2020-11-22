from django.contrib.messages import get_messages
from django.http import HttpRequest
from django.test import Client, TestCase
from django.urls import reverse

from .forms import RegisterForm
from .models import User
from .validators import NumberValidator


class ViewTests(TestCase):

    def setUp(self):
        self.credentials = {'email': 'a-user@user.com', 'password': 'password'}
        self.user = User.objects.create_user(**self.credentials)

    def log_in(self):
        client = Client()
        client.login(**self.credentials)
        return client

    def test_login(self):
        response = self.client.get(reverse('login'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_redirect(self):
        response = self.client.post(reverse('login'), self.credentials)

        self.assertRedirects(response, reverse('index'))

    def test_register(self):
        response = self.client.get(reverse('register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_successful_message(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'b-user',
            'last_name': 'user',
            'email': 'b-user@user.com',
            'password1': '1b-Password',
            'password2': '1b-Password',
        })
        expected_message = 'Potwierdź swój adres e-mail, aby zakończyć rejestrację.'
        messages = list(response.context['messages'])

        self.assertEqual(str(messages[0]), expected_message)

    def test_profile(self):
        client = self.log_in()
        response = client.get(reverse('profile'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_settings(self):
        client = self.log_in()
        response = client.get(reverse('settings'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/settings.html')

    def test_change_password(self):
        client = self.log_in()
        response = client.get(reverse('change_password'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_password.html')


class RegisterFormTests(TestCase):

    def setUp(self):
        self.form_data = {
            'first_name': 'abc',
            'last_name': 'xyz',
            'email': 'a-user@user.com',
        }

    def test_valid_password(self):
        self.form_data['password1'] = '9bmnHwert'
        self.form_data['password2'] = '9bmnHwert'
        form = RegisterForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_password_no_number(self):
        self.form_data['password1'] = 'bmnHwert'
        self.form_data['password2'] = 'bmnHwert'
        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEqual(form.errors['password2'][0],
                         'Twoje hasło musi zawierać co najmniej 1 cyfrę, 0–9.')

    def test_invalid_password_no_uppercase(self):
        self.form_data['password1'] = '9bmnhwert'
        self.form_data['password2'] = '9bmnhwert'
        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEqual(form.errors['password2'][0],
                         'Twoje hasło musi zawierać co najmniej 1 wielką literę A-Z.')

    def test_invalid_password_no_lowercase(self):
        self.form_data['password1'] = '9BMNHWERT'
        self.form_data['password2'] = '9BMNHWERT'
        form = RegisterForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEqual(form.errors['password2'][0],
                         'Twoje hasło musi zawierać co najmniej 1 małą literę, a-z.')
