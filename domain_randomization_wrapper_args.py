CUSTOM_COLOR_ARGS = {
    "geom_names": None,  # all geoms are randomized
    "randomize_local": True,  # sample nearby colors   !!Changed!!
    "randomize_material": True,  # randomize material reflectance / shininess / specular
    "local_rgb_interpolation": 0.2,
    "local_material_interpolation": 2,
    "texture_variations": ["rgb", "checker", "noise", "gradient"],  # all texture variation types
    "randomize_skybox": True,  # by default, randomize skybox too
}

CUSTOM_CAMERA_ARGS = {
    "camera_names": None,  # all cameras are randomized
    "randomize_position": True,
    "randomize_rotation": True,
    "randomize_fovy": True,
    "position_perturbation_size": 0.01,
    "rotation_perturbation_size": 0.087,
    "fovy_perturbation_size": 2.0,
}

CUSTOM_LIGHTING_ARGS = {
    "light_names": None,  # all lights are randomized
    "randomize_position": True,
    "randomize_direction": True,
    "randomize_specular": True,
    "randomize_ambient": True,
    "randomize_diffuse": True,
    "randomize_active": True,
    "position_perturbation_size": 0.3,
    "direction_perturbation_size": 0.35,
    "specular_perturbation_size": 0.2,
    "ambient_perturbation_size": 0.2,
    "diffuse_perturbation_size": 0.2,
}

CUSTOM_DYNAMICS_ARGS = {
    # Opt parameters
    "randomize_density": True,
    "randomize_viscosity": True,
    "density_perturbation_ratio": 0.1,
    "viscosity_perturbation_ratio": 0.1,
    # Body parameters
    "body_names": None,  # all bodies randomized
    "randomize_position": True,
    "randomize_quaternion": True,
    "randomize_inertia": True,
    "randomize_mass": True,
    "position_perturbation_size": 0.0015,
    "quaternion_perturbation_size": 0.003,
    "inertia_perturbation_ratio": 0.02,
    "mass_perturbation_ratio": 0.02,
    # Geom parameters
    "geom_names": None,  # all geoms randomized
    "randomize_friction": True,
    "randomize_solref": True,
    "randomize_solimp": True,
    "friction_perturbation_ratio": 0.1, #def 0.1
    "solref_perturbation_ratio": 0.1,
    "solimp_perturbation_ratio": 0.1,
    # Joint parameters
    "joint_names": None,  # all joints randomized
    "randomize_stiffness": True,
    "randomize_frictionloss": True,
    "randomize_damping": True,
    "randomize_armature": True,
    "stiffness_perturbation_ratio": 0.1,
    "frictionloss_perturbation_size": 0.05,
    "damping_perturbation_size": 0.01,
    "armature_perturbation_size": 0.01,
}



NO_LIGHTING_ARGS = {
    "light_names": None,  # all lights are randomized
    "randomize_position": False,
    "randomize_direction": False,
    "randomize_specular": False,
    "randomize_ambient": False,
    "randomize_diffuse": False,
    "randomize_active": False,
    "position_perturbation_size": 0.1,
    "direction_perturbation_size": 0.35,
    "specular_perturbation_size": 0.1,
    "ambient_perturbation_size": 0.1,
    "diffuse_perturbation_size": 0.1,
}

NO_COLOR_ARGS = {
    "geom_names": None,  # all geoms are randomized
    "randomize_local": True,  # sample nearby colors   !!Changed!!
    "randomize_material": True,  # randomize material reflectance / shininess / specular
    "local_rgb_interpolation": 0,
    "local_material_interpolation": 0,
    "texture_variations": ["rgb", "checker", "noise", "gradient"],  # all texture variation types
    "randomize_skybox": False,  # by default, randomize skybox too
}


NO_CAMERA_ARGS = {
    "camera_names": None,  # all cameras are randomized
    "randomize_position": True,
    "randomize_rotation": False,
    "randomize_fovy": False,
    "position_perturbation_size": 0.0001,
    "rotation_perturbation_size": 0.087,
    "fovy_perturbation_size": 50.0,
}