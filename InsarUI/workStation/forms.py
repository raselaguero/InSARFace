from django import forms
from django.forms import inlineformset_factory, formset_factory, widgets
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from workStation.models import Study, Evidence, Title
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOMAIN_CHOICES = [
    ('PUBLIC', 'PÚBLICO'),
    ('PRIVATE', 'PRIVADO')
]

FORMAT_CHOICES = [
    ('geojson', 'GEOJSON'),
    ('gml', 'GML'),
    ('kml', 'KML'),
    ('kwt', 'KWT'),
    ('csv', 'CSV'),
    ('shp', 'SHAPEFILE')
]


# class StudyForm(forms.Form):
#     name = forms.CharField(label='Nombre:', max_length=50)
#     description = forms.CharField(label='Descripcion:', widget=forms.Textarea)
#     help = forms.CharField(label='Zona:', max_length=1500)
#     is_public = forms.ChoiceField(choices=DOMAIN_CHOICES)
#     # file = forms.FilePathField(path=os.path.join(BASE_DIR, 'media'))
#     file = forms.FileField()
#     # date_start = forms.CharField(max_length=10)
#     # date_final = forms.CharField(max_length=10)


class StudyForm(forms.ModelForm):
    pass

    class Meta:
        model = Study
        fields = ('name', 'description', 'is_public', 'help', 'file', 'date_start', 'date_final')
        widgets = {
            'date_start': widgets.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'date_final': widgets.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            })
        }


class SignUpForm(UserCreationForm):
    pass

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class ExportForm(forms.Form):
    format = forms.ChoiceField(label='FORMATO', choices=FORMAT_CHOICES)


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ('header',)


class EvidenceForm(forms.ModelForm):
    class Meta:
        model = Evidence
        fields = ('name', 'help', 'image')


EvidenceFormSet = inlineformset_factory(Study, Evidence, fields=('name', 'help', 'image'), extra=3, can_delete=False)


class InputFilesForm(forms.Form):
    master = forms.FileField()
    slave = forms.FileField()
    orbit = forms.FileField()


class InputVariablesForm(forms.Form):
    pass
