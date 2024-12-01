from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),               # Page d'accueil
    path('about/', views.about, name='about'),         # À propos
    path('blog/', views.blog, name='blog'),            # Blog
    path('s_h/', views.s_h, name='s_h'),  # Service d'hôtellerie
    path('contact/', views.contact, name='contact'),   # Contact
    path('reservation/', views.reservation, name='reservation'),  # Portfolio
    path('services/', views.services, name='services'),  # Services
    path('testimonials/', views.testimonials, name='testimonials'),
    path('blog_list/', views.blog_list, name='blog_list'),
    path('career/', views.career, name='career'),
    path('resources/', views.resources, name='resources'),
    path('news_feed/', views.news_feed, name='news_feed'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('acces/', views.acces, name='acces'),
    path('contact/', views.contact, name='contact'),
    ######################################################################
    path('liste/', views.liste, name='liste'),
    path('ajouter/', views.ajouter, name='ajouter'),
    ######################################################################
    path('reservation/formulaire/<int:chambre_id>/', views.reservation_form, name='reservation_form'),
    path('mettre_a_jour/<int:chambre_id>/', views.mettre_a_jour, name='mettre_a_jour'),
    path('supprimer/<int:chambre_id>/', views.supprimer, name='supprimer'),
    ######################################################################
    path('reservation/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('reservation/<int:reservation_id>/modifier/', views.reservation_update, name='reservation_update'),
    path('reservation/<int:reservation_id>/supprimer/', views.reservation_delete, name='reservation_delete'),
    #######################################################################
    path('reservations_par_date/', views.reservations_par_date, name='reservations_par_date'),
    path('reservation/<int:reservation_id>/pdf/',views.generate_pdf, name='generate_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
