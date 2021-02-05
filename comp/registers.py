testRegister = [
    "grid_hierarchy",
    "parentage_relationships",
    "grid_values",
    "projection_values",
    "field_values",
    "pixelized_projection_values",
    "pixelized_particle_projection_values",
    "yt_data_field",
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
    "enzo_p" : [
        "ENZOP_DD0140",
    ],
    "fits" : [
        "grs-50-cube_fits",
        "velocity_field_20_fits",
        "A2052_merged_0_3-2_match-core_tmap_bgecorr_fits",
    ],
    "flash" : [
        "sloshing_low_res_hdf5_plt_cnt_0300",
        "windtunnel_4lev_hdf5_plt_cnt_0030",
        "fiducial_1to3_b1_hdf5_part_0080",
    ],
    "gadget" : [
        "snap_505",
    ],
    "gadget_fof" : [
        "fof_subhalo_tab_005",
        "fof_subhalo_tab_042",
    ],
    "gamer" : [
        "jet_000002",
        "psiDM_000020",
        "plummer_000000",
        "Data_000018",
    ],
    "gdf" : [
        "sedov_tst_0004",
    ],
    "gizmo" : [
        "snap_N64L16_135",
    ],
    "owls" : [
        "snap_033",
    ],
    "rockstar" : [
        "halos_0_0_bin",
    ],
    "tipsy" : [
        "halo1e11_run1_00400",
        "agora_1e11_00400",
        "galaxy_00300",
    ],
    "ytdata" : [
        "DD0046_sphere_h5",
        "DD0046_covering_grid_h5",
        "DD0046_arbitrary_grid_h5",
        "DD0046_quad_proj_h5",
        "DD0046_Profile1D_h5",
        "DD0046_Profile2D_h5",
        "test_data_h5",
        "random_data_h5",
    ],
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
    "enzo_p" : [
        "total_energy",
        "particle_position_x",
        "particle_position_y",
        "particle_position_z",
        "particle_velocity_x",
        "particle_velocity_y",
        "particle_velocity_z",
        "velocity_x",
        "velocity_y",
    ],
    "fits" : [
        "velocity_x",
        "velocity_y",
        "velocity_z",
        "counts_0.1-2.0",
        "counts_2.0-5.0",
    ],
    "flash" : [
        "velocity_magnitude",
    ],
    "gadget" : [
        "('gas', 'density')",
        "('gas', 'temperature')",
        "('gas', 'velocity_magnitude')",
    ],
    "gamer" : [
        "velocity_magnitude",
        "('gamer', 'ParDens')",
        "('deposit', 'io_cic')",
        "('gamer', 'CCMagX')",
        "('gamer', 'CCMagY')",
        "('gas', 'magnetic_energy')",
    ],
    "gdf" : [
        "velocity_x",
    ],
    "gizmo" : [
        "('gas', 'density')",
        "('gas', 'temperature')",
        "('gas', 'metallicity')",
        "('gas', 'O_metallicity')",
        "('gas', 'velocity_magnitude')",
    ],
    "moab" : [
        "('moab', 'flux')",
    ],
    "owls" : [
        "('gas', 'density')",
        "('gas', 'temperature')",
        "('gas', 'velocity_magnitude')",
        "('gas', 'He_p0_number_density')",
    ],
    "rockstar" : [
        "particle_position_x",
        "particle_position_y",
        "particle_position_z",
        "particle_mass",
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
    "ytdata" : [
        "('grid', 'density')",
        "('all', 'particle_mass')",
        "region_density",
        "sphere_density",
        "cell_mass",
        "('density',)",
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
    "enzo_p" : [
        "sphere_('max', (0_25, 'unitary'))",
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "fits" : [
        "sphere_('c', (0_1, 'unitary'))",
    ],
    "flash" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "gadget" : [
        "sphere_('c', (0_1, 'unitary'))",
    ],
    "gamer" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "gdf" : [
        "sphere_('max', (0_1, 'unitary'))",
    ],
    "gizmo" : [
        "sphere_('c', (0_1, 'unitary'))",
    ],
    "moab" : [
        "sphere_('c', (0_1, 'unitary'))",
        "sphere_('c', (0_2, 'unitary'))",
    ],
    "owls" : [
        "sphere_('c', (0_1, 'unitary'))",
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
