import gym
from gym import spaces
from backend import *
import numpy as np
import logging

logging.basicConfig(format='%(asctime)s %(lavelname)s %(message)s' ,filename="awesome-env.log", encoding='utf-8', level=logging.INFO)


class BottleneckEnv(gym.Env):
    MAX_RETRY = 1000
    MAX_RTT = 10000
    ACTION_LENGTH = 10
    ACTIONS = list(range(ACTION_LENGTH))

    def __init__(self, bw_mean, bw_deviation) -> None:
        self.__version__ = "0.1.0"
        logging.info("LGD - Version {}".format(self.__version__))

        self.backend = BottleneckBackend(AwesomeBottleneckTopo())


        # (BW, RTT, Rtry)
        # Rtry: total number of TCP retries
        observation_low = np.array([0, 0, 0])
        observation_high = np.array([bw_mean + bw_deviation, self.MAX_RTT, self.MAX_RETRY])
        self.observation_space = spaces.Box(observation_low, observation_high, dtype=np.float32)
        
        # TODO(gpl): param
        self.action_space = spaces.Discrete(self.ACTION_LENGTH)
        
        self.done = False
        self.info = {}

    def step(self, action):
        """The agent takes a step in the environment.

        Returns: tuple of (ob, reward, done, info)

            observation (object): an environment-specific object representing (BW, RTT, Rtry).
            reward (float): amount of reward achieved by the previous action.
            done (boolean): whether it’s time to reset the environment again.
            info (dict): diagnostic information useful for debugging.
        """
        # NetPwr, Rtry,
        # NetPwr: Network Power(Throuput / RTT),
        

        return 

    def take_action(self, action):
        ...

    def reset(self):
        return super().reset()

    def get_state(self):
        ...

    def get_reward(self):
        ...

    def clean(self):
        self.backend.clean()


class LongFatEnv(gym.Env):
    ...
