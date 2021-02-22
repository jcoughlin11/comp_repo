import re

from .registers import attrNameRegister
from .registers import callbackRegister
from .registers import dsRegister
from .registers import fieldRegister
from .registers import funcNameRegister
from .registers import geomRegister
from .registers import objRegister
from .registers import particlePlotDecompress
from .registers import plotFieldRegister
from .registers import plotWindowDecompress
from .registers import profilePlotsDecompress
from .registers import specialFields
from .registers import xrayDecompress


# ============================================
#               parse_yt_desc
# ============================================
def parse_yt_desc(desc, frontend):
    """
    yt descriptions are:
        1. test name
        2. ds
        3. dobj
        4. other test parameters
    These are separated by underscores.
    """
    params = {}
    # Remove underscores from the names of the various components
    # Some of the xray tests have a test suffix appended to the end of the
    # description that does not correspond to any test parameter
    if frontend == "xray":
        for suffix in ["_dist_1Mpc", "_current_redshift"]:
            if suffix in desc:
                desc = desc.replace(suffix, "")
    if frontend == "particle_trajectories":
        if desc.endswith("_None"):
            desc = desc[:-5]
    components = sanitize_yt_desc(desc, frontend)
    params["test"] = camel_to_snake(components[0])
    params["ds"] = components[1]
    params["d"] = components[2]
    otherParams = get_other_yt_params(params["test"], components[3:])
    params.update(otherParams)
    # Undo the underscore removal
    params = undo_string_compressions(params, frontend)
    # The way the tests are chosen is by using the name from the
    # nose file, which will always be `plot_window_attribute`
    # regardless of whether or not the callback is being used, which
    # means the comparison will fail when it's supposed to be with
    # the callback. As such, we explicitly set the test to the `with_callback`
    # version here so that loading the pytest data will be done correctly
    if frontend == "particle_plot":
        if params["callback_id"] == "":
            params["test"] = "plot_window_attribute"
        else:
            params["test"] = "plot_window_attribue_with_callback"
    return params


# ============================================
#             sanitize_yt_desc
# ============================================
def sanitize_yt_desc(desc, frontend):
    """
    Certain ds names, fields, and objects have underscores in them,
    which messes up parsing, since each test component is also
    separated by an underscore. This function removes the intra-
    component underscores.
    """
    # Datasets
    desc = sanitize_component(desc, "ds", frontend)
    # Fields
    desc = sanitize_component(desc, "field", frontend)
    # Objects
    desc = sanitize_component(desc, "object", frontend)
    desc = sanitize_component(desc, "geom", frontend)
    desc = sanitize_component(desc, "func_name", frontend)
    # Misc; frontend specific
    desc = sanitize_component(desc, "plot_field", frontend)
    desc = sanitize_component(desc, "plot_attr", frontend)
    desc = sanitize_component(desc, "callback", frontend)
    return desc.split("_")


# ============================================
#             sanitize_component
# ============================================
def sanitize_component(desc, componentType, frontend):
    if componentType == "ds":
        try:
            register = dsRegister[frontend]
        except KeyError:
            return desc
    elif componentType == "field":
        try:
            register = fieldRegister[frontend]
        except KeyError:
            return desc
    elif componentType == "object":
        try:
            register = objRegister[frontend]
        except KeyError:
            return desc
    elif componentType == "geom":
        try:
            register = geomRegister[frontend]
        except KeyError:
            return desc
    elif componentType == "func_name":
        try:
            register = funcNameRegister[frontend]
        except KeyError:
            return desc
    elif componentType == "plot_field":
        try:
            register = plotFieldRegister[frontend]
        except KeyError:
            return desc
    elif componentType == "plot_attr":
        try:
            register = attrNameRegister[frontend]
        except KeyError:
            return desc
    elif componentType == "callback":
        try:
            register = callbackRegister[frontend]
        except KeyError:
            return desc
    for comp in register:
        if comp in desc:
            if "sphere" in comp:
                sanitizedSphere = sanitize_sphere(comp)
                desc = desc.replace(comp, sanitizedSphere)
            else:
                try:
                    sanitizedField = specialFields[frontend][comp]
                    desc = desc.replace(comp, sanitizedField)
                    comp = sanitizedField
                except KeyError:
                    pass
                joined = "".join(comp.split("_"))
                desc = desc.replace(comp, joined)
                # For these tests (particle_plot, etc.) both the attribute
                # name and the attribute value are written in the description.
                # Both need to be parsed, since they can both have underscores
                # in them. As such, the attrNameRegister is a dictionary
                # whose values are dictionaries containing the attribute name
                # and the list of possible values that it can take
                if componentType == "plot_attr":
                    for attrVal in register[comp]:
                        if "_" in attrVal:
                            joined = "".join(attrVal.split("_"))
                            desc = desc.replace(attrVal, joined)
    return desc


