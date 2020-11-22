from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import User

from .forms import DonationForm
from .models import Category, Donation, Institution


class ViewTests(TestCase):

    def test_index(self):
        response = self.client.get(reverse('index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'charitydonation_app/index.html')

    def test_add_donation_not_logged_in(self):
        response = self.client.get(reverse('add_donation'))

        self.assertRedirects(
            response, f'{reverse("login")}?next={reverse("add_donation")}')

    def test_add_donation_logged_in(self):
        self.client.force_login(
            User.objects.get_or_create(email='a-user@user.com')[0])
        response = self.client.get(reverse('add_donation'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'charitydonation_app/add_donation.html')

    def test_form_confirmation(self):
        response = self.client.get(reverse('form_confirmation'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'charitydonation_app/form_confirmation.html')

    def test_contact(self):
        response = self.client.get(reverse('contact'))

        self.assertRedirects(response, reverse('index'))


class DonationFormTests(TestCase):

    def setUp(self):
        self.category1 = Category.objects.create(name='category1')
        self.institution1 = Institution.objects.create(
            name='institution1',
            description='text',
            kind=0
        )
        self.institution1.categories.add(self.category1)
        self.form_data = {
            'quantity': 50,
            'categories': (self.category1,),
            'institution': self.institution1,
            'address': 'Polna',
            'phone_number': '123123123',
            'city': 'Warszawa',
            'zip_code': '01-234',
            'pick_up_date': '2020-07-16',
            'pick_up_time': '12:00:00',
        }

    def test_valid_data(self):
        form = DonationForm(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_no_data(self):
        form = DonationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 9)

    def test_invalid_phone_number(self):
        self.form_data['phone_number'] = '0123'
        form = DonationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEqual(form.errors['phone_number'][0],
                         'Numer telefonu jest nieprawidłowy.')

    def test_invalid_zip_code(self):
        self.form_data['zip_code'] = '0123'
        form = DonationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
        self.assertEqual(form.errors['zip_code'][0],
                         'Kod pocztowy jest nieprawidłowy.')
