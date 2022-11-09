from typing import List
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class EnvironmentMiddleware(LifetimeControllerMiddleware):

    def __init__(self, config, logger):
        super().__init__()
        self.config = config
        self.logger = logger

    async def pre_process(self, obj, data, *args):
        data["config"] = self.config
        data['logger'] = self.logger

    async def post_process(self, obj, data, *args):
        pass
