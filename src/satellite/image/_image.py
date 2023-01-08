import numpy as np
import pandas as pd
import collections

from .. import tools
from . import crop


# Refactor our process from above into functions
def select_best_item(items, date, latitude, longitude):
    """
    Select the best satellite item given a sample's date, latitude, and longitude.
    If any Sentinel-2 imagery is available, returns the closest sentinel-2 image by
    time. Otherwise, returns the closest Landsat imagery.

    Returns a tuple of (STAC item, item platform name, item date)
    """
    # get item details
    item_details = pd.DataFrame(
        [
            {
                "datetime": item.datetime.strftime("%Y-%m-%d"),
                "platform": item.properties["platform"],
                "min_long": item.bbox[0],
                "max_long": item.bbox[2],
                "min_lat": item.bbox[1],
                "max_lat": item.bbox[3],
                "item_obj": item,
            }
            for item in items
        ]
    )

    # filter to items that contain the point location, or return None if none contain the point
    item_details["contains_sample_point"] = (
            (item_details.min_lat < latitude)
            & (item_details.max_lat > latitude)
            & (item_details.min_long < longitude)
            & (item_details.max_long > longitude)
    )
    item_details = item_details[item_details["contains_sample_point"] == True]
    if len(item_details) == 0:
        return np.nan, np.nan, np.nan

    # add time difference between each item and the sample
    item_details["time_diff"] = pd.to_datetime(date) - pd.to_datetime(
        item_details["datetime"]
    )

    # if we have sentinel-2, filter to sentinel-2 images only
    item_details["sentinel"] = item_details.platform.str.lower().str.contains(
        "sentinel"
    )
    if item_details["sentinel"].any():
        item_details = item_details[item_details["sentinel"] == True]
        feature_bbox = tools.get_bounding_box(latitude, longitude, meter_buffer=200)

        # Is there water cell in sentinel?
        # ref: https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l2a/#units
        try:
            item_details['scl_water'] = [6 in collections.Counter(np.ravel(_scl_array)).keys()
                                         for _scl_array
                                         in [crop.crop_sentinel_image(_item, feature_bbox, col_name='SCL')
                                         for _item in item_details.item_obj]]
            if np.sum(item_details['scl_water']) >= 1:
                item_details = item_details[item_details["scl_water"] == True]
        except Exception:
            print('scl_water error')

    # return the closest imagery by time
    best_item = item_details.sort_values(by="time_diff", ascending=True).iloc[0]

    return item_details, best_item["item_obj"], best_item["platform"], best_item["datetime"]


def image_to_features(image_array):
    """
    Convert an image array of the form (color band, height, width) to a
    1-dimensional list of features. Returns a list where the first three
    values are the averages of each color band, and the second three
    values are the medians of each color band.
    """
    averages = image_array.mean(axis=(1, 2)).tolist()
    medians = np.median(image_array, axis=(1, 2)).tolist()

    return averages + medians
