import requests
import tempfile
import cfgrib
import xarray as xr

"""
Read module of hrrr temperature data
ref: https://nbviewer.org/github/microsoft/AIforEarthDataSets/blob/main/data/noaa-hrrr.ipynb
"""


def create_url(year: str, month: str, date: str, container: str = "windows", sector: str = "conus") -> str:
    """Create url of hrrr"""

    container_dict = {"windows": "https://noaahrrr.blob.core.windows.net/hrrr", "aws": "https://noaa-hrrr-bdp-pds.s3.amazonaws.com"}
    sector_list = ["conus", "alaska"]
    product_dict = {"windows": "wrfsfcf", "aws": "wrfprsf"}
    if sector not in sector_list:
        raise ValueError(f'{sector} is not in {sector_list}')
    container_url = container_dict[container]
    cycle = 12          # noon
    forecast_hour = 1   # offset from cycle time
    product = product_dict[container]  # windows: 2D surface, aws: 3D pressure

    # Put it all together
    file_path = f"hrrr.t{cycle:02}z.{product}{forecast_hour:02}.grib2"
    url = f"{container_url}/hrrr.{year+month+date}/{sector}/{file_path}"
    print(url)

    return url


def hrrr_dataset(year: str, month: str, date: str, container: str = "windows", sector: str = "conus") -> object:
    url = create_url(year, month, date, container=container, sector=sector)
    # Fetch the idx file by appending the .idx file extension to our already formatted URL
    r = requests.get(f"{url}.idx")
    idx = r.text.splitlines()

    # You can see it has a 1-indexed base line number, staring byte position, date, variable, atmosphere level,
    # and forecast description. The lines are colon-delimited.

    # Let's grab surface temperature `TMP:surface`.
    sfc_temp_idx = [l for l in idx if ":TMP:surface" in l][0].split(":")

    # Pluck the byte offset from this line, plus the beginning offset of the next line
    line_num = int(sfc_temp_idx[0])
    range_start = sfc_temp_idx[1]

    # The line number values are 1-indexed, so we don't need to increment it to get the next list index,
    # but check we're not already reading the last line
    next_line = idx[line_num].split(':') if line_num < len(idx) else None

    # Pluck the start of the next byte offset, or nothing if we were on the last line
    range_end = next_line[1] if next_line else None
    file = tempfile.NamedTemporaryFile(prefix="tmp_", delete=False)

    headers = {"Range": f"bytes={range_start}-{range_end}"}
    resp = requests.get(url, headers=headers, stream=True)

    with file as f:
        f.write(resp.content)

    ds = xr.open_dataset(file.name, engine='cfgrib',
                         backend_kwargs={'indexpath': ''})

    return ds
