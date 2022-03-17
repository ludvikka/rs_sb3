import numpy as np
from time import sleep
#import mujoco_py
import robosuite as suite

from custom_task import LiftRandomObject

from custom_utils import euler_angel_to_quat
from custom_gym_wrapper import CustomGymWrapper
from robosuite import load_controller_config
from objects import LemonObject, BreadObject

from domain_randomization_wrapper_args import CUSTOM_CAMERA_ARGS, CUSTOM_COLOR_ARGS, CUSTOM_DYNAMICS_ARGS, CUSTOM_LIGHTING_ARGS

from robosuite.wrappers import GymWrapper

from stable_baselines3 import PPO

controller_config = load_controller_config(default_controller="OSC_POSE")

objects = [LemonObject(name = "Lemon"),BreadObject(name = "Bread")]

env = suite.make(
    camera_pos = (-0.4,  -0.4 ,  1.5), 
    camera_quat = euler_angel_to_quat([40,0,-40]),
    env_name="LiftRandomObject", # try with other tasks like "Stack" and "Door"
    robots="IIWA",  # try with other robots like "Sawyer" and "Jaco"
    gripper_types="Robotiq85Gripper",
    has_renderer=False,
    has_offscreen_renderer=True,
    use_camera_obs=True,
    camera_names =['calibrated_camera'],
    camera_heights =[1280],
    camera_widths=[2560],
    #camera_depths=[True],
    use_object_obs=False,
    controller_configs=controller_config,
    objects = objects,
)
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage




obs = env.reset()
print(obs['robot0_gripper_qpos'])
img = obs['calibrated_camera_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()


action = [0,0,0,0,0,0,-1]
obs, x,x,x = env.step(action)
img = obs['calibrated_camera_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()
print(obs['robot0_gripper_qpos'])

obs, x,x,x  = env.step(action)
print(obs['robot0_gripper_qpos'])
img = obs['calibrated_camera_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()