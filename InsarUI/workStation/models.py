from django.contrib.gis.db import models
# from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


DOMAIN_CHOICES = [
    ('PUBLIC', 'PÚBLICO'),
    ('PRIVATE', 'PRIVADO')
]


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Investigator(BaseModel):
    name = models.CharField(max_length=50)
    degree = models.CharField(max_length=50)
    about = models.TextField(max_length=250, default='desconocido')
    company = models.CharField(max_length=100, default='desconocida')
    country = models.CharField(max_length=30, default='desconocido')
    address = models.CharField(max_length=100, default='desconocida')
    image = models.ImageField(upload_to='imagenes/')
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    twitter = models.URLField(default='https://twitter.com/')
    facebook = models.URLField(default='https://facebook.com/')
    instagram = models.URLField(default='https://instagram.com/')
    linkedin = models.URLField(default='https://linkedin.com/')
    created_date = models.DateTimeField(auto_now_add=timezone.now(), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=timezone.now(), null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Investigators'


class Study(BaseModel):
    name = models.CharField('Nombre', max_length=50)
    description = models.TextField('Descripcion', max_length=250, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=150, null=True, blank=True)
    municipality = models.CharField(max_length=250, null=True, blank=True)
    town = models.CharField(max_length=500, null=True, blank=True)
    is_public = models.CharField('Estado', max_length=7, choices=DOMAIN_CHOICES)
    help = models.CharField('Zona', max_length=1500, default='')
    file = models.FileField(upload_to='imports/', null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_final = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=timezone.now(), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=timezone.now(), null=True, blank=True)
    zone = models.PolygonField('Zona')
    investigator = models.ForeignKey('Investigator', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Studies'


class Displacement(BaseModel):
    velocity = models.FloatField('Velocidad Vertical', max_length=20, null=True, blank=True)
    altitude = models.FloatField('Altura', max_length=20, null=True, blank=True)
    point = models.PointField('Punto')
    study = models.ForeignKey('Study', on_delete=models.CASCADE, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=timezone.now(), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=timezone.now(), null=True, blank=True)

    def __str__(self):
        return str(self.altitude)

    class Meta:
        ordering = ['altitude']


class Evidence(BaseModel):
    name = models.CharField('Nombre', max_length=50, null=True)
    help = models.CharField('Geolocalizacion', max_length=100, null=True)
    point = models.PointField('Punto')
    image = models.ImageField('Imagen', upload_to='imagenes/', null=True)
    study = models.ForeignKey('Study', on_delete=models.CASCADE)
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=timezone.now(), null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=timezone.now(), null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Evidences'


class Title(BaseModel):
    header = models.CharField('Encabezado', max_length=50, default='Desconocido')

    def __str__(self):
        return self.header

    def natural_key(self):
        return self.header

    class Meta:
        ordering = ['header']
        verbose_name_plural = 'Titles'


# class Elevation(BaseModel):
#     name = models.CharField(max_length=100)
#     rast = models.RasterField()
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ['name']
#         verbose_name_plural = 'Elevations'


# class PolyLayer(BaseModel):
#     name = models.CharField(max_length=30, default='', null=True, blank=True)
#     layer = models.MultiPolygonField()
#
#     class Meta:
#         verbose_name_plural = 'Poly Layers'


# class LineLayer(BaseModel):
#     name = models.CharField(max_length=30, default='', null=True, blank=True)
#     layer = models.MultiLineStringField()
#
#     class Meta:
#         verbose_name_plural = 'Line Layers'
#
#
# class PointLayer(BaseModel):
#     name = models.CharField(max_length=30, default='', null=True, blank=True)
#     layer = models.MultiPointField()
#
#     class Meta:
#         verbose_name_plural = 'Point Layers'


class CollectionLayer(BaseModel):
    name = models.CharField(max_length=30, null=True, blank=True)
    layer = models.GeometryCollectionField()
    study = models.ForeignKey('Study', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']


class Provincia(BaseModel):
    gid = models.IntegerField()
    provincia = models.CharField(max_length=38)
    codigo = models.IntegerField()
    dtrepresen = models.CharField(max_length=254)
    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.provincia

    class Meta:
        ordering = ['codigo']
        verbose_name_plural = 'Provincias'


class ConsejoPopular(BaseModel):
    gid = models.IntegerField()
    id_cpopula = models.CharField(max_length=16)
    nombre = models.CharField(max_length=60)
    codigo = models.CharField(max_length=16)
    provincia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    habitantes = models.IntegerField()
    viviendas = models.IntegerField()
    mpoly = models.MultiPolygonField()

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['provincia']
        verbose_name_plural = 'Consejos Populares'
