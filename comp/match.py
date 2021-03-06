import yaml


# ============================================
#                 find_match
# ============================================
def find_match(ytParams, frontend, nf):
    """
    Finds the pytest test corresponding to the nose test. There isn't
    a direct mapping, so the bulk of the work is in converting the
    pytest parameters to match those of nose and then comparing the
    two.
    """
    if nf:
        yf = "/home/latitude/data/yt_data/answers/non_frontends/"
    else:
        yf = "/home/latitude/data/yt_data/answers/frontends/"
    yf += f"{frontend}/{frontend}_answers_000.yaml"
    with open(yf, "r") as fd:
        tests = yaml.safe_load(fd)
        for test, params in tests.items():
            params = convert_pytest_params(params, ytParams, frontend, test)
            if params == ytParams:
                break
    return test


# ============================================
#           convert_pytest_params
# ============================================
def convert_pytest_params(params, ytParams, frontend, test):
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
                # The axial pixelization test actually uses fake data, so
                # the ds isn't parametrizedd and therefore not saved to
                # params in the yaml file. The nose version saves each
                # instance as the same ds name anyway, despite the fact
                # that each one is created with a different geometry, so
                # even if I did save it, they would all match anyway
                elif key == "ds" and ytParams["test"] == "axial_pixelization":
                    convParams[key] = value
                # The weight is always None for the xray tests, which is why
                # it's not parametrized in pytest, but for some reason nose
                # saves it
                elif key == 'w' and frontend == "xray":
                    convParams[key] = 'None'
                elif key == "ds" and frontend == "particle_trajectories":
                    if "orbit" in test:
                        convParams[key] = "orbit_hdf5_chk_0000"
                    elif "etc" in test:
                        convParams[key] = "DD0000"
                    else:
                        convParams[key] = "None"
                # The plot field is always the same, which is why pytest
                # doesn't save it, but nose does
                elif key == "plot_field" and frontend == "particle_plot":
                    convParams[key] = ytParams[key]
                # Pytest also doesn't save the plot type since, for a given
                # function, it's always the same, but nose does
                elif key == "plot_type" and frontend == "particle_plot":
                    if "particle_projection" in test:
                        convParams[key] = "particle_projection_plot"
                    elif "phase" in test:
                        convParams[key] = "particle_phase_plot"
                    else:
                        return None
                # The callback also isn't stored. All the nose test descriptions
                # end with "_", so when the split is done, the last element is
                # ''. As such, when setting the callback_id in parse.py, it's
                # never None
                elif key == "callback_id" and frontend == "particle_plot":
                   convParams[key] = ytParams[key] 
                # Same with the ds
                elif key == "ds" and frontend == "particle_plot":
                    convParams[key] = ytParams[key]
                # For plot_window, the ds isn't stored and the callback
                # is stored with the key `callback`, not `callback_id`
                elif key == "ds" and frontend == "plot_window":
                    convParams[key] = ytParams[key]
                # The way the tests are set up is that each plot_attribute_test
                # is called both with and without the callback. pytest simply
                # parametrizes this, so the results of both tests are saved
                # in a single "entry" in the yaml file, with the keys
                # `plot_window_attribute` and `plot_window_attribute_with_callback`.
                # This means that simply assigning convParams["callback_id"] to
                # whatever the value of callback is in params will cause the
                # case of no callback to be skipped every time, since the pytest
                # dictionary will always have a callback but nose won't, so the
                # dictionary assertion done above will never work
                elif key == "callback_id" and frontend == "plot_window":
                    # If no callback, explicitly set pytest dict to not have
                    # one so the dictionary comp can work
                    if ytParams[key] == "":
                        convParams[key] = ""
                    # Otherwise, use the callback saved in the pytest file
                    # so we can compare against it correctly
                    else:
                        convParams["callback_id"] = params["callback"]
                else:
                    return None
    # For some reason nose stores fields as a full tuple...
    # sometimes. Other times it doesn't, even though the
    # field is a tuple (for example, for f = ('nbody', 'particle_position_x')
    # in ahf, nose stores it as "particle_position_x" while pytest uses
    # "('nbody', 'particle_position_x')")

    # A second complication is the "in" keyword below. It works for the
    # tuple issue mentioned above, but there is another issue. For example,
    # in amrvac, there is the "energy_density" and the "magnetic_energy_density"
    # fields. pytest stores them as tuples, which is what triggers the
    # AssertionError, but then we hit the "in" condition which will be True
    # despite the two descriptions being different. This sets the "f" param equal
    # to the nose value. For the grid_values test, this results in convParams and
    # ytParams being equal despite the fact that convParams is for the magnetic
    # energy density, not the energy density. The data are obviously different, so
    # the test is marked as a failure when, in fact, we were comparing apples and
    # oranges.
    if "f" in convParams:
        try:
            assert convParams["f"] == ytParams["f"]
        except AssertionError:
            baseField = get_base_field(convParams["f"])
            # if ytParams["f"] in convParams["f"]:
            if baseField is not None:
                if ytParams["f"] == baseField:
                    convParams["f"] = ytParams["f"]
                else:
                    return None
            else:
                return None
    # As a last check, if d was in params but happens to be None, we
    # need to switch it to "all" to match nose
    if convParams["d"] == "None":
        convParams["d"] = "all"
    return convParams


# ============================================
#                get_base_field
# ============================================
def get_base_field(field):
    """
    In the case that field is saved as a tuple in pytest but not in
    nose, this function extracts the field name from the tuple. For
    example: if f = "('gas', 'magnetic_energy_density')", then the
    result of this function is 'magnetic_energy_density'.
    """
    try:
        assert "(" in field and ")" in field
    except AssertionError:
        return None
    baseField = field.split(",")[-1]
    baseField = baseField.strip(")")
    baseField = baseField.strip()
    baseField = baseField.strip("'")
    return baseField
