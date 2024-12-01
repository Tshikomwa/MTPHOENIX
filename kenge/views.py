from django.shortcuts import render

# Views pour chaque page HTML
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def s_h(request):
    return render(request, 's_h.html')

def blog_list(request):
    return render(request, 'blog-list.html')

def contact(request):
    return render(request, 'contact.html')

from django.http import HttpResponse
from django.shortcuts import render

def contact_submit(request):
    if request.method == "POST":
        # Traitez les données du formulaire ici
        return HttpResponse("Formulaire envoyé avec succès !")
    return HttpResponse("Méthode non autorisée.")


def reservation(request):
    return render(request, 'reservation.html')

def services(request):
    return render(request, 'services.html')

def testimonials(request):
    return render(request, 'services.html')

def career(request):
    return render(request, 'services.html')

def resources(request):
    return render(request, 'services.html')

def news_feed(request):
    return render(request, 'services.html')


###################################################################################################
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm  # Assurez-vous d'avoir importé votre formulaire personnalisé

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # Correction ici
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('acces')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        else:
            messages.error(request, "Formulaire invalide. Veuillez vérifier les champs.")
    else:
        form = LoginForm()  # Formulaire vide pour GET request

    return render(request, 'login.html', {'form': form})

#########################################################################################################

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm  # Assurez-vous que le chemin d'importation est correct

# Vue pour l'enregistrement d'un nouvel utilisateur
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Si tout est bon, enregistrez l'utilisateur
            form.save()
            messages.success(request, "Inscription réussie !")
            return redirect('login')  # Redirige vers la page de connexion
        else:
            # Afficher les erreurs de validation
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})

######################################################################################

def acces(request):
    return render(request, 'acces.html')

######################################################################################
# Vue pour le contact
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm  # Assurez-vous que ce formulaire est défini dans forms.py

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extraire les données du formulaire
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Préparer le contenu de l'email
            email_message = f"""
            Nouveau message de contact :

            Nom : {name}
            Email : {email}
            Sujet : {subject}
            Message :
            {message}
            """

            # Envoyer l'email
            send_mail(
                subject=f"[Contact Form] {subject}",  # Sujet de l'email
                message=email_message,              # Contenu de l'email
                from_email='lightmutanda@gmail.com', # Expéditeur (votre email configuré dans settings)
                recipient_list=['lightmutanda@gmail.com'],  # Destinataire (votre email)
                fail_silently=False,               # Déclenche une erreur si l'envoi échoue
            )

            # Message de succès stylisé
            html_content = """
            <html>
                <head>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }
                        .message-box {
                            text-align: center;
                            padding: 30px;
                            background-color: #4CAF50;
                            color: white;
                            border-radius: 10px;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                            font-size: 20px;
                            max-width: 600px;
                            width: 100%;
                        }
                        h1 {
                            margin: 0;
                            font-size: 24px;
                        }
                        p {
                            font-size: 18px;
                        }
                    </style>
                </head>
                <body>
                    <div class="message-box">
                        <h1>Merci de nous avoir contactés !</h1>
                        <p>Votre message a été envoyé avec succès.</p>
                    </div>
                </body>
            </html>
            """
            return HttpResponse(html_content)

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

###################################################################################################
from django.shortcuts import render, redirect
from .forms import ChambreForm
from .models import Chambre
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def ajouter(request):
    if request.method == "POST":
        form = ChambreForm(request.POST, request.FILES)
        if form.is_valid():
            chambre = form.save(commit=False)
            
            # Générer le code avant de créer le QR Code
            if not chambre.code:  # Si le code n'est pas encore généré
                dernier_chambre = Chambre.objects.all().order_by('id').last()
                numero = dernier_chambre.id + 1 if dernier_chambre else 1
                initiales_nom_de_la_chambre = ''.join([c for c in chambre.nom_de_la_chambre if c.isalnum()])[:4].upper()
                mois = chambre.date_enregistrement.strftime('%m')
                annee = chambre.date_enregistrement.strftime('%y')
                chambre.code = f"{str(numero).zfill(2)}-{initiales_nom_de_la_chambre}-{mois}-{annee}"

            # Maintenant, générer le QR Code avec le code et autres infos
            qr_data = f"""
            Nom de la chambre: {chambre.nom_de_la_chambre}
            Code: {chambre.code}
            Enregistrée le: {chambre.date_enregistrement}
            """

            # Génération du QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            # Sauvegarder l'image du QR Code
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            chambre.qrcode.save(f"qrcode_{chambre.nom_de_la_chambre}.png", ContentFile(buffer.read()), save=False)

            # Enregistrer la chambre avec le code généré et le QR Code
            chambre.save()

            return redirect("liste")  # Rediriger vers la liste des chambres après l'enregistrement
    else:
        form = ChambreForm()

    return render(request, "ajouter.html", {"form": form})
