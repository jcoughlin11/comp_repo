import h5py
import numpy as np


# ============================================
#                get_my_data
# ============================================
def get_my_data(desc, test, frontend):
    # The description passed is the one from the yaml file, which can
    # have slashes in it. The hdf5 version does not because that creates
    # erroneous groups
    myData = None
    desc = desc.replace("/", "_")
    hf = "/home/latitude/data/yt_data/answers/frontends/"
    hf += f"{frontend}/{frontend}_answers_raw_000.h5"
    with h5py.File(hf, "r") as fd:
        data = fd[desc][test]
        if isinstance(data, h5py.Group):
            myData = parse_group(data)
            assert isinstance(myData, dict)
            for key, value in myData.items():
                try:
                    assert isinstance(value, np.ndarray)
                except AssertionError:
                    assert isinstance(value, np.float)
        elif isinstance(data, h5py.Dataset):
            try:
                myData = data[:]
            except ValueError:
                myData = data[()]
            assert isinstance(myData, np.ndarray) or isinstance(myData, np.int64)
    return myData


# ============================================
#                parse_group
# ============================================
def parse_group(group):
    data = {}
    for key, value in group.items():
        assert isinstance(value, h5py.Dataset)
        try:
            data[key] = value[:]
        except ValueError:
            data[key] = value[()]
    return data
