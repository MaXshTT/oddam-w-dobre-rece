from django.urls import path

from . import views

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='index'),
    path('add-donation/', views.AddDonationView.as_view(), name='add_donation'),
    path('form-confirmation/', views.ConfirmationView.as_view(),
         name='form_confirmation'),
    path('institutions/', views.InstitutionsList.as_view(), name='institutions'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
