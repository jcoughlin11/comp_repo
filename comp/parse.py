import re

from .registers import dsRegister
from .registers import fieldRegister
from .registers import objRegister


# ============================================
#                parse_yt_desc
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
    # Remove underscores from the names of the various components
    components = sanitize_yt_desc(desc, frontend)
    params["test"] = camel_to_snake(components[0])
    params["ds"] = components[1]
    params["dobj"] = components[2]
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
    separated by an underscore. This function removes the inter-
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
        register = dsRegister[frontend]
    elif componentType == "field":
        register = fieldRegister[frontend]
    elif componentType == "object":
        register = objRegister[frontend]
    for comp in register:
        if comp in desc:
            joined = "".join(comp.split("_"))
            desc = desc.replace(comp, joined)
    return desc


# ============================================
#         undo_string_compression
# ============================================
def undo_string_compression(params, frontend):
    for comp in dsRegister[frontend]:
        joined = "".join(comp.split("_"))
        if joined == params["ds"]:
            params["ds"] = comp
    for comp in fieldRegister[frontend]:
        joined = "".join(comp.split("_"))
        if joined == params["field"]:
            params["field"] = comp
    for comp in objRegister[frontend]:
        joined = "".join(comp.split("_"))
        if joined == params["dobj"]:
            params["dobj"] = comp
    return params

# ============================================
#                snake_to_camel
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
        otherParams["field"] = otherComponents[0]
    elif testName in projTests:
        otherParams["field"] = otherComponents[0]
        otherParams["axis"] = otherComponents[1]
        otherParams["weight"] = otherComponents[2]
    return otherParams
