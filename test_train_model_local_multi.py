
import gym
import robosuite as suite

from objects import LemonObject, BreadObject, BoxObject
objects = [LemonObject(name = "Lemon"),BreadObject(name = "Bread")]

import time

from custom_task import LiftSquareObject

from custom_utils import euler_angel_to_quat
from custom_gym_wrapper import CustomGymWrapper
from custom_gym_wrapper_RGBD import CustomGymWrapperRGBD
from robosuite import load_controller_config
from domain_randomization_wrapper_args import CUSTOM_CAMERA_ARGS, CUSTOM_COLOR_ARGS, CUSTOM_DYNAMICS_ARGS, CUSTOM_LIGHTING_ARGS, NO_CAMERA_ARGS, NO_COLOR_ARGS, NO_LIGHTING_ARGS
from robosuite.wrappers import DomainRandomizationWrapper

from stable_baselines3 import PPO

import numpy as np

trans_matrix_org = np.array([[ 0.171221,  0.730116, -0.661524,  1124.551880], 
  [ 0.985078, -0.138769,  0.101808, -46.181087], 
  [-0.017467, -0.669085, -0.742981,  815.163208+800], 
  [ 0.000000,  0.000000,  0.000000,  1.000000]])
trans_matrix_org = np.array([[ 5.55111512e-17,  2.57400000e-01, -9.63200000e-01,  1.60000000e+00],
 [ 9.97000000e-01,  0.00000000e+00,  0.00000000e+00,  0.00000000e+00],
 [ 0.00000000e+00, -9.63200000e-01, -2.57400000e-01,  1.45000000e+00],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]])



from robosuite.utils.transform_utils import mat2quat
camera_quat = mat2quat(trans_matrix_org[:3,:3])
print(camera_quat)
camera_quat = [0.6743090152740479, 0.21285612881183624, 0.21285581588745117, 0.6743084788322449]
#camera_quat = [-camera_quat[0],camera_quat[2],camera_quat[3],-camera_quat[1]]

pos = trans_matrix_org[0:3,3]
pos = [0.626,0,1.6815]
height_vs_width_relattion = 754/449
camera_attribs = {'fovy': 31.0350747}
camera_h = 240
camera_w = int(camera_h * height_vs_width_relattion)




controller_config = load_controller_config(default_controller="JOINT_POSITION")
def makeEnv():
  env = suite.make(
      camera_pos = pos,#(1.1124,-0.046,1.615),#(1.341772827,  -0.312295471 ,  0.182150085+1.5), 
      camera_quat = camera_quat,#(0.5608417987823486, 0.4306466281414032, 0.4306466579437256, 0.5608419179916382),# frontview quat
      camera_attribs = camera_attribs,
      env_name="LiftSquareObject", # try with other tasks like "Stack" and "Door"
      robots="IIWA",  # try with other robots like "Sawyer" and "Jaco"
      gripper_types="Robotiq85Gripper",
      has_renderer=False,
      has_offscreen_renderer=True,
      use_camera_obs=True,
      camera_names =['calibrated_camera'],
      camera_widths =[camera_w],
      camera_heights=[camera_h],
      camera_depths=[True],
      use_object_obs=False,
      controller_configs=controller_config,
      control_freq = 1,
      horizon = 25,
  )

  env = DomainRandomizationWrapper(
      env = env,
      randomize_color=True,
      randomize_camera=True,
      randomize_lighting=True,
      randomize_dynamics=True,
      color_randomization_args=CUSTOM_COLOR_ARGS,
      camera_randomization_args=CUSTOM_CAMERA_ARGS,
      lighting_randomization_args=CUSTOM_LIGHTING_ARGS,
      dynamics_randomization_args=CUSTOM_DYNAMICS_ARGS,
      randomize_on_reset=True, randomize_every_n_steps=0)
  env = CustomGymWrapper(env,['calibrated_camera_image','robot0_joint_pos'])
  return env
    

from stable_baselines3.common.vec_env import SubprocVecEnv

from stable_baselines3.common.utils import set_random_seed

num_cpu = 8
def make_env(rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = makeEnv()
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

#vec_gym_env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])


#model = PPO('MultiInputPolicy', vec_gym_env, n_steps = 1000,verbose=2, tensorboard_log='./ppo_lift_4_objects_tensorboard/')
#print("starting to learn")
#model.learn(total_timesteps = 100000, log_interval= 10000,  tb_log_name="test")
if __name__ == '__main__':
  tic = time.perf_counter()
  vec_gym_env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])
  toc_1 = time.perf_counter()


  model = PPO('MultiInputPolicy', vec_gym_env, n_steps = 100,verbose=2, tensorboard_log=None)
  print(f"envs and model setup in {toc_1 - tic:0.4f}")
  print("starting to learn")
  tic = time.perf_counter()
  model.learn(total_timesteps = 200)
  toc_2 = time.perf_counter()
  print(f"training done in  {toc_2 - tic:0.4f}")
