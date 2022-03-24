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

from wandb.integration.sb3 import WandbCallback
import wandb
def makeEnv():
  camera_quat = [0.6743090152740479, 0.21285612881183624, 0.21285581588745117, 0.6743084788322449]
  pos = [0.626,0,1.6815]
  height_vs_width_relattion = 754/449
  camera_attribs = {'fovy': 31.0350747}
  camera_h = 240
  camera_w = int(camera_h * height_vs_width_relattion)

  controller_config = load_controller_config(default_controller="OSC_POSE")

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
      control_freq = 20,
      horizon = 400,
      reward_shaping = True,
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
  env = CustomGymWrapper(env,['calibrated_camera_image','robot0_eef_pos'])
  return env

    
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.monitor import Monitor
num_cpu = 2
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
        env = Monitor(env)
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

if __name__ == '__main__':
    run = wandb.init(project="my-test-project", 
                    entity="ludvikka",
                    sync_tensorboard=True,)
    callback=WandbCallback(verbose =2)
    tic = time.perf_counter()
    vec_gym_env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])
    toc_1 = time.perf_counter()


    model = PPO('MultiInputPolicy', vec_gym_env, n_steps = 400,verbose=1, batch_size=50, tensorboard_log=f"runs/{run.id}")
    print(f"envs and model setup in {toc_1 - tic:0.4f}")
    print("starting to learn")
    tic = time.perf_counter()
    model.learn(total_timesteps = 200000, log_interval= 1, tb_log_name="test",)
    toc_2 = time.perf_counter()
    print(f"training done in  {toc_2 - tic:0.4f}")
    model.save('trained_models/' + "1")