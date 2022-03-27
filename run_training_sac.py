
import robosuite as suite
import time

from custom_task import LiftSquareObject
from stable_baselines3.common.env_checker import check_env

from custom_gym_wrapper import CustomGymWrapper
from custom_gym_wrapper_RGBD import CustomGymWrapperRGBD
from robosuite import load_controller_config
from domain_randomization_wrapper_args import CUSTOM_CAMERA_ARGS, CUSTOM_COLOR_ARGS, CUSTOM_DYNAMICS_ARGS, CUSTOM_LIGHTING_ARGS, NO_CAMERA_ARGS, NO_COLOR_ARGS, NO_LIGHTING_ARGS
from robosuite.wrappers import DomainRandomizationWrapper

from stable_baselines3 import PPO

from wandb.integration.sb3 import WandbCallback
import wandb
from stable_baselines3.common.vec_env import SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.monitor import Monitor


def makeEnv(cfg):
    from custom_task import LiftSquareObject
    camera_w = int(cfg.ENV.CAMERA_VIEW_H * cfg.ENV.HWREL)
    env = suite.make(
        camera_pos = cfg.ENV.CAMERA_POS,
        camera_quat = cfg.ENV.CAMERA_QUAT,
        camera_attribs = {'fovy': cfg.ENV.FOVY},
        env_name='LiftSquareObject', 
        robots=cfg.ENV.ROBOTS, 
        gripper_types=cfg.ENV.GRIPPER_TYPES,
        has_renderer=cfg.ENV.HAS_RENDERER,
        has_offscreen_renderer= cfg.ENV.HAS_OFFSCREEN_RENDERER,
        use_camera_obs=cfg.ENV.USE_CAMERA_OBS,
        camera_names =cfg.ENV.CAMERA_NAMES,
        camera_widths =[camera_w],
        camera_heights=cfg.ENV.CAMERA_VIEW_H,
        camera_depths=cfg.ENV.CAMERA_DEPTHS,
        use_object_obs=cfg.ENV.USE_OBJECT_POS,
        controller_configs=load_controller_config(default_controller=cfg.ENV.CONTROLLER_TYPE),
        control_freq = cfg.ENV.CONTROL_FREQ,
        horizon = cfg.ENV.HORIZON,
        reward_shaping = cfg.ENV.REWARD_SHAPING,
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
    env = CustomGymWrapper(env,cfg.OBSERVATIONS)
    return env


def make_env(rank, cfg ,seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """
    def _init():
        env = makeEnv(cfg)
        env = Monitor(env)    
        env.seed(seed + rank)
        return env
    set_random_seed(seed)
    return _init

def run_training_sac(cfg):
    num_cpu = cfg.NUM_CPUS
    run = wandb.init(project=cfg.WANDB.NAME,
                     entity="ludvikka",
                     sync_tensorboard=True,
                     config = cfg)
    
    callback = WandbCallback(verbose = 2)
    env = SubprocVecEnv([make_env(i , cfg) for i in range(num_cpu)])
    
    
    from stable_baselines3.common.vec_env import VecTransposeImage
    env = VecTransposeImage(env)
    from stable_baselines3.common.vec_env.vec_monitor import VecMonitor
    from stable_baselines3.common.vec_env import VecNormalize
    env = VecNormalize(env, training=True, norm_obs=True, norm_reward=True)
    from stable_baselines3 import SAC
    

    #policy_kwargs = {"layers":[64, 64], "layer_norm":False}
    
    model = SAC("MultiInputPolicy",
                env,
                #policy_kwargs=policy_kwargs,
                verbose=1,
                gamma=0.99,
                buffer_size=1000000,
                batch_size=64,
                learning_rate= 0.0003,
                tensorboard_log=f"runs/{run.id}",
                device ='cpu')
    
    print("starting to learn")
    tic = time.perf_counter()
    model.learn(total_timesteps=2000000, log_interval= 1, tb_log_name="test", callback=callback)
    model.save("trained_models/" + cfg.POLICYNAME)
    toc_2 = time.perf_counter()
    print(f"training done in  {toc_2 - tic:0.4f}")
    run.finish()
    env.close()
    tb_log_name="test"