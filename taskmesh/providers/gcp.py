import json

from google.cloud import pubsub_v1

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
            "topic": self.provider.topic_id,
            "args": args,
            "kwargs": kwargs,
        }

        if not self.conf.TASK_ENABLED:
            return process_task(message)

        self.provider.publish_message(message)

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)


class GCPProvider(Provider):
    def __init__(self, credential_file=None, project_id=None):
        """
        @credential_file: str
            Path to the GCP credential file
        @project_id: str
            The project id
        """
        self.credential_file = credential_file
        self.project_id = project_id

        if self.credential_file:
            self.set_credential_file(self.credential_file)

        if self.project_id:
            self.set_project_id(self.project_id)

    def set_credential_file(self, credential_file):
        self.credential_file = credential_file
        self.publisher = pubsub_v1.PublisherClient.from_service_account_file(
            self.credential_file
        )

    def set_project_id(self, project_id):
        self.project_id = project_id

    def set_topic_id(self, topic_id):
        self.topic_id = topic_id
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def publish_message(self, data: dict) -> str:
        try:
            message_json = json.dumps(data).encode("utf-8")
            future = self.publisher.publish(self.topic_path, message_json)
            message_id = future.result()
            print(f"Published message ID: {message_id}")
            return message_id
        except Exception as e:
            print(f"Failed to publish message: {e}")
            return None

    def run(self, topic, func, config):
        self.set_topic_id(topic)
        return BackgroundTask(provider=self, callback=func, conf=config)
