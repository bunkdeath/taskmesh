from taskmesh.config import Config
from taskmesh.providers import Provider


class Task:
    def __init__(self, provider: Provider, config: Config = None):
        self.provider = provider
        self.config = config or Config()

    def listen(self, topic=None):
        print(self, topic)

        # def decorator(*args, **kwargs):
        def decorator(func, *args, **kwargs):
            return self.provider.run(topic, func, config=self.config)

        return decorator


# class Subscriber:
#     def listen(self, topic):
#         def decorator(func):
#             return run(topic, func, config=self.config)

#         return decorator