###################################################################################################

def liste(request):
    # Récupérer toutes les chambres
    chambres = Chambre.objects.all()
    return render(request, 'liste.html', {'chambres': chambres})

####################################################################################################
from django.shortcuts import render, get_object_or_404, redirect
from .models import Chambre, Reservation
from .forms import ReservationForm

def reservation_form(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.chambre = chambre  # Associez la réservation à la chambre
            reservation.save()
            return redirect('reservation_detail', reservation_id=reservation.id)  # Redirigez après l'enregistrement
    else:
        form = ReservationForm()

    context = {
        'form': form,
        'chambre': chambre,  # Passez l'objet chambre au contexte
    }
    return render(request, 'reservation_form.html', context)



####################################################################################################
from django.shortcuts import get_object_or_404

def mettre_a_jour(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    if request.method == "POST":
        form = ChambreForm(request.POST, request.FILES, instance=chambre)
        if form.is_valid():
            form.save()
            return redirect('liste')
    else:
        form = ChambreForm(instance=chambre)
    return render(request, 'mettre_a_jour.html', {'form': form, 'chambre': chambre})
###############################################################################################

def supprimer(request, chambre_id):
    chambre = get_object_or_404(Chambre, id=chambre_id)
    if request.method == "POST":
        chambre.delete()
        return redirect('liste')
    return render(request, 'confirmer_suppression.html', {'chambre': chambre})


#################################################################################################
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Reservation
from .forms import ReservationForm  # Assurez-vous d'avoir un formulaire pour la réservation

def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservation_detail.html', {'reservation': reservation})

#################################################################################################

def reservation_update(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservation_detail', reservation_id=reservation.id)
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservation_form.html', {'form': form})

###################################################################################################

def reservation_delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservation_list')  # Redirigez vers la liste des réservations
    return render(request, 'reservation_confirm_delete.html', {'reservation': reservation})



###################################################################################################
from django.shortcuts import render
from .models import Reservation
from collections import defaultdict
from datetime import timedelta

def reservations_par_date(request):
    reservations = Reservation.objects.all().order_by('date')
    grouped_reservations = defaultdict(list)

    # Grouper les réservations par date
    for reservation in reservations:
        grouped_reservations[reservation.date].append(reservation)

    # Ajouter les totaux et les dates de sortie
    grouped_with_lengths = {}
    for date, reservations_list in grouped_reservations.items():
        reservations_with_index = [
            {
                'index': i,
                'reservation': reservation,
                'date_sortie': reservation.date + timedelta(days=reservation.nombre_de_jours),
            }
            for i, reservation in enumerate(reservations_list)
        ]
        grouped_with_lengths[date] = {
            'reservations': reservations_with_index,
            'rowspan': len(reservations_with_index) + 1,  # Inclure la ligne pour le total
            'total': sum(reservation.montant_paye for reservation in reservations_list),
        }

    return render(request, 'reservations_par_date.html', {
        'grouped_with_lengths': grouped_with_lengths,
    })


####################################################################################################
import random
import string
from io import BytesIO
from datetime import timedelta
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from django.shortcuts import get_object_or_404
from .models import Reservation
from decimal import Decimal

# Fonction pour générer une lettre aléatoire
def generate_random_letter():
    return random.choice(string.ascii_uppercase)

# Fonction pour générer un numéro de facture incrémental
def get_next_invoice_number():
    # Logique simplifiée : remplacer par un champ dans la base de données pour un environnement de production
    # Exemple : chercher le dernier numéro de facture dans la base de données
    from django.core.cache import cache
    last_number = cache.get('last_invoice_number', 0)
    next_number = last_number + 1
    cache.set('last_invoice_number', next_number)
    return f"{next_number:04d}"  # Formatage en 4 chiffres (ex. 0001, 0002)

def generate_pdf(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Calcul de la date de sortie prévue
    date_sortie_prevue = reservation.date + timedelta(days=reservation.nombre_de_jours)

    # Générer un numéro de facture unique
    invoice_number = get_next_invoice_number()
    random_letter = generate_random_letter()
    facture_numero = f"MTP-{invoice_number}-{random_letter}"

    # TVA en pourcentage
    tva_percentage = Decimal('0.16')  # TVA de 16%

    # Calcul du montant HT (hors taxes)
    montant_ttc = Decimal(reservation.montant_paye)
    montant_ht = montant_ttc / (1 + tva_percentage)

    # Calcul du montant de la TVA
    tva_amount = montant_ttc - montant_ht

    # Création du PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # En-têtes de la facture
    headers = [
        ("REPUBLIQUE DEMOCRATIQUE DU CONGO", 16, (0, 0, 0)),
        ("PROVINCE DU LUALABA", 14, (1, 0, 0)),
        ("HOTEL, RESTAURANT & SALLE DE FÊTES", 17, (0, 0, 1)),
        ("MUSOLE TSHINYAMA PHOENIX", 24, (0, 0, 0)),
        ("-----------------------------------------------------------------------------", 16, (0, 0, 0)),
        ("FACTURE", 20, (0, 0, 0)),
        ("Adresse : Avenue Principale, Ville de Kolwezi, RDC", 12, (0, 0, 1)),
        ("Téléphone : +243 99 44 73 711 | Email : contact@mtphoenix.com", 12, (0, 0, 1)),
    ]

    y_position = 750
    for text, font_size, color in headers:
        c.setFont("Times-Bold", font_size)
        c.setFillColorRGB(*color)
        text_width = c.stringWidth(text)
        c.drawString((width - text_width) / 2, y_position, text)
        y_position -= 20

    # Ajouter un espace avant les informations supplémentaires
    y_position -= 20

    # Informations sur le client, la facturation et le numéro de facture
    c.setFont("Times-Bold", 14)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, y_position, f"Client(e) : {reservation.nom_du_client}")
    y_position -= 25
    c.drawString(50, y_position, f"Adresse : {reservation.adresse_client}")
    y_position -= 25
    c.drawString(50, y_position, f"Téléphone : {reservation.telephone_client}")
    y_position -= 25
    c.drawString(50, y_position, f"E-mail : {reservation.email_client}")
    y_position -= 25
    c.drawString(50, y_position, f"Date de la facturation : {reservation.date.strftime('%d-%m-%Y')}")
    y_position -= 25
    c.drawString(50, y_position, f"Numéro de Facture : {facture_numero}")

    # Ajouter un espace avant le tableau
    y_position -= 20

    # Données pour le tableau
    data = [
        ["Désignation", "Nombre de jours", "Prix (USD)"],  # En-tête des colonnes
        [reservation.chambre.nom_de_la_chambre, str(reservation.nombre_de_jours), f"{montant_ttc:.2f}"],
    ]

    # Largeur des colonnes
    col_widths = [width * 0.4, width * 0.2, width * 0.3]
    total_table_width = sum(col_widths)

    # Centrer le tableau
    x_position = (width - total_table_width) / 2

    # Styles du tableau
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([ 
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Aligner toutes les colonnes au centre
        ('FONTNAME', (0, 0), (-1, -1), 'Times-Bold'),  # Police Times en gras
        ('FONTSIZE', (0, 0), (-1, -1), 14),  # Taille de la police agrandie
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espacement en bas des cellules
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordure noire pour le tableau
    ]))


    # Dessiner le tableau
    table.wrapOn(c, width, height)
    table_height = 40 + len(data) * 20
    table.drawOn(c, x_position, y_position - table_height)

    # Ajouter les détails de la TVA et le total
    y_position = y_position - table_height - 40
    c.setFont("Times-Bold", 14)
    c.setFillColorRGB(0, 0, 0)

    # Affichage du montant HT, TVA et montant total TTC
    c.drawString(320, y_position, f"Montant HT :                {montant_ht:.2f} USD")
    y_position -= 25
    c.drawString(320, y_position, f"TVA ({tva_percentage * 100:.0f} %) :                {tva_amount:.2f} USD")
    y_position -= 25
    c.drawString(320, y_position, f"Montant Total TTC :   {montant_ttc:.2f} USD")


    # Ajouter la date de sortie en bas en rouge
    footer_y_position = y_position - 50
    c.setFont("Times-Bold", 14)
    c.setFillColorRGB(1, 0, 0)  # Rouge pour la date de sortie
    c.drawString(50, footer_y_position, f"Echéance : {date_sortie_prevue.strftime('%d-%m-%Y')}")

    # Finaliser le PDF
    c.showPage()
    c.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')



######################################################################################
######################################################################################
######################################################################################
######################################################################################




