import numpy as np


def _tude_list(min_tude, max_tude, length) -> list:
    delta_tude = (max_tude-min_tude) / (length-1)

    return [min_tude+delta_tude*_i for _i in range(length)]


class hrrr_dataset:
    def __init__(self, ds):
        self.ds = ds

    def tude_range_list(self, tude: str) -> list:
        if tude == 'latitude':
            min_tude, max_tude = np.min(self.ds.latitude), np.max(self.ds.latitude)
            length = np.shape(self.ds.t[0])
        elif tude == 'longitude':
            min_tude, max_tude = np.min(self.ds.longitude), np.max(self.ds.longitude)
            length = np.shape(self.ds.t[0])
        else:
            raise ValueError(f'You must select latitude or longitude as tude. {tude} is not them.')

        return _tude_list(min_tude, max_tude, length)
