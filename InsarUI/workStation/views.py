from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from workStation.models import Study, Investigator, ConsejoPopular, Evidence, Title, Displacement
from workStation.forms import InputFilesForm, InputVariablesForm, SignUpForm, StudyForm, EvidenceForm, \
    EvidenceFormSet, TitleForm, ExportForm
from django.utils import timezone
# GEODJANGO
from django.contrib.gis.geos import GEOSGeometry, Point, Polygon, MultiPolygon
from django.contrib.gis.db.models.functions import Length, AsGeoJSON, AsKML, AsGML, AsWKT
from django.core.serializers import serialize

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors, pagesizes
from reportlab.platypus import Paragraph, SimpleDocTemplate, Image, Spacer, Table, TableStyle
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib.units import inch
# ISCE
from shutil import copyfile, move
from osgeo import gdal
from pathlib import Path
from django.core.files import File
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import io
import json
import csv
import cv2
import shutil
import datetime
import pytz
import time
# import matplotlib.pyplot as plt
import numpy as np


# Create your views here.
# global variables
home_dir = os.path.join(os.getenv("HOME"), "work")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTSIDE_DIR = os.path.abspath(__file__)


def register(request):  # todo: ok
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('investigator-add')
    else:
        form = UserCreationForm()
    return render(request, 'sign-up.html', {'form': form})


# class SignUpView(CreateView):
#     model = User
#     form_class = SignUpForm
#     template_name = 'sign-up.html'
#
#     def form_valid(self, form):
#         form.save()
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         login(self.request, user)
#         return redirect('/')
    # return render(request, 'sign-up.html')


class UsersView(LoginRequiredMixin, ListView):  # todo: ok
    model = User
    context_object_name = 'users'
    template_name = 'users.html'


@login_required
def add_user(request):  # todo: ok
    if not request.user.is_superuser:
        raise PermissionDenied
    else:
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])  # , email=form1.cleaned_data['correo']
                user.save()
                return redirect('user-create')
    return render(request, 'create-user.html', {'form': form})


@login_required
def update_user(request, pk):  # todo: ok
    if not request.user.is_superuser:
        raise PermissionDenied
    else:
        usuario = get_object_or_404(User, id=pk)
        form = SignUpForm(instance=usuario)
        if request.method == "POST":
            form = SignUpForm(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('users')
    return render(request, 'update-user.html', {'form': form})


@login_required
def delete_user(request, pk):  # todo: ok
    if not request.user.is_superuser:
        raise PermissionDenied
    else:
        usuario_temp = User.objects.get(id=pk).delete()
    return redirect('users')


@login_required
def active_deactivate_user(request, pk):  # todo: en implementacion
    if not request.user.is_superuser:
        raise PermissionDenied
    else:
        usuario_temp = User.objects.get(id=pk)
        if usuario_temp.is_active:
            usuario_temp.is_active = False
            print('desactivado')
        else:
            usuario_temp.is_active = True
            print('activar')
    return redirect('users')


@login_required
def change_your_password(request, pk):  # todo: ok
    if not request.user.is_superuser:
        raise PermissionDenied
    else:
        usuario = get_object_or_404(User, id=pk)
        form = SignUpForm(instance=usuario)
        if request.method == "POST":
            form = SignUpForm(request.POST, instance=usuario)
            if form.is_valid():
                u = User.objects.get(username=form.cleaned_data['username'])
                u.set_password(form.cleaned_data['password2'])
                u.save()
                return redirect('users')
    return render(request, 'change-your-password.html', {'form': form})


@login_required
def change_my_password(request):  # todo: ok
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'La contraseña fue modificada correctamente')
            print(request, 'La contraseña fue modificada correctamente')
            return redirect('inicio')
        else:
            # messages.error(request, 'Ha ocurrido un error')
            print(request, 'Ha ocurrido un error')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change-my-password.html', {'form': form})


class SignInView(LoginView):  # todo: ok
    template_name = 'sign-in.html'


class SignOutView(LogoutView):  # todo: ok
    pass


class HomePageView(TemplateView):  # todo: ok
    template_name = 'inicio.html'


class HelpsView(TemplateView):  # todo: ok
    template_name = 'helps.html'


