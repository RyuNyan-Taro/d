class hrrr_dataset:
    def __init__(self, ds):
        self.ds = ds

    def tude_list(self, min_tude, max_tude, len_list) -> list:
        delta_tude = (max_tude-min_tude) / (len_list-1)

        return [min_tude+delta_tude*_i for _i in range(len_list)]

