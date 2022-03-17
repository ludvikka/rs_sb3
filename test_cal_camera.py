import mujoco_py
import robosuite as suite

from custom_task import LiftRandomObject
from time import sleep

from custom_utils import euler_angel_to_quat
from custom_gym_wrapper import CustomGymWrapper
from robosuite import load_controller_config
from objects import LemonObject, BreadObject

from domain_randomization_wrapper_args import CUSTOM_CAMERA_ARGS, CUSTOM_COLOR_ARGS, CUSTOM_DYNAMICS_ARGS, CUSTOM_LIGHTING_ARGS, NO_CAMERA_ARGS, NO_COLOR_ARGS, NO_LIGHTING_ARGS

from robosuite.wrappers import GymWrapper, DomainRandomizationWrapper

"""If you are using 2d camera, 55,84 mm has to be added to the Y translation in camera frame"""

controller_config = load_controller_config(default_controller="OSC_POSE")

objects = [LemonObject(name = "Lemon"),BreadObject(name = "Bread")]
import numpy as np


trans_matrix_org = np.array([[ 0.171221,  0.730116, -0.661524,  1124.551880], 
  [ 0.985078, -0.138769,  0.101808, -46.181087], 
  [-0.017467, -0.669085, -0.742981,  815.163208+800], 
  [ 0.000000,  0.000000,  0.000000,  1.000000]])

trans_matrix = np.array([[ 5.55111512e-17,  2.57400000e-01, -9.63200000e-01,  1.60000000e+00],
 [ 9.97000000e-01,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
 [ 0.00000000e+00, -9.63200000e-01, -2.57400000e-01,  1.45000000e+00],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])


from robosuite.utils.transform_utils import mat2quat, convert_quat, mat2pose
camera_quat = mat2quat(trans_matrix_org[:3,:3])
#camera_quat = convert_quat(camera_quat, to="wxyz")
camera_quat = [-camera_quat[0],camera_quat[2],camera_quat[3],-camera_quat[1]]
print("hand_eye", camera_quat)
#camera_quat = [0.7071068, 0.7071068, 0, 0]
pos = trans_matrix_org[0:3,3]*0.001
print("pos",pos)

height_vs_width_relattion = 754/449
camera_attribs = {'fovy': 31.0350747}
camera_h = 1280
camera_w = int(camera_h * height_vs_width_relattion)
env = suite.make(
    camera_pos = pos,#(1.1124,-0.046,1.615),#(1.341772827,  -0.312295471 ,  0.182150085+1.5), 
    camera_quat = camera_quat,#(0.5608417987823486, 0.4306466281414032, 0.4306466579437256, 0.5608419179916382),# frontview quat
    camera_attribs = camera_attribs,
    env_name="LiftRandomObject", # try with other tasks like "Stack" and "Door"
    robots="IIWA",  # try with other robots like "Sawyer" and "Jaco"
    gripper_types="Robotiq85Gripper",
    has_renderer=False,
    has_offscreen_renderer=True,
    use_camera_obs=True,
    camera_names =['calibrated_camera','frontview','sideview'],
    camera_widths =[camera_w,2560,2560],
    camera_heights=[camera_h,2560,2560],
    camera_depths=[True,True,True],
    use_object_obs=False,
    controller_configs=controller_config,
    objects = objects,
)

gym


import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage




print(get_camera_intrinsic_matrix(env.sim,'calibrated_camera',2560,2560))

obs = env.reset()
obs, r,s,d = env.step([0,0,0,0,0,0,0])
obs = env.reset()
img = obs['calibrated_camera_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()

sleep(6)
    