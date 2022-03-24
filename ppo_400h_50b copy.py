from run_training import run_training

from yacs.config import CfgNode as CN


cfg = CN()
cfg.ENV = CN()
cfg.WANDB = CN()
cfg.MODEL = CN()
cfg.WANDB.NAME = "ppo_batch_testing"
cfg.POLICYNAME = 'ppo_400_2'

cfg.N_STEPS = 20
cfg.BATCH_SIZE = 20
cfg.TOTAL_TIMESTEPS = 40

cfg.NUM_CPUS = 3
cfg.DEVICE = 'auto'

cfg.ENV.FOVY = 31.0350747
cfg.ENV.CAMERA_VIEW_H = 240
cfg.OBSERVATIONS = ['calibrated_camera_image','robot0_eef_pos']
cfg.ENV.CONTROLLER_TYPE = "OSC_POSE"

cfg.ENV.CONTROL_FREQ = 20
cfg.ENV.HORIZON = 400

cfg.ENV.CAMERA_QUAT = [0.6743090152740479, 0.21285612881183624, 0.21285581588745117, 0.6743084788322449]
cfg.ENV.CAMERA_POS = [0.626,0,1.6815]
cfg.ENV.HWREL = 754/449


cfg.ENV.ENV_NAME="LiftSquareObject" # try with other tasks like "Stack" and "Door"
cfg.ENV.ROBOTS="IIWA"  # try with other robots like "Sawyer" and "Jaco"
cfg.ENV.GRIPPER_TYPES="Robotiq85Gripper"
cfg.ENV.HAS_RENDERER =False
cfg.ENV.HAS_OFFSCREEN_RENDERER = True
cfg.ENV.USE_CAMERA_OBS=True
cfg.ENV.CAMERA_NAMES =['calibrated_camera']
cfg.ENV.CAMERA_DEPTHS=[True]
cfg.ENV.USE_OBJECT_POS=False
cfg.ENV.REWARD_SHAPING = True



if __name__ == '__main__':
    run_training(cfg)