class ContactView(TemplateView):  # todo: ok
    template_name = 'contact.html'


class InvestigatorListView(LoginRequiredMixin, ListView):  # todo: ok
    queryset = Investigator.objects.order_by('-created_date')
    context_object_name = 'investigators'
    template_name = 'investigators.html'


class InvestigatorDetailView(LoginRequiredMixin, DetailView):  # todo: ok
    model = Investigator
    context_object_name = 'investigator'
    template_name = 'update-profile.html'


class InvestigatorAdminCreateView(LoginRequiredMixin, CreateView):  # todo: ok
    model = Investigator
    fields = ['user', 'name', 'degree', 'email', 'phone', 'about', 'country', 'address',
              'company', 'image', 'facebook', 'instagram', 'linkedin', 'twitter']
    template_name = 'create-investigator-admin.html'
    success_url = reverse_lazy('investigators')

    def form_valid(self, form):
        return super().form_valid(form)


class InvestigatorCreateView(LoginRequiredMixin, CreateView):  # todo: ok
    model = Investigator
    fields = ['name', 'degree', 'email', 'phone', 'about', 'country', 'address',
              'company', 'image', 'facebook', 'instagram', 'linkedin', 'twitter']
    template_name = 'create-investigator.html'
    success_url = reverse_lazy('investigators')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class InvestigatorUpdateView(LoginRequiredMixin, UpdateView):  # todo: ok
    model = Investigator
    fields = ['name', 'degree', 'email', 'phone', 'about', 'country', 'address',
              'company', 'image', 'facebook', 'instagram', 'linkedin', 'twitter']
    template_name = 'update-profile.html'
    success_url = reverse_lazy('investigators')


class InvestigatorDeleteView(LoginRequiredMixin, DeleteView):  # todo: ok
    model = Investigator
    success_url = reverse_lazy('investigators')


class StudiesByInvestigator(LoginRequiredMixin, ListView):  # todo: ok
    template_name = 'studies-by-investigator.html'
    context_object_name = 'studies'

    def get_queryset(self):
        self.investigator = get_object_or_404(Investigator, pk=self.kwargs['pk'])
        studies = Study.objects.filter(investigator=self.investigator)
        return studies


class StudyListView(LoginRequiredMixin, ListView):  # todo: ok
    queryset = Study.objects.order_by('-updated_date')
    context_object_name = 'studies'
    template_name = 'studies.html'


def study_export(request, pk):  # todo: en implementacion
    form = ExportForm()
    if request.method == "POST":
        form = ExportForm(request.POST)
        if form.is_valid():
            path = os.path.join(BASE_DIR, 'media/exports/')
            stu = get_object_or_404(Study, pk=pk)
            formatt = form.cleaned_data['format']
            geo = format_file(formatt, pk)
            filename = '{}_{}.{}'.format(stu.name, timezone.now(), formatt)
            try:
                with open(path + filename, 'x') as file:
                    file.write(geo)
            except FileNotFoundError:
                print('La direccion ingresada no existe!!!')

            return FileResponse(open(path+filename, 'rb'), as_attachment=True, filename=filename)
    return render(request, 'study_export.html', {'form': form})


def format_file(f, pk):  # todo: en implementacion
    study = get_object_or_404(Study, pk=pk)
    geometry = ''
    if f == 'geojson':
        geometry = Study.objects.annotate(json=AsGeoJSON(study.zone, bbox=True, crs=True)).values('json')
        geometry = geometry[0]['json']
    if f == 'gml':
        geometry = Study.objects.annotate(gml=AsGML(study.zone)).values('gml')
        geometry = geometry[0]['gml']
    if f == 'kml':
        geometry = Study.objects.annotate(kml=AsKML(study.zone)).values('kml')
        geometry = geometry[0]['kml']
    if f == 'kwt':
        geometry = Study.objects.annotate(wkt=AsWKT(study.zone)).values('wkt')
        geometry = geometry[0]['wkt']
    if f == 'csv':
        export_csv(study.name)
    if f == 'shp':  # todo: en investigacion
        pass
    return geometry


