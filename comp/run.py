import argparse
import os
import shelve

from progress.bar import Bar

from .compare import compare_answers
from .data import get_my_data
from .match import find_match
from .parse import parse_yt_desc
from .registers import testRegister


# ============================================
#                    run
# ============================================
def run():
    """
    The nose results are saved in a shelve file. The pytest results
    are saved in an hdf5 file.
        1. Loop over each test in the shelve file
        2. Find the corresponding test in the h5 file
        3. Compare
    """
    clArgs = parse_args()
    frontend = clArgs.frontend
    debug = clArgs.pdb
    nf = clArgs.nf
    if nf:
        path = "/home/latitude/data/yt_data/answers/non_frontends"
    else:
        path = "/home/latitude/data/yt_data/answers/frontends"
    fname = f"{frontend}/local-{frontend}/local-{frontend}"
    noseFile = os.path.join(path, fname)
    progBar = get_prog_bar(noseFile)
    if debug:
        import pdb; pdb.set_trace()
    with shelve.open(noseFile, "r") as yfd:
        # The yt shelve file is keyed by ds then test description
        for ds in yfd.keys():
            for ytDesc in yfd[ds].keys():
                progBar.next()
                # Parse the yt description so it can be compared to the
                # pytest description
                ytParsedDesc = parse_yt_desc(ytDesc, frontend)
                if "ds" in ytParsedDesc:
                    ytParsedDesc["ds"] = ds
                try:
                    assert ytParsedDesc["test"] in testRegister
                except AssertionError:
                    msg = f"NOT IMPLEMENTED: {ytParsedDesc['test']}\n"
                    write_error(msg, frontend, nf)
                # Find the matching pytest description
                myDesc = find_match(ytParsedDesc, frontend, nf)
                # Load the yt data
                ytData = yfd[ds][ytDesc]
                # Load pytest data
                try:
                    myData = get_my_data(myDesc, ytParsedDesc["test"], frontend, nf)
                except KeyError:
                    msg = f"PYTEST KEYERROR: {ytDesc}\t{myDesc}\n"
                    write_error(msg, frontend, nf)
                # Now compare the results
                try:
                    compare_answers(ytData, myData, ytParsedDesc["test"], frontend)
                except AssertionError:
                    msg = f"RESULTS UNEQUAL: {ytDesc}\t{myDesc}\n"
                    write_error(msg, frontend, nf)
                except ValueError:
                    msg = f"TESTS NOT COMPARED: {ytDesc}\t{myDesc}\n"
                    write_error(msg, frontend, nf)
                except KeyError:
                    msg = f"KEYERROR: {ytDesc}\t{myDesc}\n"
                    write_error(msg, frontend, nf)
                except:
                    msg = f"UNHANDLED EXCEPTION: {ytDesc}\t{myDesc}\n"
                    write_error(msg, frontend, nf)
    progBar.finish()


# ============================================
#                  parse_args
# ============================================
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "frontend",
        help="The name of the frontend to compare tests for.",
    )
    parser.add_argument(
        "--pdb",
        dest = "pdb",
        action = "store_true",
        help = "Use debugger,",
    )
    parser.add_argument(
        "--nf",
        dest = "nf",
        action = "store_true",
        help = "Indicates a non-frontend test.",
    )
    clArgs = parser.parse_args()
    return clArgs


# ============================================
#                 get_prog_bar
# ============================================
def get_prog_bar(noseFile):
    nTests = get_n_tests(noseFile)
    progBar = Bar("Processing", max=nTests)
    return progBar


# ============================================
#                 get_n_tests
# ============================================
def get_n_tests(noseFile):
    ntests = 0
    with shelve.open(noseFile, "r") as fd:
        for ds in fd.keys():
            ntests += len(fd[ds].keys())
    return ntests


# ============================================
#                 write_error
# ============================================
def write_error(msg, frontend, nf):
    if nf:
        errorFile = "/home/latitude/data/yt_data/answers/non_frontends/"
    else:
        errorFile = "/home/latitude/data/yt_data/answers/frontends/"
    errorFile += f"{frontend}/{frontend}_failures.txt"
    with open(errorFile, "a") as ffd:
        ffd.write(msg)
