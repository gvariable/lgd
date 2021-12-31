import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)
register(
    id = "lgd-v0",
    entry_point = 'gym_lgd.envs:BottleneckBackend'
)