def export_csv(name):  # todo: en implementacion
    path = os.path.join(BASE_DIR, 'media/exports/')
    filename = '{}_{}.csv'.format(name, timezone.now())
    header = ['hola']
    data = ['mundo']
    try:
        with open(path + filename, 'w', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)
    except FileNotFoundError:
        print('La direccion ingresada no existe!!!')
    return FileResponse(open(path + filename, 'rb'), as_attachment=True, filename=filename)


@login_required
def study_detail(request, pk):  # todo: en implementacion
    study = Study.objects.get(pk=pk)
    geo = Study.objects.annotate(json=AsGeoJSON(study.zone, bbox=True, crs=True)).values('name', 'json')
    evi = Evidence.objects.filter(study=study)
    des = Displacement.objects.filter(study=study)
    title = {e.title.header for e in evi}
    title.discard('')
    header = json.dumps(list(title))
    evid = serialize('geojson', evi, geometry_field='point', use_natural_foreign_keys=True,
                      fields=('name', 'image', 'title'))
    disp = serialize('geojson', des, geometry_field='point', use_natural_foreign_keys=True,
                              fields=('velocity', 'altitude'))
    geom = geo[0]['json']
    # prop = geo[0]['name']

    # statistics_image() # todo: esto es provisional

    return render(request, 'study-details.html', {'study': study, 'geom': geom, 'evidence': evid,
                                                  'displacements': disp, 'header': header})


@login_required
def study_create(request):  # todo: en implementacion
    form = StudyForm()
    if request.method == 'POST':
        form = StudyForm(request.POST, request.FILES)
        if form.is_valid():
            zone_layer = GEOSGeometry(form.cleaned_data['help'], srid=4326)
            cp = ConsejoPopular.objects.filter(mpoly__intersects=zone_layer)
            list_nom = {c.nombre for c in cp}
            list_nom.discard('')
            list_muni = {m.municipio for m in cp}
            list_muni.discard('')
            list_prov = {p.provincia for p in cp}
            list_prov.discard('')
            towns = ", ".join(list(list_nom))
            municipalities = ", ".join(list(list_muni))
            provinces = ", ".join(list(list_prov))
            inv = Investigator.objects.get(user=request.user)
            study = Study(name=form.cleaned_data['name'], description=form.cleaned_data['description'],
                          is_public=form.cleaned_data['is_public'], investigator=inv, country='Cuba',
                          province=provinces, help=form.cleaned_data['help'], file=form.cleaned_data['file'],
                          date_start=form.cleaned_data['date_start'], date_final=form.cleaned_data['date_final'],
                          municipality=municipalities, town=towns, zone=zone_layer)
            study.save()
            path = study.file.name
            file = request.FILES['file']
            if file.content_type.__contains__('csv') is True:
                import_csv(path, study.pk)
            elif file.content_type.__contains__('json') is True or file.content_type.__contains__('geo') is True:
                import_json(path, study.pk)
            elif file.content_type.__contains__('zip') is True or file.content_type.__contains__('kml') is True:
                import_kmz(path, study.pk)
            else:
                print('************formato desconocido*************')
            return redirect('evidence-create', study.pk)
    return render(request, 'create-study.html', {'form': form})


