import hashlib

import numpy as np


# ============================================
#               compare_answers
# ============================================
def compare_answers(ytData, myData, test):
    if isinstance(myData, np.ndarray):
        try:
            np.testing.assert_array_equal(ytData, myData)
        except:
            # It's possible there are nans, which causes the comparison
            # to fail even though the arrays are actually the same
            check_for_nans(ytData, myData)
    elif isinstance(myData, np.float):
        np.testing.assert_array_equal(ytData, myData)
    elif isinstance(myData, dict):
        if test == "grid_values":
            compare_gv(ytData, myData)
        elif test == "parentage_relationships":
            compare_pr(ytData, myData)
        else:
            for key, value in ytData.items():
                try:
                    np.testing.assert_array_equal(value, myData[key])
                # For some fields (e.g., ('enzo', 'Density')) the yt key
                # is a tuple while the pytest key is a str version of that
                # tuple
                except KeyError:
                    np.testing.assert_array_equal(value, myData[str(key)])
                except AssertionError:
                    # It's possible there are nans, which causes the comparison
                    # to fail even though the arrays are actually the same
                    check_for_nans(value, myData[key])


# ============================================
#               check_for_nans
# ============================================
def check_for_nans(a, b):
    assert a.shape == b.shape
    with np.nditer(a, flags=["multi_index"]) as it:
        for x in it:
            if np.isnan(x):
                assert np.isnan(b[it.multi_index])
            elif np.isinf(x):
                assert np.isinf(b[it.multi_index])
            else:
                assert x == b[it.multi_index]


# ============================================
#                 compare_gv
# ============================================
def compare_gv(ytData, myData):
    """
    The yt answer is hashed, but mine isn't
    The yt data is also keyed by an integer whereas mine is keyed by
    a string version of that integer.
    """
    for key, value in ytData.items():
        myValue = myData[str(key)]
        myValue = hashlib.md5(myValue.tostring()).hexdigest()
        assert value == myValue


# ============================================
#                 compare_pr
# ============================================
def compare_pr(ytData, myData):
    """
    The parentage relationships test is laid out differently in yt.
    In yt:
        ytData = {
            "parents" : [[], x, ...],
            "children" : [[], x, ...],
        }

        that is, each key's value is a list. This list is ragged, meaning
        that some of the entries are multi-valued, some single, some
        empty, and some not lists at all, but scalars.

    My data:
        myData = {
            "parents" : r x c ndarray, where r = len(ytData["parents"])
                and c = len(longest sublist in ytData["parents"])
            "children" : ibid 
        }

        The rows of myData that are naturally shorter than nCols are
        padded with -2. Additionally, where ytData stores None, I store
        -1. This was done for several reasons. If the array is ragged
        then its dtype is object, which, when hashed, makes use of the
        memory location of the array, which causes the hash to change
        from run to run. The presence of None also produces a dtype of
        object. Additionally, hdf5 cannot save ragged arrays or arrays
        of dtype object. As such, I need to de-pad myData.
    """
    convData = {"parents" : [], "children" : []}
    assert isinstance(myData["parents"], np.ndarray)
    assert isinstance(myData["children"], np.ndarray)
    for key, array in myData.items():
        for i in range(array.shape[0]):
            temp = []
            for j in range(array.shape[1]):
                val = array[i][j]
                if val == -1:
                    val = None
                elif val == -2:
                    break
                temp.append(val)
            if len(temp) == 1:
                convData[key].append(temp[0])
            else:
                convData[key].append(temp)
    assert convData == ytData