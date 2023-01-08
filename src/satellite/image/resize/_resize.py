import numpy as np


def twice_len_array(base_array: np.ndarray, resize_len: int) -> np.ndarray:
    """
    Return twice 2D array of resize_len x resize_len
    Parameters
    ----------
    base_array : np.array
        2D array
    resize_len : int
        Length of return array

    Returns
    -------
        resized_array : np.ndarray
            2D array which resized to resize_len

    """
    resized_array = list()
    resize_range = range(resize_len)
    for _i in resize_range:
        resized_array.append([base_array[_i//2][_j//2] for _j in resize_range])

    return np.array(resized_array)
