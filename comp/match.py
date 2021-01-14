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
    with open(f"{frontend}/{frontend}_answers_000.yaml", "r") as fd:
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
    for key in ytParams:
        try:
            convParams[key] = params[key]
        except KeyError:
            break
    return convParams
