from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from accounts.models import User

from .forms import ContactForm, DonationForm
from .models import Category, Donation, Institution
from .serializers import InstitutionSerializer


class LandingPageView(View):

    def get(self, request):
        context = {}
        quantity = 0

        # Sum of all bags
        for donation in Donation.objects.values_list('quantity', flat=True):
            quantity += donation
        context['quantity'] = quantity
        context['institutions'] = Institution.objects.all()

        # Pagination for institutions
        foundations = Institution.objects.filter(kind=0)
        organizations = Institution.objects.filter(kind=1)
        local_collections = Institution.objects.filter(kind=2)

        paginator_foundations = Paginator(foundations, 5)
        first_page_foundations = paginator_foundations.page(1).object_list
        page_range_foundations = paginator_foundations.page_range
        sum_page_range_foundations = sum(page_range_foundations)

        paginator_organizations = Paginator(organizations, 5)
        first_page_organizations = paginator_organizations.page(1).object_list
        page_range_organizations = paginator_organizations.page_range
        sum_page_range_organizations = sum(page_range_organizations)

        paginator_local_collections = Paginator(local_collections, 5)
        first_page_local_collections = paginator_local_collections.page(
            1).object_list
        page_range_local_collections = paginator_local_collections.page_range
        sum_page_range_local_collections = sum(page_range_local_collections)

        context['first_page_foundations'] = first_page_foundations
        context['page_range_foundations'] = page_range_foundations
        context['sum_page_range_foundations'] = sum_page_range_foundations

        context['first_page_organizations'] = first_page_organizations
        context['page_range_organizations'] = page_range_organizations
        context['sum_page_range_organizations'] = sum_page_range_organizations

        context['first_page_local_collections'] = first_page_local_collections
        context['page_range_local_collections'] = page_range_local_collections
        context['sum_page_range_local_collections'] = sum_page_range_local_collections

        return render(request, 'charitydonation_app/index.html', context)

    def post(self, request):
        context = {}
        kind = request.POST.get('kind')
        institutions = Institution.objects.filter(kind=kind)
        paginator = Paginator(institutions, 5)
        page_number = request.POST.get('page')
        serializer = InstitutionSerializer(
            paginator.page(page_number).object_list, many=True)
        return JsonResponse(serializer.data, safe=False)


class AddDonationView(LoginRequiredMixin, View):

    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'charitydonation_app/add_donation.html', {'categories': categories})

    def post(self, request):
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            donation.categories.set(request.POST.getlist('categories'))
            return JsonResponse({'success': 'Success'})
        else:
            response = JsonResponse(form.errors.get_json_data())
            response.status_code = 422
            return response


class ConfirmationView(View):

    def post(self, request):
        return redirect('index')

    def get(self, request):
        return render(request, 'charitydonation_app/form_confirmation.html')


class InstitutionsList(View):

    def get(self, request):
        cat_ids = request.GET.getlist('category')
        if not cat_ids:
            return HttpResponse(status=204)
        institutions = Institution.objects.filter(categories=cat_ids[0])
        for cat_id in cat_ids[1:]:
            institutions = institutions.filter(categories=cat_id)
        serializer = InstitutionSerializer(institutions, many=True)
        return JsonResponse(serializer.data, safe=False)


class ContactView(View):

    def get(self, request):
        return redirect('index')

    def post(self, request):
        form = ContactForm(request.POST)
        context = {}
        if form.is_valid():
            mail_subject = 'Formularz kontaktowy'
            message = f'{request.POST.get("message")}\n{request.POST.get("email")}'
            superusers_emails = list(User.objects.filter(
                is_superuser=True).values_list('email', flat=True))
            to_email = 1
            email = EmailMessage(
                mail_subject, message, to=[superusers_emails]
            )
            email.send()
            context['message'] = ('Sukces!\nDziękujemy za twoją wiadomość.'
                                  '\nSpróbujemy skontaktować się z tobą jak najszybciej!')
            return render(request, 'charitydonation_app/blank_page.html', context)
        return render(request, 'charitydonation_app/contact_error.html')
