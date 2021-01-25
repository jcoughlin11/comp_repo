import yaml


# ============================================
#                 find_match
# ============================================
def find_match(ytParams, frontend):
    """
    Finds the pytest test corresponding to the nose test. There isn't
    a direct mapping, so the bulk of the work is in converting the
    pytest parameters to match those of nose and then comparing the
    two.
    """
    yf = "/home/latitude/data/yt_data/answers/frontends/"
    yf += f"{frontend}/{frontend}_answers_000.yaml"
    with open(yf, "r") as fd:
        tests = yaml.safe_load(fd)
        for test, params in tests.items():
            params = convert_pytest_params(params, ytParams)
            if params == ytParams:
                break
    return test


# ============================================
#           convert_pytest_params
# ============================================
def convert_pytest_params(params, ytParams):
    """
    When dobj is None, the nose description has it logged as "all".
    Also need to extract the test in the case that there's more than
    one (e.g., both grid_hierarchy and parentage_relationships)
    """
    convParams = {}
    for key, value in ytParams.items():
        # Test isn't a key in params; it uses the actual test name as
        # a key instead. This is also done to extract only the test in
        # question in the case that more than one test is stored in
        # params
        if key == "test":
            try:
                assert value in params
            except AssertionError:
                return None
            convParams[key] = value
        else:
            try:
                convParams[key] = params[key]
            except KeyError:
                if key == "d":
                    # d is always in nose's parameters regardless of whether
                    # or not the test uses it. If the test doesn't use it,
                    # it's not in pytest, hence the KeyError. However, if
                    # d isn't used then it should be "all", which is what
                    # nose uses as the value when d is None
                    convParams[key] = value
                    try:
                        assert value == "all"
                    except AssertionError:
                        return None
                else:
                    return None
    # For some reason nose stores fields as a full tuple...
    # sometimes. Other times it doesn't, even though the
    # field is a tuple (for example, for f = ('nbody', 'particle_position_x')
    # in ahf, nose stores it as "particle_position_x" while pytest uses
    # "('nbody', 'particle_position_x')")
    if "f" in convParams:
        try:
            assert convParams["f"] == ytParams["f"]
        except AssertionError:
            if ytParams["f"] in convParams["f"]:
                convParams["f"] = ytParams["f"]
            else:
                return None
    # As a last check, if d was in params but happens to be None, we
    # need to switch it to "all" to match nose
    if convParams["d"] == "None":
        convParams["d"] = "all"
    return convParams
