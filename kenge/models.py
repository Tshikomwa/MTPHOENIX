from django.db import models
from django.utils import timezone

class Chambre(models.Model):
    NOM_CHAMBRE_CHOICES = [
        ("01 Rose", "01 Rose"),
        ("02 Tulipe", "02 Tulipe"),
        ("03 Orchidée", "03 Orchidée"),
        ("04 Lys", "04 Lys"),
        ("05 Magnolia", "05 Magnolia"),
        ("06 Violette", "06 Violette"),
        ("07 Dahlia", "07 Dahlia"),
        ("08 Pivoine", "08 Pivoine"),
        ("09 Iris", "09 Iris"),
        ("10 Chrysanthème", "10 Chrysanthème"),
        ("11 Jonquille", "11 Jonquille"),
        ("12 Anémone", "12 Anémone"),
        ("13 Bleuet", "13 Bleuet"),
        ("14 Coquelicot", "14 Coquelicot"),
        ("15 Jasmin", "15 Jasmin"),
        ("16 Hibiscus", "16 Hibiscus"),
        ("17 Glycine", "17 Glycine"),
        ("18 Azalée", "18 Azalée"),
        ("19 Camélia", "19 Camélia"),
        ("20 Freesia", "20 Freesia"),
    ]

    nom_de_la_chambre = models.CharField(max_length=50, choices=NOM_CHAMBRE_CHOICES)
    date_enregistrement = models.DateField(default=timezone.now, editable=False)
    date_mise_a_jour = models.DateField(default=timezone.now, editable=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    qrcode = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.code:
            dernier_chambre = Chambre.objects.all().order_by('id').last()
            numero = dernier_chambre.id + 1 if dernier_chambre else 1
            initiales_nom_de_la_chambre = ''.join([c for c in self.nom_de_la_chambre if c.isalnum()])[:4].upper()
            mois = self.date_enregistrement.strftime('%m')
            annee = self.date_enregistrement.strftime('%y')
            self.code = f"{str(numero).zfill(2)}-{initiales_nom_de_la_chambre}-{mois}-{annee}"

        self.date_mise_a_jour = timezone.now()
        super(Chambre, self).save(*args, **kwargs)

    def __str__(self):
        return self.nom_de_la_chambre

##########################################################################################
from django.db import models
from decimal import Decimal

class Reservation(models.Model):
    chambre = models.ForeignKey('Chambre', on_delete=models.CASCADE)
    date = models.DateField()  # Date de début de la réservation
    nombre_de_jours = models.PositiveIntegerField()  # Nombre de jours réservés
    nom_du_client = models.CharField(max_length=255)  # Nom du client
    adresse_client = models.TextField(blank=True, null=True)  # Adresse du client
    telephone_client = models.CharField(max_length=15, blank=True, null=True)  # Téléphone du client
    email_client = models.EmailField(blank=True, null=True)  # Email du client
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2)  # Montant payé
    date_creation = models.DateTimeField(auto_now_add=True)  # Date de création de la réservation

    @property
    def tva(self):
        """
        Calcul de la TVA (16% du montant payé).
        """
        return self.montant_paye * Decimal(0.16)

    @property
    def total_apres_tva(self):
        """
        Calcul du montant total après déduction de la TVA.
        """
        return self.montant_paye - self.tva

    def __str__(self):
        return f"Reservation de {self.nom_du_client} - Chambre {self.chambre.nom_de_la_chambre}"

