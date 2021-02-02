import hashlib

import numpy as np
import unyt

from .registers import specialFields


# ============================================
#               compare_answers
# ============================================
def compare_answers(ytData, myData, test, frontend):
    didComp = False
    if isinstance(ytData, list):
        ytData = unyt.array.unyt_array(ytData)
    if hasattr(ytData, "d"):
        ytData = ytData.d
    # Some tests need special treatment
    if test == "grid_values":
        compare_gv(ytData, myData)
        didComp = True
    elif test == "parentage_relationships":
        compare_pr(ytData, myData)
        didComp = True
    elif isinstance(myData, np.ndarray):
        comp_arrays(ytData, myData)
        didComp = True
    elif isinstance(myData, np.float):
        np.testing.assert_array_equal(ytData, myData)
        didComp = True
    elif isinstance(myData, np.int64):
        # pytest uses -1 to represent None values in order to make
        # hashing and saving to hdf5 work
        if ytData is None:
            ytData = np.int64(-1)
        np.testing.assert_array_equal(ytData, myData)
        didComp = True
    elif isinstance(myData, dict):
        comp_dict(ytData, myData, frontend)
        didComp = True
    if not didComp:
        raise ValueError


# ============================================
#                comp_arrays
# ============================================
def comp_arrays(ytData, myData):
    try:
        np.testing.assert_array_equal(ytData, myData)
    except:
        # It's possible there are nans, which causes the comparison
        # to fail even though the arrays are actually the same
        check_for_nans(ytData, myData)


# ============================================
#                 comp_dict
# ============================================
def comp_dict(ytData, myData, frontend):
    for key, value in ytData.items():
        if hasattr(value, "d"):
            value = value.d
        try:
            # For some frontends (e.g., athena), nose uses an alias
            # for certain fields (e.g., ('gas', 'density') for
            # ('athena', 'density')). Need to convert in order to avoid
            # a KeyError
            if frontend in specialFields and key in specialFields[frontend]:
                key = specialFields[frontend][key]
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
    if len(ytData) == 0:
        assert len(myData) == 0


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
    if len(ytData) == 0:
        assert len(myData) == 0


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
