testRegister = [
    "grid_hierarchy",
    "parentage_relationships",
    "grid_values",
    "projection_values",
    "field_values",
    "pixelized_projection_values",
    "pixelized_particle_projection_values",
]


# Dataset register. Contains the datasets whose names have underscores
# in them, organized by frontend. This is how they appear in the
# description (so dots are underscores)
dsRegister = {
    "ahf" : [
        "snap_N64L16_135_parameter",
    ],
    "amrvac" : [
        "bw_2d0000_dat",
        "kh_2d0000_dat",
        "kh_3D0000_dat",
        "Jet0003_dat",
        "R_1d0005_dat",
        "bw_3d0000_dat",
        "bw_polar_2D0000_dat",
        "bw_cylindrical_3D0000_dat",
        "RM2D_dust_Kwok0000_dat",
    ], 
    "artio" : [
        "sizmbhloz-clref04SNth-rs9_a0_9011_art",
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
    "amrvac" : [
        "velocity_magnitude",
        "magnetic_energy_density",
        "energy_density",
    ],
    "artio" : [
        "velocity_magnitude",
        "('deposit', 'all_density')",
        "('deposit', 'all_count')",
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
    "amrvac" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "artio" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "enzo" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "tipsy" : [
        "sphere_('c', (0_3, 'unitary'))",
        "sphere_('c', (0_1, 'unitary'))",
    ],
}
