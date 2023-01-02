from .. import tools


def read_planet_computer(ref_latitude, ref_longitude, meter_buffer, ref_date, time_buffer_days, catalog) -> object:
    """
    Return items in meter_buffer and time_buffer range satellite items

    Parameters
    ----------
    ref_latitude, ref_longitude: float
        Center of image
    meter_buffer: float
        Buffer meter
    ref_date: datetime.datetime
        The Latest date
    time_buffer_days
        Buffer of date
    catalog: Client
        pystac Client of planetary computer

    Returns
    -------
    items: object
        satellite data in buffer meter and time range

    """

    search_bbox = tools.get_bounding_box(
        ref_latitude, ref_longitude, meter_buffer=meter_buffer
    )
    date_range = tools.get_date_range(ref_date, time_buffer_days=time_buffer_days)

    search = catalog.search(
        collections=["sentinel-2-l2a", "landsat-c2-l2"],
        bbox=search_bbox,
        datetime=date_range,
    )

    return [item for item in search.get_all_items()]