# ============================================
#              sanitize_sphere
# ============================================
def sanitize_sphere(comp):
    sanitized = "('sphere', ("
    if "max" in comp:
        sanitized += "'max', ("
    elif "m" in comp:
        sanitized += "'m', ("
    elif "c" in comp:
        sanitized += "'c', ("
    if "0_1" in comp:
        sanitized += "0.1, 'unitary')))"
    elif "0_3" in comp:
        sanitized += "0.3, 'unitary')))"
    elif "0_25" in comp:
        sanitized += "0.25, 'unitary')))"
    elif "0_2" in comp:
        sanitized += "0.2, 'unitary')))"
    return sanitized


# ============================================
#          undo_string_compressions
# ============================================
def undo_string_compressions(params, frontend):
    # Don't need to undo the dobj joining since the joined version
    # should already match the pytest version.
    # NOTE: Get ds from the key in the shelve file
    registersToUndo = [
        fieldRegister,
        geomRegister,
        attrNameRegister,
        plotFieldRegister,
    ]
    paramKeyList = [
        "f",
        "geom",
        "attr_name",
        "plot_field",
    ]
    for register, key in zip(registersToUndo, paramKeyList):
        try:
            reg = register[frontend]
        except KeyError:
            continue
        for comp in reg:
            joined = "".join(comp.split("_"))
            # Use in and replace here because the field can be a tuple
            if key in params:
                if joined in params[key]:
                    params[key] = params[key].replace(joined, comp)
    if frontend == "xray":
        for f in xrayDecompress:
            if f in params["f"]:
                params["f"] = params["f"].replace(f, xrayDecompress[f])
    if frontend == "particle_trajectories":
        for undFuncName, joinFuncName in funcNameRegister["particle_trajectories"].items():
            if joinFuncName in params["func_name"]:
                params["func_name"] = undFuncName
    if frontend == "particle_plot":
        for joinedAttr, actualAttr in particlePlotDecompress.items():
            if joinedAttr in params["attr_args"]:
                params["attr_args"] = actualAttr
    if frontend == "plot_window":
        for joinedAttr, actualAttr in plotWindowDecompress.items():
            if joinedAttr in params["attr_args"]:
                params["attr_args"] = actualAttr
    return params

# ============================================
#                camel_to_snake 
# ============================================
def camel_to_snake(camel):
    """
    The test names produces by nose have CamelCase, but the test names
    produces by pytest have snake_case.
    """
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    if camel == "YTDataTest":
        return "yt_data_field"
    else:
        return pattern.sub('_', camel).lower()


# ============================================
#             get_other_yt_params
# ============================================
def get_other_yt_params(testName, otherComponents):
    otherParams = {}
    projTests = [
        "projection_values",
        "pixelized_projection_values",
        "pixelized_particle_projection_values",
    ]
    if testName in ["grid_values", "field_values"]:
        otherParams["f"] = otherComponents[0]
    elif testName in projTests:
        otherParams["f"] = otherComponents[0]
        otherParams["a"] = otherComponents[1]
        otherParams["w"] = otherComponents[2]
    elif testName in ["generic_array", "generic_image",]:
        otherParams["func_name"] = otherComponents[0]
        otherParams["args"] = otherComponents[1]
        otherParams["kwargs"] = otherComponents[2]
    elif testName in ["axial_pixelization",]:
        otherParams["geom"] = otherComponents[0]
    elif testName in ["phase_plot_attribute",]:
        otherParams["plot_type"] = camel_to_snake(otherComponents[0])
        otherParams["x_field"] = otherComponents[1]
        otherParams["y_field"] = otherComponents[2]
        otherParams["z_field"] = otherComponents[3]
        otherParams["attr_name"] = otherComponents[4]
        otherParams["attr_args"] = otherComponents[5]
    elif testName in ["plot_window_attribute",]:
        otherParams["plot_type"] = camel_to_snake(otherComponents[0])
        otherParams["plot_field"] = otherComponents[1]
        otherParams["axis"] = otherComponents[2]
        otherParams["attr_name"] = otherComponents[3]
        otherParams["attr_args"] = otherComponents[4]
        try:
            otherParams["callback_id"] = otherComponents[5]
        except IndexError:
            otherParams["callback_id"] = None
    elif testName in ["vr_image_comparison",]:
        otherParams["desc"] = otherComponents[0]
    return otherParams
