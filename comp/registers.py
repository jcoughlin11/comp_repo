# Dataset register. Contains the datasets whose names have underscores
# in them, organized by frontend
dsRegister = {
    "tipsy" : [
        "halo1e11_run1_00400",
        "agora_1e11_00400",
        "galaxy_00300",
    ]
}

# Field register. Contains the fields whose names have underscores in
# them, organized by frontend
fieldRegister = {
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
}
