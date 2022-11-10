from typing import List
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class EnvironmentMiddleware(LifetimeControllerMiddleware):

    def __init__(self, config, logger, p2p):
        super().__init__()
        self.config = config
        self.logger = logger
        self.p2p = p2p

    async def pre_process(self, obj, data, *args):
        data["config"] = self.config
        data['logger'] = self.logger
        data['p2p'] = self.p2p

    async def post_process(self, obj, data, *args):
        pass
