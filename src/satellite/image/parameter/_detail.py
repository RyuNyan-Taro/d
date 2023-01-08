import pystac

from .. import crop


def water_dict(item: pystac.item.Item,  bounding_box: list) -> dict:
    """
    Create dict which has information whether  water region is included in an image

    Parameters
    ----------
    item : Item
        Pystac Item
    bounding_box : list
        Return of tools.get_bounding_box()

    Returns
    -------
    water_dict : dict
        Water key has dict

    """

    return {"datetime": item.datetime.strftime("%Y-%m-%d"),
            "platform": item.properties["platform"],
            "water": water_bool(item, bounding_box),
            "item_obj": item}


def water_bool(item: pystac.item.Item,  bounding_box: list) -> bool:
    """
    Bool whether item image has water region

    Parameters
    ----------
    item : Item
        Pystac Item
    bounding_box : list
        Return of tools.get_bounding_box()

    Returns
    -------
    water_bool : bool
        Return True If the image has water region

    """

    _platform = item.properties['platform']
    if 'sentinel' in _platform.lower():
        try:
            class_array = crop.crop_sentinel_image(item, bounding_box, col_name='SCL')[0]
        except:
            return False
        water_num = 6
    elif _platform == 'landsat-7':
        try:
            class_array = crop.crop_sentinel_image(item, bounding_box, col_name='cloud_qa')[0]
        except:
            return False
        water_num = 32
    else:
        return False

    return water_num in class_array



