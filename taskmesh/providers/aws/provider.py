import json

import boto3

from taskmesh.config import Config
from taskmesh.core import process_task
from taskmesh.providers import Provider
from taskmesh.providers.core import BackgroundTask


class AWSProvider(Provider):
    def __init__(
        self,
        access_key_id=None,
        secret_access_key=None,
        region_name=None,
        account_id=None,
        topic=None,
        config=None,
    ):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name or "us-east-1"
        self.account_id = account_id
        self.topic = topic
        self.config = config or Config()

        if self.access_key_id and self.secret_access_key:
            self.setup_client(access_key_id, secret_access_key)

        if self.topic:
            self.set_topic(self.topic)

    def setup_client(self, access_key_id, secret_access_key):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

        self.sqs_client = boto3.client(
            "sqs",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region_name,
        )

    def _build_sqs_url(self, topic):
        return f"https://sqs.{self.region_name}.amazonaws.com/{self.account_id}/{topic}"

    def set_topic(self, topic):
        self.topic = topic
        self.sqs_url = self._build_sqs_url(topic)

    def publish_message(self, data: dict) -> str:
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.sqs_url, MessageBody=json.dumps(data)
            )
            print(f"Message sent! Message ID: {response['MessageId']}")
            return response["MessageId"]
        except Exception as e:
            print(f"Failed to send message: {e}")
            return None

    def run(self, topic, func, config=None):
        self.set_topic(topic)
        return BackgroundTask(provider=self, callback=func)

    def ack_message(self, receipt_handle):
        self.sqs_client.delete_message(
            QueueUrl=self.sqs_url, ReceiptHandle=receipt_handle
        )

    def start_listening(self):
        while True:
            try:
                response = self.sqs_client.receive_message(
                    QueueUrl=self.sqs_url,
                    MaxNumberOfMessages=5,
                    WaitTimeSeconds=20,
                )

                messages = response.get("Messages", [])
                if not messages:
                    print("No new messages. Waiting...")
                    continue

                for message in messages:
                    try:
                        data = json.loads(message["Body"])
                        print(f"Received Message: {data}")
                        process_task(data)
                        self.ack_message(message["ReceiptHandle"])
                    except Exception as e:
                        print(f"Failed to process message: {e}")
                    finally:
                        if self.config.ack_message_on_error:
                            self.ack_message(message["ReceiptHandle"])
            except Exception as e:
                print(f"Failed to receive messages: {e}")
                break
