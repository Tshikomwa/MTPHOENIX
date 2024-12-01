from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Nom d\'utilisateur', max_length=150)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)


###########################################################################################################

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur")
    email = forms.EmailField(label="Adresse e-mail")  # Ajout du champ email
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmez le mot de passe")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']  # Ajout de password_confirm ici

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Un compte avec cet email existe déjà.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 6 caractères.")
        if not re.search(r'[A-Z]{4,}', password):
            raise ValidationError("Le mot de passe doit contenir au moins 3 lettres majuscules.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")
        if not re.search(r'\d', password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")
        if not re.search(r'[^a-zA-Z0-9]', password):
            raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
#################################################################################################
from django import forms

# Autre exemple : formulaire de contact
class ContactForm(forms.Form):
    name = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre nom'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre email'
        })
    )
    subject = forms.CharField(
        label="Sujet",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le sujet'
        })
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Entrez votre message'
        })
    )
########################################################################################################
from django import forms
from .models import Chambre

class ChambreForm(forms.ModelForm):
    class Meta:
        model = Chambre
        # Inclure uniquement les champs modifiables
        fields = ['nom_de_la_chambre', 'photo']

#######################################################################################################
from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'chambre',
            'date',
            'nombre_de_jours',
            'nom_du_client',
            'adresse_client',
            'telephone_client',
            'email_client',
            'montant_paye',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'nombre_de_jours': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'nom_du_client': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse_client': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telephone_client': forms.TextInput(attrs={'class': 'form-control'}),
            'email_client': forms.EmailInput(attrs={'class': 'form-control'}),
            'montant_paye': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'chambre': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_montant_paye(self):
        montant_paye = self.cleaned_data.get('montant_paye')
        if montant_paye is not None and montant_paye <= 0:
            raise forms.ValidationError("Le montant payé doit être supérieur à zéro.")
        return montant_paye
    
    def clean_telephone_client(self):
        telephone_client = self.cleaned_data.get('telephone_client')
        
        if telephone_client:
            # Vérifie si le numéro commence par un "+" suivi de chiffres
            if not telephone_client.startswith('+') or not telephone_client[1:].isdigit():
                raise forms.ValidationError(
                    "Le numéro de téléphone doit commencer par un '+' suivi de chiffres uniquement (ex : +243123456789)."
                )
            # Vérifie la longueur minimale pour un numéro valide (par exemple, au moins 10 caractères après '+')
            if len(telephone_client) < 10:
                raise forms.ValidationError(
                    "Le numéro de téléphone est trop court. Veuillez entrer un numéro valide."
                )

        return telephone_client






