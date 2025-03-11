from taskmesh.config import Config
from taskmesh.core import process_task
from taskmesh.providers import Provider


class BackgroundTask:
    def __init__(self, provider: Provider, callback, conf: Config = None):
        self.provider = provider
        self.conf = conf or Config()
        self.callback = callback

    def delay(self, *args, **kwargs):
        message = {
            "module": self.callback.__module__,
            "function": self.callback.__name__,
            "topic": self.provider.topic,
            "args": args,
            "kwargs": kwargs,
        }

        if not self.conf.TASK_ENABLED:
            return process_task(message)

        self.provider.publish_message(message)

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)
