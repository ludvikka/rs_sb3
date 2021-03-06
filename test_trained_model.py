from stable_baselines3 import PPO
import robosuite as suite
from robosuite import load_controller_config
from custom_gym_wrapper import CustomGymWrapper
from custom_gym_wrapper_RGBD import CustomGymWrapperRGBD
import numpy as np

num_episods = 10
video_name = 'ppo_400h.mp4'
model = PPO.load('trained_models/ppo_400h_2.zip')
from test_sac_config import cfg



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

env = CustomGymWrapper(env,cfg.OBSERVATIONS)


import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from IPython.display import HTML
import PIL.Image
def display_video(frames, framerate=2):
    height, width, __ = frames[0].shape
    dpi = 70
    orig_backend = matplotlib.get_backend()
    matplotlib.use('Agg')  # Switch to headless 'Agg' to inhibit figure rendering.
    fig, ax = plt.subplots(1, 1, figsize=(width / dpi, height / dpi), dpi=dpi)
    matplotlib.use(orig_backend)  # Switch back to the original backend.
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_position([0, 0, 1, 1])
    im = ax.imshow(frames[0])

    def update(frame):
      im.set_data(frame)
      return [im]
    interval = 1000/framerate
    anim = animation.FuncAnimation(fig=fig, func=update, frames=frames,
                                   interval=interval, blit=True, repeat=False)
    writer = animation.writers['ffmpeg'](fps=30)
    anim.save(video_name,writer=writer,dpi=dpi)

from scipy import ndimage

frames = []
for i in range(num_episods):
    obs = env.reset()
    img = obs['calibrated_camera_image']
    rotated_img = ndimage.rotate(img, 180)
    frames.append(rotated_img)
    for i in range(30):
        chosen_action = model.predict(obs)
        obs,reward,done,info = env.step(chosen_action[0])
        img = obs['calibrated_camera_image']
        rotated_img = ndimage.rotate(img, 180)
        frames.append(rotated_img)
display_video(frames)


