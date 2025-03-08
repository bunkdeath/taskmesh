from taskmesh.config import Config
from taskmesh.core import process_task
from taskmesh.providers import Provider


class Task:
    def __init__(self, provider: Provider, config: Config = None):
        self.provider = provider
        self.config = config or Config()

    def listen(self, topic=None):
        def decorator(func, *args, **kwargs):
            return self.provider.run(topic, func, config=self.config)

        return decorator

    def delay(self, *args, **kwargs):
        message = {
            "module": self.callback.__module__,
            "function": self.callback.__name__,
            "topic": self.provider.topic_id,
            "args": args,
            "kwargs": kwargs,
        }

        if not self.config.TASK_ENABLED:
            return process_task(message)

        self.provider.publish_message(message)
