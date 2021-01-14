import argparse
import shelve

from progress.bar import Bar

from .compare import compare_answers
from .data import get_my_data
from .match import find_match
from .parse import parse_yt_desc


# ============================================
#                    run
# ============================================
def run():
    """
    The nose results are saved in a shelve file. The pytest results
    are saved in an hdf5 file.
        1. Loop over each test in the shelve file
        2. For each test, find the corresponding test in the h5 file
        3. Compare
    """
    frontend = parse_args()
    noseFile = f"{frontend}/local-{frontend}/local-{frontend}"
    progBar = get_prog_bar(noseFile)
    with shelve.open(noseFile, "r") as yfd:
        # The yt shelve file is keyed by ds then test description
        for ds in yfd.keys():
            for ytDesc in yfd[ds].keys():
                # Parse the yt description so it can be compared to the
                # pytest description
                ytParsedDesc = parse_yt_desc(ytDesc, frontend)
                # Find the matching pytest description
                myDesc = find_match(ytParsedDesc, frontend)
                # Load the yt data
                ytData = yfd[ds][ytDesc]
                # Load pytest data
                myData = get_my_data(myDesc, ytParsedDesc["test"], frontend)
                # Now compare the results
                try:
                    compare_answers(ytData, myData, ytParsedDesc["test"])
                except:
                    with open(f"{frontend}_failures.txt", "a") as ffd:
                        ffd.write(ytDesc + "\t" + myDesc + "\n")
                progBar.next()
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
    clArgs = parser.parse_args()
    return clArgs.frontend


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
