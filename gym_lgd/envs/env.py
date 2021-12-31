import gym
from gym import spaces
from gym_lgd.envs.backend import *
import numpy as np
import logging
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s %(lavelname)s %(message)s' ,filename="awesome-env.log", encoding='utf-8', level=logging.INFO)


class BottleneckEnv(gym.Env):
    MAX_RETRY = 1000
    MAX_RTT = 10000
    ACTION_LENGTH = 10
    ACTIONS = list(range(ACTION_LENGTH))
    MAX_TICKS = 30

    def __init__(self, bw_mean, bw_deviation) -> None:
        self.__version__ = "0.1.0"
        logging.info("LGD - Version {}".format(self.__version__))

        self.backend = BottleneckBackend(AwesomeBottleneckTopo())
        self.ticks = 0 

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
        self.take_action(action)
        observation = self.get_state()
        reward = self.get_reward()

        return observation, reward, self.done, self.info

    def take_action(self, action):
        
        self.ticks += 1
        ...
        # TODO(lrk): adjust beta

    def reset(self):
        ...

    def get_state(self):

        self.backend.take_measurements()
        return (self.backend.bws[-2], self.backend.rtts[-2], self.backend.rtrys[-2])

    def get_reward(self):
        return self.backend.netpwrs[-2]

    def plot(self):
        measurements = ["bws", "rtrys", "rtts", "cwnds", "netpwrs"]
        for idx, measurement in enumerate(measurements):

            plt.figure(idx + 1)
            plt.plot(getattr(self.backend, measurement))
            plt.title(f"Measurements of {measurement.upper()}")
            plt.ylabel(f"{measurement.upper()}")
            plt.xlabel("t")
            plt.savefig(f"figs/{measurement}.png")




    def clean(self):
        self.backend.clean()


class LongFatEnv(gym.Env):
    ...


