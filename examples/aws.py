import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from taskmesh import Task
from taskmesh.config import Config
from taskmesh.providers.aws import AWSProvider

PROJECT_ROOT = Path(__file__).resolve().parent

load_dotenv()
config = Config()
# # setting false will bypass the background task. The funciton will be called directly
config.background_task_status(False)

aws = AWSProvider(
    access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    region_name=os.environ.get("AWS_REGION"),
    account_id=os.environ.get("AWS_ACCOUNT_ID"),
    config=config,
)


task = Task(provider=aws, config=config)


@task.listen(topic="taskmesh")
def hello_world(msg, counter):
    print(f"Hello World from {msg} - {counter}")


def setup_config():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Process provider, subscribe, and publish options."
    )

    # Add mutually exclusive group for subscribe and publish
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--subscribe",
        "-s",
        type=str,
        help="Specify the subscribe topic name (string).",
    )
    group.add_argument(
        "--publish",
        "-p",
        action="store_true",
        help="Enable publishing (no value needed).",
    )

    return parser


def parse_args(parser):
    # Parse arguments
    args = parser.parse_args()

    # Access the arguments
    subscribe = args.subscribe

    if subscribe:
        print(f"GCP: Subscribing to {subscribe}")
        aws.start_listening()
    else:
        for i in range(10):
            hello_world("Direct call", i)
            hello_world.delay("Delayed call", i)


if __name__ == "__main__":
    parser = setup_config()
    parse_args(parser)