def import_csv(f, k):  # todo: ok
    path = os.path.join(BASE_DIR, 'media/')
    stu = get_object_or_404(Study, pk=k)
    with open(path+f, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # salto de las 2 primeras lineas
        next(reader)
        for row in reader:
            velocity = float(row[4].strip())
            altitude = float(row[3].strip())
            lng = float(row[2].strip())
            lat = float(row[1].strip())
            mpoint = GEOSGeometry('POINT({} {})'.format(lng, lat), srid=4326)
            disp = Displacement(velocity=velocity, altitude=altitude, point=mpoint, study=stu)
            disp.save()


def import_json(f, k):  #todo: en implementacion
    stu = get_object_or_404(Study, pk=k)
    path = os.path.join(BASE_DIR, 'media/')
    with open(path+f, 'r') as file:
        reader = json.load(file)
        for row in reader['features']:
            if row['geometry']['type'] == 'Point':
                name = row['properties']['Name']
                desc = row['properties']['description']
                color = row['properties']['timestamp']
                lng, lat, alt = row['geometry']['coordinates']
                mpoint = GEOSGeometry('POINT({} {})'.format(lng, lat), srid=4326)
                disp = Displacement(name=name, description=desc,
                                    color=color, altitude=alt, point=mpoint, study=stu)
                disp.save()


def statistics_image():
    path = os.path.join(BASE_DIR, 'media/imagenes/')
    img = 'overlay.png'
    image = cv2.imread(path + img)
    filas, columnas, canales = image.shape
    mayor = max(filas, columnas)
    menor = min(filas, columnas)
    if canales:
        for ma in range(mayor):
            for me in range(menor):
                azul, verde, rojo = image[ma][me]
                print(azul, verde, rojo)
                # todo: si esta en el rango de los colores (azul claro, azul fuerte, verde, amarillo, rojo) cuentalo
                #  por esos colores. Hallar porciento de cada uno. Enviar a grafica y reporte


def import_kmz(f, k):  #todo: en implementacion
    # mpoint = GEOSGeometry(f, srid=4326)
    path = os.path.join(BASE_DIR, 'media/')
    print(f)
    shutil.unpack_archive(path+f)



@login_required
def study_update(request, pk):  # todo: en implementacion
    study = get_object_or_404(Study, id=pk)
    geo = Study.objects.annotate(json=AsGeoJSON(study.zone, bbox=True, crs=True)).values('json')
    geom = geo[0]['json']
    des = Displacement.objects.filter(study=study)
    disp = serialize('geojson', des, geometry_field='point', use_natural_foreign_keys=True, fields=('color', 'altitude'))
    form = StudyForm(instance=study)
    if request.method == "POST":
        form = StudyForm(request.POST, request.FILES, instance=study)
        if form.is_valid():
            zone_layer = GEOSGeometry(form.cleaned_data['help'], srid=4326)
            cp = ConsejoPopular.objects.filter(mpoly__intersects=zone_layer)
            list_nom = {c.nombre for c in cp}
            list_nom.discard('')
            list_muni = {m.municipio for m in cp}
            list_muni.discard('')
            list_prov = {p.provincia for p in cp}
            list_prov.discard('')
            towns = ", ".join(list(list_nom))
            municipalities = ", ".join(list(list_muni))
            provinces = ", ".join(list(list_prov))
            inv = Investigator.objects.get(user=request.user)
            Study.objects.filter(pk=pk).update(name=form.cleaned_data['name'],
                        description=form.cleaned_data['description'], is_public=form.cleaned_data['is_public'],
                        help=form.cleaned_data['help'], file=form.cleaned_data['file'], investigator=inv,
                        updated_date=timezone.now(), country='Cuba', province=provinces, municipality=municipalities,
                        date_start=form.cleaned_data['date_start'], date_final=form.cleaned_data['date_final'],
                        town=towns, zone=zone_layer)
            return redirect('studies')
    return render(request, 'update-study.html', {'form': form, 'geom': geom, 'disp': disp})


class StudyDeleteView(LoginRequiredMixin, DeleteView):  # todo: ok
    model = Study
    success_url = reverse_lazy('studies')


class EvidencesView(LoginRequiredMixin, ListView):  # todo: ok
    template_name = 'evidences.html'

    def get_queryset(self):
        self.study = get_object_or_404(Study, pk=self.kwargs['pk'])
        evidences = Evidence.objects.filter(study=self.study)
        return evidences

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        st = Study.objects.get(pk=self.kwargs['pk'])
        context['study'] = st
        context['evidences'] = Evidence.objects.filter(study=st)
        return context


@login_required
def evidence_create(request, pk):  # todo: ok
    study = Study.objects.get(id=pk)
    if request.method == 'POST':
        formset = EvidenceFormSet(request.POST, request.FILES, instance=study)
        title = TitleForm(request.POST)
        if formset.is_valid() and title.is_valid():
            title.save()
            ti = Title.objects.get(header=title.cleaned_data['header'])
            for form in formset:
                point = GEOSGeometry(form.cleaned_data['help'], srid=4326)
                evi = form.save(commit=False)
                evi.point = point
                evi.title = ti
                evi.save()
            return redirect('evidence-create', pk)
    formset = EvidenceFormSet()
    title = TitleForm()
    return render(request, 'create-evidence.html', {'form': formset, 'title': title})


@login_required
def evidence_update(request, pk, pq):  # todo: ok
    evidence = get_object_or_404(Evidence, id=pq)
    title = get_object_or_404(Title, id=evidence.title.pk)
    study = Study.objects.get(pk=pk)
    geo = Evidence.objects.annotate(json=AsGeoJSON(evidence.point, bbox=True, crs=True)).values('json')
    geom = geo[0]['json']
    if request.method == "POST":
        form1 = TitleForm(request.POST, instance=title)
        form = EvidenceForm(request.POST, request.FILES, instance=evidence)
        if form.is_valid() and form1.is_valid():
            point = GEOSGeometry(form.cleaned_data['help'], srid=4326)
            evi = form.save(commit=False)
            evi.point = point
            evi.study = study
            evi.save()
            form1.save()
            return redirect('evidences', pk)
    form = EvidenceForm(instance=evidence)
    form1 = TitleForm(instance=title)
    return render(request, 'update-evidence.html', {'form': form, 'form1': form1, 'study': study, 'geom': geom})


class EvidenceAskDelete(TemplateView):  # todo: ok
    template_name = 'workStation/evidence_confirm_delete.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['pq'] = self.kwargs['pq']
        return context


@login_required
def evidence_delete(request, pk, pq):  # todo: ok
    evidence = get_object_or_404(Evidence, id=pq)
    evidence.delete()
    return redirect('evidences', pk)


@login_required
def investigator_report_PDF(request, pk):  # todo: ok
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = investigador.pdf'
    document = SimpleDocTemplate(response, pagesize=pagesizes.portrait(pagesizes.LETTER), )
    story = []
    styles = getSampleStyleSheet()

    styleN = styles['Bullet']
    styleT = styles['Title']
    styleH3 = styles['Heading3']

    investigator = Investigator.objects.get(pk=pk)
    study = Study.objects.filter(investigator=investigator)

    path = os.path.join(BASE_DIR, 'static_files/img/logo-uho.jpg')
    img = Image(path, 100, 51)
    img.hAlign = 'CENTER'
    story.append(img)
    story.append(Spacer(0, 20))
    inv = Paragraph('Investigador', styleT)
    story.append(inv)
    story.append(Spacer(0, 20))

    path = os.path.join(BASE_DIR, 'media/{}'.format(investigator.image))
    img = Image(path, 100, 71)
    img.hAlign = 'LEFT'
    txt = Paragraph('<strong>Nombre: </strong>' + investigator.name + '<br></br>' + '<strong>Titulo: </strong>' +
                    investigator.degree + '<br></br>' + '<strong>Institucion: </strong>' + investigator.company + '<br></br>' +
                    '<strong>Pais: </strong>' + investigator.country, styleN)

    table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'CENTER')])
    story.append(Table([[img, txt]], colWidths=[1.5*inch, 5*inch], rowHeights=[inch], style=table_style))

    story.append(Paragraph('Acerca de', styleH3))
    story.append(Paragraph(investigator.about, styleN))
    story.append(Paragraph('Contactos', styleH3))
    story.append(Paragraph('<strong>Direccion: </strong>' + investigator.address, styleN))
    story.append(Paragraph('<strong>Correo electronico: </strong>' + investigator.email, styleN))
    story.append(Paragraph('<strong>Telefono: </strong>' + str(investigator.phone), styleN))
    story.append(Paragraph('<strong>Twitter: </strong>' + investigator.twitter, styleN))
    story.append(Paragraph('<strong>Facebook: </strong>' + investigator.facebook, styleN))
    story.append(Paragraph('<strong>Instagram: </strong>' + investigator.instagram, styleN))
    story.append(Paragraph('<strong>Linkedin: </strong>' + investigator.linkedin, styleN))
    story.append(Paragraph('Estudios', styleH3))
    for s in study:
        story.append(Paragraph('<strong>{}</strong>'.format(s.name), styleN))
        story.append(Paragraph(s.description, styleN))
        story.append(Spacer(0, 10))

    document.build(story)
    return response


