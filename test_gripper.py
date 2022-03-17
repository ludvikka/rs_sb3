import numpy as np
from time import sleep
#import mujoco_py
import robosuite as suite

from custom_task import LiftSquareObject

from custom_utils import euler_angel_to_quat
from custom_gym_wrapper import CustomGymWrapper
from robosuite import load_controller_config
from objects import LemonObject, BreadObject

from domain_randomization_wrapper_args import CUSTOM_CAMERA_ARGS, CUSTOM_COLOR_ARGS, CUSTOM_DYNAMICS_ARGS, CUSTOM_LIGHTING_ARGS

from robosuite.wrappers import GymWrapper

from stable_baselines3 import PPO

controller_config = load_controller_config(default_controller="JOINT_POSITION")

objects = [LemonObject(name = "Lemon"),BreadObject(name = "Bread")]

env = suite.make(
    env_name="LiftSquareObject", # try with other tasks like "Stack" and "Door"
    robots="IIWA",  # try with other robots like "Sawyer" and "Jaco"
    gripper_types="Robotiq85Gripper",
    has_renderer=False,
    has_offscreen_renderer=True,
    use_camera_obs=True,
    camera_names =['birdview'],
    camera_widths =[300],
    camera_heights=[300],
    camera_depths=[True],
    use_object_obs=False,
    controller_configs=controller_config,
    control_freq = 1
)
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage




obs = env.reset()
print(obs['robot0_joint_pos'])
img = obs['birdview_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()


action = [3.14/6,0,0,0,0,0,0,0]
obs, x,x,x = env.step(action)
img = obs['birdview_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()
print(obs['robot0_joint_pos'])

#action = [1,0,0,0,0,0,0,0]
obs, x,x,x  = env.step(action)
print(obs['robot0_joint_pos'])
img = obs['birdview_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()

obs, x,x,x  = env.step(action)
print(obs['robot0_joint_pos'])
img = obs['birdview_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()

obs, x,x,x  = env.step(action)
print(obs['robot0_joint_pos'])
img = obs['birdview_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()
obs, x,x,x  = env.step(action)
print(obs['robot0_joint_pos'])
img = obs['birdview_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()
obs, x,x,x  = env.step(action)
print(obs['robot0_joint_pos'])
img = obs['birdview_image']
rotated_img = ndimage.rotate(img, 180)
plt.figure(figsize = (10,10))
plt.imshow(rotated_img)
plt.show()