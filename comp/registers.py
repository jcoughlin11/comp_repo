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
    "athena" : [
        "Cloud_0050",
        "Blast_0100",
        "rps_0062",
    ],
    "athena_pp" : [
        "disk_out1_00000",
        "AM06_out1_00400",
    ],
    "chombo" : [
        "data_0077_3d_hdf5",
        "data_0005_3d_hdf5",
        "data_0000_3d_hdf5",
        "plt32_2d_hdf5",
        "data_0004_hdf5",
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
    "athena" : [
        "scalar[0]",
        "total_energy",
        "velocity_magnitude",
        "specific_scalar[0]",
    ],
    "athena_pp" : [
        "velocity_magnitude",
        "magnetic_field_x",
    ],
    "chombo" : [
        "velocity_magnitude",
        "magnetic_field_x",
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
    "athena" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "athena_pp" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "chombo" : [
        "sphere_('max', (0_1, 'unitary'))",
        "sphere_('c', (0_1, 'unitary'))",
    ],
    "enzo" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "tipsy" : [
        "sphere_('c', (0_3, 'unitary'))",
        "sphere_('c', (0_1, 'unitary'))",
    ],
}


# For some frontends, nose uses an alias for certain fields. This
# causes a KeyError in comp_dict, so this register serves as a map
# between them
specialFields = {
    "athena" : {
        ('gas', 'density') : "('athena', 'density')",
        ('gas', 'total_energy') : "('athena', 'total_energy')",
    },
}
