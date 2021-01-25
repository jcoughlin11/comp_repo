import re

from .registers import dotRegister
from .registers import dsRegister
from .registers import fieldRegister
from .registers import objRegister


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
    components = sanitize_yt_desc(desc, frontend)
    params["test"] = camel_to_snake(components[0])
    params["ds"] = components[1]
    params["d"] = components[2]
    otherParams = get_other_yt_params(params["test"], components[3:])
    params.update(otherParams)
    # Undo the underscore removal
    params = undo_string_compressions(params, frontend)
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
    for comp in register:
        if comp in desc:
            if "sphere" in comp:
                sanitizedSphere = sanitize_sphere(comp)
                desc = desc.replace(comp, sanitizedSphere)
            else:
                joined = "".join(comp.split("_"))
                desc = desc.replace(comp, joined)
    return desc


# ============================================
#              sanitize_sphere
# ============================================
def sanitize_sphere(comp):
    sanitized = "('sphere', ("
    if "max" in comp:
        sanitized += "'max', ("
    elif "c" in comp:
        sanitized += "'c', ("
    if "0_1" in comp:
        sanitized += "0.1, 'unitary')))"
    elif "0_3" in comp:
        sanitized += "0.3, 'unitary')))"
    return sanitized


# ============================================
#          undo_string_compressions
# ============================================
def undo_string_compressions(params, frontend):
    # Don't need to undo the dobj joining since the joined version
    # should already match the pytest version
    for comp in dsRegister[frontend]:
        joined = "".join(comp.split("_"))
        if joined == params["ds"]:
            # There are certain names with dots in them
            if comp in dotRegister:
                params["ds"] = dotRegister[comp]
            else:
                params["ds"] = comp
    for comp in fieldRegister[frontend]:
        joined = "".join(comp.split("_"))
        # Use in and replace here because the field can be a tuple
        if "f" in params:
            if joined in params["f"]:
                params["f"] = params["f"].replace(joined, comp)
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
    return otherParams
