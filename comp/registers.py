dotRegister = {
    "snap_N64L16_135_parameter" : "snap_N64L16_135.parameter",
}


# Dataset register. Contains the datasets whose names have underscores
# in them, organized by frontend. This is how they appear in the
# description. The actual version (if there are dots), are given above
# in dotRegister
dsRegister = {
    "ahf" : [
        "snap_N64L16_135_parameter",
    ],
    "tipsy" : [
        "halo1e11_run1_00400",
        "agora_1e11_00400",
        "galaxy_00300",
    ]
}

# Field register. Contains the fields whose names have underscores in
# them, organized by frontend
fieldRegister = {
    "ahf" : [
        "particle_position_x",
        "particle_position_y",
        "particle_position_z",
        "particle_mass",
    ],
    "enzo" : [
        "velocity_magnitude",
        "velocity_divergence",
    ],
    "tipsy" : [
        "particle_mass",
        "particle_velocity_x",
        "particle_velocity_y",
        "particle_velocity_z",
        "particle_ones",
        "velocity_magnitude",
        "Fe_fraction",
    ],
}


# Object register. Contains the objects whose names have underscores
# in them, organized by frontend
objRegister = {
    "enzo" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "tipsy" : [
        "sphere_('c', (0_3, 'unitary'))",
        "sphere_('c', (0_1, 'unitary'))",
    ],
}
