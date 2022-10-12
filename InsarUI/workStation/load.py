from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from workStation.models import Municipio
from static_files import geojson

prov_mapping = {
    'layer': 'LAYER',
    'map_name': 'MAP_NAME',
    'cod_munic': 'COD_MUNIC',
    'munic': 'MUNIC',
    'sup_distkm': 'SUP_DISTKM',
    'provincia': 'PROVINCIA',
    'closed': 'CLOSED',
    'border_sty': 'BORDER_STY',
    'border_col': 'BORDER_COL',
    'border_wid': 'BORDER_WID',
    'fill_style': 'FILL_STYLE',
    'mpoly': 'MULTIPOLYGON',
}

ws_shp = Path(__file__).resolve().parent / 'DPA_Cuba_2010_mun_src_4326.shp'


def run(verbose=True):
    lm = LayerMapping(Municipio, ws_shp, prov_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)