@login_required
def study_report_PDF(request, pk):  # todo: en implementacion
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = estudio.pdf'
    document = SimpleDocTemplate(response, pagesize=pagesizes.portrait(pagesizes.LETTER), )
    story = []
    styles = getSampleStyleSheet()
    styleN = styles['Bullet']
    styleT = styles['Title']
    styleH3 = styles['Heading3']
    table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'CENTER')])

    path = os.path.join(BASE_DIR, 'static_files/img/logo-uho.jpg')
    img = Image(path, 100, 51)
    img.hAlign = 'CENTER'
    story.append(img)
    story.append(Spacer(0, 20))

    study = Study.objects.get(pk=pk)

    # seccion de informacion general
    story.append(Paragraph(study.name, styleT))
    story.append(Spacer(0, 20))
    story.append(Paragraph('Acerca de', styleH3))
    story.append(Paragraph('<i>{}</i>'.format(study.description), styleN))
    story.append(Paragraph('Investigador principal', styleH3))
    path = os.path.join(BASE_DIR, 'media/{}'.format(study.investigator.image))
    img = Image(path, 100, 71)
    img.hAlign = 'LEFT'
    person = Paragraph('<strong>Nombre: </strong>' + study.investigator.name + '<br></br>' +
              '<strong>Titulo: </strong>' + study.investigator.degree + '<br></br>' +
              '<strong>Institucion: </strong>' + study.investigator.company + '<br></br>' +
              '<strong>Pais: </strong>' + study.investigator.country, styleN)
    story.append(Table([[img, person]], colWidths=[1.5 * inch, 5 * inch], rowHeights=[inch], style=table_style))

    story.append(Paragraph('Informacion general', styleH3))
    story.append(Paragraph('<strong>Pais: </strong>' + study.country, styleN))
    story.append(Paragraph('<strong>Provincia(s): </strong>' + study.province, styleN))
    story.append(Paragraph('<strong>Municipio(s): </strong>' + study.municipality, styleN))
    story.append(Paragraph('<strong>Consejo(s) Popular(es): </strong>' + study.town, styleN))
    story.append(Paragraph('<strong>Zona de estudio: </strong>' + str(study.zone), styleN))
    story.append(Paragraph('<strong>Fecha de creado: </strong>' + str(study.created_date), styleN))
    story.append(Paragraph('<strong>Fecha de modificado: </strong>' + str(study.updated_date), styleN))

    # seccion de insar


    # seccion de graficas
    story.append(Paragraph('Analisis estadistico', styleH3))
    d = Drawing(100, 150)
    pc = Pie()
    pc.x = 65
    pc.y = 15
    pc.width = 100
    pc.height = 100
    pc.data = [10, 12, 60, 10, 8]
    pc.labels = ['Ascenso Max', 'Ascenso Min', 'Normalidad', 'Descenso Max', 'Descenso Min']
    pc.sideLabels = 1

    pc.sideLabelsOffset = 0.1
    d.add(pc)
    story.append(d)

    # drawing = Drawing(80, 200)
    # data = [
    #     (13, 5, 20, 22, 37, 45, 19, 4),
    #     (5, 20, 46, 38, 23, 21, 6, 14)
    # ]
    # lc = HorizontalLineChart()
    # lc.x = 50
    # lc.y = 50
    # lc.height = 125
    # lc.width = 300
    # lc.data = data
    # lc.joinedLines = 1
    # catNames = 'Jan Feb Mar Apr May Jun Jul Aug'.split(' ')
    # lc.categoryAxis.categoryNames = catNames
    # lc.categoryAxis.labels.boxAnchor = 'n'
    # lc.valueAxis.valueMin = 0
    # lc.valueAxis.valueMax = 60
    # lc.valueAxis.valueStep = 15
    # lc.lines[0].strokeWidth = 2
    # lc.lines[1].strokeWidth = 1.5
    # drawing.add(lc)
    # story.append(drawing)

    # seccion de evidencias
    story.append(Paragraph('Evidencias', styleH3))
    evi = Evidence.objects.filter(study=study)
    rows = []
    if len(evi) > 0:
        for e in evi:
            path = os.path.join(BASE_DIR, 'media/{}'.format(e.image))
            img = Image(path, 120, 81)
            img.hAlign = 'LEFT'
            txt = Paragraph('<strong>Lugar: </strong>' + e.name + '<br></br>' + '<strong>Posicion: </strong>' +
                            str(e.point) + '<br></br>' + '<strong>Fecha de creado: </strong>' + str(e.created_date) +
                            '<br></br>' + '<strong>Fecha de modificado: </strong>' + str(e.updated_date), styleN)
            rows.append([img, txt])
        story.append(Table(rows, colWidths=[2*inch, 5*inch], rowHeights=[inch]*len(evi), style=table_style))
    else:
        story.append(Paragraph('No hay evidencias disponibles', styleN))

    # seccion de conclusiones y recomendaciones
    story.append(Paragraph('Conclusion', styleH3))
    txt = 'La presente investigacion fue localizada en la provincia de <strong>{}</strong>, en las localidades ' \
          'anteriormente mencionadas. Fueron tomadas de la zona de estudio una serie de imagenes con periodo desde ' \
          'el <strong>{}</strong> hasta el <strong>{}</strong> y se les realizo un procesamiento interferometrico, ' \
          'obteniendo como resultado deformaciones y desplazamientos del ' \
          'terreno.'.format(study.province, study.date_start.strftime('%d/%b/%Y'), study.date_final.strftime('%d/%b/%Y'))
    argu = 'Segun el analisis realizado teniendo en cuenta los parametros de peligro, vulnerabilidad y riesgo; ' \
           'asi como los indices de vulnerabilidad geotecnica se concluye lo siguiente:'
    nivel = 'bajo'  # todo: o alto
    riesgo = 'no representa'  # todo: o representa
    result = 'La zona en estudio presenta un <strong>{}</strong> nivel de afectacion, <strong>{}</strong> un riesgo ' \
             'para cualquier edificacion o comunidad.'.format(nivel, riesgo)
    story.append(Paragraph(txt, styleN))
    story.append(Paragraph(argu, styleN))
    story.append(Paragraph(result, styleN))

    document.build(story)
    return response


