import rioxarray
import planetary_computer as pc
import odc.stac


def sentinel_image(item, col_name='visual'):
    return rioxarray.open_rasterio(pc.sign(item.assets[col_name].href))


def landsat_image(item, bands_list: list = ["red", "green", "blue"], bbox_list=None):
    if bbox_list is None:
        landsat_im = odc.stac.stac_load([pc.sign(item)], bands=bands_list)
    else:
        landsat_im = odc.stac.stac_load([pc.sign(item)], bands=bands_list, bbox=bbox_list)
    print('fin im.')

    return landsat_im.isel(time=0)