# todo: **************** pendiente a futuro *********************


def input_files(request):  # todo: en implementacion
    file_list = []
    form = InputFilesForm()
    if request.method == 'POST' and request.FILES['master'] and request.FILES['slave'] and request.FILES['orbit']:
        form = InputFilesForm(request.POST, request.FILES)
        if form.is_valid():
            for f in range(0, len(form.fields)):
                file_list.append()
            # master = request.FILES['master']
            # file_list.append(master)
            # slave = request.FILES['slave']
            # file_list.append(slave)
            # orbit = request.FILES['orbit']
            # file_list.append(orbit)
            fs = FileSystemStorage()
            for f in file_list:
                filename = fs.save(f.name, f)
                uploaded_file_url = fs.url(filename)
                move_files(filename, uploaded_file_url)

            # for file in files:
            #     localorbit = os.path.join(orbit_dir, file)
            #     if not os.path.exists(localorbit):
            #         move(file, localorbit)
            #         print(file + " done")
            #     else:
            #         print(file + " already exists")

            return redirect('input-variables')
    return render(request, 'input-files.html', {'form': form})


def move_files(filename, source):
    localfilename = os.path.join(slc_dir, filename)
    if not os.path.exists(localfilename):
        print(source, localfilename)
        move(source, localfilename)
    else:
        print(filename + " already exists")


def input_variables(request):  # todo: en implementacion
    if request.method == 'POST':
        form = InputVariablesForm(request.POST)
        if form.is_valid():
            pass
            return redirect('inicio')
    return render(request, 'input-variables.html')


def create_directories(name, date_time):  # todo: ok
    global slc_dir, orbit_dir, insar_dir, process_dir
    title = name + '-' + str(date_time)
    # directory for data downloads
    process_dir = os.path.join(home_dir, title)
    slc_dir = os.path.join(process_dir, 'data', 'slcs')
    orbit_dir = os.path.join(process_dir, 'data', 'orbits')
    insar_dir = os.path.join(process_dir, 'insar')
    # generate all the folders in case they do not exist yet
    os.makedirs(process_dir, exist_ok=True)
    os.makedirs(slc_dir, exist_ok=True)
    os.makedirs(orbit_dir, exist_ok=True)
    os.makedirs(insar_dir, exist_ok=True)
